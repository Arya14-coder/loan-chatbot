"""
Document Downloader and Text Extractor
--------------------------------------
This script downloads a list of configured URLs (PDFs and HTML web pages),
extracts clean text content, and saves raw files, processed text, and metadata
to disk.

Features:
- PDF text extraction using pdfplumber with page break markers ("--- Page N ---").
- HTML text extraction using BeautifulSoup4, stripping headers, footers, nav, scripts, and styles.
- Content hashing (SHA256) to skip redundant downloads/processing unless forced.
- JSON metadata output for each document tracking source URL, SHA256, and timestamp.
- Detailed summary report listing successful, skipped, and failed downloads.

Usage:
  python download_and_extract.py              # Runs with default caching
  python download_and_extract.py --force      # Overrides cache and forces re-downloading/re-extracting

Note on URL_CONFIG:
  This script only reads "url", "label", and "type" from each entry below.
  A richer version of this config (with "authority", "source_type", "priority",
  "topics", etc. for retrieval/metadata purposes) lives in url_config_final.py —
  those extra fields are unused here and were stripped out to keep this file
  in sync with what process_url() actually consumes.
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# External libraries (installed via pip)
import requests
from bs4 import BeautifulSoup
import pdfplumber


# ==============================================================================
# 1. CONFIGURATION
# Add your list of URLs to download below.
# Each entry is a dictionary containing:
#   - "url":   The web address to download
#   - "label": Short unique name used for output filenames (no extension)
#   - "type":  Document type hint ("pdf" or "html")
# ==============================================================================
URL_CONFIG = [

    # ==========================================================================
    # RBI — CORE LOAN / BORROWER REGULATION
    # ==========================================================================

    {
        "label": "01_kfs_circular",
        "url": "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/CIRCULARKFS1504242AE2500BAF494C2A82442B0B642705C1.PDF",
        "type": "pdf",
        "authority": "RBI",
        "source_type": "regulatory",
        "priority": 1,
        "topics": ["KFS", "APR", "fees", "repayment", "loan_cost"],
        "document_date": "2024-04-15",
        "last_updated": None,
        "effective_from": "2024-10-01",
        "effective_until": None,
        "status": "active",
    },

    # --- NEW: added ---
    # This is deliberately placed right after the KFS circular because it is
    # the borrower-facing counterpart to KFS: it explicitly tells consumers
    # that "all banks are obliged to explain the most important terms and
    # conditions of the home loan in detail" and to obtain a written offer
    # letter. Verified live on 2026-08-12 (page dated 10/11/2009, still served
    # at this URL). Good for grounding "what is MITC / what should be
    # disclosed" answers in an RBI consumer-education source rather than a
    # bank's own document.
    {
        "label": "02_rbi_housing_loans_faq",
        "url": "https://rbi.org.in/CommonPerson/english/scripts/FAQs.aspx?Id=701",
        "type": "html",
        "authority": "RBI",
        "source_type": "consumer_guidance",
        "priority": 2,
        "topics": [
            "home_loan",
            "housing_loan",
            "MITC",
            "loan_terms",
            "prepayment",
            "interest_rate",
            "offer_letter",
            "borrower_rights",
            "reverse_mortgage",
        ],
        "document_date": "2009-11-10",
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "active",
    },

    {
        "label": "03_prepayment_charges_directions_2025",
        "url": "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12878&Mode=0",
        "type": "html",
        "authority": "RBI",
        "source_type": "regulatory",
        "priority": 1,
        "topics": ["prepayment", "foreclosure", "charges", "loan_closure"],
        "document_date": "2025-07-02",
        "last_updated": None,
        "effective_from": "2026-01-01",
        "effective_until": None,
        "status": "active",
    },

    {
        "label": "04_interest_rate_on_advances_master_direction",
        "url": "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/MD20D6FC6F31E8E5458F9E0411F433B7D40A.PDF",
        "type": "pdf",
        "authority": "RBI",
        "source_type": "regulatory",
        "priority": 1,
        "topics": [
            "interest_rate",
            "advances",
            "MCLR",
            "repo_rate",
            "lending_rate",
        ],
        "document_date": "2016-03-03",
        "last_updated": "2025-10-01",
        "effective_from": "2016-03-03",
        "effective_until": None,
        "status": "active",
    },

    {
        "label": "05_housing_finance_master_circular",
        "url": "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/NT168E73C887EB7C4C69A01A0F2FB458C9AB.PDF",
        "type": "pdf",
        "authority": "RBI",
        "source_type": "regulatory",
        "priority": 1,
        "topics": [
            "housing_finance",
            "home_loan",
            "property",
            "construction",
            "housing_credit",
        ],
        "document_date": "2025-04-01",
        "last_updated": None,
        "effective_from": "2025-04-01",
        "effective_until": None,
        "status": "active",
    },

    {
        "label": "06_emi_floating_rate_reset_circular",
        "url": "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12529",
        "type": "html",
        "authority": "RBI",
        "source_type": "regulatory",
        "priority": 1,
        "topics": [
            "EMI",
            "floating_rate",
            "interest_reset",
            "personal_loans",
            "fixed_rate_switch",
        ],
        "document_date": "2023-08-18",
        "last_updated": "2025-10-01",
        "effective_from": "2023-08-18",
        "effective_until": None,
        "status": "active",
    },

    {
        "label": "07_property_document_release_circular",
        "url": "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12535&Mode=0",
        "type": "html",
        "authority": "RBI",
        "source_type": "regulatory",
        "priority": 1,
        "topics": [
            "property_documents",
            "loan_closure",
            "collateral",
            "release_of_documents",
            "compensation",
        ],
        "document_date": "2023-09-13",
        "last_updated": None,
        "effective_from": "2023-12-01",
        "effective_until": None,
        "status": "active",
    },

    {
        "label": "08_penal_charges_circular",
        "url": "https://rbi.org.in/Scripts/NotificationUser.aspx?Id=12527&Mode=0",
        "type": "html",
        "authority": "RBI",
        "source_type": "regulatory",
        "priority": 1,
        "topics": [
            "penal_charges",
            "default",
            "late_payment",
            "penal_interest",
            "MITC",  # RBI's own material says penal charges must be disclosed
                     # in the loan agreement and MITC/KFS, as applicable.
        ],
        "document_date": "2023-08-18",
        "last_updated": "2023-12-29",
        "effective_from": "2024-04-01",
        "effective_until": None,
        "status": "active",
    },

    {
        "label": "09_banking_regulation_act_1949",
        "url": "https://www.indiacode.nic.in/bitstream/123456789/1885/1/aa1949-10.pdf",
        "type": "pdf",
        "authority": "Government of India",
        "source_type": "statute",
        "priority": 1,
        "topics": [
            "banking_regulation",
            "banking_law",
            "banking_act",
            "regulated_entities",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "active",
    },


    # ==========================================================================
    # RBI — BORROWER / CUSTOMER PROTECTION
    # ==========================================================================

    {
        "label": "10_rbi_fair_practices_code",
        "url": "https://www.rbi.org.in/commonman/english/scripts/Notification.aspx?Id=1572",
        "type": "html",
        "authority": "RBI",
        "source_type": "consumer_regulatory",
        "priority": 2,
        "topics": [
            "fair_practices",
            "loan_application",
            "disclosure",
            "grievance",
            "borrower_rights",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "historical_reference",
    },

    {
        "label": "11_rbi_ombudsman_2026_faq",
        "url": "https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=3407",
        "type": "html",
        "authority": "RBI",
        "source_type": "consumer_guidance",
        "priority": 2,
        "topics": [
            "complaints",
            "grievance",
            "ombudsman",
            "consumer_protection",
            "bank_complaints",
            "NBFC_complaints",
        ],
        "document_date": "2026-07-01",
        "last_updated": None,
        "effective_from": "2026-07-01",
        "effective_until": None,
        "status": "active",
    },

    {
        "label": "12_rbi_kyc_faq_2025",
        "url": "https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=3782",
        "type": "html",
        "authority": "RBI",
        "source_type": "consumer_guidance",
        "priority": 2,
        "topics": [
            "KYC",
            "identity",
            "documents",
            "customer_due_diligence",
            "account_update",
        ],
        "document_date": "2025-06-09",
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "active",
    },

    {
        "label": "13_rbi_digital_lending_guidelines",
        "url": "https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=3547",
        "type": "html",
        "authority": "RBI",
        "source_type": "regulatory_guidance",
        "priority": 2,
        "topics": [
            "digital_lending",
            "online_loans",
            "LSP",
            "lending_service_provider",
            "KFS",
            "APR",
            "borrower_protection",
        ],
        "document_date": "2023-02-14",
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    {
        "label": "14_rbi_secured_assets_sarfaesi_faq",
        "url": "https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=3572",
        "type": "html",
        "authority": "RBI",
        "source_type": "consumer_guidance",
        "priority": 2,
        "topics": [
            "secured_loan",
            "collateral",
            "SARFAESI",
            "secured_assets",
            "default",
        ],
        "document_date": "2024-02-06",
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },


    # ==========================================================================
    # BANK-ISSUED MITC / PRODUCT TERMS
    # (real, product-specific documents — NOT general RBI rules. Keep these
    #  clearly tagged "bank_product_terms" so retrieval never answers a
    #  general regulatory question with one bank's specific facility terms.)
    # ==========================================================================

    # --- NEW: added, primary MITC document ---
    # This is ICICI's actual, dedicated page titled "Most Important Terms and
    # Conditions (MITC)" for the EMI @ UPI facility — verified live on
    # 2026-08-12. It's the better of the two ICICI URLs floating around
    # because it is literally the MITC document, not just a T&C page that
    # mentions MITC. Contains: schedule of charges, EMI/interest rate details,
    # grievance redressal, compensation policy, default reporting to credit
    # bureaus, loss/theft handling, disclosure clauses.
    {
        "label": "15_icici_emi_upi_mitc",
        "url": "https://www.icici.bank.in/personal-banking/loans/smart-loan/most-important-terms-and-conditions",
        "type": "html",
        "authority": "ICICI Bank",
        "source_type": "bank_product_terms",
        "priority": 3,
        "topics": [
            "MITC",
            "EMI",
            "charges",
            "interest_rate",
            "default",
            "credit_bureau_reporting",
            "grievance_redressal",
            "compensation_policy",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    # --- NEW: added, companion document ---
    # The fuller "Primary Terms and Conditions" page for the same facility.
    # This is where definitions, events of default, set-off/lien, indemnity,
    # and dispute-resolution clauses actually live. The MITC page above
    # explicitly refers back to this one for the complete version — so keep
    # both, linked by topic, with this one lower priority since it's the
    # supporting doc rather than the named "MITC" itself.
    {
        "label": "16_icici_emi_upi_terms_and_conditions",
        "url": "https://www.icici.bank.in/personal-banking/loans/smart-loan/terms-and-conditions-for-emi-upi",
        "type": "html",
        "authority": "ICICI Bank",
        "source_type": "bank_product_terms",
        "priority": 4,
        "topics": [
            "MITC",
            "loan_terms",
            "EMI",
            "repayment",
            "default",
            "late_payment",
            "events_of_default",
            "lien",
            "set_off",
            "indemnity",
            "dispute_resolution",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    # --- NEW: added, verified live 2026-08-12 ---
    # HDFC Bank's actual home loan MITC/T&C PDF (title tag on the landing
    # page is literally "MITC For HDFC Bank Home Loans"). Covers fees,
    # prepayment, insurance requirements, disbursement conditions, borrower
    # obligations. HDFC's home-loan business was HDFC Ltd. (an HFC) before
    # its 2023 merger into HDFC Bank — worth knowing if you want to explain
    # to the chatbot's users why some HDFC paperwork still says "HDFC" not
    # "HDFC Bank".
    {
        "label": "17_hdfc_home_loan_mitc",
        "url": "https://homeloans.hdfc.bank.in/content/dam/housingdevelopmentfinancecorp/pdf/terms-and-conditions/others/Terms-Conditions-for-HDFC-Bank-Home-Loan.pdf",
        "type": "pdf",
        "authority": "HDFC Bank",
        "source_type": "bank_product_terms",
        "priority": 4,
        "topics": [
            "MITC",
            "home_loan",
            "loan_terms",
            "fees",
            "prepayment",
            "insurance",
            "disbursement",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    # --- NEW: added, verified live 2026-08-12 ---
    # SBI's official home loan MITC PDF, hosted on their home loan subdomain.
    # Explicitly titled "SBI HOME LOAN: MOST IMPORTANT TERMS AND CONDITIONS".
    # Covers all major SBI home loan variants (regular, MaxGain, FlexiPay,
    # NRI, Privilege/Shaurya, etc.) in one document — useful because it shows
    # how one bank's MITC can bundle multiple product variants under a
    # single disclosure.
    {
        "label": "18_sbi_home_loan_mitc",
        "url": "https://homeloans.sbi.bank.in/downloads/Terms-and-Conditions.pdf",
        "type": "pdf",
        "authority": "State Bank of India",
        "source_type": "bank_product_terms",
        "priority": 4,
        "topics": [
            "MITC",
            "home_loan",
            "loan_terms",
            "penal_charges",
            "prepayment",
            "fees",
            "default",
            "disclosure",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    # --- NEW: added, verified live 2026-08-12 ---
    # Kotak Mahindra Bank's personal loan MITC PDF — short, clean, and a
    # good contrast to the HDFC/SBI home loan MITCs since it's an unsecured
    # personal loan (different fee/charge structure: foreclosure charges,
    # part-prepayment rules, EMI bounce charges, etc.).
    {
        "label": "19_kotak_personal_loan_mitc",
        "url": "https://www.kotak.bank.in/content/dam/Kotak/Customer-Service/Download-Forms/Personal-Banking/loans/personal_loan/pl-mitc-24oct.pdf",
        "type": "pdf",
        "authority": "Kotak Mahindra Bank",
        "source_type": "bank_product_terms",
        "priority": 4,
        "topics": [
            "MITC",
            "personal_loan",
            "loan_terms",
            "foreclosure",
            "prepayment",
            "penal_charges",
            "fees",
            "default",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    # --- NEW: added, verified live 2026-08-12 ---
    # Note: renamed from the originally proposed "personal_loan_mitc" — this
    # page is titled "Axis Bank Personal Loans Terms and Conditions" and
    # itself refers out to a separate "key fact sheet" for rates/fees, so
    # it's the loan-agreement companion doc (same role as
    # 16_icici_emi_upi_terms_and_conditions above), not a page literally
    # named MITC. Still valuable: has a detailed SMA/NPA classification
    # walkthrough with dated worked examples, FIFO payment-appropriation
    # order, foreclosure/cooling-off terms, and lien/set-off language that
    # none of the other bank docs in this corpus cover.
    {
        "label": "20_axis_bank_personal_loan_terms_and_conditions",
        "url": "https://www.axis.bank.in/docs/default-source/default-document-library/personal-loans-tc.pdf",
        "type": "pdf",
        "authority": "Axis Bank",
        "source_type": "bank_product_terms",
        "priority": 4,
        "topics": [
            "loan_terms",
            "personal_loan",
            "foreclosure",
            "prepayment",
            "penal_charges",
            "default",
            "NPA",
            "SMA",
            "lien",
            "set_off",
            "arbitration",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    # --- NEW: added, verified live 2026-08-12 ---
    # Bajaj Housing Finance Limited (BHFL) — a genuine HFC (NBFC), not a
    # bank, retail MITC covering both secured (home loan / LAP) and
    # unsecured loans. This is the entry that matters most for the "HFC"
    # gap: RBI's own material specifically calls out HFCs as required to
    # give borrowers this document, and this is the first non-bank lender
    # in the corpus. Notably it shows the HFC-specific 4-level grievance
    # escalation path, which ends at the *National Housing Bank* (not the
    # RBI Ombudsman that bank MITCs point to) — a genuinely different
    # regulatory pathway worth having the chatbot aware of. Also documents
    # penal/default interest (24% p.a.), pre-payment charge structure by
    # loan type, and fee schedule in detail.
    {
        "label": "21_bajaj_housing_finance_retail_mitc",
        "url": "https://www.bajajhousingfinance.in/documents/37350/3993180/MITC+-+Retail+(Secured+and+Unsecured)+-+English+(2).pdf",
        "type": "pdf",
        "authority": "Bajaj Housing Finance Limited",
        "source_type": "bank_product_terms",
        "priority": 4,
        "topics": [
            "MITC",
            "HFC",
            "home_loan",
            "loan_against_property",
            "unsecured_loan",
            "prepayment",
            "penal_charges",
            "grievance_redressal",
            "national_housing_bank",
            "fees",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },


    # ==========================================================================
    # CIBIL / CREDIT INFORMATION
    # ==========================================================================

    {
        "label": "22_cibil_score_and_report_brochure",
        "url": "https://www.cibil.com/content/dam/cibil/consumer/cibil-score-and-report-brochure-15-10-25.pdf",
        "type": "pdf",
        "authority": "TransUnion CIBIL",
        "source_type": "consumer_education",
        "priority": 3,
        "topics": [
            "CIBIL",
            "credit_score",
            "credit_report",
            "credit_information",
            "credit_history",
        ],
        "document_date": "2025-10-15",
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    {
        "label": "23_cibil_credit_score_and_loan_basics",
        "url": "https://www.cibil.com/faq/credit-score-and-loan-basics",
        "type": "html",
        "authority": "TransUnion CIBIL",
        "source_type": "consumer_education",
        "priority": 3,
        "topics": [
            "credit_score",
            "loan",
            "credit_history",
            "creditworthiness",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    {
        "label": "24_cibil_loan_rejections_and_disputes",
        "url": "https://www.cibil.com/faq/loan-rejections-disputes",
        "type": "html",
        "authority": "TransUnion CIBIL",
        "source_type": "consumer_education",
        "priority": 3,
        "topics": [
            "loan_rejection",
            "credit_report",
            "disputes",
            "creditworthiness",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    {
        "label": "25_cibil_consumer_awareness",
        "url": "https://www.cibil.com/faq/consumer-awareness",
        "type": "html",
        "authority": "TransUnion CIBIL",
        "source_type": "consumer_education",
        "priority": 3,
        "topics": [
            "consumer_awareness",
            "credit",
            "loans",
            "credit_report",
            "disputes",
            "enquiries",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    {
        "label": "26_cibil_understand_credit_score_and_report",
        "url": "https://www.cibil.com/faq/understand-your-credit-score-and-report",
        "type": "html",
        "authority": "TransUnion CIBIL",
        "source_type": "consumer_education",
        "priority": 3,
        "topics": [
            "credit_score",
            "credit_report",
            "credit_history",
            "enquiries",
            "account_information",
            "payment_history",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

    {
        "label": "27_cibil_report_understanding",
        "url": "https://www.cibil.com/content/dam/cibil/consumer/CIBIL-Report-Understanding.pdf",
        "type": "pdf",
        "authority": "TransUnion CIBIL",
        "source_type": "consumer_education",
        "priority": 3,
        "topics": [
            "credit_report",
            "credit_score",
            "account_information",
            "payment_history",
            "credit_enquiries",
            "overdue",
            "credit_utilisation",
        ],
        "document_date": None,
        "last_updated": None,
        "effective_from": None,
        "effective_until": None,
        "status": "reference",
    },

]


# Directory paths for outputs
OUTPUT_DIR = Path("output")
RAW_DIR = OUTPUT_DIR / "raw"
PROCESSED_DIR = OUTPUT_DIR / "processed"
METADATA_DIR = OUTPUT_DIR / "metadata"

# Manual-fallback folder: if a site's bot-protection blocks this script
# entirely (see note in process_url), manually download the file in a real
# browser and save it here as "<label>.pdf" or "<label>.html" — the script
# will pick it up automatically when the live fetch fails.
MANUAL_DIR = OUTPUT_DIR / "manual"

RETRY_DELAY_SECONDS = 8.0  # pause before retrying once on 403/429/503


def setup_directories():
    """Ensure all required output folders exist."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    MANUAL_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# 2. PDF TEXT EXTRACTION
