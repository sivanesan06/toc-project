"""
test_dfa.py
Automated unit tests for Deterministic Finite Automata (DFA) implementation.
Verifies all acceptance criteria, word boundary handling, and rejection states.
"""

import pytest
from src.dfa_search import simulate_word, search_dfa, dfa_transition


class TestDFAImplementation:
    """Test suite verifying DFA behavior and state transitions."""

    def test_tc1_computer_accepted(self):
        """TC1: Word 'computer' -> Accepted by DFA."""
        res = simulate_word("computer")
        assert res["is_accepted"] is True
        assert res["final_state"] == "q3"

    def test_tc2_communication_accepted(self):
        """TC2: Word 'communication' -> Accepted by DFA."""
        res = simulate_word("communication")
        assert res["is_accepted"] is True
        assert res["final_state"] == "q3"

    def test_tc3_computation_accepted(self):
        """TC3: Word 'computation' -> Accepted by DFA."""
        res = simulate_word("computation")
        assert res["is_accepted"] is True
        assert res["final_state"] == "q3"

    def test_tc4_complete_accepted(self):
        """TC4: Word 'complete' -> Accepted by DFA."""
        res = simulate_word("complete")
        assert res["is_accepted"] is True
        assert res["final_state"] == "q3"

    def test_tc5_com_accepted(self):
        """TC5: Minimal prefix word 'com' -> Accepted by DFA."""
        res = simulate_word("com")
        assert res["is_accepted"] is True
        assert res["final_state"] == "q3"

    def test_tc6_computer_uppercase_accepted(self):
        """TC6: Word 'COMPUTER' (all uppercase) -> Accepted by DFA."""
        res = simulate_word("COMPUTER")
        assert res["is_accepted"] is True
        assert res["final_state"] == "q3"

    def test_tc7_information_rejected(self):
        """TC7: Word 'information' -> Rejected by DFA (starts with 'i')."""
        res = simulate_word("information")
        assert res["is_accepted"] is False
        assert res["final_state"] == "qd"

    def test_tc8_welcome_rejected(self):
        """TC8: Word 'welcome' -> Rejected by DFA (contains 'come' internally but not prefix)."""
        res = simulate_word("welcome")
        assert res["is_accepted"] is False
        assert res["final_state"] == "qd"

    def test_tc9_computer_punctuation(self):
        """TC9: 'computer,' in document text -> Accepted as 'computer' before punctuation."""
        res = search_dfa("The computer, functioning properly.")
        words = [m.word for m in res.matches]
        assert "computer" in words
        assert res.total_occurrences == 1

    def test_tc10_empty_string_rejected(self):
        """TC10: Empty string -> Rejected."""
        res = simulate_word("")
        assert res["is_accepted"] is False
        assert res["final_state"] == "q0"

    def test_tc11_repeated_words(self):
        """TC11: Repeated matching words -> Each occurrence counted."""
        text = "computer computer computer"
        res = search_dfa(text)
        assert res.total_occurrences == 3
        assert [m.word for m in res.matches] == ["computer", "computer", "computer"]

    def test_tc12_words_separated_by_newlines(self):
        """TC12: Words separated by newlines -> Correctly identified."""
        text = "computer\ncommunication\ncomputation"
        res = search_dfa(text)
        assert res.total_occurrences == 3
        words = [m.word for m in res.matches]
        assert words == ["computer", "communication", "computation"]

    def test_tc13_words_adjacent_to_numbers(self):
        """TC13: Words adjacent to numbers -> Follow defined tokenization rules."""
        text = "123computer456"
        res = search_dfa(text)
        assert res.total_occurrences == 1
        assert res.matches[0].word == "computer"

    def test_tc14_document_without_matches(self):
        """TC14: Document without matching words -> Zero results."""
        text = "The quick brown fox jumps over the lazy dog."
        res = search_dfa(text)
        assert res.total_occurrences == 0
        assert len(res.matches) == 0

    def test_tc15_transition_accuracy(self):
        """Detailed transition step validation for 'computer'."""
        sim = simulate_word("computer")
        assert sim["steps"] == [
            ("q0", "c", "q1"),
            ("q1", "o", "q2"),
            ("q2", "m", "q3"),
            ("q3", "p", "q3"),
            ("q3", "u", "q3"),
            ("q3", "t", "q3"),
            ("q3", "e", "q3"),
            ("q3", "r", "q3")
        ]

