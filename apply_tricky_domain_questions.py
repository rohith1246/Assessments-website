import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Applying tricky, advanced domain questions (Q1-Q10) with ZERO answer giveaways across all 6 Round 2 tracks...")

tracks = {
    # ── 1. PYTHON DEVELOPER (ID: 14) ──
    14: [
        {"q": "In Python memory management, what built-in sequence type represents a fixed, read-only collection of elements that cannot be mutated after instantiation?", "a": "tuple"},
        {"q": "In Python, which keyword transforms a regular function into an iterator that yields values lazily on demand without loading the entire sequence into RAM?", "a": "yield"},
        {"q": "In Python object-oriented programming, which special double-underscore method acts as the instance constructor to initialize newly created object attributes?", "a": "__init__"},
        {"q": "In Python, to ensure operating system file handles and network sockets are automatically closed via the context manager protocol, we wrap execution using the '_____' keyword.", "a": "with"},
        {"q": "In Python function definitions, which prefix operator allows a function to accept an arbitrary dictionary of keyword-value arguments?", "a": "**kwargs|**"},
        {"q": "In Python, which standard built-in data type utilizes a hashtable to deliver average O(1) time complexity for key-based lookups and assignments?", "a": "dict|dictionary"},
        {"q": "In Python exception handling architecture, which code block is guaranteed to execute unconditionally regardless of whether an exception was raised, caught, or missed?", "a": "finally"},
        {"q": "In Python, which list method inserts an individual element at the terminal index in-place without creating a new list object in memory?", "a": "append"},
        {"q": "In CPython runtime architecture, which internal mutex mechanism prevents multiple native OS threads from executing Python bytecodes simultaneously in a single process?", "a": "GIL|Global Interpreter Lock"},
        {"q": "In Python, which symbol is prefixed above a function signature to apply a higher-order wrapper function / decorator?", "a": "@"}
    ],

    # ── 2. JAVA DEVELOPER (ID: 15) ──
    15: [
        {"q": "In JVM architecture, all newly instantiated objects and class instances allocated via the 'new' operator reside in which shared memory region?", "a": "Heap|Heap Memory"},
        {"q": "In Java multi-threaded concurrent programming, which keyword is applied to methods or code blocks to acquire an intrinsic object monitor lock and prevent race conditions?", "a": "synchronized"},
        {"q": "In Java OOP design, which keyword is declared in a subclass definition to inherit non-private fields and methods from a superclass?", "a": "extends"},
        {"q": "In Java, which keyword is specified in a concrete class declaration to fulfill the contractual abstract method signatures defined in an interface?", "a": "implements"},
        {"q": "In Java, which modifier keyword prevents a variable from being reassigned, a method from being overridden, or a class from being subclassed?", "a": "final"},
        {"q": "In Java structured exception handling, which block executes unconditionally to ensure database connections and file streams are safely closed?", "a": "finally"},
        {"q": "In Java String comparison, while the '==' operator tests memory reference identity, which method must be invoked to evaluate actual character sequence equality?", "a": "equals"},
        {"q": "In the Java Collections Framework, which generic class backed by a dynamic array implements the List interface with fast random access?", "a": "ArrayList"},
        {"q": "In Java concurrency, which keyword guarantees that writes to a field are immediately visible to all other threads by bypassing CPU hardware caches?", "a": "volatile"},
        {"q": "In Java memory management, setting an object reference to '_____' makes the unreferenced heap instance eligible for reclamation by the Garbage Collector.", "a": "null"}
    ],

    # ── 3. CYBER SECURITY (ID: 16) ──
    16: [
        {"q": "In fundamental information security architecture, which pillar of the CIA Triad ensures that sensitive data has not been altered, tampered with, or corrupted in transit?", "a": "Integrity"},
        {"q": "In internet networking standards, which standard default TCP transport port is designated for encrypted TLS/SSL communication over HTTPS?", "a": "443"},
        {"q": "Which deceptive cyber attack vector involves crafting fraudulent communications that mimic trusted institutions to deceive employees into disclosing confidential credentials?", "a": "phishing"},
        {"q": "In asymmetric public-key cryptography, ciphertext encrypted with a recipient's public key can only be decrypted using that recipient's corresponding _____ key.", "a": "private"},
        {"q": "Which web application vulnerability occurs when unsanitized user input concatenated into dynamic database commands alters the intended query logic?", "a": "SQL Injection|SQLi"},
        {"q": "Security verification systems requiring two or more distinct validation categories (something you know, have, or are) are termed Multi-_____ Authentication.", "a": "Factor"},
        {"q": "Which web vulnerability occurs when malicious JavaScript injected into a web application executes in the browsers of victim users?", "a": "XSS|Cross-Site Scripting"},
        {"q": "In network security infrastructure, which hardware or software appliance monitors and filters inbound and outbound packet flows according to predefined security rules?", "a": "firewall"},
        {"q": "What mathematical algorithm transforms arbitrary input data into a fixed-length digest that cannot be mathematically reversed to recover the original plaintext?", "a": "hash|hashing|hash function"},
        {"q": "An attack orchestrated across a distributed botnet to flood a target web service with synthetic traffic and exhaust its server bandwidth is a _____ of Service (DDoS) attack.", "a": "Denial"}
    ],

    # ── 4. DATA ANALYST (ID: 17) ──
    17: [
        {"q": "In Structured Query Language (SQL), which primary statement begins every read query to retrieve specified column records from a database table?", "a": "SELECT"},
        {"q": "In SQL queries containing aggregated calculation metrics, which specific clause is mandatory to filter summarized subsets generated by the GROUP BY clause?", "a": "HAVING"},
        {"q": "In SQL execution order, which clause filters individual table records before any grouping or mathematical aggregations take place?", "a": "WHERE"},
        {"q": "In SQL relational queries, which join returns all records from the primary left table regardless of whether matching foreign keys exist in the right table?", "a": "LEFT JOIN|LEFT"},
        {"q": "In SQL data cleansing queries, which keyword eliminates duplicate rows from the query output to retain only unique instances of column values?", "a": "DISTINCT"},
        {"q": "In Python data analytics libraries, what is the two-dimensional size-mutable tabular data structure with labeled axes (rows and columns) in Pandas called?", "a": "DataFrame"},
        {"q": "In Pandas data preprocessing pipelines, which method is invoked on a DataFrame to replace null/NaN records with statistical averages or default constants?", "a": "fillna"},
        {"q": "In Pandas, which function is executed to parse and ingest comma-separated tabular text files directly into an in-memory DataFrame?", "a": "read_csv|pd.read_csv"},
        {"q": "In exploratory data visualization, which standard chart type displays quantitative comparisons across discrete categories using rectangular columns?", "a": "bar|bar chart"},
        {"q": "In Pandas exploratory analysis, which method automatically computes summary statistics (count, mean, standard deviation, percentiles) for all numeric series in a dataset?", "a": "describe"}
    ],

    # ── 5. .NET DEVELOPER (ID: 18) ──
    18: [
        {"q": "In C# type system architecture, while classes are reference types allocated on the Heap, structures ('struct') are value types allocated on the _____.", "a": "Stack"},
        {"q": "In C# OOP encapsulation, which access modifier restricts access so that fields and methods are accessible only within the declaring type and nowhere else?", "a": "private"},
        {"q": "In C# asynchronous programming, a method declared with the 'async' modifier uses which contextual keyword to yield execution until the awaited Task finishes?", "a": "await"},
        {"q": "In C# exception handling, which block executes unconditionally to guarantee that unmanaged system handles and database connections are freed?", "a": "finally"},
        {"q": "In .NET, what declarative SQL-like querying syntax embedded directly into C# allows developers to filter, project, and transform in-memory collections?", "a": "LINQ"},
        {"q": "In the System.Collections.Generic namespace, which generic collection class represents a strongly-typed, auto-resizing sequential collection?", "a": "List"},
        {"q": "In C#, which keyword is used to declare an immutable compile-time scalar value whose value is baked directly into IL metadata at build time?", "a": "const"},
        {"q": "In C#, which language statement ensures that an object implementing the IDisposable interface has its Dispose() method automatically invoked when leaving scope?", "a": "using"},
        {"q": "In C# string formatting, which special character prefix enables interpolated string expressions containing embedded variable expressions inside curly braces?", "a": "$"},
        {"q": "In the ASP.NET Core Dependency Injection container, which service lifetime registers a dependency that is created once per HTTP client request cycle?", "a": "Scoped"}
    ],

    # ── 6. SAP MM (ID: 19) ──
    19: [
        {"q": "In SAP Invoice Verification (MIRO), the automated control mechanism that cross-validates line items against the Purchase Order and Goods Receipt is known as a _____-way match.", "a": "3|Three"},
        {"q": "In SAP inventory management, which standard 3-digit movement type is posted when accepted goods are received into warehouse storage from an approved supplier order?", "a": "101"},
        {"q": "In SAP enterprise structure, to enable cross-plant procurement within a single company code, the Purchasing Organization must be directly assigned to the Company _____.", "a": "Code"},
        {"q": "In the SAP ABAP database dictionary, which central transparent table stores client-level general master attributes (such as base unit of measure, gross weight, and material type)?", "a": "MARA"},
        {"q": "In SAP MM-FI integration, which transaction code is configured by functional consultants to assign G/L accounts automatically based on valuation classes and transaction keys?", "a": "OBYC|OMWB"},
        {"q": "In modern SAP ERP, which single-screen transaction code is executed to perform receipts, scrap issues, and storage location transfer postings under one unified interface?", "a": "MIGO"},
        {"q": "In SAP Purchasing, which single-letter item category is specified on a purchase order item when raw components are provided to a third-party vendor for contract manufacturing?", "a": "L"},
        {"q": "In SAP periodic physical inventory workflow, after generating the inventory sheet (MI01), which transaction code is used to enter the counted physical quantities?", "a": "MI04"},
        {"q": "In SAP database architecture, while client-level material data is in MARA, which database table stores plant-level data and MRP parameters for materials?", "a": "MARC"},
        {"q": "In SAP S/4HANA Enterprise Management, traditional vendor and customer masters are completely unified and maintained under the strategic central entity called a Business _____.", "a": "Partner"}
    ]
}

