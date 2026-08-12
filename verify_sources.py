"""
Source Verification / Drift Monitor
------------------------------------
Run this periodically (e.g. monthly, via cron / Task Scheduler) against the
SAME URL_CONFIG used by download_and_extract.py. It does NOT re-extract text
for storage — it only checks two things per source, fast and cheap:

  1. LIVENESS  - does the URL still return 200 OK?
  2. DRIFT     - has the *visible text content* changed since the last time
                 download_and_extract.py ran?

Important: this hashes the same CLEANED TEXT that download_and_extract.py
extracts (via extract_pdf_text / extract_html_text), not raw response bytes.
Raw HTML from .aspx-style government pages often embeds session tokens,
view-state fields, or timestamp widgets that change on every request even
when the actual regulatory text hasn't moved — hashing raw bytes would flag
those as "changed" every single run and bury real changes in noise.

Output is a single report (console + JSON file) with four buckets:
  - "broken"    : URL is dead / erroring -> needs a replacement URL, OR the
                  site's bot-protection is blocking this script specifically
                  (see note below) -> verify manually before assuming it's
                  really gone
  - "changed"   : cleaned text differs from last recorded -> re-run
                  download_and_extract.py --force on this label, and
                  have a human (or the LLM prompt in verify_prompt.md)
                  check whether it's a minor edit or a substantive
                  regulatory update
  - "unchanged" : all good, nothing to do
  - "new"       : never downloaded yet by download_and_extract.py

A NOTE ON 403 ERRORS: a 403 (Forbidden) is not always a dead link. Many
sites run bot-protection (Akamai, Cloudflare, etc.) that blocks simple
scripted requests, especially several in a row from the same script run.
If a batch of sources from the SAME domain all return 403 together, that's
a strong sign of bot-blocking, not six pages disappearing at once. This
script adds a short delay between requests and a browser-realistic header
set to reduce false positives, and retries once on 403/429/503 after a
longer pause — but if a domain still fails, treat it as "needs manual
check", not "confirmed dead", until you've verified by opening it in an
actual browser.

This script does NOT judge whether a source has been "superseded" by a
newer regulation it doesn't know the URL for yet. That's a research task,
not a diffing task — see verify_prompt.md for that half.

Usage:
  python verify_sources.py                      # human-readable report
  python verify_sources.py --json report.json    # also write JSON report
"""

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import pdfplumber
import io

# Import the same URL_CONFIG your downloader uses, so the two scripts never
# drift apart. Adjust the import if you rename the downloader file.
from download_and_extract import URL_CONFIG

METADATA_DIR = Path("output") / "metadata"

# A fuller, more browser-realistic header set than a bare User-Agent — some
# WAFs (CIBIL's included) are more likely to block requests missing these.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

REQUEST_DELAY_SECONDS = 2.0   # be polite between requests, and to WAFs
RETRY_DELAY_SECONDS = 8.0     # longer pause before a single retry on 403/429/503


def extract_pdf_text_from_bytes(content: bytes) -> str:
    """Same logic as download_and_extract.extract_pdf_text, but works
    directly on in-memory bytes so this script doesn't need to write a
    temp file just to hash the text."""
    page_texts = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            page_texts.append(f"--- Page {page_num} ---\n{text.strip()}")
    return "\n\n".join(page_texts)


def extract_html_text(html_content: str) -> str:
    """Identical to download_and_extract.extract_html_text — kept in sync
    intentionally so the two scripts hash the exact same representation."""
    soup = BeautifulSoup(html_content, "html.parser")
    unwanted_tags = [
        "script", "style", "nav", "header", "footer",
        "aside", "noscript", "iframe", "svg"
    ]
    for tag in soup(unwanted_tags):
        tag.decompose()
    lines = soup.get_text(separator="\n").splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned_lines)


