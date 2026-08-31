import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Updating Screening Test - Java Developer (ID: 10)...")

# Delete old questions for Assessment ID 10
cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id = 10);")
cur.execute("DELETE FROM assessment_questions WHERE assessment_id = 10;")

# 20 MCQs: 10 Core Java + 10 Project & Enterprise Tech Stack (5 A, 5 B, 5 C, 5 D)
mcq_questions = [
    # ── PART 1: 10 CORE & ADVANCED JAVA QUESTIONS ──
    {
        "q": "In Java memory management, where are local primitive variables and object reference variables declared inside a method allocated?",
        "a": "In the thread-specific Call Stack memory",
        "b": "In the shared Heap memory Young Generation",
        "c": "In the Metaspace class metadata area",
        "d": "In the Native Method Stack area",
        "key": "A",
        "type": "mcq"
    },
    {
        "q": "In Java multi-threading, what is the primary purpose of the 'volatile' keyword when applied to a shared class field?",
        "a": "It acquires an exclusive monitor lock on the object before reading or writing",
        "b": "It ensures CPU cache coherency and visibility of writes across all threads without mutual exclusion",
        "c": "It prevents the object from being garbage collected while the thread is active",
        "d": "It forces the variable to be serialized and stored on the disk",
        "key": "B",
        "type": "mcq"
    },
    {
        "q": "Consider Java Collections: How does ConcurrentHashMap achieve high-throughput thread safety compared to Collections.synchronizedMap()?",
        "a": "It uses a global reentrant lock that locks the entire table during read operations",
        "b": "It converts all keys and values into immutable read-only records",
        "c": "It uses fine-grained bucket-level locking with CAS (Compare-And-Swap) and synchronized node heads",
        "d": "It runs each read and write operation inside an isolated background daemon thread",
        "key": "C",
        "type": "mcq"
    },
    {
        "q": "In Java 8+ Stream API, which intermediate operation is designed to transform each element into a Stream and flatten multiple nested collections into a single output Stream?",
        "a": "map()",
        "b": "reduce()",
        "c": "collect()",
        "d": "flatMap()",
        "key": "D",
        "type": "mcq"
    },
    {
        "q": "Why is 'String' immutable in Java, and what major performance and security benefit does this design provide?",
        "a": "It enables String Pool caching, thread-safety, and secure usage as Map keys and network credentials",
        "b": "It prevents any substring or concatenation operations from allocating heap memory",
        "c": "It allows the JVM to execute Java code without requiring a Garbage Collector",
        "d": "It eliminates the need for constructors and heap memory pointers in C++ JVM code",
        "key": "A",
        "type": "mcq"
    },
    {
        "q": "What is the key difference between an 'abstract class' and an 'interface' with default methods in Java 8+?",
        "a": "Interfaces can maintain instance state fields, whereas abstract classes cannot",
        "b": "A class can implement multiple interfaces but can only extend a single abstract class (single class inheritance)",
        "c": "Abstract classes cannot have constructors, while interfaces require a default no-arg constructor",
        "d": "Default methods in interfaces cannot execute runtime Java code logic",
        "key": "B",
        "type": "mcq"
    },
    {
        "q": "In Java Exception Handling, which statement accurately distinguishes 'Checked' exceptions from 'Unchecked' exceptions?",
        "a": "Unchecked exceptions inherit from Throwable directly, while Checked inherit from Exception",
        "b": "Checked exceptions occur only in multi-threaded code during deadlock conditions",
        "c": "Checked exceptions are verified at compile-time (must be declared/handled), whereas Unchecked exceptions inherit from RuntimeException",
        "d": "Unchecked exceptions are automatically resolved by the JVM without terminating the execution",
        "key": "C",
        "type": "mcq"
    },
    {
        "q": "In Java 17+, which feature allows a developer to explicitly declare and restrict which specific subclasses are permitted to extend a parent class?",
        "a": "Virtual Classes",
        "b": "Module Descriptors",
        "c": "Type Annotations",
        "d": "Sealed Classes with 'permits' clause",
        "key": "D",
        "type": "mcq"
    },
    {
        "q": "What occurs during Java Generics 'Type Erasure' by the Java compiler?",
        "a": "Generic type parameters (like <T>) are replaced with raw types (like Object) or bounding classes in the compiled bytecode",
        "b": "All runtime objects are converted into JSON strings before memory allocation",
        "c": "The JVM duplicates bytecode for every unique type argument instantiated",
        "d": "The JVM disables type casting checks during reflection calls",
        "key": "A",
        "type": "mcq"
    },
    {
        "q": "In Java 21+, what are 'Virtual Threads' (Project Loom) and how do they differ from traditional Platform Threads?",
        "a": "They are simulated threads that run only inside web browser WebAssembly engines",
        "b": "They are lightweight, JVM-managed user-mode threads that do not maintain 1:1 binding to OS kernel threads, enabling massive concurrency",
        "c": "They are hardware-level threads that bypass CPU core scheduling using GPU cores",
        "d": "They are synchronized threads that automatically prevent all race conditions without locks",
        "key": "B",
        "type": "mcq"
    },

    # ── PART 2: 10 PROJECT & ENTERPRISE TECH STACK QUESTIONS ──
    {
        "q": "In a Spring Boot enterprise project, what is the role of the '@RestController' annotation?",
        "a": "It defines a database repository bean that automatically executes SQL queries",
        "b": "It configures an OAuth2 authentication server for microservices tokens",
        "c": "It combines '@Controller' and '@ResponseBody', automatically serializing Java return objects directly into JSON/XML HTTP responses",
        "d": "It marks the class as a scheduled background cron job worker",
        "key": "C",
        "type": "mcq"
    },
    {
        "q": "In Spring Framework / Spring Boot, which annotation is used for Dependency Injection (DI) to automatically inject a collaborator bean by type?",
        "a": "@Entity",
        "b": "@Service",
        "c": "@Repository",
        "d": "@Autowired",
        "key": "D",
        "type": "mcq"
    },
    {
        "q": "In Spring Boot & Hibernate/JPA, what is the well-known 'N+1 Select Problem' and how is it typically resolved?",
        "a": "Executing 1 query for a parent list and N individual queries for each child relation; resolved using 'JOIN FETCH' or '@EntityGraph'",
        "b": "Having N+1 threads attempting to write to the same database row simultaneously; resolved by table locking",
        "c": "Allocating N+1 database connections in HikariCP; resolved by reducing maxPoolSize",
        "d": "Inserting N+1 duplicate records due to missing unique index constraints",
        "key": "A",
        "type": "mcq"
    },
    {
        "q": "In enterprise Spring Boot applications, what is the default and recommended database Connection Pool library used for high-performance connection management?",
        "a": "Commons DBCP 1.4",
        "b": "HikariCP",
        "c": "C3P0 Pool",
        "d": "Tomcat JDBC Pool",
        "key": "B",
        "type": "mcq"
    },
    {
        "q": "In Spring Data JPA, what does placing the '@Transactional' annotation on a service method ensure during database operations?",
        "a": "It exports the method parameters to a remote Kafka cluster topic",
        "b": "It caches the query result in Redis distributed cache for 24 hours",
        "c": "It executes all database operations within an ACID transaction, automatically rolling back on unchecked exceptions (RuntimeException)",
        "d": "It converts all synchronous SQL queries into asynchronous non-blocking queries",
        "key": "C",
        "type": "mcq"
    },
    {
        "q": "In a modern Spring Boot Microservices architecture, what is the primary function of an 'API Gateway' (e.g., Spring Cloud Gateway)?",
        "a": "To store relational database tables in memory",
        "b": "To compile Java source code into Docker container images",
        "c": "To run unit test suites before production deployment",
        "d": "To act as a single entry point providing reverse proxy routing, load balancing, security filtering, rate limiting, and SSL termination",
        "key": "D",
        "type": "mcq"
    },
    {
        "q": "In Maven-based Java projects, what is the purpose of the 'pom.xml' file?",
        "a": "It is the Project Object Model configuration declaring dependencies, plugins, project coordinates (groupId, artifactId), and build lifecycle",
        "b": "It contains the compiled binary bytecode of the Java application",
        "c": "It stores database user credentials and SSL certificates for production",
        "d": "It serves as the main startup class containing the JVM entry point 'public static void main'",
        "key": "A",
        "type": "mcq"
    },
    {
        "q": "In Docker containerization for a Java Spring Boot microservice, which instruction in a 'Dockerfile' specifies the command executed to run the packaged JAR file?",
        "a": "FROM openjdk:17-slim",
        "b": "ENTRYPOINT [\"java\", \"-jar\", \"app.jar\"]",
        "c": "EXPOSE 8080",
        "d": "WORKDIR /workspace",
        "key": "B",
        "type": "mcq"
    },
    {
        "q": "In Java backend projects, what is the core role of Apache Kafka in an event-driven architecture?",
        "a": "It acts as a relational database replacing PostgreSQL and MySQL tables",
        "b": "It is an HTML template rendering engine used for server-side JSP pages",
        "c": "It is a distributed, fault-tolerant event streaming platform providing high-throughput publish-subscribe message queues between microservices",
        "d": "It compiles Java bytecode into native machine code binaries",
        "key": "C",
        "type": "mcq"
    },
    {
        "q": "In Java unit testing with JUnit 5 and Mockito, how do you verify that a service method accurately invoked a dependent repository method?",
        "a": "By checking the operating system CPU usage graph",
        "b": "By restarting the Spring Boot application context",
        "c": "By querying the production database logs manually",
        "d": "Using 'Mockito.verify(repositoryMock, Mockito.times(1)).save(any())'",
        "key": "D",
        "type": "mcq"
    }
]

