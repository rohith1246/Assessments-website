import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Setting exact 20 FIB questions for all 5 Technical Round 2 Assessments...")

# Exact 10 Linux, Docker & Git FIB questions (Q11 - Q20)
tech_fib_10 = [
    {
        "q": "In Linux, the command used to list files and folders in the current directory is _____.",
        "a": "ls|ls -la|ls -a"
    },
    {
        "q": "In Linux, the command used to navigate or change the current working directory is _____.",
        "a": "cd|cd .."
    },
    {
        "q": "In Linux, the command used to create a new folder/directory is _____.",
        "a": "mkdir"
    },
    {
        "q": "In Linux, the command used to change permissions of a file (e.g. 'chmod +x file.sh') is _____.",
        "a": "chmod|chmod +x"
    },
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
        "a": "d|-d|--detach|-detach"
    },
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

# ── 1. Python 10 FIB (ID: 14) ──
python_fib_10 = [
    {"q": "In Python, the built-in function used to find the number of elements in a list or string is _____().", "a": "len"},
    {"q": "In Python, the keyword used to define a custom function is _____.", "a": "def"},
    {"q": "In Python OOP, the constructor/initializer method for a class is named _____.", "a": "__init__|__init__"},
    {"q": "In Python, the data structure that stores key-value pairs is called a _____ (or dict).", "a": "dictionary|dict"},
    {"q": "In Python exception handling, the code block that always executes after try-except is the _____ block.", "a": "finally"},
    {"q": "In Python, an ordered collection that cannot be modified after creation (immutable) is a _____.", "a": "tuple"},
    {"q": "In Python, to safely open and automatically close a file, use the '_____ open(...)' statement.", "a": "with"},
    {"q": "In Python, to convert a string of numbers like '42' into an integer, use the _____() function.", "a": "int"},
    {"q": "In Python, to add a new item to the end of a list 'nums', you call nums._____ (item).", "a": "append"},
    {"q": "In Python, the boolean keyword representing a truth value with a capitalized first letter is _____.", "a": "True"}
]

# ── 2. Java 10 FIB (ID: 15) ──
java_fib_10 = [
    {"q": "In Java, all objects and class instances are allocated in the shared _____ memory area.", "a": "Heap|Heap Memory"},
    {"q": "In Java, the keyword used to create a new instance of a class is _____.", "a": "new"},
    {"q": "In Java OOP, when a subclass inherits from a superclass, it uses the keyword _____.", "a": "extends"},
    {"q": "In Java, a class implements an interface using the keyword _____.", "a": "implements"},
    {"q": "In Java, to prevent a variable from being modified or a class from being inherited, use the keyword _____.", "a": "final"},
    {"q": "In Java exception handling, the block of code that always executes after try-catch (regardless of exception) is the _____ block.", "a": "finally"},
    {"q": "In Java Collections Framework, the most commonly used dynamic array class that implements the List interface is _____List.", "a": "Array"},
    {"q": "In Java, to prevent multiple threads from accessing a shared method or block concurrently, use the _____ keyword.", "a": "synchronized"},
    {"q": "In Java, the special method that has the same name as the class and initializes an object when instantiated is called a _____.", "a": "constructor"},
    {"q": "In Java, the primitive data type used to store true or false values is _____.", "a": "boolean"}
]

# ── 3. Cyber Security 10 FIB (ID: 16) ──
cyber_fib_10 = [
    {"q": "In the CIA Triad of cybersecurity, the letters stand for Confidentiality, _____, and Availability.", "a": "Integrity"},
    {"q": "The default TCP port used for secure encrypted HTTPS web traffic is Port _____.", "a": "443"},
    {"q": "The fraudulent practice of sending emails purporting to be from reputable companies to induce individuals to reveal passwords is _____.", "a": "phishing"},
    {"q": "In asymmetric cryptography, data encrypted with a public key can only be decrypted by the corresponding _____ key.", "a": "private"},
    {"q": "The attack where malicious SQL statements are inserted into entry fields for execution on the database is SQL _____.", "a": "Injection"},
    {"q": "Authentication that requires two or more pieces of evidence (like password + SMS code) is Multi-_____ Authentication.", "a": "Factor|Factor Authentication|MFA"},
    {"q": "The security vulnerability where attackers inject malicious scripts into trusted websites is Cross-Site _____ (XSS).", "a": "Scripting"},
    {"q": "A security device or software that monitors and filters network traffic based on security rules is a _____.", "a": "firewall"},
    {"q": "A one-way mathematical algorithm that transforms data into a fixed-size string is a cryptographic _____ function.", "a": "hash|hashing"},
    {"q": "An attack that floods a server with massive fake traffic to make it unavailable to users is a _____ of Service (DoS/DDoS) attack.", "a": "Denial"}
]

