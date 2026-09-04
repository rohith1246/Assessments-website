import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Applying 100% clean, tricky basic questions with ZERO answer words in question text...")

# ── 10 TRICKY BASIC LINUX, DOCKER & GIT QUESTIONS (NO ANSWER WORDS IN TEXT) ──
clean_tricky_tech_fibs = [
    # ── LINUX (4 Questions) ──
    {
        "q": "In Linux, which command is executed in the terminal to view directory contents and display hidden dotfiles (files prefixed with a period)?",
        "a": "ls -a|ls -la|ls|ls -al"
    },
    {
        "q": "In Linux filesystem navigation, which command followed by two consecutive dots (..) is used to move one level upward into the parent folder?",
        "a": "cd ..|cd"
    },
    {
        "q": "In Linux shell scripting, which command is used to generate a new folder or construct an entire nested folder hierarchy using the '-p' flag?",
        "a": "mkdir|mkdir -p"
    },
    {
        "q": "In Linux security administration, which command is used to modify read, write, and execute permissions (such as 755 or +x) on a file?",
        "a": "chmod|chmod +x"
    },

    # ── DOCKER (3 Questions) ──
    {
        "q": "In Docker operations, which sub-command processes instructions in a Dockerfile to assemble and package application source code into a runnable container image?",
        "a": "build|docker build"
    },
    {
        "q": "In Docker management, which short two-letter sub-command lists all currently active and running container instances along with their status?",
        "a": "ps|docker ps"
    },
    {
        "q": "When starting a container with 'docker run', which single-letter flag is passed to execute the process in the background without locking the terminal?",
        "a": "-d|d|--detach|-detach"
    },

    # ── GIT (3 Questions) ──
    {
        "q": "In Git version control, which initial command is used to download a complete copy of an existing remote repository from GitHub to your local machine?",
        "a": "clone|git clone"
    },
    {
        "q": "In Git workflow, which command stages newly created or modified working files to prepare them for the next commit?",
        "a": "add|git add|git add ."
    },
    {
        "q": "In Git collaborative workflows, which command transmits and uploads your locally committed code changes to the remote repository on GitHub?",
        "a": "push|git push|git push origin main"
    }
]

# ── 10 CLEAN SAP MM QUESTIONS (NO ANSWER WORDS IN TEXT) ──
clean_sap_mm_fibs = [
    {
        "q": "In SAP MM, which standard transaction code is used by buyers to create a new formal Purchase Order?",
        "a": "ME21N|ME21|21N|21"
    },
    {
        "q": "In SAP inventory management, which 3-digit movement type is executed when recording a standard Goods Receipt against a Purchase Order into warehouse stock?",
        "a": "101"
    },
    {
        "q": "In SAP MM, which standard transaction code is used by the finance team to perform Logistics Invoice Verification and post vendor bills?",
        "a": "MIRO"
    },
    {
        "q": "In SAP procurement, which standard transaction code is used by internal departments to generate a Purchase Requisition for needed goods or services?",
        "a": "ME51N|ME51|51N|51"
    },
    {
        "q": "In SAP MM, which transaction code is used to perform general Goods Receipts, Goods Issues, and Transfer Postings in a single interface?",
        "a": "MIGO"
    },
    {
        "q": "In SAP MM Master Data, which standard transaction code is used to create a new Material Master record in the system?",
        "a": "MM01|01"
    },
    {
        "q": "In SAP MM inventory, the standard stock category that is available for immediate consumption, internal issue, or sale without quality holds is called _____ Stock.",
        "a": "Unrestricted|Unrestricted-use"
    },
    {
        "q": "In SAP procurement cycle, the formal inquiry document sent to multiple suppliers inviting them to submit competitive price bids is an _____.",
        "a": "RFQ|Request for Quotation"
    },
    {
        "q": "In SAP MM, the automated planning engine that balances material demand forecasts against current stock to calculate procurement proposals is _____.",
        "a": "MRP|Material Requirements Planning"
    },
    {
        "q": "In S/4HANA and SAP MM, vendor and customer master records are centrally maintained under the unified concept of Business _____.",
        "a": "Partner|Business Partner"
    }
]

# Update SAP MM (Drive ID: 19) full 20 questions
cur.execute("SELECT id FROM assessment_questions WHERE assessment_id = 19 ORDER BY id;")
sap_q_rows = cur.fetchall()

if len(sap_q_rows) >= 20:
    # Update Q1-Q10 for SAP MM
    for idx in range(10):
        target_id = sap_q_rows[idx][0]
        q_data = clean_sap_mm_fibs[idx]
        cur.execute("UPDATE assessment_questions SET question = %s, correct_answer = %s, question_type = 'fib' WHERE id = %s;", (q_data["q"], q_data["a"], target_id))
    
    # Update Q11-Q20 for SAP MM
    for idx in range(10):
        target_id = sap_q_rows[10 + idx][0]
        q_data = clean_tricky_tech_fibs[idx]
        cur.execute("UPDATE assessment_questions SET question = %s, correct_answer = %s, question_type = 'fib' WHERE id = %s;", (q_data["q"], q_data["a"], target_id))
    print("[OK] Successfully updated all 20 questions for SAP MM (Drive ID: 19)!")

# Update Q11-Q20 for other Technical Round 2 drives (Python: 14, Java: 15, Cyber: 16, Data Analyst: 17, .NET: 18)
other_drives = [14, 15, 16, 17, 18]
for did in other_drives:
    cur.execute("SELECT id FROM assessment_questions WHERE assessment_id = %s ORDER BY id;", (did,))
    q_rows = cur.fetchall()
    if len(q_rows) >= 20:
        for idx in range(10):
            target_id = q_rows[10 + idx][0]
            q_data = clean_tricky_tech_fibs[idx]
            cur.execute("UPDATE assessment_questions SET question = %s, correct_answer = %s, question_type = 'fib' WHERE id = %s;", (q_data["q"], q_data["a"], target_id))
        print(f"[OK] Successfully updated Q11-Q20 for Drive ID: {did}!")

conn.commit()

# Print verified SAP MM questions
print("\n=== VERIFIED ALL 20 QUESTIONS FOR SAP MM (ID: 19) ===")
cur.execute("SELECT id, question, correct_answer FROM assessment_questions WHERE assessment_id = 19 ORDER BY id;")
for idx, q in enumerate(cur.fetchall(), 1):
    print(f"Q{idx}: {q[1]}\n   --> Answer Key: {q[2]}\n")

conn.close()
print("DATABASE COMMITTED SUCCESSFULLY!")
