import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

uri = os.environ.get('DATABASE_URL', '')
if '&channel_binding=' in uri:
    uri = uri.split('&channel_binding=')[0]

conn = psycopg2.connect(uri, connect_timeout=15)
cur = conn.cursor()

cur.execute("DELETE FROM assessment_answers WHERE submission_id IN (SELECT id FROM assessment_submissions WHERE status = 'in_progress');")
cur.execute("DELETE FROM assessment_submissions WHERE status = 'in_progress';")
conn.commit()
print("Successfully cleared all stale in-progress sessions!")
conn.close()