for q in mcq_questions:
    cur.execute("""
        INSERT INTO assessment_questions (assessment_id, question, option_a, option_b, option_c, option_d, correct_answer, question_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (10, q["q"], q["a"], q["b"], q["c"], q["d"], q["key"], "mcq"))

print("Screening Test - Java Developer (ID: 10) updated successfully!")

# ─────────────────────────────────────────────────────────────
# UPDATE TECHNICAL ROUND 2 - JAVA DEVELOPER (ID: 15) FIB
# ─────────────────────────────────────────────────────────────
print("\nUpdating Technical Round 2 - Java Developer (ID: 15)...")

cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id = 15);")
cur.execute("DELETE FROM assessment_questions WHERE assessment_id = 15;")

fib_questions = [
    # ── 10 CORE & ADVANCED JAVA FIB QUESTIONS ──
    {
        "q": "In the Java Virtual Machine (JVM) memory architecture, all class instances and arrays are allocated in the shared _____ memory area.",
        "a": "Heap|Heap Memory"
    },
    {
        "q": "In Java concurrency, the keyword that guarantees memory visibility so changes written by one thread are immediately visible to all other threads is _____.",
        "a": "volatile"
    },
    {
        "q": "In Java Generics, the compile-time mechanism that removes generic type parameters (like <T>) and inserts appropriate casts in bytecode is Type _____.",
        "a": "Erasure"
    },
    {
        "q": "In the JVM Garbage Collection subsystem, the low-latency, low-pause garbage collector introduced for multi-gigabyte/terabyte heaps is _____.",
        "a": "ZGC|Z|G1GC"
    },
    {
        "q": "In Java, to prevent a class from being subclassed or a method from being overridden, it must be declared with the _____ modifier keyword.",
        "a": "final"
    },
    {
        "q": "In Java 8+ Streams, the intermediate operation used to transform each element into a stream and flatten multiple nested collections into a single stream is _____.",
        "a": "flatMap"
    },
    {
        "q": "In 'java.util.concurrent', the thread-safe hash map that utilizes fine-grained lock striping and CAS for concurrent reads and writes is _____HashMap.",
        "a": "Concurrent"
    },
    {
        "q": "In Java 14+, the keyword used to declare a compact, immutable data-carrier class that automatically generates constructors, getters, equals, and hashCode is _____.",
        "a": "record"
    },
    {
        "q": "In Project Loom (Java 21+), lightweight user-mode threads managed directly by the JVM runtime rather than 1:1 OS kernel threads are called _____ Threads.",
        "a": "Virtual"
    },
    {
        "q": "In Java 17+, to declare a class that strictly restricts which specific subclasses are allowed to extend it using the 'permits' clause, use the keyword _____.",
        "a": "sealed"
    },

    # ── 10 PROJECT & ENTERPRISE TECH STACK FIB QUESTIONS ──
    {
        "q": "In Spring Boot enterprise applications, the annotation that marks a class as a RESTful controller returning serialized JSON responses is @_____Controller.",
        "a": "Rest"
    },
    {
        "q": "In Spring Framework Dependency Injection (DI), the core annotation used to automatically inject collaborating beans by type is @_____.",
        "a": "Autowired"
    },
    {
        "q": "In Spring Boot and Spring Data JPA, to execute service methods within an atomic database transaction with automatic rollback on error, use the @_____ annotation.",
        "a": "Transactional"
    },
    {
        "q": "In Spring Boot projects, the default high-performance database connection pooling library managed under the hood is _____CP.",
        "a": "Hikari"
    },
    {
        "q": "In Hibernate ORM, the performance issue where querying N child entities causes N additional database SELECT queries is known as the N+_____ problem.",
        "a": "1|One"
    },
    {
        "q": "In Maven Java projects, the XML configuration file that manages project dependencies, plugins, and build lifecycle is named _____.",
        "a": "pom.xml|pom"
    },
    {
        "q": "In secure Spring Security enterprise REST APIs, stateless user authorization is typically verified using a JSON Web Token, abbreviated as _____.",
        "a": "JWT"
    },
    {
        "q": "In Dockerizing Java Spring Boot microservices, the Dockerfile instruction that defines the default command executed when the container starts is _____.",
        "a": "ENTRYPOINT|CMD"
    },
    {
        "q": "In modern distributed Java microservices architectures, the distributed event-streaming and message broker platform developed by Apache is Apache _____.",
        "a": "Kafka"
    },
    {
        "q": "In Java unit testing using the Mockito framework, the annotation placed on a field to create a mock dependency instance is @_____.",
        "a": "Mock"
    }
]

for q in fib_questions:
    cur.execute("""
        INSERT INTO assessment_questions (assessment_id, question, correct_answer, question_type)
        VALUES (%s, %s, %s, %s);
    """, (15, q["q"], q["a"], "fib"))

print("Technical Round 2 - Java Developer (ID: 15) updated successfully!")

conn.commit()
conn.close()
print("ALL JAVA ASSESSMENTS UPDATED SUCCESSFULLY: 10 Core Java + 10 Project Tech Stack!")
