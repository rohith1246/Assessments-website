import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("=" * 60)
print("UPDATING DATA ANALYST ASSESSMENTS (100% PURE DATA ANALYST QUESTIONS)")
print("=" * 60)

# ==============================================================================
# 1. ROUND 1 MCQ: Drive ID 12 - 'Screening Test - Data Analyst' (20 Pure MCQs)
# ==============================================================================
cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id = 12);")
cur.execute("DELETE FROM assessment_questions WHERE assessment_id = 12;")

data_analyst_20_mcqs = [
    {
        "q": "In SQL, which clause is used to filter rows returned by a query BEFORE any GROUP BY aggregation is applied?",
        "a": "WHERE",
        "b": "HAVING",
        "c": "ORDER BY",
        "d": "LIMIT",
        "ans": "A"
    },
    {
        "q": "In SQL, which aggregate function calculates the average value of a numeric column across a group of rows?",
        "a": "SUM()",
        "b": "AVG()",
        "c": "MEDIAN()",
        "d": "COUNT()",
        "ans": "B"
    },
    {
        "q": "What is the primary difference between the 'WHERE' and 'HAVING' clauses in SQL?",
        "a": "WHERE works on columns with strings, while HAVING works only on numeric data types.",
        "b": "HAVING can only be used with subqueries, while WHERE cannot.",
        "c": "WHERE filters individual records before grouping, while HAVING filters aggregated results after GROUP BY.",
        "d": "WHERE and HAVING are completely interchangeable with zero performance difference.",
        "ans": "C"
    },
    {
        "q": "In relational SQL databases, which JOIN type returns all records from the left table, and matching records from the right table, filling with NULL where no match exists?",
        "a": "INNER JOIN",
        "b": "CROSS JOIN",
        "c": "FULL OUTER JOIN",
        "d": "LEFT JOIN",
        "ans": "D"
    },
    {
        "q": "In Python for Data Analysis, which library is the primary industry standard for tabular data manipulation and DataFrame structures?",
        "a": "Pandas",
        "b": "Matplotlib",
        "c": "Scikit-Learn",
        "d": "Requests",
        "ans": "A"
    },
    {
        "q": "In Pandas, which function is used to load and parse a comma-separated values file into a DataFrame?",
        "a": "pd.import_csv()",
        "b": "pd.read_csv()",
        "c": "pd.load_table()",
        "d": "pd.from_csv()",
        "ans": "B"
    },
    {
        "q": "In Pandas data preprocessing, which method is used to remove all rows that contain missing (NaN / null) values?",
        "a": "df.remove_nulls()",
        "b": "df.delete_na()",
        "c": "df.dropna()",
        "d": "df.fillna()",
        "ans": "C"
    },
    {
        "q": "In exploratory data analysis, which statistical chart is best suited for visualizing the frequency distribution of a continuous numeric variable?",
        "a": "Pie Chart",
        "b": "Scatter Plot",
        "c": "Heatmap",
        "d": "Histogram",
        "ans": "D"
    },
    {
        "q": "In SQL, which keyword is placed immediately after SELECT to eliminate duplicate rows and return unique combinations of values?",
        "a": "DISTINCT",
        "b": "UNIQUE",
        "c": "DIFFERENT",
        "d": "GROUP",
        "ans": "A"
    },
    {
        "q": "In Pandas, which method computes quick summary statistics (count, mean, std, min, 25%, 50%, 75%, max) for numeric columns?",
        "a": "df.summary()",
        "b": "df.describe()",
        "c": "df.info()",
        "d": "df.stats()",
        "ans": "B"
    },
    {
        "q": "In statistics for Data Analytics, what is the 'Median' of a numerical dataset?",
        "a": "The arithmetic average obtained by dividing the sum by total count.",
        "b": "The most frequently occurring value in the distribution.",
        "c": "The middle value separating the higher half from the lower half when data is sorted.",
        "d": "The difference between the maximum and minimum values in the dataset.",
        "ans": "C"
    },
    {
        "q": "In Pandas, what is the difference between `.loc[]` and `.iloc[]` indexers?",
        "a": ".loc[] is for multi-threading, while .iloc[] is for single-threaded processing.",
        "b": ".loc[] only works on Series, while .iloc[] works only on DataFrames.",
        "c": ".loc[] is used for deleting columns, while .iloc[] is used for inserting rows.",
        "d": ".loc[] is label-based indexing, whereas .iloc[] is integer position-based indexing.",
        "ans": "D"
    },
    {
        "q": "In SQL window functions, which function assigns a unique sequential integer to each row within a partition, starting at 1 with no gaps?",
        "a": "ROW_NUMBER()",
        "b": "RANK()",
        "c": "DENSE_RANK()",
        "d": "NTILE()",
        "ans": "A"
    },
    {
        "q": "In descriptive statistics, what does the Pearson Correlation Coefficient value of -0.92 between two numerical variables indicate?",
        "a": "No linear relationship between the two variables.",
        "b": "A strong negative linear relationship (as one variable increases, the other decreases).",
        "c": "A calculation error since correlation values must always be positive.",
        "d": "A perfect positive linear correlation between the variables.",
        "ans": "B"
    },
    {
        "q": "In data visualization, which plot is specifically designed to display the 5-number summary (Minimum, Q1, Median, Q3, Maximum) and identify outliers?",
        "a": "Line Chart",
        "b": "Donut Chart",
        "c": "Box Plot (Box-and-Whisker)",
        "d": "Bubble Chart",
        "ans": "C"
    },
    {
        "q": "In SQL, which clause is used to sort the query result set in ascending or descending order?",
        "a": "SORT BY",
        "b": "GROUP BY",
        "c": "ARRANGE BY",
        "d": "ORDER BY",
        "ans": "D"
    },
    {
        "q": "In data warehousing and Business Intelligence (BI), what does the ETL pipeline process stand for?",
        "a": "Extract, Transform, Load",
        "b": "Evaluate, Test, Log",
        "c": "Execute, Terminate, Launch",
        "d": "Export, Transfer, Leverage",
        "ans": "A"
    },
    {
        "q": "In Pandas, which method is used to replace missing (NaN) values with a specified default value or calculated mean/median?",
        "a": "df.replacena()",
        "b": "df.fillna()",
        "c": "df.impute()",
        "d": "df.set_default()",
        "ans": "B"
    },
    {
        "q": "In relational database modeling for data analytics, what defines a 'Star Schema'?",
        "a": "A fully normalized model where every dimension table is decomposed into multiple sub-tables.",
        "b": "A network graph schema where each table connects to every other table directly.",
        "c": "A central fact table containing numerical measures surrounded by denormalized dimension tables.",
        "d": "A single flat file without foreign keys or primary key constraints.",
        "ans": "C"
    },
    {
        "q": "In SQL, which operator is used in a WHERE clause to search for a specified pattern in a column using wildcards like '%' and '_'?",
        "a": "MATCHES",
        "b": "CONTAINS",
        "c": "EQUALS",
        "d": "LIKE",
        "ans": "D"
    }
]

