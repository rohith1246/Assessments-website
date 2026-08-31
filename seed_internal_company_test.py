"""
seed_internal_company_test.py
Creates and populates the 'Screening Test' assessment with 20 accessible MCQs:
- 10 Linux / Ubuntu / Docker Basics MCQs
- 5 Git / GitHub everyday commands MCQs (clone, add, commit, push, pull)
- 5 Python OOP Concepts MCQs (Classes, __init__, self, Inheritance, Encapsulation, Polymorphism)
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def seed_assessment():
    uri = os.environ.get('DATABASE_URL', '')
    if '&channel_binding=' in uri:
        uri = uri.split('&channel_binding=')[0]

    print("Connecting to Neon database...", flush=True)
    conn = psycopg2.connect(uri, connect_timeout=15)
    cur = conn.cursor()

    # 1. Sync primary key sequences
    print("Syncing sequences...", flush=True)
    cur.execute("SELECT setval('assessment_drives_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_drives));")
    cur.execute("SELECT setval('assessment_questions_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_questions));")
    conn.commit()

    # 2. Check if assessment exists and clean up old questions/submissions
    cur.execute("SELECT id, title FROM assessment_drives WHERE title ILIKE %s OR title ILIKE %s;", ('%Screening Test%', '%Internal Company Test%'))
    existing = cur.fetchall()
    for eid, etitle in existing:
        print(f"Cleaning up existing assessment {eid}: {etitle}", flush=True)
        cur.execute("DELETE FROM assessment_answers WHERE submission_id IN (SELECT id FROM assessment_submissions WHERE assessment_id = %s);", (eid,))
        cur.execute("DELETE FROM assessment_submissions WHERE assessment_id = %s;", (eid,))
        cur.execute("DELETE FROM assessment_questions WHERE assessment_id = %s;", (eid,))
        cur.execute("DELETE FROM assessment_drives WHERE id = %s;", (eid,))
    conn.commit()

    # 3. Create new Assessment
    print("Creating new 'Screening Test' assessment...", flush=True)
    cur.execute("""
        INSERT INTO assessment_drives (title, description, duration, pass_percentage, status, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        RETURNING id;
    """, (
        "Screening Test",
        "Fundamental Technical Screening Assessment covering Linux/Ubuntu Essentials, Docker Basics, Everyday Git & GitHub Commands, and Core Python Object-Oriented Programming (OOP) Concepts. Contains 20 MCQs. Time limit: 20 minutes.",
        20,
        50.0,
        "active"
    ))
    assessment_id = cur.fetchone()[0]
    print(f"Assessment created with ID: {assessment_id}", flush=True)

    questions = [
        # ── SECTION 1: LINUX / UBUNTU / DOCKER BASICS (10 Questions) ──
        (
            "Q1. Which command is used in Linux/Ubuntu to list all files and directories, including hidden ones?",
            "ls -a",
            "list --all",
            "show -hidden",
            "dir /h",
            "A"
        ),
        (
            "Q2. Which Linux command is used to navigate back to the parent directory?",
            "cd ..",
            "cd ~",
            "cd /",
            "back",
            "A"
        ),
        (
            "Q3. Which command is used to create a new directory named 'project' in Linux?",
            "mkdir project",
            "touch project",
            "create project",
            "newdir project",
            "A"
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
            "cat app.log",
            "open app.log",
            "echo app.log",
            "print app.log",
            "A"
        ),
        (
            "Q6. Which package management command is used to install new software packages on Ubuntu Linux?",
            "sudo apt install <package-name>",
            "sudo yum install <package-name>",
            "brew install <package-name>",
            "pip install-ubuntu <package-name>",
            "A"
        ),
        (
            "Q7. Which Docker command is used to download an image (if not present) and start a new container from it?",
            "docker run",
            "docker start",
            "docker build",
            "docker init",
            "A"
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
            "docker build -t myapp .",
            "docker create myapp",
            "docker compile -i myapp",
            "docker make myapp",
            "A"
        ),
        (
            "Q10. How do you stop a running Docker container with container ID 'abc123'?",
            "docker stop abc123",
            "docker kill-all",
            "docker pause",
            "docker delete abc123",
            "A"
        ),

        # ── SECTION 2: GIT & GITHUB BASICS (5 Questions) ──
        (
            "Q11. Which Git command is used to download an existing remote repository from GitHub to your local computer?",
            "git clone <repository-url>",
            "git download <repository-url>",
            "git copy <repository-url>",
            "git fetch-new <repository-url>",
            "A"
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
            "git commit -m \"Your commit message\"",
            "git save -message \"Your commit message\"",
            "git push -m \"Your commit message\"",
            "git log -m \"Your commit message\"",
            "A"
        ),
        (
            "Q14. Which command uploads your committed changes from the local 'main' branch to the remote repository on GitHub?",
            "git push origin main",
            "git upload origin main",
            "git send origin main",
            "git export main",
            "A"
        ),
        (
            "Q15. Which command fetches the latest commits from the remote GitHub repository and merges them into your current local branch?",
            "git pull",
            "git push",
            "git sync-only",
            "git refresh",
            "A"
        ),

        # ── SECTION 3: PYTHON OBJECT-ORIENTED PROGRAMMING (OOP) (5 Questions) ──
        (
            "Q16. In Python Object-Oriented Programming, what is the primary role of the '__init__' method inside a class?",
            "It acts as the constructor method that initializes an object's attributes when an instance is created",
            "It automatically deletes the object from memory when finished",
            "It converts class data into a JSON string format",
            "It imports external Python libraries into the class",
            "A"
        ),
        (
            "Q17. Why is 'self' passed as the first parameter in instance methods of a Python class?",
            "It represents the specific instance of the class and provides access to its attributes and methods",
            "It is a required keyword that makes Python code execute faster",
            "It defines the parent class from which the class inherits",
            "It converts local variables into global variables",
            "A"
        ),
        (
            "Q18. Consider the following Python OOP code:\n\nclass Animal:\n    def speak(self):\n        return \"Animal sound\"\n\nclass Dog(Animal):\n    def speak(self):\n        return \"Woof!\"\n\npet = Dog()\nprint(pet.speak())\n\nWhat will be printed?",
            "Woof!",
            "Animal sound",
            "None",
            "AttributeError: Dog has no speak method",
            "A"
        ),
        (
            "Q19. In Python OOP (Encapsulation), what naming convention is commonly used to indicate that an attribute or method is private/internal?",
            "Prefixing the attribute name with an underscore or double underscore (e.g., _age or __salary)",
            "Using the 'private' keyword before variable declaration",
            "Writing the attribute name entirely in UPPERCASE",
            "Declaring the variable inside a tuple",
            "A"
        ),
        (
            "Q20. What is the concept of 'Polymorphism' in Python Object-Oriented Programming?",
            "The ability of different classes to implement methods with the same name, allowing them to be called uniformly",
            "Creating a class that cannot be inherited by any other class",
            "Storing all class variables in a single global dictionary",
            "Preventing functions from accepting multiple arguments",
            "A"
        )
    ]

    for q, a, b, c, d, ans in questions:
        cur.execute("""
            INSERT INTO assessment_questions (assessment_id, question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (assessment_id, q, a, b, c, d, ans))

    conn.commit()
    print(f"Successfully inserted {len(questions)} questions into 'Screening Test' (ID: {assessment_id})!", flush=True)

    # Display active assessments
    cur.execute("SELECT id, title, duration, status, (SELECT count(*) FROM assessment_questions WHERE assessment_id=assessment_drives.id) as qcount FROM assessment_drives ORDER BY id;")
    rows = cur.fetchall()
    print("\n--- Current Assessments in Database ---", flush=True)
    for r in rows:
        print(f"ID: {r[0]} | Title: {r[1]} | Duration: {r[2]}m | Status: {r[3]} | Questions: {r[4]}", flush=True)

    conn.close()

if __name__ == '__main__':
    seed_assessment()
