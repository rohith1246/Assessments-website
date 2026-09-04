import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.environ.get('DATABASE_URL', '').split('&channel_binding=')[0]
conn = psycopg2.connect(uri)
cur = conn.cursor()

print("Setting up Technical Round 3 (Coding Sandbox & Live Execution) for all roles...")

# Define 6 Technical Round 3 Assessment Drives
drives_r3 = [
    {"id": 20, "title": "Technical Round 3 - Python Developer", "desc": "Live Coding & Algorithm Execution in Python 3.11 with Real-Time Test Cases.", "duration": 45, "cutoff": 70},
    {"id": 21, "title": "Technical Round 3 - Java Developer", "desc": "Live Coding & Algorithm Execution in Java 17 with Real-Time Test Cases.", "duration": 45, "cutoff": 70},
    {"id": 22, "title": "Technical Round 3 - Cyber Security", "desc": "Security Scripting, String Manipulation, and Packet Validation Sandbox.", "duration": 45, "cutoff": 70},
    {"id": 23, "title": "Technical Round 3 - Data Analyst", "desc": "Data Parsing, Aggregation Metrics, and Frequency Algorithms Sandbox.", "duration": 45, "cutoff": 70},
    {"id": 24, "title": "Technical Round 3 - .NET Developer", "desc": "Data Structures, Stack Evaluation, and Matrix Algorithms Sandbox.", "duration": 45, "cutoff": 70},
    {"id": 25, "title": "Technical Round 3 - Full Stack Developer", "desc": "Full Stack Algorithmic Problem Solving & Data Formatting Sandbox.", "duration": 45, "cutoff": 70},
]

for d in drives_r3:
    cur.execute("""
        INSERT INTO assessment_drives (id, title, description, duration, pass_percentage, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (id) DO UPDATE 
        SET title = EXCLUDED.title, description = EXCLUDED.description, duration = EXCLUDED.duration, pass_percentage = EXCLUDED.pass_percentage, status = 'active';
    """, (d["id"], d["title"], d["desc"], d["duration"], d["cutoff"], "active"))
    print(f"[OK] Assessment Drive Ready: {d['title']} (ID: {d['id']})")

# Clean old coding problems for these drives
drive_ids_tuple = tuple(d["id"] for d in drives_r3)
cur.execute("DELETE FROM assessment_coding_testcases WHERE problem_id IN (SELECT id FROM assessment_coding_problems WHERE assessment_id IN %s);", (drive_ids_tuple,))
cur.execute("DELETE FROM assessment_coding_submissions WHERE problem_id IN (SELECT id FROM assessment_coding_problems WHERE assessment_id IN %s);", (drive_ids_tuple,))
cur.execute("DELETE FROM assessment_coding_problems WHERE assessment_id IN %s;", (drive_ids_tuple,))

# ── CODING PROBLEMS SPECIFICATIONS ──

# Helper for standard starter code
def make_starters(func_name, py_body, java_body, cpp_body, js_body):
    return {
        "python": f"# Write your solution below\nimport sys\n\ndef solution():\n    lines = sys.stdin.read().splitlines()\n    if not lines:\n        return\n    {py_body}\n\nif __name__ == '__main__':\n    solution()\n",
        "java": f"import java.util.*;\nimport java.io.*;\n\npublic class Solution {{\n    public static void main(String[] args) throws Exception {{\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextLine()) return;\n        {java_body}\n    }}\n}}\n",
        "cpp": f"#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\n\nint main() {{\n    {cpp_body}\n    return 0;\n}}\n",
        "javascript": f"const fs = require('fs');\nconst input = fs.readFileSync('/dev/stdin', 'utf-8').trim().split('\\n');\n\nfunction solution() {{\n    if (!input || input.length === 0 || input[0] === '') return;\n    {js_body}\n}}\nsolution();\n"
    }

