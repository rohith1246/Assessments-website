"""
seed_data_analyst_assessment.py
Creates and populates the 'Screening Test - Data Analyst' assessment with
20 Advanced, Hard-Level Data Analytics & Data Engineering MCQs:
- Advanced SQL (Window frames, NULL semantics in NOT IN, Dense Rank, Self joins, CUBE/ROLLUP, Recursive CTEs)
- Python Pandas & NumPy (Transform vs Apply, SettingWithCopyWarning, Vectorization, Cartesian joins)
- Applied Statistics & Probability (Bayes theorem, Hypothesis testing p-values, Simpson's paradox, Power analysis, Poisson distribution, Multicollinearity/VIF)
- Data Architecture & Experimentation (SCD Type 2, Feature transformations, Guardrail metrics)

Configuration: 20 Questions, 20 Minutes, 75% Cutoff, Balanced A/B/C/D keys.
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATA_ANALYST_QUESTIONS = [
    # ── ADVANCED SQL, DATA MANIPULATION & STATISTICS (20 Hard Questions) ──
    (
        "Q1. Consider the query executed on a daily sales table (Day 1: 100, Day 2: 200, Day 3: 300, Day 4: 600):\n\nSELECT sale_date, amount, AVG(amount) OVER (\n    ORDER BY sale_date \n    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n) as moving_avg FROM daily_sales;\n\nWhat is the value of 'moving_avg' on Day 4?",
        "300.00",
        "366.67",
        "450.00",
        "600.00",
        "B"
    ),
    (
        "Q2. Given table A (id INT) containing [1, 2, 3] and table B (id INT) containing [2, NULL], what is the output of:\n\nSELECT * FROM A WHERE id NOT IN (SELECT id FROM B);",
        "[1, 3]",
        "[1, 2, 3]",
        "Empty result set (0 rows returned)",
        "NULL",
        "C"
    ),
    (
        "Q3. In SQL analytics over a score dataset [100, 95, 95, 90, 85], what integer value will 'DENSE_RANK() OVER (ORDER BY score DESC)' assign to the score 90?",
        "4",
        "2",
        "5",
        "3",
        "D"
    ),
    (
        "Q4. A rare disease affects 0.1% of a population. A diagnostic test has 99% Sensitivity (True Positive Rate) and 95% Specificity (True Negative Rate). If a randomly selected individual tests positive, what is the approximate probability (Bayes' Rule) that they actually have the disease?",
        "~1.94%",
        "~95.0%",
        "~99.0%",
        "~50.0%",
        "A"
    ),
    (
        "Q5. You have a DataFrame 'df' with columns ['user_id', 'order_amount']. You want to append a new column 'user_avg_spend' containing each user's mean spending repeated across all their original rows without changing the DataFrame index or collapsing rows. Which operation is most optimal and idiomatic?",
        "df['user_avg_spend'] = df.groupby('user_id')['order_amount'].mean()",
        "df['user_avg_spend'] = df.groupby('user_id')['order_amount'].transform('mean')",
        "df['user_avg_spend'] = df.apply(lambda x: df[df['user_id']==x['user_id']]['order_amount'].mean())",
        "df['user_avg_spend'] = df.groupby('user_id')['order_amount'].agg('mean').to_frame()",
        "B"
    ),
    (
        "Q6. In an A/B test with 50,000 visitors per variant, the analyst obtains a p-value of 0.03 for conversion difference under alpha = 0.05. What is the precise statistical interpretation of this p-value?",
        "There is a 97% probability that Variant B is truly superior to Variant A in production",
        "There is a 3% probability that the null hypothesis is true",
        "Assuming the null hypothesis of no difference is true, the probability of observing a difference at least as extreme as measured is 3%",
        "The conversion rate will increase revenue by at least 3% in all future quarters",
        "C"
    ),
    (
        "Q7. In pandas, why does 'sub_df = df[df[\"category\"] == \"Tech\"]; sub_df[\"discount\"] = 0.15' trigger a 'SettingWithCopyWarning', and what is the proper fix?",
        "The dataframe is too large for memory; call df.dropna() first",
        "'Tech' is a reserved keyword in pandas",
        "Assigning floating point numbers requires explicit casting via float()",
        "sub_df may be a view on the original DataFrame rather than an isolated copy; use sub_df = df[df['category'] == 'Tech'].copy()",
        "D"
    ),
    (
        "Q8. Given an 'employees' table with columns (emp_id, emp_name, salary, manager_id), which SQL query correctly returns all employees whose salary exceeds their direct manager's salary?",
        "SELECT e.emp_name FROM employees e JOIN employees m ON e.manager_id = m.emp_id WHERE e.salary > m.salary;",
        "SELECT e.emp_name FROM employees e WHERE e.salary > (SELECT AVG(salary) FROM employees);",
        "SELECT e.emp_name FROM employees e LEFT JOIN employees m ON e.emp_id = m.manager_id WHERE e.salary > m.salary;",
        "SELECT e.emp_name FROM employees e CROSS JOIN employees m WHERE e.salary > m.salary;",
        "A"
    ),
    (
        "Q9. What statistical phenomenon describes a scenario where an apparent trend or correlation appears within several disaggregated groups of data, but reverses or disappears when the groups are combined?",
        "Berkson's Bias",
        "Simpson's Paradox",
        "Central Limit Convergence",
        "Hawthorne Effect",
        "B"
    ),
    (
        "Q10. For a DataFrame containing 10 million transaction amounts, what is the most performant way to compute 'log_amount = np.log1p(amount)' avoiding Python GIL and iteration overhead?",
        "df['amount'].apply(lambda x: math.log(x + 1))",
        "[math.log(x + 1) for x in df['amount']]",
        "np.log1p(df['amount'].values)",
        "for idx, row in df.iterrows(): row['amount'] = math.log1p(row['amount'])",
        "C"
    ),
    (
        "Q11. In Kimball dimensional data warehousing, how does a Slowly Changing Dimension Type 2 (SCD Type 2) maintain historical accuracy when an attribute changes?",
        "By overwriting the existing attribute in place without preserving historical values",
        "By dropping and rebuilding the dimension table daily",
        "By appending a new column for every historical change",
        "By inserting a new record with effective date ranges (start_date, end_date) and an is_current flag to preserve historical lineage",
        "D"
    ),
    (
        "Q12. In statistical hypothesis testing and power analysis, if an experimenter increases the sample size N while keeping significance level alpha constant, what occurs to Statistical Power (1 - beta) and Type II Error (beta)?",
        "Statistical Power increases and Type II Error (beta) decreases",
        "Statistical Power decreases and Type I Error (alpha) increases",
        "Both Statistical Power and Type II Error remain unchanged",
        "Type II Error increases to 1.0",
        "A"
    ),
    (
        "Q13. When querying 50 million order rows in a cloud data warehouse, which construct calculates a cumulative running total of revenue partitioned by customer_id and ordered by order_date with optimal single-pass execution?",
        "SELECT (SELECT SUM(o2.revenue) FROM orders o2 WHERE o2.customer_id = o1.customer_id AND o2.order_date <= o1.order_date) FROM orders o1",
        "SUM(revenue) OVER (PARTITION BY customer_id ORDER BY order_date ROWS UNBOUNDED PRECEDING)",
        "orders o1 JOIN orders o2 ON o1.customer_id = o2.customer_id GROUP BY o1.id",
        "Repeated UNION ALL queries across day partitions",
        "B"
    ),
    (
        "Q14. In predictive analytics and regression modeling, what transformation is standardly applied to compress heavily right-skewed financial data containing long positive tails?",
        "Min-Max scaling to [0, 1] without distributional adjustments",
        "Squaring the feature values (x^2)",
        "Logarithmic transformation (log(x + 1)) or Box-Cox transformation",
        "Multiplying values by feature variance",
        "C"
    ),
    (
        "Q15. In SQL multidimensional aggregations across (region, department, year), what is the key difference between 'GROUP BY CUBE(region, department, year)' and 'GROUP BY ROLLUP'?",
        "CUBE only aggregates the highest hierarchy level (region)",
        "CUBE excludes NULL values from generated subtotals",
        "CUBE generates subtotals for all 2^3 = 8 possible combination subsets of dimensions, whereas ROLLUP computes only hierarchical prefix subsets",
        "CUBE runs only on MySQL databases",
        "C"
    ),
    (
        "Q16. When performing 'pd.merge(df1, df2, on=\"customer_id\", how=\"inner\")' where df1 contains 5 rows with customer_id=101 and df2 contains 4 rows with customer_id=101, how many rows for customer_id=101 will exist in the merged DataFrame?",
        "1 row",
        "9 rows",
        "5 rows",
        "20 rows (Cartesian product 5 * 4)",
        "D"
    ),
    (
        "Q17. In multiple linear regression modeling, which diagnostic metric is calculated to evaluate severe multicollinearity among independent predictor variables?",
        "Variance Inflation Factor (VIF), where VIF > 5-10 indicates problematic collinearity",
        "Durbin-Watson serial correlation statistic",
        "Silhouette clustering coefficient",
        "Confusion Matrix Accuracy score",
        "A"
    ),
    (
        "Q18. If customer incoming calls occur independently at a constant average rate of lambda = 6 calls per minute, what discrete probability distribution models the exact probability of receiving k calls in a given minute?",
        "Uniform distribution",
        "Poisson distribution: P(X=k) = (lambda^k * e^-lambda) / k!",
        "Beta distribution",
        "Cauchy distribution",
        "B"
    ),
    (
        "Q19. In SQL Recursive Common Table Expressions (e.g., WITH RECURSIVE hierarchy AS (...)), which operator is mandatory to union the base anchor member query with the recursive member query?",
        "INTERSECT",
        "EXCEPT",
        "CROSS APPLY",
        "UNION or UNION ALL",
        "D"
    ),
    (
        "Q20. In enterprise A/B experimentation, why do data teams monitor 'Guardrail Metrics' (e.g., page load latency, unsubscribe rate) alongside the primary KPI?",
        "To detect unintended operational regressions, user friction, or system degradation caused by a variant that seemingly improves the primary KPI",
        "To replace standard p-value statistical testing with heuristics",
        "To artificially manipulate sample sizes and statistical significance",
        "To bypass analytics tracking privacy consent laws",
        "A"
    )
]

def seed_data_analyst_test():
    uri = os.environ.get('DATABASE_URL', '')
    if '&channel_binding=' in uri:
        uri = uri.split('&channel_binding=')[0]

    print("Connecting to Neon database...", flush=True)
    conn = psycopg2.connect(uri, connect_timeout=15)
    cur = conn.cursor()

    title = "Screening Test - Data Analyst"
    print(f"Syncing sequences and creating '{title}'...", flush=True)
    cur.execute("SELECT setval('assessment_drives_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_drives));")
    cur.execute("SELECT setval('assessment_questions_id_seq', (SELECT COALESCE(MAX(id), 1) FROM assessment_questions));")
    conn.commit()

    # Clean up previous instance
    cur.execute("SELECT id FROM assessment_drives WHERE title = %s;", (title,))
    existing = cur.fetchall()
    for (eid,) in existing:
        print(f"  Cleaning up previous assessment ID {eid}...", flush=True)
        cur.execute("DELETE FROM assessment_answers WHERE submission_id IN (SELECT id FROM assessment_submissions WHERE assessment_id = %s);", (eid,))
        cur.execute("DELETE FROM assessment_submissions WHERE assessment_id = %s;", (eid,))
        cur.execute("DELETE FROM assessment_questions WHERE assessment_id = %s;", (eid,))
        cur.execute("DELETE FROM assessment_drives WHERE id = %s;", (eid,))
    conn.commit()

    # Insert Drive
    cur.execute("""
        INSERT INTO assessment_drives (title, description, duration, pass_percentage, status, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        RETURNING id;
    """, (
        title,
        "Advanced Technical Screening for Data Analysts & Analytics Engineers. Covers Advanced SQL (Window frames, NULL handling, Dense Ranking, CTEs, CUBE/ROLLUP), Python Pandas & Vectorization, Applied Statistics (Bayes Rule, Power Analysis, Simpson's Paradox, Poisson, VIF), Dimensional Modeling (SCD Type 2), and Experimentation Guardrail Metrics. Contains 20 Hard MCQs. Time limit: 20 minutes.",
        20,
        75.0,
        "active"
    ))
    drive_id = cur.fetchone()[0]
    print(f"Created Assessment ID: {drive_id} for '{title}'", flush=True)

    # Insert Questions
    for q, a, b, c, d, ans in DATA_ANALYST_QUESTIONS:
        cur.execute("""
            INSERT INTO assessment_questions (assessment_id, question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (drive_id, q, a, b, c, d, ans))
    conn.commit()
    print(f"Successfully inserted {len(DATA_ANALYST_QUESTIONS)} questions (5 A, 5 B, 5 C, 5 D balanced).", flush=True)

    # Summary
    cur.execute("SELECT id, title, duration, pass_percentage, status, (SELECT count(*) FROM assessment_questions WHERE assessment_id=assessment_drives.id) as qcount FROM assessment_drives ORDER BY id;")
    rows = cur.fetchall()
    print("\n================ ACTIVE ASSESSMENTS IN DATABASE ================", flush=True)
    for r in rows:
        print(f"ID: {r[0]} | Title: {r[1]} | Pass: {r[3]}% | Status: {r[4]} | Questions: {r[5]}", flush=True)

    conn.close()

if __name__ == '__main__':
    seed_data_analyst_test()
