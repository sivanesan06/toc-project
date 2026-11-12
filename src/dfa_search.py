"""
dfa_search.py
Pure Python implementation of Deterministic Finite Automata (DFA) for Pattern 1 ("com*").
STRICT REQUIREMENT: NO regex modules or external parsing libraries are imported or used.
Operates via pure character-by-character scanning with manual ASCII word boundary detection.
"""

import time
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter


# Mathematical 5-Tuple Definition of DFA M = (Q, Σ, δ, q0, F)
# Q  = {q0, q1, q2, q3, qd}
# Σ  = {a, b, c, ..., z} (ASCII English letters, case-insensitive)
# q0 = 'q0' (Initial State)
# F  = {'q3'} (Accepting/Final States)
# δ  = Transition Function

STATES = ["q0", "q1", "q2", "q3", "qd"]
INITIAL_STATE = "q0"
ACCEPTING_STATES = {"q3"}

STATE_DESCRIPTIONS = {
    "q0": "Initial State (at start of word)",
    "q1": "State 'c' Matched",
    "q2": "State 'co' Matched",
    "q3": "State 'com' Matched (Accepting)",
    "qd": "Dead / Trap State (Rejected Word)"
}


def is_ascii_letter(char: str) -> bool:
    """Checks whether a character is an ASCII English letter (A-Z, a-z)."""
    return ('a' <= char <= 'z') or ('A' <= char <= 'Z')


def dfa_transition(current_state: str, char: str) -> str:
    """
    Computes δ(current_state, char) using explicit manual transition logic.
    Accepts any character; non-ASCII letters lead to 'qd'.
    """
    if not is_ascii_letter(char):
        return "qd"

    c = char.lower()

    if current_state == "q0":
        return "q1" if c == "c" else "qd"
    elif current_state == "q1":
        return "q2" if c == "o" else "qd"
    elif current_state == "q2":
        return "q3" if c == "m" else "qd"
    elif current_state == "q3":
        # Any subsequent ASCII letter remains in accepting state q3 (prefix matched)
        return "q3"
    elif current_state == "qd":
        # Trap state self-loop on any letter
        return "qd"
    else:
        return "qd"


def simulate_word(word: str) -> Dict[str, Any]:
    """
    Simulates the DFA on a single word string step-by-step.
    Returns the step sequence, final state, path string, and acceptance status.
    """
    if not word:
        return {
            "input": word,
            "steps": [],
            "final_state": INITIAL_STATE,
            "is_accepted": False,
            "path_string": "q0",
            "explanation": "Empty input string is rejected."
        }

    current_state = INITIAL_STATE
    steps: List[Tuple[str, str, str]] = []  # (from_state, char, to_state)
    states_sequence = [INITIAL_STATE]

    for ch in word:
        next_state = dfa_transition(current_state, ch)
        steps.append((current_state, ch, next_state))
        current_state = next_state
        states_sequence.append(current_state)

    is_accepted = (current_state in ACCEPTING_STATES)

    # Form human-readable arrow path e.g. "q0 → q1 → q2 → q3 → q3"
    path_string = " → ".join(states_sequence)

    explanation = (
        f"Input '{word}' terminates in accepting state '{current_state}'. Word is ACCEPTED."
        if is_accepted
        else f"Input '{word}' terminates in non-accepting state '{current_state}'. Word is REJECTED."
    )

    return {
        "input": word,
        "steps": steps,
        "states_sequence": states_sequence,
        "final_state": current_state,
        "is_accepted": is_accepted,
        "path_string": path_string,
        "explanation": explanation
    }


class DFAMatchRecord:
    """Stores metadata for a word accepted by the DFA during document scanning."""

    def __init__(
        self,
        word: str,
        start_idx: int,
        end_idx: int,
        line_num: int,
        col_num: int,
        page_num: Optional[int] = None,
        para_num: Optional[int] = None
    ):
        self.pattern_id = "Pattern 1 (DFA)"
        self.pattern_name = "Words Starting with 'com' [Pure DFA]"
        self.algorithm = "Deterministic Finite Automata"
        self.word = word
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.line_num = line_num
        self.col_num = col_num
        self.page_num = page_num
        self.para_num = para_num

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Algorithm": self.algorithm,
            "Pattern": self.pattern_name,
            "Matched Word": self.word,
            "Start Index": self.start_idx,
            "End Index": self.end_idx,
            "Line": self.line_num,
            "Column": self.col_num,
            "Page": self.page_num if self.page_num is not None else "N/A",
            "Paragraph": self.para_num if self.para_num is not None else "N/A"
        }


