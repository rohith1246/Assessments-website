import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

uri = os.environ.get('DATABASE_URL', '')
if '&channel_binding=' in uri:
    uri = uri.split('&channel_binding=')[0]

print("Connecting to Neon database...", flush=True)
conn = psycopg2.connect(uri, connect_timeout=15)
cur = conn.cursor()

# ═══════════════════════════════════════════════════════════════════
# PART 1: DELETE CANDIDATE RECORDS (sravani, divya, sai, banu, naveena)
# ═══════════════════════════════════════════════════════════════════
search_terms = ['%sravani%', '%divya%', '%sai%', '%banu%', '%bhanu%', '%naveena%']

query = """
SELECT id, full_name, email, hall_ticket, created_at 
FROM assessment_candidates 
WHERE full_name ILIKE ANY(%s) OR email ILIKE ANY(%s);
"""

cur.execute(query, (search_terms, search_terms))
candidates = cur.fetchall()

print(f"\n=== Found {len(candidates)} matching candidate records to delete ===")
cand_ids = []
for c in candidates:
    print(f"  [DELETE] ID: {c[0]} | Name: {c[1]} | Email: {c[2]} | Hall Ticket: {c[3]}")
    cand_ids.append(c[0])

if cand_ids:
    # Delete answers
    cur.execute("""
        DELETE FROM assessment_answers 
        WHERE submission_id IN (SELECT id FROM assessment_submissions WHERE candidate_id = ANY(%s));
    """, (cand_ids,))
    
    # Delete coding submissions
    cur.execute("""
        DELETE FROM assessment_coding_submissions 
        WHERE submission_id IN (SELECT id FROM assessment_submissions WHERE candidate_id = ANY(%s));
    """, (cand_ids,))

    # Delete submissions
    cur.execute("DELETE FROM assessment_submissions WHERE candidate_id = ANY(%s);", (cand_ids,))

    # Delete candidates
    cur.execute("DELETE FROM assessment_candidates WHERE id = ANY(%s);", (cand_ids,))
    conn.commit()
    print(f"[OK] Successfully deleted {len(cand_ids)} candidate record(s) and all associated data permanently!")
else:
    print("No matching candidate records found to delete.")

# ═══════════════════════════════════════════════════════════════════
# PART 2: CREATE / SEED 'Screening Test - .NET Developer'
# ═══════════════════════════════════════════════════════════════════
print("\n=== Setting up 'Screening Test - .NET Developer' assessment ===")

cur.execute("SELECT setval('assessment_drives_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_drives));")
cur.execute("SELECT setval('assessment_questions_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_questions));")
conn.commit()

title = "Screening Test - .NET Developer"
cur.execute("SELECT id FROM assessment_drives WHERE title = %s;", (title,))
existing = cur.fetchall()
for (eid,) in existing:
    print(f"  Cleaning up existing assessment ID {eid}...", flush=True)
    cur.execute("DELETE FROM assessment_answers WHERE submission_id IN (SELECT id FROM assessment_submissions WHERE assessment_id = %s);", (eid,))
    cur.execute("DELETE FROM assessment_submissions WHERE assessment_id = %s;", (eid,))
    cur.execute("DELETE FROM assessment_questions WHERE assessment_id = %s;", (eid,))
    cur.execute("DELETE FROM assessment_drives WHERE id = %s;", (eid,))
conn.commit()

cur.execute("""
    INSERT INTO assessment_drives (title, description, duration, pass_percentage, status, created_at)
    VALUES (%s, %s, %s, %s, %s, NOW())
    RETURNING id;
""", (
    title,
    "Technical Screening Assessment for .NET / C# Developers covering Linux/Ubuntu Essentials, Docker Basics, Everyday Git & GitHub Commands, and C# / .NET Core OOP Concepts (Encapsulation, Structs vs Classes, Virtual/Override Polymorphism, Dependency Injection Scopes, IDisposable). Contains 20 MCQs. Time limit: 20 minutes.",
    20,
    75.0,
    "active"
))
drive_id = cur.fetchone()[0]
print(f"Created Assessment ID: {drive_id} for '{title}'")

