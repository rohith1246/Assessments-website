import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Cleaning all giveaway examples from questions across all assessments...")

# ── Clean Linux chmod question across all drives ──
cur.execute("""
    UPDATE assessment_questions 
    SET question = 'In Linux, the command used to change the access permissions of a file or directory is _____.'
    WHERE question ILIKE '%chmod +x%' OR question ILIKE '%permissions of a file (e.g.%';
""")
print(f"Updated chmod questions: {cur.rowcount} rows")

# ── Clean Python dictionary question ──
cur.execute("""
    UPDATE assessment_questions 
    SET question = 'In Python, the built-in data structure that stores key-value pairs is called a _____.'
    WHERE question ILIKE '%stores key-value pairs is called a %' AND question ILIKE '%(or dict)%';
""")
print(f"Updated Python dict questions: {cur.rowcount} rows")

# ── Clean SAP MM Purchase Order question ──
cur.execute("""
    UPDATE assessment_questions 
    SET question = 'In SAP MM, the standard transaction code used to create a Purchase Order is _____.'
    WHERE assessment_id = 19 AND question ILIKE '%Purchase Order%';
""")

# ── Clean SAP MM Purchase Requisition question ──
cur.execute("""
    UPDATE assessment_questions 
    SET question = 'In SAP MM, the standard transaction code used to create an initial Purchase Requisition is _____.'
    WHERE assessment_id = 19 AND question ILIKE '%Purchase Requisition%';
""")

# ── Clean SAP MM Material Master question ──
cur.execute("""
    UPDATE assessment_questions 
    SET question = 'In SAP MM Master Data, the standard transaction code used to create a Material Master record is _____.'
    WHERE assessment_id = 19 AND question ILIKE '%Material Master record%';
""")

# ── Clean SAP MM RFQ question ──
cur.execute("""
    UPDATE assessment_questions 
    SET question = 'In SAP procurement, the formal document sent to vendors to request price quotes for materials is an _____.'
    WHERE assessment_id = 19 AND question ILIKE '%Request for Quotation%';
""")

# ── Clean SAP MM MRP question ──
cur.execute("""
    UPDATE assessment_questions 
    SET question = 'In SAP MM, the automated planning tool that calculates material requirements based on sales and demand is _____.'
    WHERE assessment_id = 19 AND question ILIKE '%Material Requirements Planning%';
""")

# ── Clean SAP MM Business Partner question ──
cur.execute("""
    UPDATE assessment_questions 
    SET question = 'In S/4HANA and SAP MM, vendor and customer master records are centrally maintained under the concept of Business _____.'
    WHERE assessment_id = 19 AND question ILIKE '%Business %';
""")

conn.commit()
print("All giveaway examples successfully purged!")

# Verify SAP MM questions
print("\n--- Current SAP MM (ID 19) Questions ---")
cur.execute("SELECT id, question, correct_answer FROM assessment_questions WHERE assessment_id = 19 ORDER BY id;")
for q in cur.fetchall():
    print(f"[{q[0]}] {q[1]} -> {q[2]}")

conn.close()
