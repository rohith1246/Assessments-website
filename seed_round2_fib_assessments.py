"""
seed_round2_fib_assessments.py
Seeds 5 Technical Round 2 (Fill In The Blanks) Assessments into Neon PostgreSQL:
1. 'Technical Round 2 - Python Developer' (20 Hard FIB Questions)
2. 'Technical Round 2 - Java Developer' (20 Hard FIB Questions)
3. 'Technical Round 2 - Cyber Security' (20 Hard FIB Questions)
4. 'Technical Round 2 - Data Analyst' (20 Hard FIB Questions)
5. 'Technical Round 2 - .NET Developer' (20 Hard FIB Questions)

Each assessment contains exactly 20 difficult, real-world Fill in the Blanks questions,
20 minutes duration, 75% pass cutoff, status 'active'.
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# ══════════════════════════════════════════════════════════════════════════
# 1. PYTHON DEVELOPER - 20 HARD FIB QUESTIONS
# ══════════════════════════════════════════════════════════════════════════
PYTHON_FIB = [
    (
        "In Python memory management, the mechanism that prevents multiple native threads from executing Python bytecodes simultaneously is called the Global _____ Lock.",
        "Interpreter|Interpreter Lock"
    ),
    (
        "To customize class instantiation before '__init__' is called (often used in metaclasses or immutable singleton types), Python executes the special dunder method named '_________'.",
        "new"
    ),
    (
        "In Python descriptor protocol, to turn a class attribute into a non-data descriptor, you only need to implement the '_________' method.",
        "get"
    ),
    (
        "When constructing generator-based coroutines, the keyword used to pause execution and yield control back to the caller while retaining state is '_____'.",
        "yield"
    ),
    (
        "To prevent dynamic creation of '__dict__' on class instances to drastically reduce memory usage, you define the '_________' attribute.",
        "slots"
    ),
    (
        "In Python's 'functools' module, the decorator used to preserve the original function's name and docstring when wrapping it inside a decorator is '@functools._____'.",
        "wraps"
    ),
    (
        "In Python 3 asyncio, the keyword used before an asynchronous function call to suspend execution until the awaitable completes is '_____'.",
        "await"
    ),
    (
        "In Python's garbage collector, cyclic references between objects that cannot be freed by reference counting are detected and collected by the '_____ ' module.",
        "gc"
    ),
    (
        "When unpacking an arbitrary number of excess positional arguments in a function definition, you prefix the parameter name with a single '_____'.",
        "*"
    ),
    (
        "In Python OOP, the method resolution order used to linearize complex multiple inheritance hierarchies is called C3 _____.",
        "Linearization|Linearisation"
    ),
    (
        "To create a context manager using a generator function without defining a full class with '__enter__' and '__exit__', you use the '@contextlib._________' decorator.",
        "contextmanager"
    ),
    (
        "In Python's typing module, a callable type definition that allows runtime static duck-typing structural subtyping is called a '_____'.",
        "Protocol"
    ),
    (
        "In Python string formatting and debugging (Python 3.8+), adding the '_____' character after an expression inside an f-string (e.g. f'{x=}') prints both expression and value.",
        "="
    ),
    (
        "In multiprocessing, to share memory between independent OS processes without serialization overhead, Python provides the '__________' module in Python 3.8+.",
        "shared_memory"
    ),
    (
        "In Python's data model, the built-in function that returns the unique identity (memory address in CPython) of an object is '_____()'.",
        "id"
    ),
    (
        "To create an immutable sequence of bytes in Python, you instantiate the built-in type '_____'.",
        "bytes"
    ),
    (
        "In Python's dictionary implementation since version 3.7, keys are guaranteed to maintain their _____ order.",
        "insertion"
    ),
    (
        "In concurrent programming, an event loop primitive used to signal state changes between asynchronous coroutines without polling is 'asyncio._____'.",
        "Event"
    ),
    (
        "To inspect the compiled CPython bytecode instructions of a function, you pass the function to the '_____.dis()' function.",
        "dis"
    ),
    (
        "In Python's object model, the default metaclass from which all standard classes and metaclasses inherit is '_____'.",
        "type"
    )
]

# ══════════════════════════════════════════════════════════════════════════
# 2. JAVA DEVELOPER - 20 HARD FIB QUESTIONS
# ══════════════════════════════════════════════════════════════════════════
JAVA_FIB = [
    (
        "In the Java Virtual Machine (JVM) memory architecture, all class instances and arrays are allocated in the _____ memory area.",
        "Heap|Heap Memory"
    ),
    (
        "In Java concurrency, the keyword that guarantees changes to a variable are always flushed to main memory and visible immediately across all threads without CPU caching is '_____'.",
        "volatile"
    ),
    (
        "In Java Generics, the compile-time mechanism that removes generic type parameters and substitutes raw types/casts in bytecode is called Type _____.",
        "Erasure"
    ),
    (
        "In the JVM Garbage Collection subsystem, the low-pause garbage collector introduced in JDK 15 that scales to multi-terabyte heaps with sub-millisecond pauses is named _____ GC.",
        "ZGC|Z"
    ),
    (
        "In Java, to prevent a class from being subclassed (inherited) or a method from being overridden, it must be marked with the '_____' modifier keyword.",
        "final"
    ),
    (
        "In Java 8+ Streams, the intermediate operation used to flatten a Stream of Collections into a single continuous stream of elements is '.______()'.",
        "flatMap"
    ),
    (
        "In Java's memory model, thread-private variables that store local method frames and primitive operand evaluations are held on the JVM _____.",
        "Stack|JVM Stack"
    ),
    (
        "In Java class loading hierarchy, the topmost classloader written in native C/C++ that loads core Java runtime classes (rt.jar / java.base) is the _____ ClassLoader.",
        "Bootstrap|Bootstrap ClassLoader"
    ),
    (
        "In 'java.util.concurrent', the thread-safe synchronized hash table that segments internal locks (or uses lock-free CAS) for high concurrency is '_____HashMap'.",
        "Concurrent"
    ),
    (
        "In Java 14+, the keyword used to declare an immutable data-carrier class that automatically generates constructor, getters, equals, and hashCode is '_____'.",
        "record"
    ),
    (
        "To execute code with mutual exclusion on a shared monitor lock, Java provides the '_____' block keyword.",
        "synchronized"
    ),
    (
        "In Java reflection, the method called on an accessible Method object to dynamically execute it on a target instance is '._____(target, args)'.",
        "invoke"
    ),
    (
        "In Spring Framework / Java EE, the design pattern where object dependencies are supplied by an external IoC container rather than instantiated directly is called Dependency _____.",
        "Injection"
    ),
    (
        "In Java serialization, to designate that a specific field should not be serialized to disk/network stream, you mark it with the '_____' keyword.",
        "transient"
    ),
    (
        "In Project Loom (Java 21+), lightweight threads managed directly by the JVM runtime rather than 1:1 OS kernel threads are known as _____ Threads.",
        "Virtual"
    ),
    (
        "In Java exception handling, exceptions that inherit from 'RuntimeException' and are not checked at compile-time are called _____ exceptions.",
        "unchecked"
    ),
    (
        "In 'java.util.concurrent.atomic', non-blocking synchronization primitives achieve thread safety without mutex locks using hardware-level Compare-And-_____ (CAS) operations.",
        "Swap"
    ),
    (
        "In Java 17+, to restrict which specific classes are permitted to extend a parent class or interface, Java introduced _____ classes using the 'permits' keyword.",
        "sealed"
    ),
    (
        "In Java collections, 'TreeSet' and 'TreeMap' maintain elements in sorted natural order using a balanced Red-_____ Tree data structure.",
        "Black|Red-Black"
    ),
    (
        "The bytecode instruction that invokes an interface method dynamically at runtime in the JVM is 'invoke_____'.",
        "interface"
    )
]

# ══════════════════════════════════════════════════════════════════════════
# 3. CYBER SECURITY - 20 HARD FIB QUESTIONS
# ══════════════════════════════════════════════════════════════════════════
CYBER_FIB = [
    (
        "In cryptographic security, a one-time random or pseudo-random number used in authentication protocols to prevent replay attacks is called a '_____'.",
        "nonce"
    ),
    (
        "In binary exploitation and buffer overflows, the compiler defense that places a known randomized canary value before the stack return pointer is called Stack _____.",
        "Canary|Canaries"
    ),
    (
        "In web application security, the vulnerability where an attacker tricks an authenticated user's browser into executing unwanted actions on a trusted website is Cross-Site Request _____ (CSRF).",
        "Forgery"
    ),
    (
        "In Network Security, the protocol that operates at the Transport Layer (Port 443) to provide encrypted communications over TCP is TLS, which stands for Transport Layer _____.",
        "Security"
    ),
    (
        "In asymmetric cryptography, the key exchange algorithm that allows two parties to establish a shared secret over an untrusted public channel without transmitting the secret itself is Diffie-_____.",
        "Hellman"
    ),
    (
        "In Linux security auditing, the mandatory access control (MAC) kernel architecture developed by the NSA is SE____ (Security-Enhanced Linux).",
        "Linux"
    ),
    (
        "In Wireshark display filters, to filter exclusively for DNS query traffic over UDP, the filter expression is 'udp.port == _____'.",
        "53"
    ),
    (
        "In memory safety defenses, the OS feature that randomizes the virtual address space locations of the stack, heap, and libraries to hinder shellcode execution is _____ (Address Space Layout Randomization).",
        "ASLR"
    ),
    (
        "In MITRE ATT&CK framework, the phase where an adversary establishes command and control channels to communicate with compromised internal hosts is Command and _____ (C2).",
        "Control"
    ),
    (
        "In PKI (Public Key Infrastructure), the protocol used to check the real-time revocation status of an X.509 digital certificate without downloading full CRL lists is _____ (Online Certificate Status Protocol).",
        "OCSP"
    ),
    (
        "In web application headers, the HTTP header that forces modern browsers to only connect over HTTPS and disallows SSL stripping is Strict-Transport-_____ (HSTS).",
        "Security"
    ),
    (
        "In database penetration testing, an attack where the adversary determines data character-by-character based on SQL execution delays is called _____ Blind SQL Injection.",
        "Time-based|Time based"
    ),
    (
        "In Active Directory Kerberos security, an attack that extracts service ticket hashes from memory to crack domain service account passwords offline is called _____roasting.",
        "Kerberoasting"
    ),
    (
        "In symmetric cipher modes, AES in GCM (Galois/Counter Mode) is an example of AEAD, which stands for Authenticated Encryption with Associated _____.",
        "Data"
    ),
    (
        "In network penetration testing, sending ARP responses with forged MAC addresses to intercept LAN subnet traffic is called ARP _____.",
        "Poisoning|Spoofing"
    ),
    (
        "In vulnerability management, the open framework used to score vulnerability severity from 0.0 to 10.0 is CVSS (Common Vulnerability _____ System).",
        "Scoring"
    ),
    (
        "In reverse engineering, the x86/x64 assembly instruction used to execute a software breakpoint interrupt (often opcode 0xCC) is 'INT _____'.",
        "3"
    ),
    (
        "In email authentication, the DNS-based record that combines SPF and DKIM policies to prevent domain spoofing and phishing is _____ (Domain-based Message Authentication, Reporting, and Conformance).",
        "DMARC"
    ),
    (
        "In SOC operations, SIEM stands for Security Information and _____ Management.",
        "Event"
    ),
    (
        "In wireless security, the 4-way handshake vulnerability discovered in WPA2 Wi-Fi networks that allows traffic decryption is named _____ (Key Reinstallation Attack).",
        "KRACK"
    )
]

# ══════════════════════════════════════════════════════════════════════════
# 4. DATA ANALYST - 20 HARD FIB QUESTIONS
# ══════════════════════════════════════════════════════════════════════════
DATA_ANALYST_FIB = [
    (
        "In SQL window functions, to access the attribute value from the immediately preceding row without performing a self-join, you use the '_____(column)' window function.",
        "LAG"
    ),
    (
        "In pandas, to reshape a DataFrame from long format to wide format by aggregating values across index and column labels, you use the '._____()' method.",
        "pivot_table|pivot"
    ),
    (
        "In statistical linear regression, the metric that quantifies the proportion of variance in the dependent variable predictable from the independent variables is denoted as R-_____.",
        "squared|Square"
    ),
    (
        "In SQL analytics, when you need to substitute a NULL expression with a fallback value across multiple arguments, you use the standard ANSI SQL function 'COALESCE' or '_____'.",
        "COALESCE|NVL|IFNULL"
    ),
    (
        "In data warehousing (Kimball), a dimensional modeling table that contains measured metrics, numerical quantities, and foreign keys to dimensions is called a _____ table.",
        "Fact|fact table"
    ),
    (
        "In probability theory, the theorem stating that the sample mean of independent and identically distributed random variables approaches a normal distribution as sample size grows is the _____ Limit Theorem.",
        "Central"
    ),
    (
        "In pandas, to broadcast aggregate statistics (like group mean) back to match the original DataFrame row count without collapsing rows, you call '.groupby()._____()'.",
        "transform"
    ),
    (
        "In SQL query optimization, an index structure that incorporates all columns requested by a SELECT query so the query engine never touches the base table data pages is called a _____ index.",
        "Covering|covering index"
    ),
    (
        "In statistical classification, the curve that plots True Positive Rate (Sensitivity) against False Positive Rate (1 - Specificity) across threshold values is the _____ Curve.",
        "ROC"
    ),
    (
        "In advanced SQL, to define hierarchical queries that reference their own output iteratively, the Common Table Expression must begin with 'WITH _____'.",
        "RECURSIVE"
    ),
    (
        "In predictive modeling, the diagnostic value calculated as 1 / (1 - R_i^2) to identify excessive multicollinearity among features is the Variance _____ Factor (VIF).",
        "Inflation"
    ),
    (
        "In time series analysis, a stochastic process whose mean, variance, and autocovariance do not change over time is said to be _____.",
        "stationary"
    ),
    (
        "In data modeling, when an attribute changes and historical state must be preserved by adding a new row with start_date and end_date, it is an SCD Type _____ dimension.",
        "2"
    ),
    (
        "In SQL, to calculate multidimensional subtotals across all 2^N possible permutations of grouped columns, you use the 'GROUP BY _____()' clause.",
        "CUBE"
    ),
    (
        "In statistical testing, rejecting the true Null Hypothesis (detecting a false positive effect when none exists) is known as a Type _____ Error.",
        "I|1|One"
    ),
    (
        "In pandas, the method used to convert a categorical column containing string labels into binary 0/1 one-hot indicator columns is 'pd.get______()'.",
        "dummies"
    ),
    (
        "In database indexing, a B-_____ Tree is the standard balanced tree structure used for fast range searches and point lookups in relational DBMS engines.",
        "Tree"
    ),
    (
        "In probability distributions, the continuous probability distribution shaped like a symmetrical bell curve is the Gaussian or _____ distribution.",
        "Normal"
    ),
    (
        "In ETL pipelines, the modern architectural paradigm where raw data is ingested directly into a cloud data warehouse before transformations are applied is called EL_____ (Extract, Load, Transform).",
        "T"
    ),
    (
        "In A/B testing power analysis, the probability of correctly rejecting the null hypothesis when an actual effect exists (1 - beta) is called Statistical _____.",
        "Power"
    )
]

# ══════════════════════════════════════════════════════════════════════════
# 5. .NET DEVELOPER - 20 HARD FIB QUESTIONS
# ══════════════════════════════════════════════════════════════════════════
DOTNET_FIB = [
    (
        "In the .NET Common Language Runtime (CLR), the engine component that converts Intermediate Language (CIL) bytecode into native CPU machine instructions at runtime is the _____ Compiler.",
        "JIT|Just-In-Time"
    ),
    (
        "In C# memory management, the lightweight ref struct type that provides a type-safe, contiguous view over arbitrary memory buffers without Heap allocation is '_____<T>'.",
        "Span"
    ),
    (
        "In C# asynchronous programming, the compiler transforms 'async' methods into an underlying state _____ struct/class.",
        "machine"
    ),
    (
        "In ASP.NET Core Dependency Injection, a service registered with lifetime 'services.Add_____()' creates a new instance exactly once and shares it across the entire application runtime.",
        "Singleton"
    ),
    (
        "In .NET Garbage Collection, large objects exceeding 85,000 bytes are allocated directly in the Large Object Heap (LOH) which is collected during Generation _____ GC.",
        "2"
    ),
    (
        "In C# OOP, to allow a base class method to be overridden dynamically by derived classes, the base class method must be marked with the '_____' keyword.",
        "virtual"
    ),
    (
        "In C# 9+, to declare an immutable property that can only be assigned during object initialization and never modified afterward, you use the '_____' accessor.",
        "init"
    ),
    (
        "In Entity Framework Core, to prevent changes to queried entity models from being tracked in memory during read-only reporting queries, you chain '.AsNo_____()'.",
        "Tracking"
    ),
    (
        "In .NET memory management, to prevent the Garbage Collector from relocating an object in memory during native P/Invoke calls, you _____ the pointer using the 'fixed' statement.",
        "pin|pinning"
    ),
    (
        "In C# pattern matching, the underscore symbol '_____' is used as the discard / default wildcard pattern that matches any expression.",
        "_"
    ),
    (
        "In ASP.NET Core request processing, custom software components connected in sequence to handle HTTP requests and responses form the HTTP _____ pipeline.",
        "middleware"
    ),
    (
        "In C# type system, the fundamental base class in the System namespace from which all value types and reference types ultimately inherit is 'System._____'.",
        "Object"
    ),
    (
        "In .NET multithreading, to coordinate asynchronous non-blocking waiting between threads, the lightweight async synchronization lock provided is 'Semaphore_____'.",
        "Slim"
    ),
    (
        "In LINQ, query execution that does not evaluate data until the sequence is actively enumerated (e.g. via foreach or ToList()) is known as _____ execution.",
        "deferred|lazy"
    ),
    (
        "In C# 8+, to declare a method or variable that can safely accept null values under the nullable reference types compiler feature, you append the '_____' symbol.",
        "?"
    ),
    (
        "In .NET assembly metadata, attributes attached to code elements are inspected at runtime using the System._____ namespace.",
        "Reflection"
    ),
    (
        "In C#, the keyword used to unwrap and execute code without arithmetic overflow checking for extreme high-performance math is '_____'.",
        "unchecked"
    ),
    (
        "In ASP.NET Core, the interface used to read strongly-typed configuration settings bound from appsettings.json via the Options Pattern is 'I_____<TOptions>'.",
        "Options"
    ),
    (
        "In .NET Core / .NET 6+, the ahead-of-time compilation mode that compiles C# directly into native platform executables without requiring a JIT compiler is Native _____.",
        "AOT"
    ),
    (
        "In C# resource management, the interface that classes implement to support asynchronous unmanaged resource disposal (used with 'await using') is 'I_____Disposable'.",
        "Async"
    )
]

ROUND2_CONFIGS = [
    {
        "title": "Technical Round 2 - Python Developer",
        "description": "Round 2 Technical Evaluation (Fill In The Blanks) for Python Developers. Covers CPython internals, GIL, descriptors, metaclasses, async coroutine pipelines, memory optimization, and bytecode. Contains 20 Hard Questions. Time limit: 20 minutes.",
        "duration": 20,
        "pass_percentage": 75.0,
        "questions": PYTHON_FIB
    },
    {
        "title": "Technical Round 2 - Java Developer",
        "description": "Round 2 Technical Evaluation (Fill In The Blanks) for Java Developers. Covers JVM memory areas, ZGC, type erasure, concurrency, classloaders, virtual threads, and Red-Black tree collections. Contains 20 Hard Questions. Time limit: 20 minutes.",
        "duration": 20,
        "pass_percentage": 75.0,
        "questions": JAVA_FIB
    },
    {
        "title": "Technical Round 2 - Cyber Security",
        "description": "Round 2 Technical Evaluation (Fill In The Blanks) for Cyber Security Specialists. Covers Cryptographic primitives, ASLR/Canary exploits, TLS handshakes, Kerberoasting, Wireshark filters, and DMARC. Contains 20 Hard Questions. Time limit: 20 minutes.",
        "duration": 20,
        "pass_percentage": 75.0,
        "questions": CYBER_FIB
    },
    {
        "title": "Technical Round 2 - Data Analyst",
        "description": "Round 2 Technical Evaluation (Fill In The Blanks) for Data Analysts. Covers Window functions, Pandas vectorized transforms, Kimball SCD2, Central Limit Theorem, ROC curves, and VIF multicollinearity. Contains 20 Hard Questions. Time limit: 20 minutes.",
        "duration": 20,
        "pass_percentage": 75.0,
        "questions": DATA_ANALYST_FIB
    },
    {
        "title": "Technical Round 2 - .NET Developer",
        "description": "Round 2 Technical Evaluation (Fill In The Blanks) for .NET / C# Developers. Covers CLR JIT internals, Span<T>, async state machines, Generation 2 LOH, EF Core AsNoTracking, and Native AOT. Contains 20 Hard Questions. Time limit: 20 minutes.",
        "duration": 20,
        "pass_percentage": 75.0,
        "questions": DOTNET_FIB
    }
]

def seed_round2():
    uri = os.environ.get('DATABASE_URL', '')
    if '&channel_binding=' in uri:
        uri = uri.split('&channel_binding=')[0]

    print("Connecting to Neon database...", flush=True)
    conn = psycopg2.connect(uri, connect_timeout=15)
    cur = conn.cursor()

    cur.execute("SELECT setval('assessment_drives_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_drives));")
    cur.execute("SELECT setval('assessment_questions_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_questions));")
    conn.commit()

    for cfg in ROUND2_CONFIGS:
        title = cfg["title"]
        print(f"\nProcessing '{title}'...", flush=True)

        cur.execute("SELECT id FROM assessment_drives WHERE title = %s;", (title,))
        existing = cur.fetchall()
        for (eid,) in existing:
            print(f"  Cleaning up previous assessment ID {eid}...", flush=True)
            cur.execute("DELETE FROM assessment_answers WHERE submission_id IN (SELECT id FROM assessment_submissions WHERE assessment_id = %s);", (eid,))
            cur.execute("DELETE FROM assessment_submissions WHERE assessment_id = %s;", (eid,))
            cur.execute("DELETE FROM assessment_questions WHERE assessment_id = %s;", (eid,))
            cur.execute("DELETE FROM assessment_drives WHERE id = %s;", (eid,))
        conn.commit()

        cur.execute("""
            INSERT INTO assessment_drives (title, description, duration, pass_percentage, status, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING id;
        """, (title, cfg["description"], cfg["duration"], cfg["pass_percentage"], "active"))
        drive_id = cur.fetchone()[0]
        print(f"  Created Assessment ID: {drive_id} for '{title}'", flush=True)

        # Insert 20 FIB questions
        for q_text, correct_ans in cfg["questions"]:
            cur.execute("""
                INSERT INTO assessment_questions (assessment_id, question, question_type, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (%s, %s, %s, NULL, NULL, NULL, NULL, %s);
            """, (drive_id, q_text, 'fib', correct_ans))
        conn.commit()
        print(f"  Successfully inserted 20 Fill In The Blanks questions.", flush=True)

    cur.execute("SELECT id, title, duration, pass_percentage, status, (SELECT count(*) FROM assessment_questions WHERE assessment_id=assessment_drives.id) as qcount FROM assessment_drives ORDER BY id;")
    rows = cur.fetchall()
    print("\n================ ALL ASSESSMENTS IN DATABASE ================", flush=True)
    for r in rows:
        print(f"ID: {r[0]} | Title: {r[1]} | Pass: {r[3]}% | Status: {r[4]} | Questions: {r[5]}", flush=True)

    conn.close()

if __name__ == '__main__':
    seed_round2()
