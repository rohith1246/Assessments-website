import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

uri = os.environ.get('DATABASE_URL', '')
if '&channel_binding=' in uri:
    uri = uri.split('&channel_binding=')[0]

conn = psycopg2.connect(uri, connect_timeout=15)
cur = conn.cursor()

# Search terms: sravani, divya, sai, banu, bhanu
terms = ['%sravani%', '%divya%', '%sai%', '%banu%', '%bhanu%']

query = """
SELECT id, full_name, email, hall_ticket, created_at 
FROM assessment_candidates 
WHERE full_name ILIKE ANY(%s) OR email ILIKE ANY(%s);
"""

cur.execute(query, (terms, terms))
candidates = cur.fetchall()

print(f"=== Found {len(candidates)} matching candidate records ===")
cand_ids = []
for c in candidates:
    print(f"ID: {c[0]} | Name: {c[1]} | Email: {c[2]} | Hall Ticket: {c[3]} | Registered: {c[4]}")
    cand_ids.append(c[0])

if cand_ids:
    print(f"\nPermanently deleting {len(cand_ids)} candidate(s) and all their associated submissions & answers...")
    
    # Check submissions
    cur.execute("SELECT id FROM assessment_submissions WHERE candidate_id = ANY(%s);", (cand_ids,))
    sub_ids = [r[0] for r in cur.fetchall()]
    print(f"Found {len(sub_ids)} submission records to delete: {sub_ids}")

    if sub_ids:
        # Delete answers
        cur.execute("DELETE FROM assessment_answers WHERE submission_id = ANY(%s);", (sub_ids,))
        # Delete coding submissions
        cur.execute("DELETE FROM assessment_coding_submissions WHERE submission_id = ANY(%s);", (sub_ids,))
        # Delete submissions
        cur.execute("DELETE FROM assessment_submissions WHERE id = ANY(%s);", (sub_ids,))
    
    # Delete candidates
    cur.execute("DELETE FROM assessment_candidates WHERE id = ANY(%s);", (cand_ids,))
    conn.commit()
    print("✅ All matching records permanently deleted successfully!")
else:
    print("No matching candidate records found.")

conn.close()
