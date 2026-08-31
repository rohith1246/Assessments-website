import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Updating Screening Test - Java Developer (ID: 10) with 10 Core Java + 10 Easy Linux/Docker/GitHub MCQs...")

cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id = 10);")
cur.execute("DELETE FROM assessment_questions WHERE assessment_id = 10;")

mcq_questions = [
    # ── PART 1: 10 CORE JAVA QUESTIONS (Q1 - Q10) ──
    {
        "q": "In Java Object-Oriented Programming (OOP), what is the primary role of a 'constructor'?",
        "a": "To initialize the state of a newly created object when instantiated with the 'new' keyword",
        "b": "To destroy and garbage collect unused objects from heap memory",
        "c": "To convert Java source code directly into machine code",
        "d": "To manage database connection transactions",
        "key": "A"
    },
    {
        "q": "In Java, what is the key difference between the '==' operator and the '.equals()' method when comparing two String objects?",
        "a": "There is no difference; both compare character contents",
        "b": "'==' compares memory reference addresses, while '.equals()' compares the actual character contents",
        "c": "'==' works only for integers, while '.equals()' works only for floating point values",
        "d": "'.equals()' compares memory address while '==' compares string lengths",
        "key": "B"
    },
    {
        "q": "In Java OOP, which concept allows a subclass to provide a specific implementation of a method that is already defined in its superclass?",
        "a": "Method Overloading",
        "b": "Constructor Chaining",
        "c": "Method Overriding",
        "d": "Data Encapsulation",
        "key": "C"
    },
    {
        "q": "Why does Java utilize 'interfaces' instead of supporting multiple inheritance of classes?",
        "a": "Because interfaces run faster than regular classes",
        "b": "Because interfaces eliminate the need for the Garbage Collector",
        "c": "Because interfaces can only contain private variables",
        "d": "To avoid method ambiguity and complexity (the Diamond Problem) while ensuring loose coupling",
        "key": "D"
    },
    {
        "q": "In Java Exception Handling (try-catch-finally), what is the guarantee provided by the 'finally' block?",
        "a": "The code inside the 'finally' block always executes, whether an exception occurs or not (used for closing resources)",
        "b": "It only executes if a severe OutOfMemoryError is thrown",
        "c": "It automatically restarts the JVM when an exception happens",
        "d": "It suppresses all compiler errors during build time",
        "key": "A"
    },
    {
        "q": "In Java Collections Framework, which interface represents an ordered collection that allows duplicate elements?",
        "a": "Set",
        "b": "List",
        "c": "Map",
        "d": "Queue",
        "key": "B"
    },
    {
        "q": "In Java, what is the primary benefit of using 'StringBuilder' instead of 'String' when performing repeated string concatenations in a loop?",
        "a": "StringBuilder is thread-safe and synchronizes every character write",
        "b": "StringBuilder creates immutable objects that cannot be modified",
        "c": "StringBuilder is mutable and modifies the character buffer in-place without creating multiple temporary objects on the heap",
        "d": "StringBuilder automatically writes data directly to a file on disk",
        "key": "C"
    },
    {
        "q": "In Java multi-threading, which keyword is used to ensure that only one thread can execute a block of code or method at a time on a shared object?",
        "a": "static",
        "b": "transient",
        "c": "volatile",
        "d": "synchronized",
        "key": "D"
    },
    {
        "q": "In Java 8+, what is a 'Lambda Expression'?",
        "a": "A concise syntax to implement a Single Abstract Method (Functional Interface) anonymously",
        "b": "A tool used to compile C++ code inside Java",
        "c": "A database query language built into the JVM",
        "d": "A class that cannot be inherited by any subclass",
        "key": "A"
    },
    {
        "q": "In Java, which keyword is used to create an instance of a class and allocate memory on the Heap?",
        "a": "alloc",
        "b": "new",
        "c": "create",
        "d": "instance",
        "key": "B"
    },

    # ── PART 2: 10 EASY LINUX, DOCKER & GITHUB QUESTIONS (Q11 - Q20) ──
    # ── Linux (Q11 - Q14) ──
    {
        "q": "Which Linux/Ubuntu command is used to list all files and folders in the current directory, including hidden files (files starting with '.')?",
        "a": "list -all",
        "b": "dir -h",
        "c": "ls -la (or ls -a)",
        "d": "show files",
        "key": "C"
    },
    {
        "q": "Which Linux command is used to navigate back to the parent directory?",
        "a": "cd /root",
        "b": "cd ~",
        "c": "cd -",
        "d": "cd ..",
        "key": "D"
    },
    {
        "q": "Which Linux command is used to create a new folder/directory named 'my_project'?",
        "a": "mkdir my_project",
        "b": "create dir my_project",
        "c": "touch my_project",
        "d": "newfolder my_project",
        "key": "A"
    },
    {
        "q": "Which Linux command gives executable permission to a shell script file named 'start.sh'?",
        "a": "execute start.sh",
        "b": "chmod +x start.sh",
        "c": "run +x start.sh",
        "d": "setperm start.sh",
        "key": "B"
    },

    # ── Docker (Q15 - Q17) ──
    {
        "q": "Which Docker command is used to build a Docker image named 'my-app' using the Dockerfile in the current directory?",
        "a": "docker make my-app .",
        "b": "docker create my-app .",
        "c": "docker build -t my-app .",
        "d": "docker compile my-app",
        "key": "C"
    },
    {
        "q": "Which Docker command shows all currently active and running Docker containers?",
        "a": "docker list",
        "b": "docker images",
        "c": "docker show",
        "d": "docker ps",
        "key": "D"
    },
    {
        "q": "Which Docker command runs a container in background (detached mode) while mapping host port 8080 to container port 8080?",
        "a": "docker run -d -p 8080:8080 my-app",
        "b": "docker start -bg -port 8080 my-app",
        "c": "docker execute -d 8080:8080 my-app",
        "d": "docker init -p 8080 my-app",
        "key": "A"
    },

    # ── Git & GitHub (Q18 - Q20) ──
    {
        "q": "Which Git command is used to download/copy an existing repository from GitHub to your local machine?",
        "a": "git download <url>",
        "b": "git clone <url>",
        "c": "git copy <url>",
        "d": "git get <url>",
        "key": "B"
    },
    {
        "q": "Which Git command stages all modified and newly created files in the current folder for the next commit?",
        "a": "git commit -all",
        "b": "git stage *",
        "c": "git add .",
        "d": "git save .",
        "key": "C"
    },
    {
        "q": "Which Git command uploads your committed local changes to the remote 'main' branch on GitHub?",
        "a": "git upload origin main",
        "b": "git export main",
        "c": "git sync github main",
        "d": "git push origin main",
        "key": "D"
    }
]