# ==============================================================================
def extract_pdf_text(pdf_file_path: Path) -> str:
    """
    Extracts text from a PDF file using pdfplumber, inserting page break markers
    (e.g., '--- Page 1 ---') so page references are preserved in the text output.
    """
    page_texts = []
    with pdfplumber.open(pdf_file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            page_texts.append(f"--- Page {page_num} ---\n{text.strip()}")
    
    return "\n\n".join(page_texts)


# ==============================================================================
# 3. HTML TEXT EXTRACTION
# ==============================================================================
def extract_html_text(html_content: str) -> str:
    """
    Strips navigation menus, headers, footers, scripts, and styles from HTML content,
    returning only clean, readable main body text.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # List of HTML tags to strip out completely
    unwanted_tags = [
        "script", "style", "nav", "header", "footer", 
        "aside", "form", "noscript", "iframe", "svg"
    ]
    for tag in soup(unwanted_tags):
        tag.decompose()

    # Extract lines of text, strip trailing whitespace, and filter empty lines
    lines = soup.get_text(separator="\n").splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    
    return "\n".join(cleaned_lines)


# ==============================================================================
# MAIN PROCESSING LOGIC
# ==============================================================================
def process_url(item: dict, force: bool) -> str:
    """
    Processes a single URL entry.
    Returns status string: "downloaded", "skipped", or raises Exception on error.
    """
    url = item.get("url")
    label = item.get("label")
    doc_type = item.get("type", "").lower()

    if not url or not label or doc_type not in ("pdf", "html"):
        raise ValueError(f"Invalid config item: {item}. Must include 'url', 'label', and 'type' ('pdf' or 'html').")

    # Define output file paths
    raw_pdf_path = RAW_DIR / f"{label}.pdf"
    processed_txt_path = PROCESSED_DIR / f"{label}.txt"
    metadata_json_path = METADATA_DIR / f"{label}.json"

    # Check if document already exists in output (unless force=True)
    if not force:
        already_in_output = (
            processed_txt_path.exists() and
            metadata_json_path.exists() and
            (doc_type != "pdf" or raw_pdf_path.exists())
        )
        if already_in_output:
            print(f"[SKIPPED] '{label}' - Already exists in output.")
            return "skipped"

    # Set standard browser user-agent header to avoid bot-blocking (403 errors)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }

    # Manual-fallback path: if a site's bot-protection blocks scripted
    # requests outright (common WAFs like Akamai/Cloudflare won't pass a
    # plain `requests` call no matter how good the headers are — they check
    # things like JS execution or TLS fingerprint that this script can't
    # replicate), you can manually download the file yourself in a real
    # browser and drop it here. If the live fetch below fails, the script
    # checks this folder before giving up.
    manual_pdf_path = MANUAL_DIR / f"{label}.pdf"
    manual_html_path = MANUAL_DIR / f"{label}.html"

    # Fetch document content from URL (one retry after a longer pause on
    # 403/429/503, since some blocks are just rate-limiting)
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code in (403, 429, 503):
            time.sleep(RETRY_DELAY_SECONDS)
            response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        content_bytes = response.content
        used_manual_fallback = False
    except Exception as live_fetch_error:
        # Live fetch failed even after retry — check for a manually placed
        # file before giving up entirely.
        manual_path = manual_pdf_path if doc_type == "pdf" else manual_html_path
        if manual_path.exists():
            with open(manual_path, "rb") as f:
                content_bytes = f.read()
            used_manual_fallback = True
            print(f"[MANUAL FALLBACK] '{label}' - using manually saved file (live fetch failed: {live_fetch_error})")
        else:
            raise

    # Calculate SHA256 hash of downloaded content
    content_hash = hashlib.sha256(content_bytes).hexdigest()

    # Process document according to type
    if doc_type == "pdf":
        # Save raw PDF file to output/raw/
        with open(raw_pdf_path, "wb") as f:
            f.write(content_bytes)

        # Extract text from PDF
        extracted_text = extract_pdf_text(raw_pdf_path)

    elif doc_type == "html":
        # Decode HTML text and clean structure. If we used the manual
        # fallback file, decode the raw bytes ourselves (no `response`
        # object exists in that path); otherwise use requests' own decoding.
        if used_manual_fallback:
            html_str = content_bytes.decode("utf-8", errors="replace")
        else:
            html_str = response.text
        extracted_text = extract_html_text(html_str)

    # Save extracted text to output/processed/
    with open(processed_txt_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    # Save JSON metadata to output/metadata/
    # Everything beyond the core download-tracking fields (sha256,
    # text_sha256, downloaded_at) is pulled straight from URL_CONFIG via
    # .get(), so this stays in sync automatically if you add/remove fields
    # in url_config_final.py — no need to edit this block for that.
    metadata = {
        "url": url,
        "label": label,
        "file_type": doc_type,
        "sha256": content_hash,
        "text_sha256": hashlib.sha256(extracted_text.encode("utf-8")).hexdigest(),
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        # --- corpus metadata, carried through from URL_CONFIG ---
        "authority": item.get("authority"),
        "source_type": item.get("source_type"),
        "priority": item.get("priority"),
        "topics": item.get("topics"),
        "document_date": item.get("document_date"),
        "last_updated": item.get("last_updated"),
        "effective_from": item.get("effective_from"),
        "effective_until": item.get("effective_until"),
        "status": item.get("status"),
    }
    with open(metadata_json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"[DOWNLOADED] '{label}' successfully processed.")
    return "downloaded"


def main():
    parser = argparse.ArgumentParser(description="Download and extract text from PDFs and Webpages.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download and re-extract text even if the file hash matches existing cache."
    )
    args = parser.parse_args()

    setup_directories()

    downloaded_count = 0
    skipped_count = 0
    failed_items = []

    print("=" * 60)
    print(f"Starting Document Downloader (Force Mode: {args.force})")
    print(f"Total items configured: {len(URL_CONFIG)}")
    print("=" * 60)

    for item in URL_CONFIG:
        label = item.get("label", "unknown")
        url = item.get("url", "")
        try:
            status = process_url(item, force=args.force)
            if status == "downloaded":
                downloaded_count += 1
            elif status == "skipped":
                skipped_count += 1
        except Exception as err:
            print(f"[FAILED] '{label}' ({url}) -> Error: {err}")
            failed_items.append({"label": label, "url": url, "error": str(err)})

    # ==============================================================================
    # SUMMARY REPORT
    # ==============================================================================
    print("\n" + "=" * 60)
    print("DOWNLOAD & EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Downloaded / Processed : {downloaded_count}")
    print(f"Skipped (Unchanged)   : {skipped_count}")
    print(f"Failed                : {len(failed_items)}")
    print("=" * 60)

    if failed_items:
        print("\nFAILED URLs LIST:")
        for item in failed_items:
            print(f" - [{item['label']}] {item['url']}\n   Reason: {item['error']}")
        print("=" * 60)


if __name__ == "__main__":
    main()