for did, q_list in tracks.items():
    cur.execute("SELECT title FROM assessment_drives WHERE id = %s;", (did,))
    row = cur.fetchone()
    if not row:
        continue
    title = row[0]
    print(f"\nUpdating Q1-Q10 for {title} (ID: {did})...")
    
    cur.execute("SELECT id FROM assessment_questions WHERE assessment_id = %s ORDER BY id;", (did,))
    q_rows = cur.fetchall()
    
    if len(q_rows) >= 10:
        for idx in range(10):
            target_id = q_rows[idx][0]
            new_q = q_list[idx]
            cur.execute("""
                UPDATE assessment_questions 
                SET question = %s, correct_answer = %s, question_type = 'fib'
                WHERE id = %s;
            """, (new_q["q"], new_q["a"], target_id))
        print(f"[OK] Successfully updated Q1-Q10 for {title}!")

conn.commit()

# Print verified SAP MM (ID: 19) full 20 questions
print("\n=== VERIFIED FULL 20 QUESTIONS FOR SAP MM (ID: 19) ===")
cur.execute("SELECT id, question, correct_answer FROM assessment_questions WHERE assessment_id = 19 ORDER BY id;")
for idx, q in enumerate(cur.fetchall(), 1):
    print(f"Q{idx} [{q[0]}]: {q[1]}\n   -> Key: {q[2]}\n")

conn.close()
print("DATABASE COMMITTED SUCCESSFULLY!")
