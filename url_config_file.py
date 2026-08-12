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
        "priority": 4,
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