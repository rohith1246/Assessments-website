"""
Lionix — Stats Service
Aggregated statistics for the admin dashboard.

Performance: Consolidated from 7 separate COUNT queries into 2 queries
using SQLAlchemy aggregate functions (func.count + case).
Results are cached for 5 minutes via Flask-Caching.
"""
from sqlalchemy import func, case
from models.models import db, Candidate, Assessment, Question, Submission, CodingSubmission, CodingProblem
from extensions import cache


def get_dashboard_stats() -> dict:
    """Return all stats card values for the admin dashboard."""
    return _compute_dashboard_stats()


@cache.cached(timeout=30, key_prefix='dashboard_stats')
def _compute_dashboard_stats() -> dict:
    try:
        counts = db.session.query(
            func.count(Assessment.id).label('total_assessments'),
            func.count(case((Assessment.status == 'active', 1))).label('active_assessments'),
        ).first()
        total_assessments = counts.total_assessments or 0
        active_assessments = counts.active_assessments or 0

        candidate_count = db.session.query(func.count(Candidate.id)).scalar() or 0

        status_rows = (
            db.session.query(
                Submission.status,
                func.count(Submission.id).label('cnt')
            )
            .group_by(Submission.status)
            .all()
        )

        status_counts = {row.status: row.cnt for row in status_rows}
        passed      = status_counts.get('pass', 0)
        failed      = status_counts.get('fail', 0)
        in_progress = status_counts.get('in_progress', 0)
        total_attempts = passed + failed + in_progress

        # Coding specific metrics
        coding_counts = db.session.query(
            func.count(CodingSubmission.id).label('total_coding_subs'),
            func.count(case((CodingSubmission.status == 'Accepted', 1))).label('accepted_coding_subs'),
            func.coalesce(func.avg(CodingSubmission.score), 0).label('avg_coding_score')
        ).first()

        total_coding_subs = coding_counts.total_coding_subs or 0
        accepted_coding_subs = coding_counts.accepted_coding_subs or 0
        avg_coding_score = round(float(coding_counts.avg_coding_score or 0), 1)

        return {
            'total_candidates':     candidate_count,
            'total_assessments':    total_assessments,
            'active_assessments':   active_assessments,
            'total_attempts':       total_attempts,
            'passed':               passed,
            'failed':               failed,
            'in_progress':          in_progress,
            'pass_rate':            round((passed / (passed + failed) * 100) if (passed + failed) > 0 else 0, 1),
            'total_coding_subs':    total_coding_subs,
            'accepted_coding_subs': accepted_coding_subs,
            'avg_coding_score':     avg_coding_score,
        }
    except Exception:
        return {
            'total_candidates':     0,
            'total_assessments':    0,
            'active_assessments':   0,
            'total_attempts':       0,
            'passed':               0,
            'failed':               0,
            'in_progress':          0,
            'pass_rate':            0,
            'total_coding_subs':    0,
            'accepted_coding_subs': 0,
            'avg_coding_score':     0,
        }


def get_recent_results(limit: int = 10):
    """Return the most recent completed submissions."""
    return (
        db.session.query(Submission)
        .filter(Submission.status != 'in_progress')
        .order_by(Submission.submitted_at.desc())
        .limit(limit)
        .all()
    )


def get_recent_coding_submissions(limit: int = 15):
    """Return the most recent coding submissions with candidate and problem details."""
    try:
        return (
            db.session.query(
                CodingSubmission.id,
                CodingSubmission.submission_id,
                CodingSubmission.language,
                CodingSubmission.passed_testcases,
                CodingSubmission.total_testcases,
                CodingSubmission.score,
                CodingSubmission.execution_time_ms,
                CodingSubmission.status,
                CodingSubmission.submitted_at,
                CodingProblem.title.label('problem_title'),
                Candidate.full_name.label('candidate_name'),
                Candidate.email.label('candidate_email'),
                Candidate.hall_ticket.label('candidate_hall_ticket')
            )
            .join(Submission, CodingSubmission.submission_id == Submission.id)
            .join(Candidate, Submission.candidate_id == Candidate.id)
            .join(CodingProblem, CodingSubmission.problem_id == CodingProblem.id)
            .order_by(CodingSubmission.submitted_at.desc())
            .limit(limit)
            .all()
        )
    except Exception:
        return []

