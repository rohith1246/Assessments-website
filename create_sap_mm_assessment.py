import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Creating Technical Round 2 - SAP MM (Materials Management)...")

# 1. Check or insert Assessment Drive
cur.execute("SELECT id FROM assessment_drives WHERE title ILIKE '%SAP MM%' OR title ILIKE '%Materials Management%';")
row = cur.fetchone()

if row:
    drive_id = row[0]
    print(f"Found existing SAP MM drive ID: {drive_id}")
    cur.execute("UPDATE assessment_drives SET title = 'Technical Round 2 - SAP MM (Materials Management)', description = 'Individual Technical Round 2 Evaluation for SAP Materials Management (MM) - 20 Fill In The Blanks Questions.', duration = 20, pass_percentage = 75, status = 'active' WHERE id = %s;", (drive_id,))
else:
    cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM assessment_drives;")
    drive_id = cur.fetchone()[0]
    # In case drive_id < 19
    drive_id = max(drive_id, 19)
    print(f"Inserting new SAP MM drive with ID: {drive_id}")
    cur.execute("""
        INSERT INTO assessment_drives (id, title, description, duration, pass_percentage, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW());
    """, (drive_id, 'Technical Round 2 - SAP MM (Materials Management)', 'Individual Technical Round 2 Evaluation for SAP Materials Management (MM) - 20 Fill In The Blanks Questions.', 20, 75, 'active'))

# Reset sequences
cur.execute("SELECT setval('assessment_drives_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_drives));")

# 2. Clean existing questions for this drive
cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id = %s);", (drive_id,))
cur.execute("DELETE FROM assessment_questions WHERE assessment_id = %s;", (drive_id,))

# 3. Define 20 FIB Questions (10 Core SAP MM + 10 Linux/Docker/Git)
sap_mm_fibs = [
    # ── 10 CORE SAP MM (MATERIALS MANAGEMENT) FIB QUESTIONS ──
    {
        "q": "In SAP MM, the standard transaction code used to create a Purchase Order (PO) is ME_____N.",
        "a": "21|21N|ME21N"
    },
    {
        "q": "In SAP MM inventory management, the standard Movement Type used for Goods Receipt against a Purchase Order into warehouse stock is _____.",
        "a": "101|Movement Type 101"
    },
    {
        "q": "In SAP MM, the standard transaction code used to post incoming Vendor Invoice Verification is _____.",
        "a": "MIRO"
    },
    {
        "q": "In SAP MM, the standard transaction code used to create a Purchase Requisition (PR) is ME_____N.",
        "a": "51|51N|ME51N"
    },
    {
        "q": "In SAP MM, the transaction code used to perform Goods Receipt (GR) and Goods Issue (GI) is _____.",
        "a": "MIGO"
    },
    {
        "q": "In SAP MM Master Data, the standard transaction code used to create a new Material Master record is MM_____.",
        "a": "01|MM01"
    },
    {
        "q": "In SAP MM inventory, the stock category that is available for immediate issue, consumption, or sale without restrictions is _____ Stock.",
        "a": "Unrestricted|Unrestricted-use"
    },
    {
        "q": "In SAP procurement cycle, the formal document sent to vendors to request price quotes for materials is an _____ (Request for Quotation).",
        "a": "RFQ|Request for Quotation"
    },
    {
        "q": "In SAP MM, the automated planning tool that calculates material requirements based on sales and demand forecasts is _____ (Material Requirements Planning).",
        "a": "MRP|Material Requirements Planning"
    },
    {
        "q": "In S/4HANA and SAP MM, vendor and customer master data are centrally managed as a Business _____ (BP).",
        "a": "Partner|Business Partner"
    },

    # ── 10 PRACTICAL LINUX, DOCKER & GITHUB FIB QUESTIONS ──
    {
        "q": "In Linux, the command used to list files and folders in the current directory is _____.",
        "a": "ls|ls -la|ls -a"
    },
    {
        "q": "In Linux, the command used to navigate or change the current working directory is _____.",
        "a": "cd|cd .."
    },
    {
        "q": "In Linux, the command used to create a new folder/directory is _____.",
        "a": "mkdir"
    },
    {
        "q": "In Linux, the command used to change permissions of a file (e.g. 'chmod +x file.sh') is _____.",
        "a": "chmod|chmod +x"
    },
    {
        "q": "In Docker, the command used to build a container image from a Dockerfile is 'docker _____ -t myapp .'.",
        "a": "build"
    },
    {
        "q": "In Docker CLI, the command used to show running containers is 'docker _____'.",
        "a": "ps"
    },
    {
        "q": "In Docker, to run a container in the background (detached mode), you pass the flag -_____.",
        "a": "d|-d|--detach|-detach"
    },
    {
        "q": "In Git, to download a copy of an existing remote repository from GitHub to your computer, run 'git _____ <url>'.",
        "a": "clone"
    },
    {
        "q": "In Git, the command used to stage all changed files before committing is 'git _____ .'.",
        "a": "add"
    },
    {
        "q": "In Git, the command used to upload local committed changes to GitHub is 'git _____ origin main'.",
        "a": "push"
    }
]

for idx, q in enumerate(sap_mm_fibs, 1):
    cur.execute("""
        INSERT INTO assessment_questions (assessment_id, question, correct_answer, question_type)
        VALUES (%s, %s, %s, %s);
    """, (drive_id, q["q"], q["a"], "fib"))

print(f"[OK] Successfully seeded 20 FIB questions for SAP MM (Drive ID: {drive_id})!")

conn.commit()
conn.close()
print("DATABASE COMMITTED SUCCESSFULLY!")
