import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Connected to Neon DB. Seeding all 5 roles (Screening MCQ & Technical Round 2 FIB)...")

# ── 10 COMMON EASY LINUX, DOCKER & GITHUB QUESTIONS (MCQ) ──
common_tech_mcqs = [
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

# ── 10 COMMON EASY LINUX, DOCKER & GITHUB QUESTIONS (FIB) ──
common_tech_fibs = [
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

# =====================================================================
# ROLE 1: PYTHON DEVELOPER (MCQ: 9, FIB: 14)
# =====================================================================
python_core_mcqs = [
    {
        "q": "In Python, which of the following built-in data types is mutable?",
        "a": "List",
        "b": "Tuple",
        "c": "String",
        "d": "Integer",
        "key": "A"
    },
    {
        "q": "In Python, which data structure stores unique elements in key-value pairs with fast O(1) lookup?",
        "a": "List",
        "b": "Dictionary (dict)",
        "c": "Tuple",
        "d": "Array",
        "key": "B"
    },
    {
        "q": "In Python Object-Oriented Programming, which special method is called automatically when a new object instance is created?",
        "a": "__str__()",
        "b": "__new__()",
        "c": "__init__()",
        "d": "__del__()",
        "key": "C"
    },
    {
        "q": "What will be the output of the list comprehension: '[x * 2 for x in [1, 2, 3]]'?",
        "a": "[1, 2, 3]",
        "b": "[1, 4, 9]",
        "c": "[2, 2, 2]",
        "d": "[2, 4, 6]",
        "key": "D"
    },
    {
        "q": "In Python, which block of code in a try-except structure is guaranteed to execute regardless of whether an exception was raised or not?",
        "a": "finally",
        "b": "else",
        "c": "catch",
        "d": "rescue",
        "key": "A"
    },
    {
        "q": "Which Python keyword is used to define a function?",
        "a": "function",
        "b": "def",
        "c": "func",
        "d": "define",
        "key": "B"
    },
    {
        "q": "In Python, what is the best practice statement used to open a file ensuring it is automatically closed after execution?",
        "a": "open file('data.txt') as f:",
        "b": "file.open('data.txt')",
        "c": "with open('data.txt') as f:",
        "d": "using open('data.txt'):",
        "key": "C"
    },
    {
        "q": "Which built-in function returns the total number of items in a list, tuple, or string in Python?",
        "a": "size()",
        "b": "count()",
        "c": "length()",
        "d": "len()",
        "key": "D"
    },
    {
        "q": "In Python function definitions, what allows a function to accept an arbitrary number of positional arguments as a tuple?",
        "a": "*args",
        "b": "**kwargs",
        "c": "params",
        "d": "varargs",
        "key": "A"
    },
    {
        "q": "In Python, what is the output of '\"hello world\".split(\" \")'?",
        "a": "\"helloworld\"",
        "b": "['hello', 'world']",
        "c": "('hello', 'world')",
        "d": "{'hello': 'world'}",
        "key": "B"
    }
]

python_core_fibs = [
    {"q": "In Python, the built-in function used to find the number of elements in a list or string is _____().", "a": "len"},
    {"q": "In Python, the keyword used to define a custom function is _____.", "a": "def"},
    {"q": "In Python OOP, the initializer/constructor method for a class is named _____.", "a": "__init__|__init__"},
    {"q": "In Python, the data structure that stores key-value pairs is called a _____ (or dict).", "a": "dictionary|dict"},
    {"q": "In Python exception handling, the code block that always runs after try-except is the _____ block.", "a": "finally"},
    {"q": "In Python, an ordered collection that cannot be modified after creation (immutable) is a _____.", "a": "tuple"},
    {"q": "In Python, to safely open and automatically close a file, use the '_____ open(...)' statement.", "a": "with"},
    {"q": "In Python, to convert a string of numbers like '42' into an integer, use the _____() function.", "a": "int"},
    {"q": "In Python, to add a new item to the end of a list 'nums', you call nums._____ (item).", "a": "append"},
    {"q": "In Python, the boolean keyword representing a truth value with capitalized first letter is _____.", "a": "True"}
]

# =====================================================================
# ROLE 2: JAVA DEVELOPER (MCQ: 10, FIB: 15)
# =====================================================================
java_core_mcqs = [
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
    }
]

java_core_fibs = [
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

# =====================================================================
# ROLE 3: CYBER SECURITY (MCQ: 11, FIB: 16)
# =====================================================================
cyber_core_mcqs = [
    {
        "q": "In Information Security, what are the three fundamental pillars of the 'CIA Triad'?",
        "a": "Confidentiality, Integrity, Availability",
        "b": "Control, Identification, Authentication",
        "c": "Cryptography, Inspection, Access",
        "d": "Cyber, Internet, Application",
        "key": "A"
    },
    {
        "q": "Which standard network port is used for secure encrypted web traffic over HTTPS (SSL/TLS)?",
        "a": "Port 80",
        "b": "Port 443",
        "c": "Port 22",
        "d": "Port 21",
        "key": "B"
    },
    {
        "q": "What type of social engineering attack involves sending deceptive emails masquerading as reputable organizations to steal user credentials?",
        "a": "DDoS attack",
        "b": "Buffer Overflow",
        "c": "Phishing attack",
        "d": "Man-in-the-Middle",
        "key": "C"
    },
    {
        "q": "In Asymmetric Cryptography (Public-Key Cryptography), how are the keys utilized for encryption and decryption?",
        "a": "Both sender and receiver use the same secret shared key",
        "b": "Data is hashed and cannot be decrypted",
        "c": "The private key encrypts and cannot be opened",
        "d": "Data is encrypted with the recipient's Public Key and decrypted only with their Private Key",
        "key": "D"
    },
    {
        "q": "What is the primary security defense against SQL Injection (SQLi) vulnerabilities in web applications?",
        "a": "Using Parameterized Queries (Prepared Statements) and input validation",
        "b": "Storing database passwords in plain text",
        "c": "Disabling the database firewall",
        "d": "Using GET requests instead of POST requests",
        "key": "A"
    },
    {
        "q": "What does Multi-Factor Authentication (MFA / 2FA) require to successfully authenticate a user?",
        "a": "Two identical passwords entered simultaneously",
        "b": "Two or more independent factors: Something you know (password), something you have (OTP/phone), or something you are (biometric)",
        "c": "Only an email address without a password",
        "d": "A static IP address from an approved VPN",
        "key": "B"
    },
    {
        "q": "Which type of web application vulnerability occurs when malicious JavaScript is injected into trusted web pages and executed in a victim's browser?",
        "a": "SQL Injection",
        "b": "Brute Force Attack",
        "c": "Cross-Site Scripting (XSS)",
        "d": "Privilege Escalation",
        "key": "C"
    },
    {
        "q": "What is the primary purpose of a Network Firewall?",
        "a": "To speed up website loading times",
        "b": "To generate SSL certificates for domains",
        "c": "To backup database files every hour",
        "d": "To monitor, filter, and control incoming and outgoing network traffic based on predetermined security rules",
        "key": "D"
    },
    {
        "q": "What is the core characteristic of a cryptographic Hash Function (like SHA-256 or bcrypt) compared to encryption?",
        "a": "Hashing is a one-way mathematical function; a hash value cannot be reversed to derive the original plaintext",
        "b": "Hashing can easily be reversed by anyone with a private key",
        "c": "Hashing requires an active internet connection to verify",
        "d": "Hashing compresses images without loss of quality",
        "key": "A"
    },
    {
        "q": "What type of attack aims to overwhelm a server or network with flood of traffic, making it unavailable to legitimate users?",
        "a": "SQL Injection",
        "b": "Distributed Denial of Service (DDoS)",
        "c": "Cross-Site Request Forgery (CSRF)",
        "d": "Trojan Horse",
        "key": "B"
    }
]

cyber_core_fibs = [
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

# =====================================================================
# ROLE 4: DATA ANALYST (MCQ: 12, FIB: 17)
# =====================================================================
data_core_mcqs = [
    {
        "q": "In SQL, which clause is used to filter rows returned by a query based on a specific condition?",
        "a": "WHERE",
        "b": "GROUP BY",
        "c": "ORDER BY",
        "d": "SELECT",
        "key": "A"
    },
    {
        "q": "In SQL, which aggregate function calculates the average value of a numeric column?",
        "a": "SUM()",
        "b": "AVG()",
        "c": "MEAN()",
        "d": "COUNT()",
        "key": "B"
    },
    {
        "q": "In SQL, what is the difference between the 'WHERE' clause and the 'HAVING' clause?",
        "a": "'WHERE' filters grouped aggregates, while 'HAVING' filters individual rows",
        "b": "There is no difference; they can be used interchangeably",
        "c": "'WHERE' filters individual rows before aggregation, while 'HAVING' filters groups created by 'GROUP BY'",
        "d": "'HAVING' is only used in subqueries",
        "key": "C"
    },
    {
        "q": "In SQL, which type of JOIN returns all records from the left table, and the matched records from the right table (with NULLs for unmatched right records)?",
        "a": "INNER JOIN",
        "b": "RIGHT JOIN",
        "c": "CROSS JOIN",
        "d": "LEFT JOIN (or LEFT OUTER JOIN)",
        "key": "D"
    },
    {
        "q": "In Python for Data Analysis, which library is the standard industry tool for tabular data manipulation and DataFrame operations?",
        "a": "Pandas",
        "b": "Flask",
        "c": "Pygame",
        "d": "Requests",
        "key": "A"
    },
    {
        "q": "In Pandas, which function is used to load and read a comma-separated values file into a DataFrame?",
        "a": "pd.read_table()",
        "b": "pd.read_csv()",
        "c": "pd.load_file()",
        "d": "pd.open_csv()",
        "key": "B"
    },
    {
        "q": "In Pandas, which method is used to remove rows containing missing (NaN / null) values from a DataFrame?",
        "a": "df.remove_null()",
        "b": "df.clean()",
        "c": "df.dropna()",
        "d": "df.delete_na()",
        "key": "C"
    },
    {
        "q": "In exploratory data analysis, which statistical chart is best suited for visualizing the frequency distribution of a continuous numeric variable?",
        "a": "Pie Chart",
        "b": "Scatter Plot",
        "c": "Line Graph",
        "d": "Histogram",
        "key": "D"
    },
    {
        "q": "In SQL, which keyword is used to eliminate duplicate rows and return only unique values from a column?",
        "a": "DISTINCT",
        "b": "UNIQUE",
        "c": "SINGLE",
        "d": "GROUP",
        "key": "A"
    },
    {
        "q": "In Pandas, which method provides quick statistical summary metrics (count, mean, std, min, 25%, 50%, max) of numeric columns?",
        "a": "df.info()",
        "b": "df.describe()",
        "c": "df.summary()",
        "d": "df.metrics()",
        "key": "B"
    }
]

data_core_fibs = [
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

# =====================================================================
# ROLE 5: .NET DEVELOPER (MCQ: 13, FIB: 18)
# =====================================================================
dotnet_core_mcqs = [
    {
        "q": "In C# and .NET runtime, what is the primary distinction between a 'struct' (Value Type) and a 'class' (Reference Type)?",
        "a": "Structs are allocated on the Stack (value copied), while classes are allocated on the Heap (reference copied)",
        "b": "Structs can have infinite inheritance, while classes cannot inherit",
        "c": "Classes cannot contain methods, while structs can",
        "d": "Structs require an active SQL database connection",
        "key": "A"
    },
    {
        "q": "In C#, which access modifier restricts access so a member is accessible only within its own class?",
        "a": "public",
        "b": "private",
        "c": "protected",
        "d": "internal",
        "key": "B"
    },
    {
        "q": "In modern C#, which feature provides a convenient syntax for declaring auto-implemented properties?",
        "a": "public string Name => get();",
        "b": "var Name = property();",
        "c": "public string Name { get; set; }",
        "d": "property Name = new()",
        "key": "C"
    },
    {
        "q": "In .NET, what is Language Integrated Query (LINQ) primarily used for?",
        "a": "Compiling C# code into native assembly binaries",
        "b": "Configuring Docker container ports",
        "c": "Running unit tests automatically",
        "d": "Querying and filtering in-memory collections, databases, and XML in a declarative SQL-like C# syntax",
        "key": "D"
    },
    {
        "q": "In C# asynchronous programming, which pair of keywords is used to write non-blocking asynchronous methods?",
        "a": "async and await",
        "b": "thread and run",
        "c": "defer and resolve",
        "d": "sync and wait",
        "key": "A"
    },
    {
        "q": "In C# Exception Handling, which block of code is guaranteed to run after try-catch for releasing resources?",
        "a": "when",
        "b": "finally",
        "c": "always",
        "d": "rescue",
        "key": "B"
    },
    {
        "q": "In C#, what is the purpose of the 'using' statement (or using declaration) when applied to an IDisposable object?",
        "a": "It imports namespaces only",
        "b": "It hides the object from the Garbage Collector",
        "c": "It guarantees that the object's Dispose() method is automatically called to free unmanaged resources",
        "d": "It makes the object globally accessible to all threads",
        "key": "C"
    },
    {
        "q": "In .NET Collections, which generic collection represents a fast hash table storing key-value pairs?",
        "a": "List<T>",
        "b": "Queue<T>",
        "c": "Array<T>",
        "d": "Dictionary<TKey, TValue>",
        "key": "D"
    },
    {
        "q": "In C# string handling, how do you perform string interpolation?",
        "a": "$\"Hello, {userName}\"",
        "b": "@\"Hello, %userName%\"",
        "c": "&\"Hello, {userName}\"",
        "d": "#\"Hello, [userName]\"",
        "key": "A"
    },
    {
        "q": "In .NET Core, what is the role of the Dependency Injection (DI) container built into ASP.NET Core?",
        "a": "To compile C# files into DLLs",
        "b": "To manage object lifetimes (Transient, Scoped, Singleton) and inject service dependencies automatically",
        "c": "To host web pages on Apache HTTP server",
        "d": "To generate SQL database schemas from memory",
        "key": "B"
    }
]

dotnet_core_fibs = [
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

# =====================================================================
# SEEDING EXECUTION FUNCTION
# =====================================================================
roles = [
    {"name": "Python Developer", "mcq_id": 9, "fib_id": 14, "core_mcqs": python_core_mcqs, "core_fibs": python_core_fibs},
    {"name": "Java Developer", "mcq_id": 10, "fib_id": 15, "core_mcqs": java_core_mcqs, "core_fibs": java_core_fibs},
    {"name": "Cyber Security", "mcq_id": 11, "fib_id": 16, "core_mcqs": cyber_core_mcqs, "core_fibs": cyber_core_fibs},
    {"name": "Data Analyst", "mcq_id": 12, "fib_id": 17, "core_mcqs": data_core_mcqs, "core_fibs": data_core_fibs},
    {"name": ".NET Developer", "mcq_id": 13, "fib_id": 18, "core_mcqs": dotnet_core_mcqs, "core_fibs": dotnet_core_fibs},
]

for r in roles:
    print(f"\nSeeding {r['name']} (MCQ ID: {r['mcq_id']}, FIB ID: {r['fib_id']})...")
    
    # Clean old answers and questions
    cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id IN (%s, %s));", (r['mcq_id'], r['fib_id']))
    cur.execute("DELETE FROM assessment_questions WHERE assessment_id IN (%s, %s);", (r['mcq_id'], r['fib_id']))
    
    # 1. Insert 20 MCQs for Round 1 (10 Core + 10 Linux/Docker/Git)
    all_mcqs = r['core_mcqs'] + common_tech_mcqs
    for q in all_mcqs:
        cur.execute("""
            INSERT INTO assessment_questions (assessment_id, question, option_a, option_b, option_c, option_d, correct_answer, question_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (r['mcq_id'], q["q"], q["a"], q["b"], q["c"], q["d"], q["key"], "mcq"))
    
    # 2. Insert 20 FIBs for Round 2 (10 Core + 10 Linux/Docker/Git)
    all_fibs = r['core_fibs'] + common_tech_fibs
    for q in all_fibs:
        cur.execute("""
            INSERT INTO assessment_questions (assessment_id, question, correct_answer, question_type)
            VALUES (%s, %s, %s, %s);
        """, (r['fib_id'], q["q"], q["a"], "fib"))
    
    print(f"[OK] {r['name']} seeded successfully: 20 MCQs (Round 1) + 20 FIBs (Round 2)!")

conn.commit()
conn.close()
print("\nALL 5 ROLES HAVE BEEN SEEDED WITH 10 CORE + 10 LINUX/DOCKER/GIT QUESTIONS ACROSS BOTH ROUNDS!")
