import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Updating Q18, Q19, Q20 (Git questions) across all 6 Round 2 FIB drives...")

new_git_questions = [
    # Q18: git merge
    {
        "q": "In Git branch management, which command integrates and joins lines of development from a feature branch into your currently active checked-out branch?",
        "a": "merge|git merge"
    },
    # Q19: git status
    {
        "q": "In Git repository inspection, which command displays the real-time state of the working tree, indicating which modified files are untracked or staged in the index?",
        "a": "status|git status"
    },
    # Q20: git commit
    {
        "q": "In Git version control, which command permanently records and snapshots staged changes into the project history alongside an explanatory message flag (-m)?",
        "a": "commit|git commit"
    }
]

# Round 2 Drive IDs: 14 (Python), 15 (Java), 16 (Cyber Security), 17 (Data Analyst), 18 (.NET), 19 (SAP MM)
round2_drive_ids = [14, 15, 16, 17, 18, 19]

for did in round2_drive_ids:
    cur.execute("SELECT title FROM assessment_drives WHERE id = %s;", (did,))
    row = cur.fetchone()
    if not row:
        continue
    title = row[0]
    print(f"\nUpdating Q18-Q20 for {title} (ID: {did})...")
    
    cur.execute("SELECT id FROM assessment_questions WHERE assessment_id = %s ORDER BY id;", (did,))
    q_rows = cur.fetchall()
    
    if len(q_rows) >= 20:
        # Update Q18 (index 17), Q19 (index 18), Q20 (index 19)
        for idx in range(3):
            target_id = q_rows[17 + idx][0]
            new_q = new_git_questions[idx]
            cur.execute("""
                UPDATE assessment_questions 
                SET question = %s, correct_answer = %s, question_type = 'fib'
                WHERE id = %s;
            """, (new_q["q"], new_q["a"], target_id))
        print(f"[OK] Successfully updated Q18, Q19, Q20 for {title}!")

conn.commit()

# Print verified Q18-Q20 for SAP MM (ID: 19)
print("\n=== VERIFIED Q18-Q20 ON SAP MM (ID: 19) ===")
cur.execute("SELECT id, question, correct_answer FROM assessment_questions WHERE assessment_id = 19 ORDER BY id;")
all_q = cur.fetchall()
for idx, q in enumerate(all_q, 1):
    if idx >= 18:
        print(f"Q{idx} [{q[0]}]: {q[1]}\n   -> Key: {q[2]}\n")

conn.close()
print("DATABASE COMMITTED SUCCESSFULLY!")