# ── 4. Data Analyst 10 FIB (ID: 17) ──
data_fib_10 = [
    {"q": "In SQL, the statement used to extract and query data from a database table is _____.", "a": "SELECT"},
    {"q": "In SQL, the clause used to filter rows based on a condition before grouping is _____.", "a": "WHERE"},
    {"q": "In SQL, to group rows that have the same values into summary rows, use _____ BY.", "a": "GROUP"},
    {"q": "In SQL, the aggregate function used to count the total number of rows returned is _____().", "a": "COUNT"},
    {"q": "In SQL, to sort query results in ascending or descending order, use the _____ BY clause.", "a": "ORDER"},
    {"q": "In Python Data Analysis, the primary library used for manipulating structured DataFrames is _____.", "a": "pandas|pd"},
    {"q": "In Pandas, the function used to load a CSV dataset into a DataFrame is pd.read______().", "a": "csv"},
    {"q": "In Pandas, to fill in missing NaN values with a specific default value, use df._____na().", "a": "fill"},
    {"q": "In SQL, to return only unique, non-duplicate values in a query, use SELECT _____ <column>.", "a": "DISTINCT"},
    {"q": "A visual chart that displays data using rectangular vertical or horizontal bars proportional to values is a _____ chart.", "a": "bar|Bar"}
]

# ── 5. .NET Developer 10 FIB (ID: 18) ──
dotnet_fib_10 = [
    {"q": "In C#, the keyword used to create a new object instance and allocate memory is _____.", "a": "new"},
    {"q": "In C#, the access modifier that restricts member visibility to within the declaring class only is _____.", "a": "private"},
    {"q": "In C# asynchronous programming, a method marked with 'async' uses the '_____' keyword to pause until the Task completes.", "a": "await"},
    {"q": "In C# exception handling, the code block that is guaranteed to execute for resource cleanup is the _____ block.", "a": "finally"},
    {"q": "In C#, a class implements an interface using the colon (_____) syntax.", "a": ":"},
    {"q": "In .NET, the declarative query syntax used to filter and transform collections in C# is _____.", "a": "LINQ"},
    {"q": "In C#, the generic collection class that represents a strongly-typed dynamic list is _____<T>.", "a": "List"},
    {"q": "In C#, the keyword used to declare a constant value that cannot be changed is _____.", "a": "const"},
    {"q": "In C#, the statement used to ensure an IDisposable object is properly disposed is the '_____' statement.", "a": "using"},
    {"q": "In C#, string interpolation begins with the special prefix symbol _____ before the quotes.", "a": "$"}
]

tracks = [
    {"name": "Technical Round 2 - Python Developer", "id": 14, "core": python_fib_10},
    {"name": "Technical Round 2 - Java Developer", "id": 15, "core": java_fib_10},
    {"name": "Technical Round 2 - Cyber Security", "id": 16, "core": cyber_fib_10},
    {"name": "Technical Round 2 - Data Analyst", "id": 17, "core": data_fib_10},
    {"name": "Technical Round 2 - .NET Developer", "id": 18, "core": dotnet_fib_10},
]

for t in tracks:
    print(f"\nConfiguring {t['name']} (ID: {t['id']})...")
    cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id = %s);", (t['id'],))
    cur.execute("DELETE FROM assessment_questions WHERE assessment_id = %s;", (t['id'],))
    
    all_20_fibs = t['core'] + tech_fib_10
    for idx, q in enumerate(all_20_fibs, 1):
        cur.execute("""
            INSERT INTO assessment_questions (assessment_id, question, correct_answer, question_type)
            VALUES (%s, %s, %s, %s);
        """, (t['id'], q["q"], q["a"], "fib"))
    
    print(f"[OK] {t['name']} configured with exactly 20 Fill In The Blanks (10 Role + 10 Linux/Docker/Git)!")

conn.commit()
conn.close()
print("\nALL TECHNICAL ROUND 2 ASSESSMENTS ARE NOW 100% FILL IN THE BLANKS ONLY!")
