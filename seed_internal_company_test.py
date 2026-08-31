"""
seed_internal_company_test.py
Creates and populates the 'Internal Company Test' assessment with 20 questions:
- 10 Linux / Ubuntu / Docker / Terminal-Bench / Snorkel MCQs
- 5 GitHub / Git Workflows / Repository Management MCQs
- 5 Advanced Python Programming MCQs
"""
import os
from app import create_app
from models.models import db, Assessment, Question, Submission, Answer

def seed_assessment():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Fix Postgres primary key sequences if out-of-sync
        try:
            db.session.execute(db.text("SELECT setval(pg_get_serial_sequence('assessment_drives', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM assessment_drives;"))
            db.session.execute(db.text("SELECT setval(pg_get_serial_sequence('assessment_questions', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM assessment_questions;"))
            db.session.commit()
        except Exception as e:
            print(f"Sequence sync note: {e}")
            db.session.rollback()

        # Check if an assessment titled "Internal Company Test" already exists
        existing_assessments = Assessment.query.filter(
            Assessment.title.ilike('%Internal Company Test%')
        ).all()

        for old_a in existing_assessments:
            print(f"Cleaning up existing assessment ID {old_a.id} ({old_a.title})...")
            subs = Submission.query.filter_by(assessment_id=old_a.id).all()
            for sub in subs:
                Answer.query.filter_by(submission_id=sub.id).delete()
                db.session.delete(sub)
            Question.query.filter_by(assessment_id=old_a.id).delete()
            db.session.delete(old_a)
        db.session.commit()

        # Create new Assessment
        assessment = Assessment(
            title="Internal Company Test",
            description=(
                "Comprehensive Technical Evaluation covering Ubuntu/Linux Administration, "
                "Docker Environments, Terminal-Bench & Benchmark Debugging, GitHub Workflows & CI/CD, "
                "and Advanced Python Concepts. Contains 20 MCQs. Time limit: 20 minutes."
            ),
            duration=20,
            pass_percentage=50.0,
            status='active'
        )
        db.session.add(assessment)
        db.session.commit()
        print(f"Created Assessment: '{assessment.title}' (ID: {assessment.id})")

        questions = [
            # ── SECTION 1: UBUNTU / LINUX / DOCKER / TERMINAL-BENCH (10 Questions) ──
            {
                "question": "A task works locally with 'python solution/solve.py', but inside the Docker environment it fails with: 'python: command not found' while 'python3' exists. What is the best fix?",
                "option_a": "Install Java into the container",
                "option_b": "Change the solver to explicitly use python3 or provide the expected python command/symlink in the image",
                "option_c": "Delete the evaluation tests",
                "option_d": "Run Docker with the --privileged flag",
                "correct_answer": "B"
            },
            {
                "question": "Given a Dockerfile with: 'WORKDIR /app' and 'COPY . /app' in a repository containing solution/solve.sh, tests/test.sh, and src/, what is the primary concern in an agent benchmark task?",
                "option_a": "/app cannot contain executable shell scripts",
                "option_b": "The image may expose solution and hidden test material to the benchmark agent",
                "option_c": "Docker cannot copy hidden directories",
                "option_d": "Ubuntu does not support the /app directory path",
                "correct_answer": "B"
            },
            {
                "question": "You receive the runtime error: 'bash: ./solution/solve.sh: Permission denied'. What is the most direct and appropriate fix?",
                "option_a": "chmod +x solution/solve.sh",
                "option_b": "chmod 777 /",
                "option_c": "sudo docker restart",
                "option_d": "apt install bash",
                "correct_answer": "A"
            },
            {
                "question": "A solver generates '/app/output/result.json', but the verifier container cannot find it. Which should you investigate FIRST?",
                "option_a": "Whether the LLM provider supports JSON output format",
                "option_b": "Whether /app/output is actually shared or transferred between the solver and verifier environments",
                "option_c": "Whether Ubuntu has Python installed",
                "option_d": "Whether Git is installed in the container",
                "correct_answer": "B"
            },
            {
                "question": "Inside a running container, you execute: echo 'fixed' > /tmp/result.txt. The container is subsequently destroyed and recreated. What happens to /tmp/result.txt?",
                "option_a": "/tmp/result.txt is guaranteed to remain intact",
                "option_b": "It normally disappears with the container lifecycle unless explicitly mounted or persisted externally",
                "option_c": "Docker automatically commits the modification to the base image",
                "option_d": "The file is moved to /home automatically",
                "correct_answer": "B"
            },
            {
                "question": "A Dockerfile contains: 'RUN python3 -m pip install pandas'. The build succeeds, but the runtime task later reports: 'ModuleNotFoundError: No module named pandas'. Which explanation is most plausible?",
                "option_a": "The package was installed into a different environment/interpreter than the one executing the task",
                "option_b": "Docker cannot install Python packages during build time",
                "option_c": "pandas only works natively on Windows operating systems",
                "option_d": "RUN commands execute only after the container exits",
                "correct_answer": "A"
            },
            {
                "question": "An agent is instructed to modify '/app/config/settings.yaml', but the repository contains 'environment/data/config/settings.yaml' and the Dockerfile contains 'COPY data /app/data'. What should the agent determine before editing?",
                "option_a": "Whether /app/config actually exists at runtime in the container filesystem",
                "option_b": "Whether GitHub is currently online",
                "option_c": "Whether the host machine is running Windows",
                "option_d": "Whether Java is installed on the host",
                "correct_answer": "A"
            },
            {
                "question": "A service inside Container A is listening on 127.0.0.1:8080. Container B on the same Docker network attempts to connect to 'container-a:8080' but fails. What is the likely cause?",
                "option_a": "127.0.0.1 binds exclusively to Container A's own loopback interface, not all network interfaces reachable from Container B",
                "option_b": "Docker containers cannot communicate over TCP networks",
                "option_c": "Port 8080 is restricted exclusively to Windows platforms",
                "option_d": "Python blocks all inter-container networking by default",
                "correct_answer": "A"
            },
            {
                "question": "A Terminal-Bench task asks you to determine why a background process keeps restarting unexpectedly. Which combination provides the most useful initial investigation?",
                "option_a": "ps, pgrep, journalctl, and systemctl status commands",
                "option_b": "chmod -R 777 /",
                "option_c": "rm -rf /tmp/*",
                "option_d": "git push origin main",
                "correct_answer": "A"
            },
            {
                "question": "A benchmark task has Dockerfile, run_pipeline.sh, solution/solve.sh, and tests/test.sh. Oracle passes (Reward: 1.0), but an agent receives Reward: 0.0 with logs: 'Could not find /app/repro_test.json'. What should you investigate before concluding the task is difficult for the model?",
                "option_a": "Whether the required artifact is created at the expected path and survives/transfers correctly between execution stages",
                "option_b": "Increase task difficulty score",
                "option_c": "Add more third-party dependencies",
                "option_d": "Hide the tests from the verifier",
                "correct_answer": "A"
            },

            # ── SECTION 2: GITHUB / GIT WORKFLOWS & REPO MANAGEMENT (5 Questions) ──
            {
                "question": "When you create multiple feature branches locally and want to push the main branch along with all your feature PR branches to your GitHub repository at once, which command sequence is used?",
                "option_a": "git push origin master",
                "option_b": "git push -u origin main followed by git push origin --all",
                "option_c": "git commit --push-everything",
                "option_d": "git remote push --branches",
                "correct_answer": "B"
            },
            {
                "question": "Why is 'git merge --no-ff <branch-name>' (No Fast-Forward) preferred over standard fast-forward merges when building enterprise repositories with feature pull requests?",
                "option_a": "It reduces the total repository size on disk",
                "option_b": "It creates an explicit merge commit that preserves the historical existence of the feature branch and its grouped commit history",
                "option_c": "It automatically resolves all merge conflicts without human intervention",
                "option_d": "It converts JavaScript files into TypeScript files",
                "correct_answer": "B"
            },
            {
                "question": "What is the industry best practice on GitHub for handling environment configurations and preventing secret leaks (API keys, database URLs)?",
                "option_a": "Commit the .env file directly to GitHub so team members can read the keys immediately",
                "option_b": "Add .env to .gitignore, commit only a template .env.example with dummy values, and load secrets via runtime environment variables",
                "option_c": "Encrypt passwords directly in the README.md file",
                "option_d": "Rename the .env file to .env.txt before pushing",
                "correct_answer": "B"
            },
            {
                "question": "What is GitHub's strict per-file upload size threshold, and what happens if a commit contains a single file exceeding this limit?",
                "option_a": "10 MB — Git automatically splits the file into multiple chunks",
                "option_b": "50 MB (warning) and 100 MB (hard block) — GitHub will reject the git push completely with a fatal pre-receive error",
                "option_c": "1 GB — GitHub compresses it into a ZIP archive automatically",
                "option_d": "There is no limit on file sizes on GitHub",
                "correct_answer": "B"
            },
            {
                "question": "Where must CI/CD pipeline definitions be stored in a GitHub repository so that automated test suites execute automatically on every push and pull request?",
                "option_a": "server/tests/ci.json",
                "option_b": ".github/workflows/<workflow-name>.yml",
                "option_c": "config/github-actions.xml",
                "option_d": ".git/hooks/pre-push",
                "correct_answer": "B"
            },

            # ── SECTION 3: PYTHON PROGRAMMING & CORE CONCEPTS (5 Questions) ──
            {
                "question": "Consider the following Python code:\n\ndef append_to_list(val, items=[]):\n    items.append(val)\n    return items\n\nprint(append_to_list(1))\nprint(append_to_list(2))\n\nWhat will be printed to stdout?",
                "option_a": "[1] followed by [2]",
                "option_b": "[1] followed by [1, 2]",
                "option_c": "[1, 2] followed by [1, 2]",
                "option_d": "TypeError: mutable default argument not permitted",
                "correct_answer": "B"
            },
            {
                "question": "In standard CPython, which statement accurately describes the Global Interpreter Lock (GIL) and high-concurrency execution?",
                "option_a": "The GIL prevents multi-threaded Python programs from executing CPU-bound bytecode simultaneously across multiple cores; multiprocessing or C extensions are required for true CPU parallelism",
                "option_b": "The GIL completely prevents asynchronous I/O when using asyncio",
                "option_c": "Multi-threading in Python automatically runs CPU-bound operations in parallel across all CPU cores",
                "option_d": "The GIL only affects memory allocation on Windows operating systems",
                "correct_answer": "A"
            },
            {
                "question": "Which of the following statements about Python generators (functions utilizing the 'yield' keyword) is TRUE compared to returning standard lists?",
                "option_a": "Generators load the entire dataset into RAM at initialization before yielding items",
                "option_b": "Generators produce items lazily on demand one at a time, resulting in O(1) auxiliary memory complexity during iteration",
                "option_c": "A generator function can only be iterated over using a while loop and cannot be used in a for loop",
                "option_d": "Generators cannot accept input parameters",
                "correct_answer": "B"
            },
            {
                "question": "What happens under the hood when a 'with open(\"data.txt\", \"r\") as f:' statement completes execution or encounters an unhandled exception inside the block?",
                "option_a": "Python immediately deletes the file from disk",
                "option_b": "Python invokes the context manager's __exit__ method, guaranteeing that file descriptors and system resources are cleanly closed",
                "option_c": "Python silently suppresses all exceptions and disables stack trace output",
                "option_d": "The file descriptor remains open in memory until the operating system restarts",
                "correct_answer": "B"
            },
            {
                "question": "What is the output of the following Python snippet?\n\ndef calculate_total(*args, **kwargs):\n    return sum(args) + kwargs.get('bonus', 0)\n\nnums = [10, 20, 30]\nextra = {'bonus': 15, 'multiplier': 2}\nprint(calculate_total(*nums, **extra))",
                "option_a": "60",
                "option_b": "75",
                "option_c": "150",
                "option_d": "TypeError: calculate_total() got unexpected keyword argument",
                "correct_answer": "B"
            }
        ]

        for idx, q_data in enumerate(questions, start=1):
            q_obj = Question(
                assessment_id=assessment.id,
                question=f"Q{idx}. {q_data['question']}",
                option_a=q_data['option_a'],
                option_b=q_data['option_b'],
                option_c=q_data['option_c'],
                option_d=q_data['option_d'],
                correct_answer=q_data['correct_answer']
            )
            db.session.add(q_obj)

        db.session.commit()
        print(f"Successfully seeded {len(questions)} questions into '{assessment.title}' (ID: {assessment.id})!")

if __name__ == '__main__':
    seed_assessment()
