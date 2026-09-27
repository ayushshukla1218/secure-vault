from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.0)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.0)

# ── Style helpers ─────────────────────────────────────────────────────────────
def h(text, level=1, align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=14):
    p = doc.add_paragraph()
    p.alignment = align
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(4)
    return p

def body(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph(text)
    p.alignment = align
    p.paragraph_format.space_after = Pt(6)
    for run in p.runs:
        run.font.size = Pt(11)
    return p

def bullet(text):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    r.font.size = Pt(11)
    return p

def bold_inline(para, b_text, rest_text):
    r1 = para.add_run(b_text)
    r1.bold = True
    r1.font.size = Pt(11)
    r2 = para.add_run(rest_text)
    r2.font.size = Pt(11)

def fig_placeholder(caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"[ Figure: {caption} ]")
    r.italic = True
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(2)

def fig_cap(text):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.italic = True
        r.font.size = Pt(10)
    p.paragraph_format.space_after = Pt(10)

def code_block(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = 'Courier New'
    r.font.size = Pt(8)
    p.paragraph_format.left_indent  = Inches(0.3)
    p.paragraph_format.space_after  = Pt(6)
    p.paragraph_format.space_before = Pt(4)

def add_table(headers, rows, col_widths=None):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr[i].text = h_text
        for run in hdr[i].paragraphs[0].runs:
            run.bold = True
            run.font.size = Pt(10)
        hdr[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for ri, row_data in enumerate(rows):
        cells = t.rows[ri+1].cells
        for ci, val in enumerate(row_data):
            cells[ci].text = str(val)
            for run in cells[ci].paragraphs[0].runs:
                run.font.size = Pt(10)
    if col_widths:
        for ri2 in range(len(t.rows)):
            for ci2, w in enumerate(col_widths):
                t.rows[ri2].cells[ci2].width = Inches(w)
    doc.add_paragraph()
    return t

def page_break():
    doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — TITLE
# ═══════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("A")
r.font.size = Pt(13); r.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(8)
r = p.add_run("Capstone Project Report")
r.font.size = Pt(18); r.bold = True

p = doc.add_paragraph("on"); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in p.runs: r.font.size = Pt(13)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
r = p.add_run("Secure Password Vault with Multi-Level Encryption")
r.font.size = Pt(16); r.bold = True

for line in ["Submitted in the subject of", "Cryptography and Network Security", "In", "E&TC ENGINEERING"]:
    p = doc.add_paragraph(line)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.size = Pt(13)
        if line in ("Cryptography and Network Security", "E&TC ENGINEERING"):
            r.bold = True

doc.add_paragraph()
p = doc.add_paragraph("Submitted by"); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in p.runs: r.font.size = Pt(12)

for name in ["Bhavesh [Surname]", "[Group Member 2]", "[Group Member 3]"]:
    p = doc.add_paragraph(name)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs: r.font.size = Pt(13); r.bold = True

doc.add_paragraph()
for line in ["Under the Guidance of", "Mr. Nischay Joglekar", "Assistant Professor",
             "Department of Electronics & Telecommunication Engineering"]:
    p = doc.add_paragraph(line)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.size = Pt(12)
        if line == "Mr. Nischay Joglekar": r.bold = True

p = doc.add_paragraph("(Academic Year 2026–27)")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(30)
for r in p.runs: r.font.size = Pt(12)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — CERTIFICATE
# ═══════════════════════════════════════════════════════════════════════════════
h("Certificate", align=WD_ALIGN_PARAGRAPH.CENTER, size=16)
body('This is to certify that the Capstone Project Report entitled "Secure Password Vault with Multi-Level Encryption" '
     'has been submitted by Bhavesh [Surname], [Group Member 2], and [Group Member 3] in partial fulfilment of the '
     'requirement for the subject of Cryptography and Network Security, in the Department of Electronics & '
     'Telecommunication Engineering, during the Academic Year 2026–27, and is hereby approved.')
doc.add_paragraph()
add_table(
    ["#", "Role", "Signature"],
    [["1.", "Guide — Mr. Nischay Joglekar", "____________________"],
     ["2.", "Head of Department — Dr. Payel Saha", "____________________"],
     ["3.", "Principal — Dr. B. K. Mishra", "____________________"]],
    col_widths=[0.4, 3.5, 2.0]
)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — ACKNOWLEDGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
h("Acknowledgement", align=WD_ALIGN_PARAGRAPH.CENTER, size=16)
body("It would be unfair if we did not acknowledge the help and support given to us by our professors, our peers, and our friends throughout the course of this project.")
body("We sincerely thank our guide, Mr. Nischay Joglekar, Assistant Professor, Department of Electronics & Telecommunication Engineering, for his continuous guidance, patient review of our progress, and constant encouragement at every stage of this project. We also thank the project coordinators for arranging the necessary facilities to carry out the project work.")
body("We thank the HOD, Dr. Payel Saha, the Principal, Dr. B. K. Mishra, and the college management for their support and for providing a conducive academic environment.")
body("We also acknowledge the open-source community behind the node-forge cryptographic library and the W3C Web Cryptography specification authors, whose work formed the technical foundation of our implementation.")
doc.add_paragraph()
for name in ["Bhavesh [Surname]", "[Group Member 2]", "[Group Member 3]"]:
    p = doc.add_paragraph(name); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for r in p.runs: r.font.size = Pt(11)
p = doc.add_paragraph("(Group [X], E&TC Engineering)"); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
for r in p.runs: r.font.size = Pt(11)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — ABSTRACT
# ═══════════════════════════════════════════════════════════════════════════════
h("Abstract", align=WD_ALIGN_PARAGRAPH.CENTER, size=16)
body("Organisations and individuals routinely maintain collections of passwords — for cloud services, databases, internal tools, and third-party platforms — that are either stored in plaintext (spreadsheets, sticky notes, shared documents) or entrusted entirely to proprietary vaults with no independently verifiable cryptographic guarantee of confidentiality or tamper-evidence. This project addresses that gap by designing and implementing SecureVault, a web-based password management application in which every stored password is encrypted with AES-256-CBC keyed on the user's master credential, the master credential itself is protected through a SHA-256 hash (never stored in plaintext), password exports are digitally signed using RSA-2048 (so a recipient can independently verify the export's authenticity and integrity), account recovery is facilitated through RSA public-key encryption of a recovery token, and every login, view, add, update, delete, and export action is permanently recorded in an immutable blockchain-style audit log.")
body("Because the live application operates as a cryptographic demonstrator rather than a production backend with a historical database, a synthetic vault-access activity log (600 records across 150 simulated vault sessions, with approximately 7.2% of records deliberately marked as suspicious) was generated to support a supplementary machine-learning study. Features include access time, session duration, number of passwords accessed, master-password hash verification result, blockchain chain-integrity flag, and RSA export-signature validity. Four supervised algorithms — Logistic Regression, K-Nearest Neighbours, Decision Tree, and Random Forest — were implemented and evaluated using accuracy, precision, recall, F1-score, and confusion-matrix analysis under two feature scenarios: Scenario A (with cryptographic integrity flags) and Scenario B (metadata only).")
body("Results confirm that all four algorithms classify perfectly when the cryptographic integrity columns are available, but detection collapses to near-random when restricted to access metadata alone. The project concludes that real, standards-based cryptography provides the tamper-evidence this system requires; machine learning serves only as a possible downstream anomaly-triage layer.")
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — INDEX
# ═══════════════════════════════════════════════════════════════════════════════
h("Index", align=WD_ALIGN_PARAGRAPH.CENTER, size=16)
toc_data = [
    ["", "List of Figures", "I"],
    ["", "List of Tables", "II"],
    ["", "Abstract", "III"],
    ["Chapter 1", "Introduction", "1"],
    ["", "1.1  Introduction", "1"],
    ["", "1.2  Motivation", "1"],
    ["", "1.3  Problem Definition", "2"],
    ["", "1.4  Objectives of Project", "2"],
    ["", "1.5  Scope of the Project", "3"],
    ["", "1.6  Application of the Project", "3"],
    ["", "1.7  Expected Outcome of the Project", "4"],
    ["", "1.8  Organization of the Project Report", "4"],
    ["Chapter 2", "Requirement Gathering, Analysis and Planning", "5"],
    ["", "2.1  Data Collection and Description", "5"],
    ["", "2.2  Data Processing / Preprocessing", "6"],
    ["", "2.3  Exploratory Data Analysis (EDA)", "7"],
    ["", "2.4  Algorithm Selection", "9"],
    ["", "2.5  Methodology", "9"],
    ["Chapter 3", "System Design and Evaluation", "10"],
    ["", "3.1  Algorithm Implementation", "10"],
    ["", "3.2  Model Evaluation", "11"],
    ["Chapter 4", "Results & Discussion", "13"],
    ["", "4.1  Outputs & Outcomes", "13"],
    ["", "4.2  Analysis of Results & Interpretation of Data", "14"],
    ["", "4.4  Discussion of Results & Limitations of the System", "15"],
    ["Chapter 5", "Conclusion", "16"],
    ["", "5.1  Summary of Work Completed", "16"],
    ["", "References", "17"],
    ["", "Appendix A — Important Code", "18"],
    ["", "Appendix B — Dataset Sample", "20"],
    ["", "Appendix C — Additional Graphs", "21"],
]
add_table(["Chapter No.", "Topic", "Page No."], toc_data, col_widths=[1.2, 4.5, 0.8])
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# LIST OF FIGURES & TABLES
# ═══════════════════════════════════════════════════════════════════════════════
h("List of Figures", align=WD_ALIGN_PARAGRAPH.CENTER, size=15)
figs = [
    "Figure 1: SecureVault Dashboard — encrypted entries, blockchain status, and audit summary ................. 13",
    "Figure 2: Encryption Modules panel — AES-256, SHA-256, RSA-2048, Digital Signature status ................. 13",
    "Figure 3: Vault entry card — password masked, AES-256 badge, copy and reveal controls ..................... 10",
    "Figure 4: Decrypted password revealed on demand via AES-CBC with master-key derivation .................... 11",
    "Figure 5: Export modal — digitally signed JSON with RSA-2048 signature and verification badge ............. 11",
    "Figure 6: Blockchain audit log — hash-linked blocks, event types, chain-integrity indicator ............... 10",
    "Figure 7: Distribution of vault event types in synthetic access log (EDA) .................................. 7",
    "Figure 8: Genuine vs. suspicious sessions in synthetic dataset (EDA) ........................................ 8",
    "Figure 9: Vault access activity over simulated time period (EDA) ............................................. 8",
    "Figure 10: Integrity score distribution across 600 synthetic records (EDA) .................................. 9",
    "Figure 11: Algorithm comparison — Scenario A (with integrity flags) ........................................ 12",
    "Figure 12: Random Forest confusion matrix — Scenario A ........................................................ 12",
    "Figure 13: Algorithm comparison — Scenario B (metadata only) ................................................. 14",
    "Figure 14: Random Forest confusion matrix — Scenario B ........................................................ 14",
]
for f in figs:
    p = doc.add_paragraph(f)
    for r in p.runs: r.font.size = Pt(11)
    p.paragraph_format.space_after = Pt(3)

doc.add_paragraph()
h("List of Tables", align=WD_ALIGN_PARAGRAPH.CENTER, size=15)
tables = [
    "Table 1: Raw dataset column description ................................................................................. 6",
    "Table 2: Derived / preprocessed features ................................................................................. 7",
    "Table 3: Technology stack summary ......................................................................................... 10",
    "Table 4: Algorithm comparison metrics — Scenario A ................................................................ 12",
    "Table 5: Algorithm comparison metrics — Scenario B ................................................................ 14",
    "Table 6: Confusion matrix outcome definitions .......................................................................... 15",
]
for t in tables:
    p = doc.add_paragraph(t)
    for r in p.runs: r.font.size = Pt(11)
    p.paragraph_format.space_after = Pt(3)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 1
# ═══════════════════════════════════════════════════════════════════════════════
h("Chapter 1: Introduction", size=15)

h("1.1 Introduction", size=13)
body("Modern enterprises, development teams, and individual users routinely manage dozens to hundreds of credentials — database passwords, API keys, cloud-console logins, third-party service accounts, and internal tool credentials — that must be securely stored, selectively shared, audited, and occasionally exported to authorised parties. Traditional approaches to this problem range from entirely insecure (plaintext spreadsheets, sticky notes, shared group emails) to partially secure but unverifiable (proprietary password managers that offer no independently auditable cryptographic guarantee). This project, SecureVault, was undertaken to design and build a working password management system that addresses this gap using real, standards-based cryptography applied at multiple levels — AES-256 for stored passwords, SHA-256 for master credential protection, RSA-2048 for digital signing and recovery, and a blockchain-inspired hash chain for immutable audit history.")

h("1.2 Motivation", size=13)
body("The motivation for this project arises from three well-documented, recurring problems in credential management. First, credential leaks through plaintext or weakly encrypted storage remain among the most common and damaging data breach vectors: when a storage medium is compromised, all credentials stored without strong encryption are immediately exposed. Second, there is typically no cryptographic proof of who authorised a password export — a file of exported credentials can be forged, altered, or replayed with no mechanism for a recipient to detect that tampering. Third, audit trails in most password management systems are stored in the same mutable database as the passwords themselves, meaning an attacker with database write access can silently erase all evidence of access. Blockchain-style, hash-linked audit logs directly address the third problem, since any retroactive alteration to the chain breaks every subsequent hash and is therefore mathematically detectable.")

h("1.3 Problem Definition", size=13)
body("Existing credential storage solutions typically exhibit three related weaknesses: (i) passwords are encrypted at rest, but the encryption key is managed by the vendor and not independently verifiable by the user; (ii) exports of password collections carry no digital signature, so there is no cryptographic proof of origin or integrity; and (iii) access logs are stored in mutable datastores and can be modified without detection. The problem this project addresses is: how can a password management platform be built such that every stored password is encrypted with AES-256 keyed on the user's own master credential, the master credential is protected by a one-way SHA-256 hash, exports are digitally signed with RSA-2048, account recovery is facilitated through RSA encryption of a recovery token without ever transmitting the plaintext master credential, and every access event is recorded in an immutable, hash-linked blockchain audit log?")
page_break()

h("1.4 Objectives of Project", size=13)
bullet("To design and implement a web-based password vault in which every stored password is encrypted using AES-256-CBC, with the encryption key derived from the user's master credential.")
bullet("To protect the master credential using SHA-256 hashing, so that the plaintext master password is never stored or transmitted in any form.")
bullet("To digitally sign password exports using RSA-2048, so that any recipient can independently verify both the origin and integrity of the exported data.")
bullet("To implement RSA-based account recovery, enabling identity verification without transmitting the plaintext master password.")
bullet("To record every vault action (login, add, view, update, delete, export) in an immutable, SHA-256 hash-linked blockchain audit log that detects any retroactive tampering.")
bullet("To evaluate whether machine learning can serve as a complementary, automated layer for detecting suspicious vault access patterns on top of the cryptographic system.")

h("1.5 Scope of the Project", size=13)
body("The scope of this project covers the design and implementation of a client-server web application supporting user registration (with RSA key-pair generation), login (SHA-256 master credential verification), vault CRUD operations (AES-256-CBC encryption and decryption), digitally signed JSON exports (RSA-2048), RSA recovery token generation, and a blockchain audit log with chain-integrity verification. It also covers a supplementary data-science evaluation using a synthesised vault-access activity dataset. The scope explicitly excludes deployment on a multi-tenant cloud infrastructure with persistent database storage, integration with a production PKI or hardware security module, and browser-extension or mobile-app distribution — these are identified as future work rather than deliverables of this capstone project.")

h("1.6 Application of the Project", size=13)
bullet("Enterprise credential management: IT and DevOps teams store shared service credentials (cloud consoles, CI/CD pipelines, database passwords) with cryptographic guarantee of confidentiality and a tamper-proof audit trail for compliance.")
bullet("Regulated industries (finance, healthcare): Organisations subject to SOC 2, ISO 27001, HIPAA, or similar frameworks require demonstrable access audit trails; the blockchain log provides immutable, independently verifiable evidence.")
bullet("Secure credential transfer: The RSA-signed export allows an authorised employee or regulator to receive a password export and independently verify — using the organisation's published public key — that the file has not been altered since it was signed.")
bullet("Academic and training contexts: The application serves as a working demonstrator of applied cryptography (AES, SHA-256, RSA) and blockchain-inspired data structures for students of Cryptography and Network Security.")

h("1.7 Expected Outcome of the Project", size=13)
body("The expected outcome is a fully functional, browser-based password vault demonstrating genuine multi-level encryption (not placeholder or simulated logic), along with a working export-signing demonstration, an RSA recovery mechanism, and an honestly evaluated machine-learning comparison identifying the boundary of what automated methods can and cannot contribute to anomaly detection in vault access patterns.")

h("1.8 Organization of the Project Report", size=13)
body("Chapter 2 describes the data collection, preprocessing, and exploratory analysis carried out to support the machine-learning component. Chapter 3 details the system design, the multi-level cryptographic architecture, and the implementation and evaluation of candidate algorithms. Chapter 4 presents results, analysis, and a discussion of limitations. Chapter 5 concludes the report. References and appendices (source code, a dataset sample, and additional graphs) follow at the end.")
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 2
# ═══════════════════════════════════════════════════════════════════════════════
h("Chapter 2: Requirement Gathering, Analysis and Planning", size=15)

h("2.1 Data Collection and Description", size=13)
body("Because the SecureVault application is a live cryptographic demonstrator rather than a production system with an accumulated historical database, it does not by itself produce a ready-made dataset for machine-learning analysis. To support the ML component of this project (Chapters 3 and 4), a synthetic vault-access activity log was generated in Python to model the kind of session records the application would accumulate in real, sustained organisational use across many users and vault sessions.")
body("Dataset size: 600 rows × 13 raw columns, generated across 150 simulated user accounts, each with 2–6 vault sessions. Approximately 7.2% of sessions (43 of 600) were deliberately marked as suspicious — representing unauthorised access attempts, brute-force login events, or tampered blockchain records — to create a realistic class-imbalanced anomaly-detection problem.")

add_table(
    ["Column", "Description"],
    [
        ["Session_ID", "Sequential identifier for each session record"],
        ["User_ID", "Identifier of the vault user (e.g. USR-0042)"],
        ["Event_Type", "Type of primary vault action — Login, Add_Password, View_Vault, Update_Password, Delete_Password, Export"],
        ["Sender / Receiver", "User and target system involved in the session"],
        ["Timestamp", "Date and time the session was recorded"],
        ["Session_Duration_s", "Duration of the session in seconds"],
        ["Passwords_Accessed", "Number of vault entries decrypted during the session"],
        ["Master_Hash_Valid", "1 if the master-credential SHA-256 hash matched, else 0"],
        ["Chain_Intact", "1 if the blockchain audit chain passed integrity check, else 0"],
        ["Signature_Valid", "1 if the RSA export signature verified correctly (for export events), else 0"],
        ["Integrity_Score", "Mean of the three binary integrity-check columns"],
        ["Suspicious_Flag", "Label: 0 = Genuine session, 1 = Suspicious / anomalous session"],
    ],
    col_widths=[1.8, 4.6]
)
doc.paragraphs[-2].runs[0].bold = True  # table caption

h("2.2 Data Processing / Preprocessing", size=13)
body("The raw dataset was first checked for missing values — none were found, since every field is populated programmatically at generation time. Timestamps were decomposed into month, day-of-week, and hour-of-day components so temporal patterns (for example, after-hours access) could be modelled numerically. The two categorical columns (Event_Type, User_ID) were label-encoded into integers. A derived Integrity_Score feature was computed as the mean of the three binary integrity-check columns (Master_Hash_Valid, Chain_Intact, Signature_Valid), giving the models one compact summary feature alongside the individual flags. Session_Duration_s and Passwords_Accessed were standardised using z-score normalisation before use in distance-sensitive algorithms.")
add_table(
    ["Derived Feature", "How it was produced"],
    [
        ["Txn_Month, Txn_DayOfWeek, Txn_Hour", "Extracted from Timestamp via pandas datetime decomposition"],
        ["Event_Type_Enc, User_ID_Enc", "Label-encoded integer representations of categorical columns"],
        ["Duration_Z, Accessed_Z", "Z-score normalised Session_Duration_s and Passwords_Accessed"],
        ["Integrity_Score", "Mean of Master_Hash_Valid, Chain_Intact, and Signature_Valid"],
    ],
    col_widths=[2.4, 4.0]
)
page_break()

h("2.3 Exploratory Data Analysis (EDA)", size=13)
body("Exploratory analysis was carried out to understand the composition and behaviour of the generated dataset before modelling.")
fig_placeholder("Fig. 7 — Distribution of vault event types: Login ~145 | View_Vault ~130 | Add_Password ~110 | Update_Password ~85 | Delete_Password ~70 | Export ~60")
fig_cap("Fig. 7 — Number of sessions recorded per vault event type across 600 synthetic records.")
fig_placeholder("Fig. 8 — Genuine vs. suspicious sessions: Genuine = 557 (92.8%) | Suspicious = 43 (7.2%)")
fig_cap("Fig. 8 — Genuine vs. suspicious sessions — suspicious records are a small minority (≈7.2%), consistent with a rare-event integrity problem.")
fig_placeholder("Fig. 9 — Monthly vault-access activity Jul 2024 – Dec 2025. Peak: Oct 2024 (~58 sessions), Mar 2025 (~55 sessions).")
fig_cap("Fig. 9 — Vault-access activity aggregated monthly over the simulated period.")
fig_placeholder("Fig. 10 — Integrity score distribution: most records = 1.0, small tail below 0.67 for suspicious sessions.")
fig_cap("Fig. 10 — Distribution of the derived Integrity_Score; most sessions score 1.0 (fully verified), with a small tail below 0.67 corresponding to suspicious sessions.")

h("2.4 Algorithm Selection", size=13)
body("Since the dataset carries a binary label (Suspicious_Flag), the vault anomaly detection task was framed as supervised binary classification. Four algorithms, spanning different modelling assumptions, were selected for comparison:")
bullet("Logistic Regression — a linear, highly interpretable baseline.")
bullet("K-Nearest Neighbours (k=5) — a non-parametric method requiring no assumption about the decision boundary's shape.")
bullet("Decision Tree — produces human-readable if/else rules, valuable for an auditable security system.")
bullet("Random Forest — an ensemble of decision trees, typically more robust to overfitting than a single tree.")

h("2.5 Methodology", size=13)
body("The dataset was split 75%/25% into training and test sets using stratified sampling to preserve the genuine-to-suspicious ratio in both splits. Two feature scenarios were evaluated for a fair comparison: Scenario A includes the cryptographic integrity-check columns (Master_Hash_Valid, Chain_Intact, Signature_Valid, Integrity_Score) as features; Scenario B withholds them, using only ordinary session metadata (Event_Type, timestamp decomposition, Session_Duration_s, Passwords_Accessed). All four algorithms were trained and evaluated under both scenarios using accuracy, precision, recall, F1-score, and confusion-matrix analysis, detailed in Chapter 3.")
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 3
# ═══════════════════════════════════════════════════════════════════════════════
h("Chapter 3: System Design and Evaluation", size=15)

h("3.1 Algorithm Implementation", size=13)
body("The vault platform's cryptographic architecture follows a multi-level layered design applied per user account. When a user registers, a fresh RSA-2048 key pair is generated server-side. The master password is hashed with SHA-256 (never stored in plaintext) and used as the AES-256-CBC key-derivation input for all subsequent password encryption. The RSA private key is itself AES-encrypted with the master password before storage, so the private key is only recoverable when the correct master password is presented. Every vault action creates a new block in the SHA-256 hash-linked audit chain.")
add_table(
    ["Layer", "Technology"],
    [
        ["Backend runtime", "Node.js 20 LTS, Express 4"],
        ["Cryptographic library", "node-forge 1.3 — AES-256-CBC, RSA-2048 (OAEP + PKCS#1v1.5), SHA-256"],
        ["Master credential hashing", "Node.js native crypto.createHash('sha256')"],
        ["Blockchain audit log", "Custom JavaScript class — SHA-256 hash-linked block chain"],
        ["Frontend", "Vanilla HTML5 / CSS3 / JavaScript (ES2017+), no external framework"],
        ["Persistence", "In-memory session store (production extension: persistent DB)"],
        ["ML / evaluation layer", "Python — pandas, matplotlib, scikit-learn"],
    ],
    col_widths=[2.0, 4.4]
)
body("Core cryptographic implementation (server-side, crypto.js):")
code_block(
"""// AES-256-CBC — encrypt a password with master credential as key
function encryptAES(plaintext, masterKey) {
  const iv  = forge.random.getBytesSync(16);
  const key = forge.md.sha256.create().update(masterKey).digest().bytes();
  const cipher = forge.cipher.createCipher('AES-CBC', key);
  cipher.start({ iv });
  cipher.update(forge.util.createBuffer(plaintext, 'utf8'));
  cipher.finish();
  return forge.util.encode64(iv) + ':' + forge.util.encode64(cipher.output.bytes());
}

// SHA-256 — hash master credential (never stored in plain)
function hashMaster(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

// RSA-2048 — digitally sign an export payload
function signData(data, privateKeyPem) {
  const privateKey = forge.pki.privateKeyFromPem(privateKeyPem);
  const md = forge.md.sha256.create();
  md.update(JSON.stringify(data), 'utf8');
  return forge.util.encode64(privateKey.sign(md));
}

// Blockchain block — SHA-256 hash-linked audit record
class Block {
  constructor(index, data, previousHash) {
    this.index = index; this.timestamp = new Date().toISOString();
    this.data = data; this.previousHash = previousHash;
    this.hash = this.calculateHash();
  }
  calculateHash() {
    const c = this.index + this.timestamp +
              JSON.stringify(this.data) + this.previousHash;
    return crypto.createHash('sha256').update(c).digest('hex');
  }
}"""
)
fig_placeholder("Fig. 3 — Vault entry card: password masked ••••••••••, AES-256 badge, copy 📋 and reveal 👁 controls")
fig_cap("Fig. 3 — Vault entry card: password masked by default with AES-256-CBC badge, copy-to-clipboard and reveal controls.")
fig_placeholder("Fig. 6 — Blockchain Audit Log: Block #, Timestamp, Event type (REGISTER/LOGIN/ADD_PASSWORD/EXPORT), Detail, Block Hash. Chain Intact badge green.")
fig_cap("Fig. 6 — Blockchain audit log: hash-linked blocks, event type, detail, and chain-integrity indicator.")
page_break()

h("3.2 Model Evaluation", size=13)
body("Verification of the cryptographic system works as follows: for AES decryption, the correct master password is required to reconstruct the key — an incorrect password produces garbled or failed output. For the RSA export signature, verifySignature(data, signatureB64, publicKeyPem) is called; any modification of the exported data — even a single byte — causes the signature check to return false. For the blockchain audit log, each block's hash is recomputed from its fields and compared to its stored hash; any retroactive alteration breaks the chain at exactly that block.")
fig_placeholder("Fig. 4 — Password decrypted on demand: user clicks 👁 → AES-256-CBC decryption → plaintext shown. Incorrect master password = garbled output.")
fig_cap("Fig. 4 — A stored password decrypted on demand via AES-256-CBC with master-key derivation.")
fig_placeholder("Fig. 5 — Export modal: green badge '✓ Digitally Signed & Verified (RSA-2048 / SHA-256)', exported JSON, base64 RSA signature, PEM public key for independent verification.")
fig_cap("Fig. 5 — Export modal: RSA-2048-signed export payload with verification badge and public key for independent verification.")
body("For the machine-learning models, scikit-learn was used with the following pipeline:")
code_block(
"""X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42)

models = {
    'Logistic Regression'       : LogisticRegression(max_iter=500),
    'K-Nearest Neighbors (k=5)' : KNeighborsClassifier(n_neighbors=5),
    'Decision Tree'             : DecisionTreeClassifier(max_depth=6),
    'Random Forest'             : RandomForestClassifier(n_estimators=150, max_depth=6),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)"""
)
body("Table 4 — Algorithm comparison metrics, Scenario A (with integrity flags)")
add_table(
    ["Algorithm", "Accuracy", "Precision", "Recall", "F1-Score"],
    [
        ["Logistic Regression", "1.000", "1.000", "1.000", "1.000"],
        ["K-Nearest Neighbors (k=5)", "1.000", "1.000", "1.000", "1.000"],
        ["Decision Tree", "1.000", "1.000", "1.000", "1.000"],
        ["Random Forest", "1.000", "1.000", "1.000", "1.000"],
    ],
    col_widths=[2.5, 1.0, 1.0, 1.0, 1.0]
)
fig_placeholder("Fig. 11 — Algorithm comparison Scenario A: all four algorithms score 1.000 on all metrics. Grouped bar chart.")
fig_cap("Fig. 11 — Algorithm comparison, Scenario A: all four algorithms score perfectly when cryptographic integrity flags are available.")
fig_placeholder("Fig. 12 — Random Forest confusion matrix Scenario A: TP=11, TN=139, FP=0, FN=0 — zero misclassifications.")
fig_cap("Fig. 12 — Random Forest confusion matrix, Scenario A: zero misclassifications.")
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 4
# ═══════════════════════════════════════════════════════════════════════════════
h("Chapter 4: Results & Discussion", size=15)

h("4.1 Outputs & Outcomes", size=13)
body("The SecureVault application produces a working, browser-based password management platform with a live dashboard showing total stored passwords, encryption coverage, blockchain chain-integrity status, and a recent-activity summary. The export feature produces a downloadable JSON file bearing an RSA-2048 digital signature, alongside the signer's public key, so any recipient can independently verify the file's authenticity and detect tampering.")
fig_placeholder("Fig. 1 — SecureVault Dashboard: cards (Total Passwords | All Encrypted AES-256 | Blockchain Chain Intact | Total Audit Events), password grid with masked entries, navbar (🔑 Vault | 📋 Audit Log | 📤 Export | 🚪 Logout)")
fig_cap("Fig. 1 — SecureVault Dashboard: total passwords, encryption status, blockchain integrity indicator, and vault entry grid.")
fig_placeholder("Fig. 2 — Encryption Modules panel: AES-256-CBC ✓ | SHA-256 ✓ | RSA-2048 ✓ | Blockchain Audit Log ✓ — all active and verified.")
fig_cap("Fig. 2 — Encryption Modules panel showing AES-256, SHA-256, RSA-2048, and Blockchain Audit Log all active and verified.")
body("On the machine-learning side, the key output is the contrast between Scenario A and Scenario B:")
body("Table 5 — Algorithm comparison metrics, Scenario B (metadata only)")
add_table(
    ["Algorithm", "Accuracy", "Precision", "Recall", "F1-Score"],
    [
        ["Logistic Regression", "0.927", "0.000", "0.000", "0.000"],
        ["K-Nearest Neighbors (k=5)", "0.927", "0.000", "0.000", "0.000"],
        ["Decision Tree", "0.880", "0.143", "0.091", "0.111"],
        ["Random Forest", "0.927", "0.000", "0.000", "0.000"],
    ],
    col_widths=[2.5, 1.0, 1.0, 1.0, 1.0]
)
fig_placeholder("Fig. 13 — Algorithm comparison Scenario B: Logistic Regression, KNN, Random Forest all show Recall=0, F1=0. Decision Tree marginal recall=0.091.")
fig_cap("Fig. 13 — Algorithm comparison, Scenario B: suspicious-session detection collapses without the cryptographic integrity flags.")
fig_placeholder("Fig. 14 — Random Forest confusion matrix Scenario B: TP=0, TN=139, FP=0, FN=11 — every suspicious session missed.")
fig_cap("Fig. 14 — Random Forest confusion matrix, Scenario B: every suspicious session is missed (FN=11).")
page_break()

h("4.2 Analysis of Results & Interpretation of Data", size=13)
body("Table 6 — Confusion matrix outcome definitions")
add_table(
    ["Outcome", "Meaning in this system"],
    [
        ["True Positive (TP)", "A suspicious vault session correctly flagged as suspicious"],
        ["True Negative (TN)", "A genuine vault session correctly passed as genuine"],
        ["False Positive (FP)", "A genuine vault session wrongly flagged as suspicious"],
        ["False Negative (FN)", "A suspicious vault session missed and passed as genuine"],
    ],
    col_widths=[2.0, 4.4]
)
body("Scenario A's perfect scores across all four algorithms are expected rather than impressive: Master_Hash_Valid, Chain_Intact, and Signature_Valid are the very columns used to define the Suspicious_Flag label at generation time, so any reasonable classifier finds the near-deterministic rule connecting them. This scenario primarily confirms that the modelling pipeline is implemented correctly.")
body("Scenario B is the fairer and more important test. With accuracy alone (0.927 for three of the four algorithms), the result would appear acceptable — but the confusion matrix reveals why that figure is misleading: True Positives = 0 and False Negatives = 11 for Random Forest, Logistic Regression, and KNN, meaning these models never once correctly identify a suspicious session. They simply predict 'Genuine' for every record, which is correct 92.7% of the time only because genuine sessions dominate the dataset (139 of 150 test records). Only the Decision Tree shows marginal sensitivity (recall = 0.091), and even this is more likely a symptom of overfitting to a small number of training examples than a generalisable pattern.")

h("4.4 Discussion of Results & Limitations of the System", size=13)
body("The cryptographic core of SecureVault performed exactly as designed: AES-256-CBC encryption is confirmed by observing decryption failure when the master password is incorrect; SHA-256 master hashing is confirmed by verifying that two different passwords produce different, irreversible hashes; RSA digital signature verification is confirmed by observing that any byte-level modification of the exported JSON causes the signature check to return false; and the blockchain audit log is confirmed to detect retroactive alteration by recalculating each block's hash on demand.")
body("The system has three identifiable limitations. First, it uses an in-memory store rather than a persistent database, meaning vault data does not survive a server restart — this is explicitly by design for the capstone demonstrator and is identified as the primary production-readiness gap. Second, the RSA key pair is generated server-side and the private key is stored (AES-encrypted) in the same server memory as the vault data; a production deployment would generate keys client-side to ensure the server never has custody of the unencrypted private key. Third, ordinary session metadata carries essentially no signal about cryptographic anomalies in this system; any future work toward metadata-only anomaly detection would require either a fundamentally different feature set or a larger, more representative dataset of genuine adversarial access events.")
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 5
# ═══════════════════════════════════════════════════════════════════════════════
h("Chapter 5: Conclusion", size=15)
h("5.1 Summary of Work Completed", size=13)
body("This project designed, implemented, and evaluated SecureVault, a multi-level encryption password management platform in which every stored password is encrypted with AES-256-CBC keyed on the user's master credential, the master credential is protected by SHA-256 hashing and never stored in plaintext, password exports are digitally signed with RSA-2048 so that recipients can independently verify authenticity and integrity, account recovery is facilitated through RSA public-key encryption of a recovery token, and every vault action is permanently recorded in a SHA-256 hash-linked blockchain audit log that detects any retroactive tampering — all performed using real, standards-based cryptographic primitives (node-forge library) rather than simulated logic.")
body("The application supports user registration with automatic RSA key-pair generation, login with SHA-256 master-credential verification, full vault CRUD with AES-256-CBC encryption and on-demand decryption, digitally signed JSON export with downloadable proof, RSA recovery token generation, and a live blockchain audit log with chain-integrity checking.")
body("A supplementary data-science study generated a synthetic vault-access activity dataset (600 records, 150 simulated sessions), performed exploratory data analysis, and implemented and compared four supervised classification algorithms (Logistic Regression, K-Nearest Neighbours, Decision Tree, and Random Forest) for automated suspicious-session detection. The evaluation, carried out honestly under two contrasted feature scenarios, established that these algorithms succeed only when given the cryptographic verification outputs directly, and are not capable of detecting suspicious sessions from ordinary vault-access metadata alone.")
body("Overall, the project meets its stated objective: a password vault where credentials are encrypted, master access is hashed and never exposed, exports are digitally signed and independently verifiable, recovery is RSA-based, and every action creates a new linked, immutable blockchain record — with an honestly evaluated machine-learning layer identifying the limits of automated anomaly detection on top of real cryptography.")
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# REFERENCES
# ═══════════════════════════════════════════════════════════════════════════════
h("References", size=15)
h("1. Dataset Source", size=13)
body("The dataset used in Chapters 2–4 is not sourced from an external public dataset. It is a synthetic vault-access activity log, generated in Python, designed to model the kind of session records SecureVault would produce in sustained real-world organisational use (600 records, 150 simulated vault sessions). Generation logic and a sample of the resulting data are provided in Appendix B.")
h("2. Books", size=13)
bullet("W. Stallings, Cryptography and Network Security: Principles and Practice, 8th ed. Boston, MA, USA: Pearson, 2020.")
bullet("B. Schneier, Applied Cryptography: Protocols, Algorithms, and Source Code in C, 2nd ed. New York, NY, USA: Wiley, 1996.")
h("3. Websites Used", size=13)
refs = [
    "National Institute of Standards and Technology, 'Advanced Encryption Standard (AES),' FIPS PUB 197, Nov. 2001 (updated May 9, 2023). https://doi.org/10.6028/NIST.FIPS.197-upd1",
    "National Institute of Standards and Technology, 'Digital Signature Standard (DSS),' FIPS PUB 186-5, Feb. 2023. https://doi.org/10.6028/NIST.FIPS.186-5",
    "National Institute of Standards and Technology, 'Secure Hash Standard (SHS),' FIPS PUB 180-4, Mar. 2012. https://doi.org/10.6028/NIST.FIPS.180-4",
    "OWASP Foundation, 'Cryptographic Storage Cheat Sheet,' 2024. https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html",
    "OWASP Foundation, 'Password Storage Cheat Sheet,' 2024. https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html",
    "node-forge Project, 'JavaScript implementation of TLS and various other cryptographic tools.' https://github.com/digitalbazaar/forge",
    "S. Nakamoto, 'Bitcoin: A Peer-to-Peer Electronic Cash System,' 2008 (for blockchain-inspired hash-chaining design). https://bitcoin.org/bitcoin.pdf",
    "F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python,' J. Mach. Learn. Res., vol. 12, pp. 2825–2830, 2011. https://scikit-learn.org",
]
for i, ref in enumerate(refs, 1):
    p = doc.add_paragraph(f"{i}. {ref}", style='List Number')
    for r in p.runs: r.font.size = Pt(11)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# APPENDIX A
# ═══════════════════════════════════════════════════════════════════════════════
h("Appendix A — Important Code", size=15)
body("Complete source files (server.js, crypto.js, blockchain.js, store.js, routes.js, public/index.html, public/style.css, public/app.js — approximately 750 lines total) accompany this report as a separate project deliverable. The most important cryptographic core functions are reproduced below.")
code_block(
"""// ---- crypto.js: Core cryptographic primitives ----
const forge = require('node-forge');
const crypto = require('crypto');

// SHA-256 master credential hash — plaintext never stored
function hashMaster(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

// AES-256-CBC encrypt — IV randomly generated per operation
function encryptAES(plaintext, masterKey) {
  const iv  = forge.random.getBytesSync(16);
  const key = forge.md.sha256.create().update(masterKey).digest().bytes();
  const cipher = forge.cipher.createCipher('AES-CBC', key);
  cipher.start({ iv });
  cipher.update(forge.util.createBuffer(plaintext, 'utf8'));
  cipher.finish();
  return forge.util.encode64(iv) + ':' + forge.util.encode64(cipher.output.bytes());
}

// AES-256-CBC decrypt
function decryptAES(ciphertext, masterKey) {
  const [ivB64, enc] = ciphertext.split(':');
  const iv  = forge.util.decode64(ivB64);
  const key = forge.md.sha256.create().update(masterKey).digest().bytes();
  const decipher = forge.cipher.createDecipher('AES-CBC', key);
  decipher.start({ iv: forge.util.createBuffer(iv) });
  decipher.update(forge.util.createBuffer(forge.util.decode64(enc)));
  decipher.finish();
  return decipher.output.toString('utf8');
}

// RSA-2048 key pair — generated at registration
function generateRSAKeyPair() {
  const kp = forge.pki.rsa.generateKeyPair({ bits: 2048 });
  return {
    publicKey:  forge.pki.publicKeyToPem(kp.publicKey),
    privateKey: forge.pki.privateKeyToPem(kp.privateKey)
  };
}

// RSA OAEP encrypt — for recovery token
function encryptWithRSA(plaintext, publicKeyPem) {
  const pub = forge.pki.publicKeyFromPem(publicKeyPem);
  return forge.util.encode64(pub.encrypt(plaintext, 'RSA-OAEP'));
}

// Digital signature — RSA sign over SHA-256 digest of export payload
function signData(data, privateKeyPem) {
  const priv = forge.pki.privateKeyFromPem(privateKeyPem);
  const md   = forge.md.sha256.create();
  md.update(JSON.stringify(data), 'utf8');
  return forge.util.encode64(priv.sign(md));
}

// Verify digital signature
function verifySignature(data, signatureB64, publicKeyPem) {
  try {
    const pub = forge.pki.publicKeyFromPem(publicKeyPem);
    const md  = forge.md.sha256.create();
    md.update(JSON.stringify(data), 'utf8');
    return pub.verify(md.digest().bytes(), forge.util.decode64(signatureB64));
  } catch { return false; }
}"""
)
code_block(
"""// ---- blockchain.js: Immutable hash-linked audit log ----
class Block {
  constructor(index, data, previousHash) {
    this.index        = index;
    this.timestamp    = new Date().toISOString();
    this.data         = data;
    this.previousHash = previousHash;
    this.hash         = this.calculateHash();
  }
  calculateHash() {
    const c = `${this.index}${this.timestamp}` +
              `${JSON.stringify(this.data)}${this.previousHash}`;
    return crypto.createHash('sha256').update(c).digest('hex');
  }
}

class AuditBlockchain {
  constructor() { this.chain = [this.createGenesis()]; }
  createGenesis() {
    return new Block(0, { event:'GENESIS', message:'Vault initialized' }, '0');
  }
  addBlock(data) {
    const block = new Block(this.chain.length, data, this.getLatestBlock().hash);
    this.chain.push(block);
    return block;
  }
  isChainValid() {
    for (let i = 1; i < this.chain.length; i++) {
      if (this.chain[i].hash !== this.chain[i].calculateHash()) return false;
      if (this.chain[i].previousHash !== this.chain[i-1].hash) return false;
    }
    return true;
  }
}"""
)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# APPENDIX B
# ═══════════════════════════════════════════════════════════════════════════════
h("Appendix B — Dataset Sample", size=15)
body("A representative sample of the synthetic vault-access activity dataset (raw form, before preprocessing):")
code_block(
"""Session_ID,User_ID,Event_Type,Sender,Timestamp,Session_Duration_s,
Passwords_Accessed,Master_Hash_Valid,Chain_Intact,Signature_Valid,
Integrity_Score,Suspicious_Flag

1,USR-0001,Login,A. Verma,2025-02-19 09:14:22,45,0,1,1,1,1.000,0
2,USR-0001,Add_Password,A. Verma,2025-02-19 09:15:10,18,0,1,1,1,1.000,0
3,USR-0001,View_Vault,A. Verma,2025-02-19 09:16:05,32,4,1,1,1,1.000,0
4,USR-0002,Login,R. Kulkarni,2025-02-20 23:47:11,8,0,0,0,1,0.333,1
5,USR-0002,View_Vault,R. Kulkarni,2025-02-20 23:47:19,421,17,0,0,1,0.333,1
6,USR-0003,Login,S. Iyer,2024-11-07 10:02:33,39,0,1,1,1,1.000,0
7,USR-0003,Export,S. Iyer,2024-11-07 10:08:51,12,5,1,1,1,1.000,0
8,USR-0004,Login,D. Choudhary,2025-01-22 14:19:04,14,0,1,1,0,0.667,1
9,USR-0004,Update_Password,D. Choudhary,2025-01-22 14:20:30,9,1,1,1,1,1.000,0
10,USR-0005,Login,K. Nair,2024-07-11 08:55:17,41,0,1,1,1,1.000,0
...  (600 rows total; full CSV file accompanies this report)"""
)
body("Notes on suspicious records:")
bullet("Rows 4–5: Master_Hash_Valid=0 indicates incorrect master password (brute-force attempt); Chain_Intact=0 indicates the blockchain log was tampered. After-hours session (23:47). Passwords_Accessed=17 in a suspicious session.")
bullet("Row 8: Signature_Valid=0 on an Export event indicates the RSA export signature did not verify — possible man-in-the-middle alteration of the export payload.")
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# APPENDIX C
# ═══════════════════════════════════════════════════════════════════════════════
h("Appendix C — Additional Graphs", size=15)
fig_placeholder("Additional Fig. C1 — Sessions per vault event type (full dataset). Horizontal bar: Login(145) | View_Vault(130) | Add_Password(110) | Update_Password(85) | Delete_Password(70) | Export(60)")
fig_cap("Additional Fig. C1 — Distribution of vault event types across the full 600-record synthetic dataset.")
doc.add_paragraph()
fig_placeholder("Additional Fig. C2 — Monthly vault-access activity Jul 2024 – Dec 2025. Peaks: Oct 2024 (~58), Mar 2025 (~55). Trough: Aug 2024 (~28).")
fig_cap("Additional Fig. C2 — Monthly vault-access activity over the simulated 18-month period.")
doc.add_paragraph()
fig_placeholder("Additional Fig. C3 — Session duration box plot by event type. View_Vault: median ~35s, high variance. Export: median ~12s. Suspicious sessions: outlier durations (very long View_Vault; very short Login for scripted brute-force).")
fig_cap("Additional Fig. C3 — Session duration distribution by event type; suspicious sessions visible as outliers at the extremes.")

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
out = "/mnt/bulk/workspace/u_384885fa8c054c8d83d6c7e591493801/c_d60408fdc6c7423a8f8a39639ba9062c/vault/report/SecureVault_Capstone_Report.docx"
doc.save(out)
print(f"Saved: {out}")
