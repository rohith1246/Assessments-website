import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

cur.execute("SELECT id, title, duration, pass_percentage FROM assessment_drives WHERE title ILIKE '%Java%';")
drives = cur.fetchall()
print("JAVA DRIVES:")
for d in drives:
    print(d)

cur.execute("""
    SELECT assessment_id, question_type, count(*) 
    FROM assessment_questions 
    WHERE assessment_id IN (SELECT id FROM assessment_drives WHERE title ILIKE '%Java%')
    GROUP BY assessment_id, question_type;
""")
print("\nQUESTION COUNTS:")
for q in cur.fetchall():
    print(q)

conn.close()
