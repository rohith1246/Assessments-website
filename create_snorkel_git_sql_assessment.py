import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

title = 'Technical Round 2 - Screening Test (Snorkel + Git + SQL)'
description = 'Technical Round 2 Screening Assessment covering Snorkel / TerminalBench CLI commands, Git version control workflows, and SQL database querying.'

# 1. Check or insert Assessment Drive
cur.execute("SELECT id FROM assessment_drives WHERE title ILIKE %s OR title = %s;", ('%Snorkel%', title))
row = cur.fetchone()

if row:
    drive_id = row[0]
    print(f"Found existing drive ID: {drive_id}")
    cur.execute("""
        UPDATE assessment_drives
        SET title = %s, description = %s, duration = 20, pass_percentage = 75, status = 'active'
        WHERE id = %s;
    """, (title, description, drive_id))
else:
    cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM assessment_drives;")
    drive_id = cur.fetchone()[0]
    drive_id = max(drive_id, 26)
    print(f"Inserting new drive with ID: {drive_id}")
    cur.execute("""
        INSERT INTO assessment_drives (id, title, description, duration, pass_percentage, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW());
    """, (drive_id, title, description, 20, 75, 'active'))

# Reset sequences
cur.execute("SELECT setval('assessment_drives_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_drives));")

# 2. Clean existing questions for this drive
cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id = %s);", (drive_id,))
cur.execute("DELETE FROM assessment_questions WHERE assessment_id = %s;", (drive_id,))

# 3. Define 20 FIB Questions
questions = [
    # Snorkel / TerminalBench Commands (1–10)
    {
        "q": "Login to the Snorkel platform:\n\nstb ________",
        "a": "login|stb login"
    },
    {
        "q": "View configured API keys:\n\nstb ________",
        "a": "keys|stb keys"
    },
    {
        "q": "Initialize a new TerminalBench project:\n\nstb ________",
        "a": "init|stb init"
    },
    {
        "q": "Run Harbor locally using GPT model:\n\nstb harbor ________ -m @openai/gpt-5.5 -p .",
        "a": "run|stb harbor run"
    },
    {
        "q": "Check submitted tasks:\n\nstb ________",
        "a": "submissions|stb submissions"
    },
    {
        "q": "View project reviews:\n\nstb ________",
        "a": "reviews|stb reviews"
    },
    {
        "q": "View adjudication results:\n\nstb ________",
        "a": "adjudications|stb adjudications"
    },
    {
        "q": "List available projects:\n\nstb ________",
        "a": "projects|stb projects"
    },
    {
        "q": "Open Claude through STB:\n\nstb ________",
        "a": "claude|stb claude"
    },
    {
        "q": "Create Harbor task execution:\n\nstb ________ run -m @openai/gpt-5.5 -p .",
        "a": "harbor|stb harbor"
    },

    # Git Commands (11–15)
    {
        "q": "Initialize a Git repository:\n\ngit ________",
        "a": "init|git init"
    },
    {
        "q": "Stage all files:\n\ngit add ________",
        "a": ".|all|*|-A|--all|git add ."
    },
    {
        "q": "Commit changes:\n\ngit ________ -m \"Initial Commit\"",
        "a": "commit|git commit"
    },
    {
        "q": "Upload commits to GitHub:\n\ngit ________ origin main",
        "a": "push|git push"
    },
    {
        "q": "Download and merge changes:\n\ngit ________ origin main",
        "a": "pull|git pull"
    },

    # SQL Commands (16–20)
    {
        "q": "Retrieve all records from a table:\n\n________ * FROM Employee;",
        "a": "SELECT|select"
    },
    {
        "q": "Filter rows based on a condition:\n\nSELECT * FROM Employee ________ Salary > 50000;",
        "a": "WHERE|where"
    },
    {
        "q": "Count total records:\n\nSELECT ________(*) FROM Employee;",
        "a": "COUNT|count"
    },
    {
        "q": "Group records by department:\n\nSELECT Department, COUNT(*) FROM Employee ________ BY Department;",
        "a": "GROUP|group"
    },
    {
        "q": "Filter grouped records:\n\nSELECT Department, COUNT(*) FROM Employee GROUP BY Department ________ COUNT(*) > 5;",
        "a": "HAVING|having"
    }
]

for idx, item in enumerate(questions, 1):
    cur.execute("""
        INSERT INTO assessment_questions (assessment_id, question, correct_answer, question_type)
        VALUES (%s, %s, %s, %s);
    """, (drive_id, item["q"], item["a"], "fib"))

print(f"[OK] Successfully seeded {len(questions)} FIB questions for '{title}' (Drive ID: {drive_id})!")

conn.commit()
conn.close()
print("DATABASE COMMITTED SUCCESSFULLY!")