for q in mcq_questions:
    cur.execute("""
        INSERT INTO assessment_questions (assessment_id, question, option_a, option_b, option_c, option_d, correct_answer, question_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (10, q["q"], q["a"], q["b"], q["c"], q["d"], q["key"], "mcq"))

print("Screening Test - Java Developer (ID: 10) updated with 10 Easy Java + 10 Easy Linux/Docker/Git!")


# ─────────────────────────────────────────────────────────────
# UPDATE TECHNICAL ROUND 2 - JAVA DEVELOPER (ID: 15) FIB
# ─────────────────────────────────────────────────────────────
print("\nUpdating Technical Round 2 - Java Developer (ID: 15)...")

cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id = 15);")
cur.execute("DELETE FROM assessment_questions WHERE assessment_id = 15;")

fib_questions = [
    # ── 10 CORE JAVA FIB QUESTIONS ──
    {
        "q": "In Java, all objects and class instances are allocated in the shared _____ memory area.",
        "a": "Heap|Heap Memory"
    },
    {
        "q": "In Java, the keyword used to create a new instance of a class is _____.",
        "a": "new"
    },
    {
        "q": "In Java OOP, when a subclass inherits from a superclass, it uses the keyword _____.",
        "a": "extends"
    },
    {
        "q": "In Java, a class implements an interface using the keyword _____.",
        "a": "implements"
    },
    {
        "q": "In Java, to prevent a variable from being modified or a class from being inherited, use the keyword _____.",
        "a": "final"
    },
    {
        "q": "In Java exception handling, the block of code that always executes after try-catch (regardless of exception) is the _____ block.",
        "a": "finally"
    },
    {
        "q": "In Java Collections Framework, the most commonly used dynamic array class that implements the List interface is _____List.",
        "a": "Array"
    },
    {
        "q": "In Java, to prevent multiple threads from accessing a shared method or block concurrently, use the _____ keyword.",
        "a": "synchronized"
    },
    {
        "q": "In Java, the special method that has the same name as the class and initializes an object when instantiated is called a _____.",
        "a": "constructor"
    },
    {
        "q": "In Java, the primitive data type used to store true or false values is _____.",
        "a": "boolean"
    },

    # ── 10 EASY LINUX, DOCKER & GITHUB FIB QUESTIONS ──
    # Linux (Q11 - Q14)
    {
        "q": "In Linux, the command used to list files and folders in the current directory is _____.",
        "a": "ls"
    },
    {
        "q": "In Linux, the command used to navigate or change the current working directory is _____.",
        "a": "cd"
    },
    {
        "q": "In Linux, the command used to create a new folder/directory is _____.",
        "a": "mkdir"
    },
    {
        "q": "In Linux, the command used to change permissions of a file (e.g. 'chmod +x file.sh') is _____.",
        "a": "chmod"
    },

    # Docker (Q15 - Q17)
    {
        "q": "In Docker, the command used to build a container image from a Dockerfile is 'docker _____ -t myapp .'.",
        "a": "build"
    },
    {
        "q": "In Docker CLI, the command used to show running containers is 'docker _____'.",
        "a": "ps"
    },
    {
        "q": "In Docker, to run a container in the background (detached mode), you pass the flag -_____.",
        "a": "d|-detach|--detach"
    },

    # Git & GitHub (Q18 - Q20)
    {
        "q": "In Git, to download a copy of an existing remote repository from GitHub to your computer, run 'git _____ <url>'.",
        "a": "clone"
    },
    {
        "q": "In Git, the command used to stage all changed files before committing is 'git _____ .'.",
        "a": "add"
    },
    {
        "q": "In Git, the command used to upload local committed changes to GitHub is 'git _____ origin main'.",
        "a": "push"
    }
]

for q in fib_questions:
    cur.execute("""
        INSERT INTO assessment_questions (assessment_id, question, correct_answer, question_type)
        VALUES (%s, %s, %s, %s);
    """, (15, q["q"], q["a"], "fib"))

print("Technical Round 2 - Java Developer (ID: 15) updated with 10 Easy Java + 10 Easy Linux/Docker/Git FIB!")

conn.commit()
conn.close()
print("DATABASE COMMITTED SUCCESSFULLY!")
