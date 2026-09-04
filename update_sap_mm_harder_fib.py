import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Updating Technical Round 2 - SAP MM (Materials Management) with harder questions and NO giveaway text...")

# Target ID: 19
drive_id = 19
cur.execute("SELECT id, title FROM assessment_drives WHERE id = %s;", (drive_id,))
row = cur.fetchone()
if not row:
    # Try finding by title
    cur.execute("SELECT id FROM assessment_drives WHERE title ILIKE '%SAP MM%';")
    r2 = cur.fetchone()
    if r2:
        drive_id = r2[0]

print(f"Targeting Assessment Drive ID: {drive_id}")

cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id = %s);", (drive_id,))
cur.execute("DELETE FROM assessment_questions WHERE assessment_id = %s;", (drive_id,))

harder_sap_mm_fibs = [
    # ── PART 1: 10 ADVANCED SAP MM (MATERIALS MANAGEMENT) FIB QUESTIONS ──
    {
        "q": "In SAP ERP, which standard 5-character transaction code is used by purchasing agents to create an official Purchase Order with item and header details?",
        "a": "ME21N|ME21"
    },
    {
        "q": "In SAP Inventory Management, which 3-digit standard movement type is executed when recording a Goods Receipt against an approved Purchase Order into warehouse stock?",
        "a": "101"
    },
    {
        "q": "In SAP Materials Management, which transaction code is used by the accounts payable team to verify, match, and post incoming vendor invoices against purchase orders and receipts?",
        "a": "MIRO"
    },
    {
        "q": "In SAP procurement workflows, which standard transaction code is utilized by internal requisitioning departments to create a new Purchase Requisition?",
        "a": "ME51N|ME51"
    },
    {
        "q": "In the SAP database dictionary, which transparent table stores client-level general material master attributes (such as material number, base unit of measure, and material type)?",
        "a": "MARA"
    },
    {
        "q": "In SAP MM, which unified single-screen transaction code is used to execute goods receipts, goods issues, return deliveries, and transfer postings?",
        "a": "MIGO"
    },
    {
        "q": "In SAP MM-FI integration, which transaction code is used by functional consultants to configure automatic account determination and G/L account mapping for material movements?",
        "a": "OBYC|OMWB"
    },
    {
        "q": "In SAP Purchasing, which single-character item category is assigned on a purchase order line item when raw components are provided to an external vendor for contract processing?",
        "a": "L|Subcontracting|L - Subcontracting"
    },
    {
        "q": "In SAP Physical Inventory procedures, which transaction code is executed to record the actual physical stock count quantities for an existing inventory document?",
        "a": "MI04"
    },
    {
        "q": "In SAP S/4HANA Enterprise Management, traditional vendor (XK01) and customer records are completely unified and maintained under which central master data concept?",
        "a": "Business Partner|BP"
    },

    # ── PART 2: 10 ADVANCED & SCENARIO-BASED LINUX, DOCKER & GITHUB FIB QUESTIONS ──
    {
        "q": "In Linux server administration, which interactive command-line utility provides a dynamic real-time dashboard of running processes, CPU core loads, memory allocation, and swap utilization?",
        "a": "top|htop"
    },
    {
        "q": "In Linux shell environments, which command combined with a human-readable flag is used to inspect remaining disk space, total storage capacity, and mount points across all filesystem partitions?",
        "a": "df -h|df"
    },
    {
        "q": "In Linux file security and permissions, which command is executed to modify or reassign user and group ownership of a directory and its nested files?",
        "a": "chown"
    },
    {
        "q": "In Linux systems, which command with regular expression filtering capability is executed to search for a specific error text pattern across files in a directory?",
        "a": "grep|grep -rn|grep -r|egrep"
    },
    {
        "q": "In Docker CLI management, which sub-command is executed to clean up and permanently delete all stopped containers, dangling images, unused networks, and build caches in one command?",
        "a": "docker system prune|system prune|prune"
    },
    {
        "q": "In Docker container operations, which command followed by a container name or container ID is executed to inspect and stream live stdout/stderr console output?",
        "a": "docker logs|docker logs -f|logs"
    },
    {
        "q": "In Docker container troubleshooting, which command is used to start an interactive bash shell session inside an already running container?",
        "a": "docker exec|docker exec -it|exec"
    },
    {
        "q": "In modern Git version control, which dedicated command is used to navigate between branches or create a new local branch using the '-c' flag?",
        "a": "git switch|git checkout|switch|checkout"
    },
    {
        "q": "In Git collaborative workflows, which command is used to temporarily shelve and save uncommitted working directory changes so you can switch branches cleanly?",
        "a": "git stash|stash"
    },
    {
        "q": "In Git version control, which command displays the chronological commit history, commit hashes, author timestamps, and branch commit logs of a repository?",
        "a": "git log|log"
    }
]

for idx, q in enumerate(harder_sap_mm_fibs, 1):
    cur.execute("""
        INSERT INTO assessment_questions (assessment_id, question, correct_answer, question_type)
        VALUES (%s, %s, %s, %s);
    """, (drive_id, q["q"], q["a"], "fib"))

print(f"[OK] Successfully updated Assessment ID {drive_id} with 20 Harder FIB questions with ZERO answer giveaways!")

conn.commit()
conn.close()
print("DATABASE COMMITTED SUCCESSFULLY!")
