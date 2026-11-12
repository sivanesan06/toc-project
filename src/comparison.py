"""
comparison.py
Module for comparative analysis between Regular Expression (RE) and Deterministic Finite Automata (DFA).
Performs automated 100% accuracy verification and multi-iteration execution time benchmarking.
"""

import os
import time
import statistics
from typing import Dict, Any, List, Tuple
import pandas as pd
import matplotlib.pyplot as plt

from src.regex_search import search_regex_pattern
from src.dfa_search import search_dfa


def count_loc(file_path: str) -> int:
    """Calculates non-blank, non-comment lines of Python code."""
    if not os.path.exists(file_path):
        return 0
    loc = 0
    in_multiline = False
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                    in_multiline = not in_multiline
                continue
            if in_multiline:
                if '"""' in stripped or "'''" in stripped:
                    in_multiline = False
                continue
            if stripped.startswith("#"):
                continue
            loc += 1
    return loc


def verify_accuracy(re_matches: List[Any], dfa_matches: List[Any]) -> Dict[str, Any]:
    """
    Automated verification system comparing RE and DFA match results.
    Verifies match counts, exact word texts, and exact character offsets.
    Only returns '100% Match Agreement' when both match sets are identical.
    """
    re_tuples = [(m.word.lower(), m.start_idx, m.end_idx) for m in re_matches]
    dfa_tuples = [(m.word.lower(), m.start_idx, m.end_idx) for m in dfa_matches]

    re_count = len(re_tuples)
    dfa_count = len(dfa_tuples)

    # Missing in DFA: present in RE but not in DFA
    missing_matches = [t for t in re_tuples if t not in dfa_tuples]
    # Extra in DFA: present in DFA but not in RE
    extra_matches = [t for t in dfa_tuples if t not in re_tuples]

    # Exact equality check (both order and elements)
    exact_match_agreement = (re_tuples == dfa_tuples)
    match_percentage = 100.0 if exact_match_agreement else (
        round((1.0 - (len(missing_matches) + len(extra_matches)) / max(1, re_count + dfa_count)) * 100.0, 2)
    )

    accuracy_status = "100% Match Agreement" if exact_match_agreement else f"Discrepancy ({match_percentage}% Match)"

    return {
        "re_count": re_count,
        "dfa_count": dfa_count,
        "exact_match_agreement": exact_match_agreement,
        "match_percentage": match_percentage,
        "missing_count": len(missing_matches),
        "extra_count": len(extra_matches),
        "missing_matches": missing_matches,
        "extra_matches": extra_matches,
        "accuracy_status": accuracy_status
    }


def run_benchmark(text: str, iterations: int = 100) -> Dict[str, Any]:
    """
    Benchmarks RE and DFA algorithms over repeated iterations on identical text.
    Strictly excludes file loading, document extraction, and UI rendering from measurement.
    Calculates Mean, Median, Min, Max, and Standard Deviation in milliseconds.
    """
    re_times: List[float] = []
    dfa_times: List[float] = []

    # Import direct matching functions to avoid any overhead
    import re
    compiled_re = re.compile(r"(?<![A-Za-z])com[A-Za-z]*(?![A-Za-z])", re.IGNORECASE)
    from src.dfa_search import dfa_transition, is_ascii_letter, INITIAL_STATE, ACCEPTING_STATES

    text_len = len(text)

    # Benchmark Loop
    for _ in range(iterations):
        # 1. Benchmark Regular Expression
        t0 = time.perf_counter()
        _ = list(compiled_re.finditer(text))
        t1 = time.perf_counter()
        re_times.append((t1 - t0) * 1000.0)

        # 2. Benchmark DFA
        t2 = time.perf_counter()
        state = INITIAL_STATE
        in_word = False
        dfa_found = 0
        for i in range(text_len):
            ch = text[i]
            if is_ascii_letter(ch):
                if not in_word:
                    in_word = True
                    state = dfa_transition(INITIAL_STATE, ch)
                else:
                    state = dfa_transition(state, ch)
            else:
                if in_word:
                    if state in ACCEPTING_STATES:
                        dfa_found += 1
                    in_word = False
                    state = INITIAL_STATE
        if in_word and state in ACCEPTING_STATES:
            dfa_found += 1
        t3 = time.perf_counter()
        dfa_times.append((t3 - t2) * 1000.0)

    re_stats = {
        "mean_ms": round(statistics.mean(re_times), 4),
        "median_ms": round(statistics.median(re_times), 4),
        "min_ms": round(min(re_times), 4),
        "max_ms": round(max(re_times), 4),
        "stdev_ms": round(statistics.stdev(re_times), 4) if len(re_times) > 1 else 0.0
    }

    dfa_stats = {
        "mean_ms": round(statistics.mean(dfa_times), 4),
        "median_ms": round(statistics.median(dfa_times), 4),
        "min_ms": round(min(dfa_times), 4),
        "max_ms": round(max(dfa_times), 4),
        "stdev_ms": round(statistics.stdev(dfa_times), 4) if len(dfa_times) > 1 else 0.0
    }

    speed_ratio = round(dfa_stats["median_ms"] / max(0.0001, re_stats["median_ms"]), 2)

    return {
        "iterations": iterations,
        "re_stats": re_stats,
        "dfa_stats": dfa_stats,
        "speed_ratio": speed_ratio,
        "re_raw_times": re_times,
        "dfa_raw_times": dfa_times
    }


