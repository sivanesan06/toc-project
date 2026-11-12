"""
regex_search.py
Implementation of text pattern searching using Python's regular expressions (re module).
Matches five required patterns using strict ASCII word boundaries.
"""

import re
import time
from typing import List, Dict, Any, Optional
from collections import Counter


# Definition of the Five Core Patterns
# Note: (?<![A-Za-z]) and (?![A-Za-z]) strictly define word boundaries around ASCII letters,
# treating whitespace, punctuation, symbols, and digits as word separators consistently with DFA.
PATTERNS = {
    "Pattern 1": {
        "name": "Words Starting with 'com'",
        "regex": r"(?<![A-Za-z])com[A-Za-z]*(?![A-Za-z])",
        "raw_regex": r"\bcom[A-Za-z]*\b",
        "description": "Matches words starting with the prefix 'com', case-insensitive.",
        "examples": ["computer", "communication", "computation", "complete", "com"]
    },
    "Pattern 2": {
        "name": "Words Ending with 'ing'",
        "regex": r"(?<![A-Za-z])[A-Za-z]*ing(?![A-Za-z])",
        "raw_regex": r"\b[A-Za-z]*ing\b",
        "description": "Matches words ending with the suffix 'ing', case-insensitive.",
        "examples": ["learning", "processing", "computing", "searching"]
    },
    "Pattern 3": {
        "name": "Words Containing 'tion'",
        "regex": r"(?<![A-Za-z])[A-Za-z]*tion[A-Za-z]*(?![A-Za-z])",
        "raw_regex": r"\b[A-Za-z]*tion[A-Za-z]*\b",
        "description": "Matches words containing the substring 'tion', case-insensitive.",
        "examples": ["information", "computation", "education", "communication"]
    },
    "Pattern 4": {
        "name": "Words Containing Exactly Five Letters",
        "regex": r"(?<![A-Za-z])[A-Za-z]{5}(?![A-Za-z])",
        "raw_regex": r"\b[A-Za-z]{5}\b",
        "description": "Matches words consisting of exactly five ASCII letters, case-insensitive.",
        "examples": ["apple", "class", "table", "train"]
    },
    "Pattern 5": {
        "name": "Words Starting with 'pre'",
        "regex": r"(?<![A-Za-z])pre[A-Za-z]*(?![A-Za-z])",
        "raw_regex": r"\bpre[A-Za-z]*\b",
        "description": "Matches words starting with the prefix 'pre', case-insensitive.",
        "examples": ["prediction", "preprocessing", "prepare", "preview"]
    }
}


class MatchRecord:
    """Stores detailed metadata for a single pattern match."""

    def __init__(
        self,
        pattern_id: str,
        pattern_name: str,
        regex_pattern: str,
        word: str,
        start_idx: int,
        end_idx: int,
        line_num: int,
        col_num: int,
        page_num: Optional[int] = None,
        para_num: Optional[int] = None
    ):
        self.pattern_id = pattern_id
        self.pattern_name = pattern_name
        self.regex_pattern = regex_pattern
        self.word = word
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.line_num = line_num
        self.col_num = col_num
        self.page_num = page_num
        self.para_num = para_num

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Pattern ID": self.pattern_id,
            "Pattern Name": self.pattern_name,
            "Regex": self.regex_pattern,
            "Matched Word": self.word,
            "Start Index": self.start_idx,
            "End Index": self.end_idx,
            "Line": self.line_num,
            "Column": self.col_num,
            "Page": self.page_num if self.page_num is not None else "N/A",
            "Paragraph": self.para_num if self.para_num is not None else "N/A"
        }


class PatternSearchResult:
    """Holds complete results for a single pattern search execution."""

    def __init__(
        self,
        pattern_id: str,
        pattern_name: str,
        regex_pattern: str,
        matches: List[MatchRecord],
        execution_time_ms: float
    ):
        self.pattern_id = pattern_id
        self.pattern_name = pattern_name
        self.regex_pattern = regex_pattern
        self.matches = matches
        self.total_occurrences = len(matches)
        self.execution_time_ms = execution_time_ms
        self.word_frequencies = Counter([m.word.lower() for m in matches])

    def get_summary(self) -> Dict[str, Any]:
        return {
            "Pattern": f"{self.pattern_id}: {self.pattern_name}",
            "Regex": self.regex_pattern,
            "Total Occurrences": self.total_occurrences,
            "Unique Words": len(self.word_frequencies),
            "Execution Time (ms)": round(self.execution_time_ms, 4)
        }


def search_regex_pattern(
    text: str,
    pattern_id: str,
    extraction_result=None
) -> PatternSearchResult:
    """
    Executes a regex search for the specified pattern ID over the input text.
    Uses time.perf_counter() to capture pure matching time.
    """
    if pattern_id not in PATTERNS:
        raise ValueError(f"Unknown pattern ID '{pattern_id}'. Available: {list(PATTERNS.keys())}")

    pinfo = PATTERNS[pattern_id]
    regex_str = pinfo["regex"]
    compiled = re.compile(regex_str, re.IGNORECASE)

    # Pure execution time benchmark
    t_start = time.perf_counter()
    raw_matches = list(compiled.finditer(text))
    t_end = time.perf_counter()
    exec_time_ms = (t_end - t_start) * 1000.0

    match_records: List[MatchRecord] = []
    for m in raw_matches:
        start_idx = m.start()
        end_idx = m.end()
        word = m.group(0)

        if extraction_result is not None:
            line, col, page, para = extraction_result.get_position_metadata(start_idx)
        else:
            # Fallback calculation if no extraction_result passed
            line = text[:start_idx].count('\n') + 1
            last_nl = text[:start_idx].rfind('\n')
            col = start_idx + 1 if last_nl == -1 else start_idx - last_nl
            page, para = None, None

        match_records.append(
            MatchRecord(
                pattern_id=pattern_id,
                pattern_name=pinfo["name"],
                regex_pattern=pinfo["raw_regex"],
                word=word,
                start_idx=start_idx,
                end_idx=end_idx,
                line_num=line,
                col_num=col,
                page_num=page,
                para_num=para
            )
        )

    return PatternSearchResult(
        pattern_id=pattern_id,
        pattern_name=pinfo["name"],
        regex_pattern=pinfo["raw_regex"],
        matches=match_records,
        execution_time_ms=exec_time_ms
    )


def search_all_patterns(text: str, extraction_result=None) -> Dict[str, PatternSearchResult]:
    """Runs all 5 regular expression searches on the document text."""
    results = {}
    for pid in PATTERNS.keys():
        results[pid] = search_regex_pattern(text, pid, extraction_result)
    return results

