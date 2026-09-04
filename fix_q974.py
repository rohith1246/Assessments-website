import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

# Fix Q973 and Q974
cur.execute("""
    UPDATE assessment_questions 
    SET question = 'In SAP MM, the standard transaction code used to create a Purchase Order is _____.'
    WHERE id = 973;
""")

cur.execute("""
    UPDATE assessment_questions 
    SET question = 'In SAP MM inventory management, the standard Movement Type used for Goods Receipt against a Purchase Order into warehouse stock is _____.'
    WHERE id = 974;
""")

conn.commit()

print("Verified SAP MM (ID 19) Questions:")
cur.execute("SELECT id, question, correct_answer FROM assessment_questions WHERE assessment_id = 19 ORDER BY id;")
for q in cur.fetchall():
    print(f"[{q[0]}] {q[1]} -> {q[2]}")

conn.close()
