"""
test_comparison.py
Automated unit tests for RE vs DFA comparative analysis and accuracy verification.
"""

import pytest
from src.regex_search import search_regex_pattern
from src.dfa_search import search_dfa
from src.comparison import verify_accuracy, run_benchmark, get_qualitative_comparison


class TestComparisonModule:
    """Verifies that RE and DFA produce identical results on identical text."""

    def test_exact_agreement_on_sample_text(self):
        sample_text = (
            "The computer completed complex computation. "
            "Another COMPUTER joined the community communication com!"
        )
        re_res = search_regex_pattern(sample_text, "Pattern 1")
        dfa_res = search_dfa(sample_text)

        verification = verify_accuracy(re_res.matches, dfa_res.matches)
        assert verification["exact_match_agreement"] is True
        assert verification["accuracy_status"] == "100% Match Agreement"
        assert verification["missing_count"] == 0
        assert verification["extra_count"] == 0
        assert verification["re_count"] == verification["dfa_count"]

    def test_boundary_handling_agreement(self):
        boundary_text = (
            "welcome, 123computer456, complete; 'computation' "
            "com, computer\ncommunication"
        )
        re_res = search_regex_pattern(boundary_text, "Pattern 1")
        dfa_res = search_dfa(boundary_text)

        verification = verify_accuracy(re_res.matches, dfa_res.matches)
        assert verification["exact_match_agreement"] is True
        assert verification["accuracy_status"] == "100% Match Agreement"

    def test_benchmark_execution(self):
        test_text = "computer computation complete communication"
        bench = run_benchmark(test_text, iterations=20)
        assert bench["iterations"] == 20
        assert bench["re_stats"]["mean_ms"] >= 0.0
        assert bench["dfa_stats"]["mean_ms"] >= 0.0

    def test_qualitative_comparison_table(self):
        df = get_qualitative_comparison()
        assert len(df) == 9
        assert "Comparison Criterion" in df.columns