def fetch_with_retry(url: str):
    """GET with one retry on 403/429/503 after a longer pause. Returns the
    response, or raises the last exception if the retry also fails."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code in (403, 429, 503):
            time.sleep(RETRY_DELAY_SECONDS)
            resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return resp
    except Exception:
        raise


def check_source(item: dict) -> dict:
    label = item["label"]
    url = item["url"]
    doc_type = item.get("type", "").lower()
    result = {
        "label": label,
        "url": url,
        "status": None,       # "broken" | "changed" | "unchanged" | "new"
        "http_status": None,
        "error": None,
    }

    try:
        resp = fetch_with_retry(url)
        result["http_status"] = resp.status_code
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response is not None else None
        result["status"] = "broken"
        result["http_status"] = code
        if code in (403, 429, 503):
            result["error"] = (
                f"{e} — this status code is often bot-protection blocking "
                f"the script, not necessarily a dead page. Verify manually "
                f"in a real browser before treating as confirmed broken."
            )
        else:
            result["error"] = str(e)
        return result
    except Exception as e:
        result["status"] = "broken"
        result["error"] = str(e)
        return result

    # Extract clean text the same way download_and_extract.py does, so we
    # hash the same representation and avoid false positives from dynamic
    # markup (session tokens, view-state, timestamp widgets, etc.)
    try:
        if doc_type == "pdf":
            text = extract_pdf_text_from_bytes(resp.content)
        else:
            text = extract_html_text(resp.text)
    except Exception as e:
        result["status"] = "broken"
        result["error"] = f"fetched OK but text extraction failed: {e}"
        return result

    new_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    meta_path = METADATA_DIR / f"{label}.json"

    if not meta_path.exists():
        result["status"] = "new"
        return result

    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            old_meta = json.load(f)
        old_hash = old_meta.get("text_sha256")  # see note in main() re: migration
    except Exception as e:
        result["status"] = "new"
        result["error"] = f"could not read existing metadata: {e}"
        return result

    if old_hash is None:
        # Existing metadata predates this script's text-based hashing
        # (download_and_extract.py currently stores a raw-content hash
        # under "sha256", not a text hash under "text_sha256"). Treat as
        # "new" for the text-hash baseline rather than a false "changed".
        result["status"] = "new"
        result["note"] = (
            "no prior text_sha256 recorded — this source needs a baseline "
            "text hash. See the note in main() about updating "
            "download_and_extract.py to store one."
        )
    elif old_hash == new_hash:
        result["status"] = "unchanged"
    else:
        result["status"] = "changed"
        result["old_text_sha256"] = old_hash
        result["new_text_sha256"] = new_hash

    return result


def main():
    parser = argparse.ArgumentParser(description="Check sources for liveness and content drift.")
    parser.add_argument("--json", help="Optional path to also write a JSON report.")
    args = parser.parse_args()

    print("=" * 60)
    print(f"Source Verification Run — {datetime.now(timezone.utc).isoformat()}")
    print(f"Total sources: {len(URL_CONFIG)}")
    print(
        "NOTE: this script hashes extracted TEXT, not raw bytes, to avoid\n"
        "false 'changed' flags from dynamic page chrome. If your\n"
        "output/metadata/*.json files were written by an older version of\n"
        "download_and_extract.py that only stores a raw-content 'sha256'\n"
        "(not 'text_sha256'), every source will show as 'new' on this\n"
        "first run — that's expected, it's establishing a text baseline.\n"
        "See the bottom of this file for the one-line change needed in\n"
        "download_and_extract.py to keep both hashes in sync going forward."
    )
    print("=" * 60)

    results = []
    for i, item in enumerate(URL_CONFIG):
        r = check_source(item)
        results.append(r)
        tag = {
            "broken": "[BROKEN]",
            "changed": "[CHANGED]",
            "unchanged": "[OK]",
            "new": "[NEW/UNSEEN]",
        }[r["status"]]
        print(f"{tag:14s} {r['label']}")
        if r["status"] == "broken":
            print(f"               -> {r['error']}")
        if i < len(URL_CONFIG) - 1:
            time.sleep(REQUEST_DELAY_SECONDS)

    broken = [r for r in results if r["status"] == "broken"]
    changed = [r for r in results if r["status"] == "changed"]
    new = [r for r in results if r["status"] == "new"]
    unchanged = [r for r in results if r["status"] == "unchanged"]

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Unchanged : {len(unchanged)}")
    print(f"Changed   : {len(changed)}  <- re-run download_and_extract.py --force on these")
    print(f"Broken    : {len(broken)}   <- check manually in a browser; may be bot-blocking, not dead")
    print(f"New/unseen: {len(new)}      <- run download_and_extract.py, or establishing text baseline")

    # Flag domain-wide 403 clusters explicitly, since that's the strongest
    # signal of bot-protection rather than real breakage.
    from urllib.parse import urlparse
    forbidden = [r for r in broken if r.get("http_status") == 403]
    if forbidden:
        domains = {}
        for r in forbidden:
            d = urlparse(r["url"]).netloc
            domains.setdefault(d, []).append(r["label"])
        for domain, labels in domains.items():
            if len(labels) > 1:
                print(
                    f"\n[LIKELY BOT-BLOCKING] {len(labels)} sources on "
                    f"{domain} all returned 403 together: {', '.join(labels)}\n"
                    f"  This pattern (whole domain, all at once) usually "
                    f"means the site's bot-protection blocked this script,\n"
                    f"  not that the pages are gone. Open one manually in a "
                    f"browser to confirm before replacing any URLs."
                )

    if broken:
        print("\nBROKEN SOURCES (full detail):")
        for r in broken:
            print(f" - [{r['label']}] {r['url']}\n   {r['error']}")

    if changed:
        print("\nCHANGED SOURCES (text content differs from last download):")
        for r in changed:
            print(f" - [{r['label']}] {r['url']}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "run_at": datetime.now(timezone.utc).isoformat(),
                    "summary": {
                        "unchanged": len(unchanged),
                        "changed": len(changed),
                        "broken": len(broken),
                        "new": len(new),
                    },
                    "results": results,
                },
                f,
                indent=2,
            )
        print(f"\nJSON report written to {args.json}")


if __name__ == "__main__":
    main()


