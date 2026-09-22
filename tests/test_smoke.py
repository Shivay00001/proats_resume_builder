"""Smoke tests for the stdlib-only core (models, validators, ATS rules)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.resume_data import ResumeData
from utils.validators import validate_email, validate_phone, validate_url
from utils.ats_rules import calculate_ats_score


def test_validators():
    assert validate_email("a@b.com") is True
    assert validate_email("not-an-email") is False
    assert validate_email("") is False
    assert validate_phone("+91 98765 43210") is True
    assert validate_phone("abc") is False
    assert validate_url("https://example.com") is True
    assert validate_url("notaurl") is False


def test_ats_score_full_resume():
    data = ResumeData(
        full_name="Jane Doe",
        email="jane@example.com",
        phone="+1 555 1234",
        summary="Experienced engineer",
        skills=["Python", "Go"],
    )
    score, feedback = calculate_ats_score(data)
    assert isinstance(score, int) and 0 <= score <= 100
    assert isinstance(feedback, list)


def test_ats_score_empty_resume_penalized():
    score, feedback = calculate_ats_score(ResumeData())
    assert score < 100
    assert len(feedback) > 0


if __name__ == "__main__":
    test_validators()
    test_ats_score_full_resume()
    test_ats_score_empty_resume_penalized()
    print("resume builder smoke tests: 3 passed")
