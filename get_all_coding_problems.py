import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("--- All Coding Problems & Testcases in System ---")

cur.execute("""
    SELECT 
        p.id,
        p.assessment_id,
        a.title AS drive_title,
        p.title AS problem_title,
        p.difficulty,
        p.points,
        p.problem_statement,
        p.input_format,
        p.output_format
    FROM assessment_coding_problems p
    LEFT JOIN assessment_drives a ON p.assessment_id = a.id
    ORDER BY p.assessment_id ASC, p.id ASC;
""")

problems = cur.fetchall()
print(f"Total Coding Problems: {len(problems)}\n")

for p in problems:
    pid, aid, dtitle, title, diff, pts, stmt, in_fmt, out_fmt = p
    print(f"[{pid}] Track: {dtitle} (Drive ID: {aid})")
    print(f"Problem: {title} | Difficulty: {diff} | Points: {pts}")
    print(f"Statement:\n{stmt}")
    print(f"Input: {in_fmt}")
    print(f"Output: {out_fmt}")
    
    cur.execute("SELECT input_data, expected_output, is_hidden FROM assessment_coding_testcases WHERE problem_id = %s ORDER BY id;", (pid,))
    tcs = cur.fetchall()
    print("Test Cases:")
    for tc in tcs:
        t_in, t_out, hidden = tc
        h_str = "[HIDDEN]" if hidden else "[SAMPLE]"
        print(f"   {h_str} Input:\n{t_in}\n   Expected Output:\n{t_out}\n")
    print("=" * 60)

conn.close()