class DFASearchResult:
    """Encapsulates the complete results of running the pure DFA scanner."""

    def __init__(
        self,
        matches: List[DFAMatchRecord],
        execution_time_ms: float,
        total_scanned_words: int,
        total_scanned_chars: int
    ):
        self.pattern_id = "Pattern 1"
        self.pattern_name = "Words Starting with 'com'"
        self.matches = matches
        self.total_occurrences = len(matches)
        self.execution_time_ms = execution_time_ms
        self.total_scanned_words = total_scanned_words
        self.total_scanned_chars = total_scanned_chars
        self.word_frequencies = Counter([m.word.lower() for m in matches])

    def get_summary(self) -> Dict[str, Any]:
        return {
            "Algorithm": "Pure DFA (No Regex)",
            "Pattern": self.pattern_name,
            "Total Matches": self.total_occurrences,
            "Unique Words": len(self.word_frequencies),
            "Scanned Words": self.total_scanned_words,
            "Scanned Characters": self.total_scanned_chars,
            "Execution Time (ms)": round(self.execution_time_ms, 4)
        }


def search_dfa(text: str, extraction_result=None) -> DFASearchResult:
    """
    Scans entire document text character-by-character using the pure DFA.
    Treats whitespace, punctuation, digits, and symbols as word delimiters.
    Measures matching execution time via time.perf_counter().
    """
    matches: List[DFAMatchRecord] = []
    text_len = len(text)

    # Pure matching execution benchmark
    t_start = time.perf_counter()

    current_state = INITIAL_STATE
    current_word_chars: List[str] = []
    word_start_idx = 0
    in_word = False
    total_words_scanned = 0

    for i in range(text_len):
        char = text[i]

        if is_ascii_letter(char):
            if not in_word:
                # Start of a new ASCII word token
                in_word = True
                word_start_idx = i
                current_word_chars = [char]
                current_state = dfa_transition(INITIAL_STATE, char)
            else:
                current_word_chars.append(char)
                current_state = dfa_transition(current_state, char)
        else:
            if in_word:
                # Word boundary reached (space, punctuation, digit, newline, etc.)
                total_words_scanned += 1
                if current_state in ACCEPTING_STATES:
                    matched_word = "".join(current_word_chars)
                    word_end_idx = i
                    matches.append((matched_word, word_start_idx, word_end_idx))
                # Reset automaton state for the next word
                in_word = False
                current_state = INITIAL_STATE
                current_word_chars = []

    # Check for trailing word at end of document
    if in_word:
        total_words_scanned += 1
        if current_state in ACCEPTING_STATES:
            matched_word = "".join(current_word_chars)
            word_end_idx = text_len
            matches.append((matched_word, word_start_idx, word_end_idx))

    t_end = time.perf_counter()
    exec_time_ms = (t_end - t_start) * 1000.0

    # Build position metadata outside the timed benchmark
    match_records: List[DFAMatchRecord] = []
    for word, start_idx, end_idx in matches:
        if extraction_result is not None:
            line, col, page, para = extraction_result.get_position_metadata(start_idx)
        else:
            line = text[:start_idx].count('\n') + 1
            last_nl = text[:start_idx].rfind('\n')
            col = start_idx + 1 if last_nl == -1 else start_idx - last_nl
            page, para = None, None

        match_records.append(
            DFAMatchRecord(
                word=word,
                start_idx=start_idx,
                end_idx=end_idx,
                line_num=line,
                col_num=col,
                page_num=page,
                para_num=para
            )
        )

    return DFASearchResult(
        matches=match_records,
        execution_time_ms=exec_time_ms,
        total_scanned_words=total_words_scanned,
        total_scanned_chars=text_len
    )

