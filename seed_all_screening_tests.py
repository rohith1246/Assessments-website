"""
seed_all_screening_tests.py
Seeds three specialized Screening Tests into Neon PostgreSQL:
1. 'Screening Test' (Linux + Git + Python OOP)
2. 'Screening Test - Java Developer' (Linux + Git + Java OOP & Core Java)
3. 'Screening Test - Cyber Security' (Linux + Git + Cybersecurity Fundamentals)

Each test contains 20 MCQs (15 common foundational + 5 domain-specific),
20 minutes duration, 75% pass cutoff, and balanced A/B/C/D answer distribution.
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

COMMON_QUESTIONS = [
    # ── SECTION 1: LINUX / UBUNTU / DOCKER BASICS (10 Questions) ──
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

    # ── SECTION 2: GIT & GITHUB BASICS (5 Questions) ──
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
    )
]

PYTHON_QUESTIONS = [
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
        "It is a required keyword that makes Python code execute faster",
        "It represents the specific instance of the class and provides access to its attributes and methods",
        "It defines the parent class from which the class inherits",
        "It converts local variables into global variables",
        "B"
    ),
    (
        "Q18. Consider the following Python OOP code:\n\nclass Animal:\n    def speak(self):\n        return \"Animal sound\"\n\nclass Dog(Animal):\n    def speak(self):\n        return \"Woof!\"\n\npet = Dog()\nprint(pet.speak())\n\nWhat will be printed?",
        "Animal sound",
        "None",
        "Woof!",
        "AttributeError: Dog has no speak method",
        "C"
    ),
    (
        "Q19. In Python OOP (Encapsulation), what naming convention is commonly used to indicate that an attribute or method is private/internal?",
        "Using the 'private' keyword before variable declaration",
        "Writing the attribute name entirely in UPPERCASE",
        "Declaring the variable inside a tuple",
        "Prefixing the attribute name with an underscore or double underscore (e.g., _age or __salary)",
        "D"
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

JAVA_QUESTIONS = [
    (
        "Q16. In Java Object-Oriented Programming, what is the primary role of a constructor method?",
        "It initializes the state and instance variables of a newly created object",
        "It destroys unreferenced objects from heap memory during garbage collection",
        "It compiles source .java files into bytecode .class files",
        "It imports external Maven and Gradle dependencies into the JVM",
        "A"
    ),
    (
        "Q17. In Java, what is the key difference between the '==' operator and the '.equals()' method when comparing two String objects?",
        "Both always perform identical reference checks across all types",
        "'==' compares memory reference addresses, while '.equals()' compares the actual text contents of the String objects",
        "'==' converts strings to integer hashcodes before comparison",
        "'.equals()' cannot be used with String objects",
        "B"
    ),
    (
        "Q18. Consider the following Java OOP code:\n\nclass Animal {\n    void speak() { System.out.print(\"Animal\"); }\n}\nclass Dog extends Animal {\n    void speak() { System.out.print(\"Woof!\"); }\n}\npublic class Main {\n    public static void main(String[] args) {\n        Animal pet = new Dog();\n        pet.speak();\n    }\n}\n\nWhat is printed when this program runs?",
        "Animal",
        "Compilation Error",
        "Woof!",
        "NullPointerException",
        "C"
    ),
    (
        "Q19. Why does Java utilize 'interfaces' instead of allowing multiple inheritance of concrete classes?",
        "To prevent Java applications from running on multi-core processors",
        "Because interfaces cannot contain method declarations",
        "To force all Java classes to be marked as abstract",
        "To avoid the 'Diamond Problem' ambiguity while supporting contract-based multiple type implementations",
        "D"
    ),
    (
        "Q20. In Java exception handling (try-catch-finally), what is the guarantee provided by the 'finally' block?",
        "It contains clean-up code that is guaranteed to execute whether an exception was thrown or caught",
        "It automatically suppresses all unchecked RuntimeExceptions",
        "It restarts the Java Virtual Machine (JVM) when a fatal error occurs",
        "It terminates the application immediately without closing open file descriptors",
        "A"
    )
]

CYBER_QUESTIONS = [
    (
        "Q16. In Information Security and Risk Management, what three core principles form the foundation of the 'CIA Triad'?",
        "Confidentiality, Integrity, and Availability",
        "Cybersecurity, Identity, and Authentication",
        "Cryptography, Inspection, and Authorization",
        "Cloud, Infrastructure, and Access Control",
        "A"
    ),
    (
        "Q17. What is the most effective industry-standard defense mechanism against SQL Injection (SQLi) vulnerabilities in web applications?",
        "Encrypting database passwords using MD5 hashing",
        "Using Parameterized Queries (Prepared Statements) and Object-Relational Mappers (ORMs)",
        "Disabling HTTPS encryption on backend API routes",
        "Allowing unsanitized user inputs directly in concatenated SQL query strings",
        "B"
    ),
    (
        "Q18. What defines Multi-Factor Authentication (MFA / 2FA) in cybersecurity authentication systems?",
        "Typing your login password twice to confirm accuracy",
        "Changing your account password once every 30 days",
        "Requiring two or more distinct verification factors (something you know, something you have, or something you are)",
        "Using an email address containing alphanumeric symbols",
        "C"
    ),
    (
        "Q19. Which widely used open-source network security tool is utilized by administrators and security engineers for network discovery, port scanning, and vulnerability auditing?",
        "Photoshop",
        "VLC Media Player",
        "Docker Desktop",
        "Nmap",
        "D"
    ),
    (
        "Q20. In Asymmetric (Public-Key) Cryptography (such as RSA or TLS/HTTPS handshakes), which key is used to decrypt data that was encrypted with the receiver's public key?",
        "The corresponding Private Key owned exclusively by the receiver",
        "The sender's Public Key",
        "A shared plaintext password",
        "The Certificate Authority's root domain name",
        "A"
    )
]

TEST_CONFIGS = [
    {
        "title": "Screening Test",
        "description": "Technical Screening Assessment covering Linux/Ubuntu Essentials, Docker Basics, Everyday Git & GitHub Commands, and Core Python Object-Oriented Programming (OOP) Concepts. Contains 20 MCQs. Time limit: 20 minutes.",
        "duration": 20,
        "pass_percentage": 75.0,
        "questions": COMMON_QUESTIONS + PYTHON_QUESTIONS
    },
    {
        "title": "Screening Test - Java Developer",
        "description": "Technical Screening Assessment for Java Developers covering Linux/Ubuntu Essentials, Docker Basics, Everyday Git & GitHub Commands, and Core Java / OOP Concepts (Inheritance, Polymorphism, Interfaces, Exception Handling). Contains 20 MCQs. Time limit: 20 minutes.",
        "duration": 20,
        "pass_percentage": 75.0,
        "questions": COMMON_QUESTIONS + JAVA_QUESTIONS
    },
    {
        "title": "Screening Test - Cyber Security",
        "description": "Technical Screening Assessment for Cyber Security covering Linux/Ubuntu Essentials, Docker Basics, Everyday Git & GitHub Commands, and Core Cybersecurity Fundamentals (CIA Triad, SQLi Prevention, MFA, Nmap, Asymmetric Encryption). Contains 20 MCQs. Time limit: 20 minutes.",
        "duration": 20,
        "pass_percentage": 75.0,
        "questions": COMMON_QUESTIONS + CYBER_QUESTIONS
    }
]

def seed_tests():
    uri = os.environ.get('DATABASE_URL', '')
    if '&channel_binding=' in uri:
        uri = uri.split('&channel_binding=')[0]

    print("Connecting to Neon database...", flush=True)
    conn = psycopg2.connect(uri, connect_timeout=15)
    cur = conn.cursor()

    # Sync primary key sequences
    print("Syncing sequences...", flush=True)
    cur.execute("SELECT setval('assessment_drives_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_drives));")
    cur.execute("SELECT setval('assessment_questions_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_questions));")
    conn.commit()

    for cfg in TEST_CONFIGS:
        title = cfg["title"]
        print(f"\nProcessing '{title}'...", flush=True)

        # Check existing
        cur.execute("SELECT id FROM assessment_drives WHERE title = %s;", (title,))
        existing = cur.fetchall()
        for (eid,) in existing:
            print(f"  Cleaning up previous assessment ID {eid}...", flush=True)
            cur.execute("DELETE FROM assessment_answers WHERE submission_id IN (SELECT id FROM assessment_submissions WHERE assessment_id = %s);", (eid,))
            cur.execute("DELETE FROM assessment_submissions WHERE assessment_id = %s;", (eid,))
            cur.execute("DELETE FROM assessment_questions WHERE assessment_id = %s;", (eid,))
            cur.execute("DELETE FROM assessment_drives WHERE id = %s;", (eid,))
        conn.commit()

        # Insert new drive
        cur.execute("""
            INSERT INTO assessment_drives (title, description, duration, pass_percentage, status, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING id;
        """, (title, cfg["description"], cfg["duration"], cfg["pass_percentage"], "active"))
        drive_id = cur.fetchone()[0]
        print(f"  Created Assessment ID: {drive_id} for '{title}'", flush=True)

        # Insert questions
        for q, a, b, c, d, ans in cfg["questions"]:
            cur.execute("""
                INSERT INTO assessment_questions (assessment_id, question, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (drive_id, q, a, b, c, d, ans))
        conn.commit()
        print(f"  Inserted {len(cfg['questions'])} questions (5 A, 5 B, 5 C, 5 D balanced).", flush=True)

    # Print summary
    cur.execute("SELECT id, title, duration, pass_percentage, status, (SELECT count(*) FROM assessment_questions WHERE assessment_id=assessment_drives.id) as qcount FROM assessment_drives ORDER BY id;")
    rows = cur.fetchall()
    print("\n================ ACTIVE ASSESSMENTS IN DATABASE ================", flush=True)
    for r in rows:
        print(f"ID: {r[0]} | Title: {r[1]} | Pass: {r[3]}% | Status: {r[4]} | Questions: {r[5]}", flush=True)

    conn.close()

if __name__ == '__main__':
    seed_tests()