def get_qualitative_comparison(base_dir: str = ".") -> pd.DataFrame:
    """Returns the comprehensive qualitative and structural comparison matrix."""
    re_loc = count_loc(os.path.join(base_dir, "src", "regex_search.py"))
    dfa_loc = count_loc(os.path.join(base_dir, "src", "dfa_search.py"))

    comparison_data = [
        {
            "Comparison Criterion": "1. Mathematical Model",
            "Regular Expression (RE)": "Declarative pattern syntax compiled into NFA/DFA engine",
            "Deterministic Finite Automata (DFA)": "Formal 5-tuple M = (Q, Σ, δ, q0, F) state machine"
        },
        {
            "Comparison Criterion": "2. Implementation Complexity",
            "Regular Expression (RE)": "Low: Expressive 1-line regex pattern expression",
            "Deterministic Finite Automata (DFA)": "Medium-High: Explicit states, transition table, boundary scanner"
        },
        {
            "Comparison Criterion": "3. Source Code Lines (LOC)",
            "Regular Expression (RE)": f"{re_loc} lines (including metadata & search driver)",
            "Deterministic Finite Automata (DFA)": f"{dfa_loc} lines (pure manual implementation without regex)"
        },
        {
            "Comparison Criterion": "4. Execution Mechanism",
            "Regular Expression (RE)": "Compiled C-extension pattern matcher (Python re engine)",
            "Deterministic Finite Automata (DFA)": "Interpreted Python character-by-character loop transition"
        },
        {
            "Comparison Criterion": "5. Ease of Modification",
            "Regular Expression (RE)": "Very Easy: Modify regex string (e.g., change prefix to 'inter')",
            "Deterministic Finite Automata (DFA)": "Moderate-Hard: Requires modifying states, transition conditions, and diagram"
        },
        {
            "Comparison Criterion": "6. Ease of Maintenance",
            "Regular Expression (RE)": "High standard readability for experienced developers",
            "Deterministic Finite Automata (DFA)": "Self-documenting explicit states; no cryptic regex syntax"
        },
        {
            "Comparison Criterion": "7. Algorithmic Time Complexity",
            "Regular Expression (RE)": "O(n) for linear patterns; worst-case exponential if catastrophic backtracking",
            "Deterministic Finite Automata (DFA)": "Guaranteed strict linear time O(n) where n is text character length"
        },
        {
            "Comparison Criterion": "8. Key Advantages",
            "Regular Expression (RE)": "Rapid development, highly concise, backed by native C optimization",
            "Deterministic Finite Automata (DFA)": "Zero third-party library dependency, fully inspectable, predictable runtime"
        },
        {
            "Comparison Criterion": "9. Key Limitations",
            "Regular Expression (RE)": "Internal engine behaves as a black-box; risk of regex complexity bugs",
            "Deterministic Finite Automata (DFA)": "Higher code volume, requires manual token boundary logic"
        }
    ]

    return pd.DataFrame(comparison_data)


def plot_execution_time_comparison(benchmark_results: Dict[str, Any], output_path: str = "outputs/comparison_chart.png"):
    """Creates a side-by-side bar chart of execution times (Median, Mean, Min)."""
    re_s = benchmark_results["re_stats"]
    dfa_s = benchmark_results["dfa_stats"]

    metrics = ["Median Time", "Mean Time", "Min Time", "Max Time"]
    re_vals = [re_s["median_ms"], re_s["mean_ms"], re_s["min_ms"], re_s["max_ms"]]
    dfa_vals = [dfa_s["median_ms"], dfa_s["mean_ms"], dfa_s["min_ms"], dfa_s["max_ms"]]

    x = range(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    rects1 = ax.bar([i - width/2 for i in x], re_vals, width, label="Regular Expression (re)", color="#2980B9")
    rects2 = ax.bar([i + width/2 for i in x], dfa_vals, width, label="Deterministic Finite Automata (DFA)", color="#27AE60")

    ax.set_ylabel("Execution Time (milliseconds)", fontsize=11, fontweight="bold")
    ax.set_title(f"Performance Benchmark: RE vs DFA ({benchmark_results['iterations']} Iterations)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=10, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Attach value labels on bars
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f"{h:.3f} ms", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#1B4F72")

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"{h:.3f} ms", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#145A32")

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    return fig