problems_by_drive = {
    # ── PYTHON TRACK (ID: 20) ──
    20: [
        {
            "title": "Two Sum (Pair Matching Target Sum)",
            "difficulty": "Easy",
            "points": 100,
            "statement": "Given a space-separated array of integers and a target sum on the second line, find the zero-based indices of the two numbers such that they add up to the target.\n\nOutput the two indices separated by a space in ascending order. If no pair exists, output -1.",
            "input_format": "Line 1: Space-separated integers (e.g. 2 7 11 15)\nLine 2: Target integer (e.g. 9)",
            "output_format": "Space-separated zero-based indices (e.g. 0 1)",
            "starters": make_starters(
                "two_sum",
                "nums = list(map(int, lines[0].split()))\n    target = int(lines[1])\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            print(f\"{seen[diff]} {i}\")\n            return\n        seen[num] = i\n    print(\"-1\")",
                "String[] parts = sc.nextLine().split(\"\\\\s+\");\n        int[] nums = new int[parts.length];\n        for(int i=0; i<parts.length; i++) nums[i] = Integer.parseInt(parts[i]);\n        int target = sc.nextInt();\n        Map<Integer, Integer> map = new HashMap<>();\n        for(int i=0; i<nums.length; i++){\n            int diff = target - nums[i];\n            if(map.containsKey(diff)){\n                System.out.println(map.get(diff) + \" \" + i);\n                return;\n            }\n            map.put(nums[i], i);\n        }\n        System.out.println(\"-1\");",
                "// Read input and print indices\n    return 0;",
                "const nums = input[0].split(' ').map(Number);\n    const target = Number(input[1]);\n    const seen = new Map();\n    for(let i=0; i<nums.length; i++){\n        const diff = target - nums[i];\n        if(seen.has(diff)){\n            console.log(seen.get(diff) + ' ' + i);\n            return;\n        }\n        seen.set(nums[i], i);\n    }\n    console.log('-1');"
            ),
            "testcases": [
                {"in": "2 7 11 15\n9", "out": "0 1", "hidden": False, "pts": 25},
                {"in": "3 2 4\n6", "out": "1 2", "hidden": False, "pts": 25},
                {"in": "3 3\n6", "out": "0 1", "hidden": True, "pts": 25},
                {"in": "1 5 8 12 19\n20", "out": "0 4", "hidden": True, "pts": 25}
            ]
        },
        {
            "title": "Valid Alphanumeric Palindrome Filter",
            "difficulty": "Medium",
            "points": 100,
            "statement": "Given a raw string, determine if it is a palindrome considering only alphanumeric characters and ignoring case sensitivity.\n\nPrint 'true' if it is a palindrome, or 'false' otherwise.",
            "input_format": "A single line containing the raw string.",
            "output_format": "'true' or 'false'",
            "starters": make_starters(
                "is_palindrome",
                "raw = lines[0]\n    cleaned = ''.join(c.lower() for c in raw if c.isalnum())\n    print('true' if cleaned == cleaned[::-1] else 'false')",
                "String raw = sc.nextLine();\n        StringBuilder sb = new StringBuilder();\n        for(char c : raw.toCharArray()) if(Character.isLetterOrDigit(c)) sb.append(Character.toLowerCase(c));\n        String s = sb.toString();\n        String rev = sb.reverse().toString();\n        System.out.println(s.equals(rev) ? \"true\" : \"false\");",
                "return 0;",
                "const raw = input[0];\n    const cleaned = raw.toLowerCase().replace(/[^a-z0-9]/g, '');\n    const rev = cleaned.split('').reverse().join('');\n    console.log(cleaned === rev ? 'true' : 'false');"
            ),
            "testcases": [
                {"in": "A man, a plan, a canal: Panama", "out": "true", "hidden": False, "pts": 25},
                {"in": "race a car", "out": "false", "hidden": False, "pts": 25},
                {"in": "Was it a car or a cat I saw?", "out": "true", "hidden": True, "pts": 25},
                {"in": "No 'x' in Nixon", "out": "true", "hidden": True, "pts": 25}
            ]
        }
    ],

    # ── JAVA TRACK (ID: 21) ──
    21: [
        {
            "title": "Reverse Words in a Sentence",
            "difficulty": "Easy",
            "points": 100,
            "statement": "Given an input sentence string, reverse the order of the words. A word is defined as a sequence of non-space characters. The words in the output string must be separated by a single space with no leading or trailing whitespace.",
            "input_format": "A single line containing the input sentence with multiple spaces.",
            "output_format": "The reversed sentence separated by single spaces.",
            "starters": make_starters(
                "reverse_words",
                "words = lines[0].strip().split()\n    print(' '.join(reversed(words)))",
                "String s = sc.nextLine().trim();\n        String[] words = s.split(\"\\\\s+\");\n        StringBuilder sb = new StringBuilder();\n        for(int i=words.length-1; i>=0; i--){\n            sb.append(words[i]);\n            if(i > 0) sb.append(\" \");\n        }\n        System.out.println(sb.toString());",
                "return 0;",
                "const words = input[0].trim().split(/\\s+/);\n    console.log(words.reverse().join(' '));"
            ),
            "testcases": [
                {"in": "the sky is blue", "out": "blue is sky the", "hidden": False, "pts": 25},
                {"in": "  hello world  ", "out": "world hello", "hidden": False, "pts": 25},
                {"in": "a good   example", "out": "example good a", "hidden": True, "pts": 25},
                {"in": "Lionix Assessment Engine", "out": "Engine Assessment Lionix", "hidden": True, "pts": 25}
            ]
        },
        {
            "title": "Merge Two Sorted Arrays",
            "difficulty": "Medium",
            "points": 100,
            "statement": "Given two sorted integer arrays on separate lines, merge them into a single sorted array and output the space-separated elements.",
            "input_format": "Line 1: Space-separated integers of Array 1\nLine 2: Space-separated integers of Array 2",
            "output_format": "Single line of merged space-separated integers in ascending order.",
            "starters": make_starters(
                "merge_sorted",
                "a = list(map(int, lines[0].split())) if len(lines) > 0 and lines[0] else []\n    b = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1] else []\n    res = sorted(a + b)\n    print(' '.join(map(str, res)))",
                "List<Integer> list = new ArrayList<>();\n        if(sc.hasNextLine()) for(String s : sc.nextLine().split(\"\\\\s+\")) if(!s.isEmpty()) list.add(Integer.parseInt(s));\n        if(sc.hasNextLine()) for(String s : sc.nextLine().split(\"\\\\s+\")) if(!s.isEmpty()) list.add(Integer.parseInt(s));\n        Collections.sort(list);\n        StringBuilder sb = new StringBuilder();\n        for(int i=0; i<list.size(); i++){\n            sb.append(list.get(i));\n            if(i < list.size()-1) sb.append(\" \");\n        }\n        System.out.println(sb.toString());",
                "return 0;",
                "const a = input[0] ? input[0].split(' ').map(Number) : [];\n    const b = input[1] ? input[1].split(' ').map(Number) : [];\n    const res = a.concat(b).sort((x,y) => x - y);\n    console.log(res.join(' '));"
            ),
            "testcases": [
                {"in": "1 3 5\n2 4 6", "out": "1 2 3 4 5 6", "hidden": False, "pts": 25},
                {"in": "10 20\n5 15 25", "out": "5 10 15 20 25", "hidden": False, "pts": 25},
                {"in": "1 2 3\n4 5 6", "out": "1 2 3 4 5 6", "hidden": True, "pts": 25},
                {"in": "7 8\n1 2 3", "out": "1 2 3 7 8", "hidden": True, "pts": 25}
            ]
        }
    ],

    # ── CYBER SECURITY TRACK (ID: 22) ──
    22: [
        {
            "title": "Caesar Cipher Encryption Engine",
            "difficulty": "Easy",
            "points": 100,
            "statement": "Implement a Caesar cipher encoder that shifts every alphabetic letter in the plaintext string by a given integer offset K. Preserve lowercase and uppercase casing. Non-alphabetic characters (spaces, punctuation, digits) must remain unchanged.",
            "input_format": "Line 1: Plaintext string\nLine 2: Shift integer K",
            "output_format": "Encrypted ciphertext string.",
            "starters": make_starters(
                "caesar_cipher",
                "text = lines[0]\n    k = int(lines[1]) % 26\n    res = []\n    for c in text:\n        if c.isupper():\n            res.append(chr((ord(c) - 65 + k) % 26 + 65))\n        elif c.islower():\n            res.append(chr((ord(c) - 97 + k) % 26 + 97))\n        else:\n            res.append(c)\n    print(''.join(res))",
                "String text = sc.nextLine();\n        int k = Integer.parseInt(sc.nextLine()) % 26;\n        StringBuilder sb = new StringBuilder();\n        for(char c : text.toCharArray()){\n            if(Character.isUpperCase(c)) sb.append((char)((c - 'A' + k) % 26 + 'A'));\n            else if(Character.isLowerCase(c)) sb.append((char)((c - 'a' + k) % 26 + 'a'));\n            else sb.append(c);\n        }\n        System.out.println(sb.toString());",
                "return 0;",
                "const text = input[0];\n    const k = Number(input[1]) % 26;\n    let res = '';\n    for(const c of text){\n        const code = c.charCodeAt(0);\n        if(code >= 65 && code <= 90) res += String.fromCharCode((code - 65 + k) % 26 + 65);\n        else if(code >= 97 && code <= 122) res += String.fromCharCode((code - 97 + k) % 26 + 97);\n        else res += c;\n    }\n    console.log(res);"
            ),
            "testcases": [
                {"in": "Hello World!\n3", "out": "Khoor Zruog!", "hidden": False, "pts": 25},
                {"in": "Security123\n1", "out": "Tfdvsjuz123", "hidden": False, "pts": 25},
                {"in": "xyz\n3", "out": "abc", "hidden": True, "pts": 25},
                {"in": "Attack at Dawn\n5", "out": "Fyyfhp fy Ifbs", "hidden": True, "pts": 25}
            ]
        },
        {
            "title": "IPv4 Defanger & Validator",
            "difficulty": "Medium",
            "points": 100,
            "statement": "Given an IPv4 address string, validate if it consists of four octets (0-255) separated by dots with no leading zeroes (except single 0). If valid, output its defanged representation with '[.]' and 'VALID'. If invalid, output 'INVALID'.",
            "input_format": "A single line containing an IP string.",
            "output_format": "Defanged IP followed by ' VALID' or 'INVALID'.",
            "starters": make_starters(
                "defang_ip",
                "ip = lines[0].strip()\n    parts = ip.split('.')\n    if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 and (p == '0' or not p.startswith('0')) for p in parts):\n        print(ip.replace('.', '[.]') + ' VALID')\n    else:\n        print('INVALID')",
                "String ip = sc.nextLine().trim();\n        String[] parts = ip.split(\"\\\\.\");\n        boolean valid = (parts.length == 4);\n        if(valid){\n            for(String p : parts){\n                if(p.isEmpty() || !p.matches(\"\\\\d+\") || (p.length() > 1 && p.startsWith(\"0\"))) { valid = false; break; }\n                int val = Integer.parseInt(p);\n                if(val < 0 || val > 255) { valid = false; break; }\n            }\n        }\n        if(valid) System.out.println(ip.replace(\".\", \"[.]\") + \" VALID\");\n        else System.out.println(\"INVALID\");",
                "return 0;",
                "const ip = input[0].trim();\n    const parts = ip.split('.');\n    const valid = parts.length === 4 && parts.every(p => /^\\d+$/.test(p) && Number(p) >= 0 && Number(p) <= 255 && (p === '0' || !p.startsWith('0')));\n    if(valid) console.log(ip.split('.').join('[.]') + ' VALID');\n    else console.log('INVALID');"
            ),
            "testcases": [
                {"in": "192.168.1.1", "out": "192[.]168[.]1[.]1 VALID", "hidden": False, "pts": 25},
                {"in": "256.100.0.1", "out": "INVALID", "hidden": False, "pts": 25},
                {"in": "10.0.0.1", "out": "10[.]0[.]0[.]1 VALID", "hidden": True, "pts": 25},
                {"in": "192.168.01.1", "out": "INVALID", "hidden": True, "pts": 25}
            ]
        }
    ],

    # ── DATA ANALYST TRACK (ID: 23) ──
    23: [
        {
            "title": "Summary Descriptive Statistics (Mean & Median)",
            "difficulty": "Easy",
            "points": 100,
            "statement": "Given a space-separated list of numeric values, compute the arithmetic mean and the median. Output both values formatted to 2 decimal places separated by a space.",
            "input_format": "A single line of space-separated numbers.",
            "output_format": "Mean and Median rounded to 2 decimal places (e.g. 5.00 5.00).",
            "starters": make_starters(
                "calc_stats",
                "nums = sorted(list(map(float, lines[0].split())))\n    n = len(nums)\n    mean = sum(nums) / n\n    if n % 2 == 1:\n        median = nums[n//2]\n    else:\n        median = (nums[n//2 - 1] + nums[n//2]) / 2.0\n    print(f\"{mean:.2f} {median:.2f}\")",
                "String[] parts = sc.nextLine().split(\"\\\\s+\");\n        double[] nums = new double[parts.length];\n        double sum = 0;\n        for(int i=0; i<parts.length; i++){\n            nums[i] = Double.parseDouble(parts[i]);\n            sum += nums[i];\n        }\n        Arrays.sort(nums);\n        int n = nums.length;\n        double mean = sum / n;\n        double median = (n % 2 == 1) ? nums[n/2] : (nums[n/2 - 1] + nums[n/2]) / 2.0;\n        System.out.printf(Locale.US, \"%.2f %.2f\\n\", mean, median);",
                "return 0;",
                "const nums = input[0].split(' ').map(Number).sort((a,b) => a - b);\n    const n = nums.length;\n    const sum = nums.reduce((a,b) => a + b, 0);\n    const mean = sum / n;\n    const median = (n % 2 === 1) ? nums[Math.floor(n/2)] : (nums[n/2 - 1] + nums[n/2]) / 2;\n    console.log(mean.toFixed(2) + ' ' + median.toFixed(2));"
            ),
            "testcases": [
                {"in": "1 2 3 4 5", "out": "3.00 3.00", "hidden": False, "pts": 25},
                {"in": "10 20 30 40", "out": "25.00 25.00", "hidden": False, "pts": 25},
                {"in": "5 1 9 3 7", "out": "5.00 5.00", "hidden": True, "pts": 25},
                {"in": "100 200", "out": "150.00 150.00", "hidden": True, "pts": 25}
            ]
        },
        {
            "title": "Top-K Frequent Elements Finder",
            "difficulty": "Medium",
            "points": 100,
            "statement": "Given a list of space-separated strings and an integer K on the second line, return the top K most frequent elements. Output them separated by space in descending order of frequency. If two items have identical frequency, sort them alphabetically.",
            "input_format": "Line 1: Space-separated strings\nLine 2: Integer K",
            "output_format": "Top K strings separated by space.",
            "starters": make_starters(
                "top_k_frequent",
                "from collections import Counter\n    items = lines[0].split()\n    k = int(lines[1])\n    counts = Counter(items)\n    sorted_items = sorted(counts.keys(), key=lambda x: (-counts[x], x))\n    print(' '.join(sorted_items[:k]))",
                "String[] items = sc.nextLine().split(\"\\\\s+\");\n        int k = sc.nextInt();\n        Map<String, Integer> counts = new HashMap<>();\n        for(String s : items) counts.put(s, counts.getOrDefault(s, 0) + 1);\n        List<String> list = new ArrayList<>(counts.keySet());\n        list.sort((a, b) -> {\n            int cmp = counts.get(b).compareTo(counts.get(a));\n            return cmp != 0 ? cmp : a.compareTo(b);\n        });\n        StringBuilder sb = new StringBuilder();\n        for(int i=0; i<Math.min(k, list.size()); i++){\n            sb.append(list.get(i));\n            if(i < k-1) sb.append(\" \");\n        }\n        System.out.println(sb.toString().trim());",
                "return 0;",
                "const items = input[0].split(' ');\n    const k = Number(input[1]);\n    const counts = {};\n    for(const s of items) counts[s] = (counts[s] || 0) + 1;\n    const sortedKeys = Object.keys(counts).sort((a,b) => counts[b] !== counts[a] ? counts[b] - counts[a] : a.localeCompare(b));\n    console.log(sortedKeys.slice(0, k).join(' '));"
            ),
            "testcases": [
                {"in": "apple banana apple orange banana apple\n2", "out": "apple banana", "hidden": False, "pts": 25},
                {"in": "cat dog cat dog bird\n2", "out": "cat dog", "hidden": False, "pts": 25},
                {"in": "a b c a b a\n1", "out": "a", "hidden": True, "pts": 25},
                {"in": "sql python sql java python sql\n2", "out": "sql python", "hidden": True, "pts": 25}
            ]
        }
    ],

    # ── .NET DEVELOPER TRACK (ID: 24) ──
    24: [
        {
            "title": "Balanced Parentheses & Bracket Validator",
            "difficulty": "Easy",
            "points": 100,
            "statement": "Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. Brackets must close in the correct order.\n\nPrint 'true' if valid, or 'false' otherwise.",
            "input_format": "A single line containing the bracket string.",
            "output_format": "'true' or 'false'",
            "starters": make_starters(
                "is_valid_brackets",
                "s = lines[0].strip()\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                print('false')\n                return\n        else:\n            stack.append(char)\n    print('true' if not stack else 'false')",
                "String s = sc.nextLine().trim();\n        Stack<Character> stack = new Stack<>();\n        boolean valid = true;\n        for(char c : s.toCharArray()){\n            if(c == '(' || c == '{' || c == '[') stack.push(c);\n            else {\n                if(stack.isEmpty()) { valid = false; break; }\n                char top = stack.pop();\n                if((c == ')' && top != '(') || (c == '}' && top != '{') || (c == ']' && top != '[')) { valid = false; break; }\n            }\n        }\n        if(!stack.isEmpty()) valid = false;\n        System.out.println(valid ? \"true\" : \"false\");",
                "return 0;",
                "const s = input[0].trim();\n    const stack = [];\n    const pairs = { ')': '(', '}': '{', ']': '[' };\n    for(const c of s){\n        if(c === '(' || c === '{' || c === '[') stack.push(c);\n        else if(pairs[c]){\n            if(stack.pop() !== pairs[c]){ console.log('false'); return; }\n        }\n    }\n    console.log(stack.length === 0 ? 'true' : 'false');"
            ),
            "testcases": [
                {"in": "()[]{}", "out": "true", "hidden": False, "pts": 25},
                {"in": "(]", "out": "false", "hidden": False, "pts": 25},
                {"in": "([{}])", "out": "true", "hidden": True, "pts": 25},
                {"in": "[(])", "out": "false", "hidden": True, "pts": 25}
            ]
        },
        {
            "title": "Matrix Diagonals Sum",
            "difficulty": "Medium",
            "points": 100,
            "statement": "Given a square matrix of size N x N, calculate the sum of the primary diagonal (top-left to bottom-right) and secondary diagonal (top-right to bottom-left). Do not count the center element twice if N is odd.",
            "input_format": "Line 1: Integer N\nNext N lines: Space-separated integers for each row",
            "output_format": "Single integer sum of both diagonals.",
            "starters": make_starters(
                "diagonal_sum",
                "n = int(lines[0])\n    total = 0\n    for i in range(n):\n        row = list(map(int, lines[1+i].split()))\n        total += row[i]\n        if i != n - 1 - i:\n            total += row[n - 1 - i]\n    print(total)",
                "int n = Integer.parseInt(sc.nextLine().trim());\n        int total = 0;\n        for(int i=0; i<n; i++){\n            String[] parts = sc.nextLine().split(\"\\\\s+\");\n            total += Integer.parseInt(parts[i]);\n            if(i != n - 1 - i) total += Integer.parseInt(parts[n - 1 - i]);\n        }\n        System.out.println(total);",
                "return 0;",
                "const n = Number(input[0]);\n    let total = 0;\n    for(let i=0; i<n; i++){\n        const row = input[1+i].split(' ').map(Number);\n        total += row[i];\n        if(i !== n - 1 - i) total += row[n - 1 - i];\n    }\n    console.log(total);"
            ),
            "testcases": [
                {"in": "3\n1 2 3\n4 5 6\n7 8 9", "out": "25", "hidden": False, "pts": 25},
                {"in": "4\n1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1", "out": "8", "hidden": False, "pts": 25},
                {"in": "1\n5", "out": "5", "hidden": True, "pts": 25},
                {"in": "3\n2 0 2\n0 4 0\n2 0 2", "out": "12", "hidden": True, "pts": 25}
            ]
        }
    ],

    # ── FULL STACK TRACK (ID: 25) ──
    25: [
        {
            "title": "Longest Substring Without Repeating Characters",
            "difficulty": "Medium",
            "points": 100,
            "statement": "Given a string S, find the length of the longest substring without repeating characters.",
            "input_format": "A single line containing the string S.",
            "output_format": "An integer representing the maximum length.",
            "starters": make_starters(
                "length_of_longest_substring",
                "s = lines[0] if lines else ''\n    char_map = {}\n    max_len = 0\n    start = 0\n    for end, char in enumerate(s):\n        if char in char_map and char_map[char] >= start:\n            start = char_map[char] + 1\n        char_map[char] = end\n        max_len = max(max_len, end - start + 1)\n    print(max_len)",
                "String s = sc.hasNextLine() ? sc.nextLine() : \"\";\n        Map<Character, Integer> map = new HashMap<>();\n        int maxLen = 0, start = 0;\n        for(int end=0; end<s.length(); end++){\n            char c = s.charAt(end);\n            if(map.containsKey(c) && map.get(c) >= start) start = map.get(c) + 1;\n            map.put(c, end);\n            maxLen = Math.max(maxLen, end - start + 1);\n        }\n        System.out.println(maxLen);",
                "return 0;",
                "const s = input[0] || '';\n    const map = new Map();\n    let maxLen = 0, start = 0;\n    for(let end=0; end<s.length; end++){\n        const c = s[end];\n        if(map.has(c) && map.get(c) >= start) start = map.get(c) + 1;\n        map.set(c, end);\n        maxLen = Math.max(maxLen, end - start + 1);\n    }\n    console.log(maxLen);"
            ),
            "testcases": [
                {"in": "abcabcbb", "out": "3", "hidden": False, "pts": 25},
                {"in": "bbbbb", "out": "1", "hidden": False, "pts": 25},
                {"in": "pwwkew", "out": "3", "hidden": True, "pts": 25},
                {"in": "abcdef", "out": "6", "hidden": True, "pts": 25}
            ]
        },
        {
            "title": "JSON Flatten Key-Path Parser",
            "difficulty": "Medium",
            "points": 100,
            "statement": "Given a simple key-value string pairs on multiple lines formatted as 'key: value', output all keys sorted alphabetically followed by their values.",
            "input_format": "Multiple lines of 'key: value'.",
            "output_format": "Sorted keys and values line by line.",
            "starters": make_starters(
                "parse_pairs",
                "data = {}\n    for l in lines:\n        if ':' in l:\n            k, v = l.split(':', 1)\n            data[k.strip()] = v.strip()\n    for k in sorted(data.keys()):\n        print(f\"{k}: {data[k]}\")",
                "Map<String, String> map = new TreeMap<>();\n        while(sc.hasNextLine()){\n            String line = sc.nextLine();\n            if(line.contains(\":\")){\n                String[] p = line.split(\":\", 2);\n                map.put(p[0].trim(), p[1].trim());\n            }\n        }\n        for(Map.Entry<String, String> e : map.entrySet()){\n            System.out.println(e.getKey() + \": \" + e.getValue());\n        }",
                "return 0;",
                "const map = {};\n    for(const l of input){\n        if(l.includes(':')){\n            const [k, v] = l.split(':');\n            map[k.trim()] = v.trim();\n        }\n    }\n    for(const k of Object.keys(map).sort()){\n        console.log(`${k}: ${map[k]}`);\n    }"
            ),
            "testcases": [
                {"in": "name: John\nage: 25\ncity: London", "out": "age: 25\ncity: London\nname: John", "hidden": False, "pts": 25},
                {"in": "z: 10\na: 20", "out": "a: 20\nz: 10", "hidden": False, "pts": 25},
                {"in": "role: Engineer\nlevel: Senior", "out": "level: Senior\nrole: Engineer", "hidden": True, "pts": 25},
                {"in": "host: localhost\nport: 5000", "out": "host: localhost\nport: 5000", "hidden": True, "pts": 25}
            ]
        }
    ]
}

# Insert all coding problems and testcases
for did, prob_list in problems_by_drive.items():
    print(f"\nInserting Coding Problems for Drive ID: {did}...")
    for p in prob_list:
        cur.execute("""
            INSERT INTO assessment_coding_problems (assessment_id, title, difficulty, points, problem_statement, input_format, output_format, starter_code_json, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            RETURNING id;
        """, (did, p["title"], p["difficulty"], p["points"], p["statement"], p["input_format"], p["output_format"], json.dumps(p["starters"])))
        prob_id = cur.fetchone()[0]
        
        for tc in p["testcases"]:
            cur.execute("""
                INSERT INTO assessment_coding_testcases (problem_id, input_data, expected_output, is_hidden, created_at)
                VALUES (%s, %s, %s, %s, NOW());
            """, (prob_id, tc["in"], tc["out"], tc["hidden"]))
        
        print(f"  + Problem Created: '{p['title']}' (ID: {prob_id}) with {len(p['testcases'])} testcases.")

conn.commit()
conn.close()
print("\nALL TECHNICAL ROUND 3 CODING DRIVES & PROBLEMS SEEDED SUCCESSFULLY!")