DOTNET_QUESTIONS = [
    # Q1 - Q10: Linux / Docker Basics
    (
        "Q1. Which command is used in Linux/Ubuntu to list all files and directories, including hidden ones?",
        "dir /h",
        "ls -a",
        "show --hidden",
        "list -all",
        "B"
    ),
    (
        "Q2. Which Linux command is used to navigate back to the parent directory?",
        "cd ~",
        "cd /",
        "cd ..",
        "back",
        "C"
    ),
    (
        "Q3. Which command is used to create a new directory named 'project' in Linux?",
        "create project",
        "touch project",
        "newdir project",
        "mkdir project",
        "D"
    ),
    (
        "Q4. Which command makes a shell script file named 'script.sh' executable in Linux?",
        "chmod +x script.sh",
        "run script.sh",
        "exec script.sh",
        "chown +e script.sh",
        "A"
    ),
    (
        "Q5. Which command is used to view the entire contents of a text file named 'app.log' in the terminal?",
        "open app.log",
        "cat app.log",
        "echo app.log",
        "print app.log",
        "B"
    ),
    (
        "Q6. Which package management command is used to install new software packages on Ubuntu Linux?",
        "brew install <package-name>",
        "pip install-ubuntu <package-name>",
        "sudo apt install <package-name>",
        "sudo yum install <package-name>",
        "C"
    ),
    (
        "Q7. Which Docker command is used to download an image (if not present) and start a new container from it?",
        "docker start",
        "docker build",
        "docker init",
        "docker run",
        "D"
    ),
    (
        "Q8. Which command displays all currently running Docker containers?",
        "docker ps",
        "docker list",
        "docker show",
        "docker images",
        "A"
    ),
    (
        "Q9. Which Docker command builds a Docker image from a Dockerfile located in the current directory?",
        "docker create myapp",
        "docker build -t myapp .",
        "docker compile -i myapp",
        "docker make myapp",
        "B"
    ),
    (
        "Q10. How do you stop a running Docker container with container ID 'abc123'?",
        "docker delete abc123",
        "docker kill-all",
        "docker stop abc123",
        "docker pause",
        "C"
    ),

    # Q11 - Q15: Git & GitHub Basics
    (
        "Q11. Which Git command is used to download an existing remote repository from GitHub to your local computer?",
        "git copy <repository-url>",
        "git fetch-new <repository-url>",
        "git download <repository-url>",
        "git clone <repository-url>",
        "D"
    ),
    (
        "Q12. Which command stages all modified and newly created files in the current directory for the next commit?",
        "git add .",
        "git stage --all-files",
        "git save",
        "git commit -a",
        "A"
    ),
    (
        "Q13. What is the correct Git command to save your staged changes to local history with a message?",
        "git save -message \"Your commit message\"",
        "git commit -m \"Your commit message\"",
        "git push -m \"Your commit message\"",
        "git log -m \"Your commit message\"",
        "B"
    ),
    (
        "Q14. Which command uploads your committed changes from the local 'main' branch to the remote repository on GitHub?",
        "git upload origin main",
        "git send origin main",
        "git push origin main",
        "git export main",
        "C"
    ),
    (
        "Q15. Which command fetches the latest commits from the remote GitHub repository and merges them into your current local branch?",
        "git sync-only",
        "git push",
        "git refresh",
        "git pull",
        "D"
    ),

    # Q16 - Q20: C# / .NET Core OOP & Framework Concepts
    (
        "Q16. In C#, what is the primary benefit of using auto-implemented properties (e.g., 'public int Age { get; set; }') instead of public fields?",
        "They provide encapsulation by generating private backing fields while allowing future validation or access control logic without breaking the public API contract",
        "They make the C# compiler execute code directly on the GPU",
        "They prevent variables from occupying memory during program execution",
        "They automatically translate C# code into Python runtime",
        "A"
    ),
    (
        "Q17. In .NET (C#), what is the core memory allocation distinction between a 'struct' (Value Type) and a 'class' (Reference Type)?",
        "Classes are allocated on the Stack, while structs are always allocated on the Heap",
        "Structs are value types allocated on the Stack (or inlined in containing types), while class instances are reference types allocated on the Managed Heap and managed by the Garbage Collector",
        "Structs can inherit from multiple concrete classes, while classes cannot",
        "Classes cannot declare constructors or instance methods",
        "B"
    ),
    (
        "Q18. In C#, what keywords must be used in the base class and derived class respectively to enable runtime polymorphism and dynamic method overriding?",
        "static in base class and dynamic in derived class",
        "abstract in base class and final in derived class",
        "virtual (or abstract) in the base class and override in the derived class",
        "new in both classes",
        "C"
    ),
    (
        "Q19. In ASP.NET Core Dependency Injection, what is the lifetime behavior of a service registered with 'services.AddScoped<TService, TImplementation>()'?",
        "A single instance is created once and shared across all requests throughout the application lifetime (Singleton)",
        "A new instance is created every single time it is requested from the service provider (Transient)",
        "The service is destroyed immediately after constructor invocation",
        "A single instance is created per client HTTP request and disposed when the HTTP request scope ends",
        "D"
    ),
    (
        "Q20. In .NET, what is the primary purpose of implementing the 'IDisposable' interface and utilizing the 'using' statement?",
        "To deterministically release unmanaged resources (such as database connections, file streams, or network sockets) as soon as the block exits",
        "To completely disable the .NET Garbage Collector for high performance",
        "To encrypt compiled DLL assemblies on disk",
        "To force the Common Language Runtime (CLR) to run in single-threaded mode",
        "A"
    )
]

for q, a, b, c, d, ans in DOTNET_QUESTIONS:
    cur.execute("""
        INSERT INTO assessment_questions (assessment_id, question, option_a, option_b, option_c, option_d, correct_answer)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (drive_id, q, a, b, c, d, ans))

conn.commit()
print(f"Successfully inserted {len(DOTNET_QUESTIONS)} questions (5 A, 5 B, 5 C, 5 D balanced).", flush=True)

# Final summary of all assessments
cur.execute("SELECT id, title, duration, pass_percentage, status, (SELECT count(*) FROM assessment_questions WHERE assessment_id=assessment_drives.id) as qcount FROM assessment_drives ORDER BY id;")
rows = cur.fetchall()
print("\n================ ACTIVE ASSESSMENTS IN DATABASE ================", flush=True)
for r in rows:
    print(f"ID: {r[0]} | Title: {r[1]} | Pass: {r[3]}% | Status: {r[4]} | Questions: {r[5]}", flush=True)

conn.close()