for idx, q in enumerate(data_analyst_20_mcqs, 1):
    cur.execute("""
        INSERT INTO assessment_questions (assessment_id, question, option_a, option_b, option_c, option_d, correct_answer, question_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'mcq');
    """, (12, q["q"], q["a"], q["b"], q["c"], q["d"], q["ans"]))

print(f"[OK] Successfully seeded 20 100% Pure Data Analyst MCQs for Drive 12 (Screening Test - Data Analyst)!")


# ==============================================================================
# 2. ROUND 2 FIB: Drive ID 17 - 'Technical Round 2 - Data Analyst' (20 Pure FIBs)
# ==============================================================================
cur.execute("DELETE FROM assessment_answers WHERE question_id IN (SELECT id FROM assessment_questions WHERE assessment_id = 17);")
cur.execute("DELETE FROM assessment_questions WHERE assessment_id = 17;")

data_analyst_20_fibs = [
    {
        "q": "In Structured Query Language (SQL), which primary statement begins every data retrieval query to specify columns to be fetched?",
        "a": "SELECT"
    },
    {
        "q": "In SQL queries containing aggregated metrics, which specific clause is used to filter grouped results after GROUP BY is applied?",
        "a": "HAVING"
    },
    {
        "q": "In SQL query execution order, which clause filters individual raw table records before any grouping or aggregation takes place?",
        "a": "WHERE"
    },
    {
        "q": "In SQL queries, which clause is used to arrange identical data rows into summary rows (e.g. 'SELECT Dept, COUNT(*) FROM Emp _____ BY Dept;')?",
        "a": "GROUP|GROUP BY"
    },
    {
        "q": "In SQL data retrieval, which clause is used to sort the returned result set in ascending or descending sequence?",
        "a": "ORDER BY|ORDER"
    },
    {
        "q": "In SQL queries, which keyword placed right after SELECT eliminates duplicate rows and returns only unique values?",
        "a": "DISTINCT"
    },
    {
        "q": "In relational SQL joins, which join returns all rows from the left table and matched rows from the right table (filling unmatched with NULL)?",
        "a": "LEFT JOIN|LEFT"
    },
    {
        "q": "In SQL aggregate functions, which function returns the total number of rows matching the query criteria (e.g. 'SELECT ______(*) FROM Employees;')?",
        "a": "COUNT"
    },
    {
        "q": "In SQL window functions, which function assigns a consecutive rank number starting from 1 to each row without any duplicate ties or gaps?",
        "a": "ROW_NUMBER|ROW_NUMBER()"
    },
    {
        "q": "In SQL WHERE conditions, which operator performs pattern matching using the '%' wildcard character?",
        "a": "LIKE"
    },
    {
        "q": "In Python Pandas, what is the name of the primary two-dimensional, size-mutable tabular data structure with labeled axes (rows and columns)?",
        "a": "DataFrame|pd.DataFrame"
    },
    {
        "q": "In Python Pandas, what is the name of the one-dimensional labeled array data structure capable of holding any data type?",
        "a": "Series|pd.Series"
    },
    {
        "q": "In Pandas data ingestion, which function is executed to read and parse comma-separated table files into a DataFrame?",
        "a": "read_csv|pd.read_csv"
    },
    {
        "q": "In Pandas data cleaning, which method is called on a DataFrame to replace missing (NaN / null) values with a default or imputed value?",
        "a": "fillna|df.fillna"
    },
    {
        "q": "In Pandas data preprocessing, which method is called on a DataFrame to drop and remove rows containing missing (NaN) values?",
        "a": "dropna|df.dropna"
    },
    {
        "q": "In Pandas exploratory analysis, which method automatically computes summary statistics (count, mean, std, min, quartiles, max) for numeric columns?",
        "a": "describe|df.describe"
    },
    {
        "q": "In Pandas DataFrame indexing, which property indexer is used strictly for integer-position based selection (e.g. df._____ [0:5, 0:3])?",
        "a": "iloc|.iloc|df.iloc"
    },
    {
        "q": "In descriptive statistics, which measure of central tendency represents the middle value of an ordered dataset, making it robust against extreme outliers?",
        "a": "Median"
    },
    {
        "q": "In exploratory data visualization, which standard chart type displays the 5-number summary (Min, Q1, Median, Q3, Max) and highlights outlier points?",
        "a": "Box Plot|Boxplot|Box-and-Whisker|Box"
    },
    {
        "q": "In statistical analysis, what is the term for the metric that measures the strength and direction of a linear relationship between two continuous variables (ranging from -1 to +1)?",
        "a": "Correlation|Correlation Coefficient|Pearson Correlation"
    }
]

for idx, q in enumerate(data_analyst_20_fibs, 1):
    cur.execute("""
        INSERT INTO assessment_questions (assessment_id, question, correct_answer, question_type)
        VALUES (%s, %s, %s, 'fib');
    """, (17, q["q"], q["a"]))

print(f"[OK] Successfully seeded 20 100% Pure Data Analyst FIBs for Drive 17 (Technical Round 2 - Data Analyst)!")

conn.commit()
conn.close()
print("=" * 60)
print("DATABASE COMMITTED SUCCESSFULLY!")
print("=" * 60)
