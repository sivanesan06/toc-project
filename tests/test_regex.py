"""
test_regex.py
Automated unit tests for Regular Expression implementations of all 5 patterns.
"""

import pytest
from src.regex_search import search_regex_pattern, search_all_patterns


class TestRegexPatterns:
    """Test suite verifying all five regular expression search patterns."""

    def test_pattern1_starts_with_com(self):
        """Pattern 1: Words starting with 'com'."""
        text = "The computer and communication completed the computation."
        res = search_regex_pattern(text, "Pattern 1")
        assert res.total_occurrences == 4
        words = [m.word.lower() for m in res.matches]
        assert "computer" in words
        assert "communication" in words
        assert "completed" in words
        assert "computation" in words

    def test_pattern2_ends_with_ing(self):
        """Pattern 2: Words ending with 'ing'."""
        text = "Machine learning and distributed processing power modern searching."
        res = search_regex_pattern(text, "Pattern 2")
        assert res.total_occurrences == 3
        words = [m.word.lower() for m in res.matches]
        assert "learning" in words
        assert "processing" in words
        assert "searching" in words

    def test_pattern3_contains_tion(self):
        """Pattern 3: Words containing 'tion'."""
        text = "Information processing, educational tools, and communication."
        res = search_regex_pattern(text, "Pattern 3")
        # 'Information', 'educational', and 'communication' all contain 'tion'
        assert res.total_occurrences == 3
        words = [m.word.lower() for m in res.matches]
        assert "information" in words
        assert "educational" in words
        assert "communication" in words

    def test_pattern4_five_letters(self):
        """Pattern 4: Words containing exactly five letters."""
        text = "An apple on the table in the class."
        res = search_regex_pattern(text, "Pattern 4")
        words = [m.word.lower() for m in res.matches]
        assert "apple" in words
        assert "table" in words
        assert "class" in words

    def test_pattern5_starts_with_pre(self):
        """Pattern 5: Words starting with 'pre'."""
        text = "The team must prepare and preview the prediction model."
        res = search_regex_pattern(text, "Pattern 5")
        words = [m.word.lower() for m in res.matches]
        assert "prepare" in words
        assert "preview" in words
        assert "prediction" in words

    def test_case_insensitivity(self):
        """Test case insensitivity across patterns."""
        text = "COMPUTER Computing COMPUTATION Table PREPARE"
        res1 = search_regex_pattern(text, "Pattern 1")
        assert len(res1.matches) == 3
        res4 = search_regex_pattern(text, "Pattern 4")
        assert len(res4.matches) == 1
        assert res4.matches[0].word == "Table"
        res5 = search_regex_pattern(text, "Pattern 5")
        assert len(res5.matches) == 1
        assert res5.matches[0].word == "PREPARE"

    def test_word_with_multiple_patterns(self):
        """TC15: Multiple patterns matching the same word (e.g. 'computation' matches Pattern 1 and 3)."""
        text = "computation"
        all_res = search_all_patterns(text)
        # Matches Pattern 1 ('com*') and Pattern 3 ('*tion*')
        assert all_res["Pattern 1"].total_occurrences == 1
        assert all_res["Pattern 3"].total_occurrences == 1
