# Text Pattern Searching Using Regular Expressions and Deterministic Finite Automata (DFA)

**Course / Domain**: Theory of Computation / Formal Languages and Automata Theory  
**Application Field**: Digital Publishing, Lexical Analysis, and Computational Linguistics  
**Project Status**: Production-Ready College Mini-Project (100% Match Parity Verified)  

---

## 📌 Executive Summary

This college-level mini-project delivers a complete, modular, and academically rigorous application for searching and analyzing morphological and lexical text patterns across digital books and manuscripts (PDF, DOCX, DOC, TXT).

The application fulfills all requirements of **Part A**, **Part B**, and **Part C** of the case study:
- **Part A (Regular Expressions)**: Implements five core lexical patterns with exact character offset tracking (start index, end index, line number, column number, page/paragraph indices) and visual text highlighting.
- **Part B (Deterministic Finite Automata)**: Selects **Pattern 1 (Words starting with "com")** and models it as a formal 5-state automaton ($M = (Q, \Sigma, \delta, q_0, F)$) executed via pure Python character-by-character scanning with manual ASCII word boundary tokenization—**without importing or utilizing any regex libraries**. Includes a Matplotlib transition diagram and an interactive step-by-step simulator.
- **Part C (RE vs. DFA Comparative Benchmark)**: Benchmarks both algorithms over repeated runs (100 iterations) using `time.perf_counter()`, evaluates software engineering complexity (LOC, maintainability), and executes an automated verification engine that certifies **100% Exact Match Agreement**.

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Language** | Python | `3.11+` (Tested on `3.12.10`) | Core runtime environment |
| **Frontend Dashboard** | Streamlit | `>= 1.35.0` | Modern, responsive academic web dashboard |
| **Pattern Search (RE)** | Python standard `re` | Built-in | Declarative regex matching with ASCII lookarounds |
| **Automata Engine** | Pure Python | Built-in | Character-by-character DFA scanner (zero regex) |
| **PDF Extraction** | PyMuPDF (`fitz`) | `>= 1.24.0` | High-fidelity text stream extraction from PDFs |
| **Word Extraction** | `python-docx` | `>= 1.1.0` | Native extraction from `.docx` manuscripts |
| **Data Analytics** | Pandas | `>= 2.2.0` | Tabular search results, frequencies, and metrics |
| **Visualization** | Matplotlib | `>= 3.8.0` | Publication-grade DFA state diagram & benchmark charts |
| **Unit Testing** | Pytest | `>= 8.0.0` | 26 automated unit test cases (100% passing) |
| **Timer** | `time.perf_counter()` | Built-in | Sub-millisecond wall-clock timing benchmark |

---

## 📂 Project Structure

```
TEXT PATTERN/
│
├── app.py                      # Main Streamlit web application dashboard
├── requirements.txt            # Python dependencies specification
├── README.md                   # Complete documentation and execution guide
├── sample_document.docx        # Pre-generated academic corpus (599 words, 4,965 chars)
├── create_sample_doc.py        # Generator script for sample_document.docx
├── capture_screenshots.py      # Automated Selenium script for capturing live UI screenshots
│
├── src/                        # Modular source code
│   ├── document_extractor.py   # Text & structural extraction (PDF, DOCX, DOC, TXT)
│   ├── regex_search.py         # Part A: Five regex patterns & offset tracking
│   ├── dfa_search.py           # Part B: Pure Python DFA (No regex) & simulator
│   ├── dfa_visualizer.py       # High-res DFA state diagram & transition table
│   ├── comparison.py           # Part C: Benchmark runner, LOC calculator & accuracy engine
│   ├── test_suite_runner.py    # Dynamic executor for the 15 academic test cases
│   └── report_generator.py     # Generator for CSV deliverables & 28-section report
│
├── tests/                      # Automated unit test suite (Pytest)
│   ├── test_regex.py           # Tests for all 5 RE patterns & case-insensitivity
│   ├── test_dfa.py             # Tests for DFA states, boundaries & rejection
│   └── test_comparison.py      # Tests for 100% equivalence & benchmark stability
│
├── outputs/                    # Output deliverables
│   ├── pattern_results.csv     # Detailed CSV results for all 5 RE patterns
│   ├── dfa_results.csv         # Detailed CSV results for the DFA scanner
│   ├── comparison_results.csv  # Benchmark timings (Mean, Median, Min, Max)
│   ├── dfa_diagram.png         # Exported high-res DFA state transition diagram
│   ├── comparison_chart.png    # Side-by-side execution time comparison chart
│   └── screenshots/            # Real screenshots captured from live application
│       ├── 01_homepage.png
│       ├── 02_document_upload.png
│       ├── 03_five_pattern_search.png
│       ├── 04_occurrence_statistics.png
│       ├── 05_dfa_transition_diagram.png
│       ├── 06_dfa_transition_table.png
│       ├── 07_dfa_simulation_results.png
│       ├── 08_re_vs_dfa_comparison.png
│       └── 09_test_cases_and_observations.png
│
└── reports/                    # Academic report folder
    └── case_study_report.md    # Comprehensive 28-section Anna University case study
```

---

## 🚀 Setup and Execution Instructions

### Prerequisites
1. **Python 3.11 or higher** installed and available in your environment.
2. (Optional) Microsoft Word or LibreOffice for native parsing of legacy binary `.doc` files. Modern `.docx` and `.pdf` files are parsed natively without external software.

### 1. Installation
Clone or navigate to the repository directory and install all required packages:
```bash
pip install -r requirements.txt
```

### 2. Running the Application
Launch the Streamlit interactive dashboard:
```bash
streamlit run app.py
```
The application will automatically open in your default browser at `http://localhost:8501`.

### 3. Running Automated Tests
Run the comprehensive Pytest suite:
```bash
pytest tests/ -v
```
All 26 automated unit test cases will execute, validating state transitions, edge cases, and 100% RE vs. DFA match equivalence.

### 4. Regenerating Output Deliverables
To regenerate the sample document, run benchmarks, and update all output CSVs and reports from the CLI:
```bash
python -c "from src.report_generator import generate_all_deliverables; generate_all_deliverables()"
```

---

## 🔍 The Five Text Patterns (Part A)

All patterns apply strict ASCII word boundaries (`(?<![A-Za-z])` and `(?![A-Za-z])`), ensuring punctuation, digits, spaces, and symbols are uniformly treated as token delimiters:

1. **Pattern 1: Words Starting with "com"**  
   - Canonical Regex: `\bcom[A-Za-z]*\b`  
   - Examples: *computer, communication, computation, complete, com*  
   - Matches in Sample Doc: **38 occurrences** (15 unique words)
2. **Pattern 2: Words Ending with "ing"**  
   - Canonical Regex: `\b[A-Za-z]*ing\b`  
   - Examples: *learning, processing, computing, searching*  
   - Matches in Sample Doc: **56 occurrences** (34 unique words)
3. **Pattern 3: Words Containing "tion"**  
   - Canonical Regex: `\b[A-Za-z]*tion[A-Za-z]*\b`  
   - Examples: *information, computation, education, communication*  
   - Matches in Sample Doc: **51 occurrences** (32 unique words)
4. **Pattern 4: Words Containing Exactly Five Letters**  
   - Canonical Regex: `\b[A-Za-z]{5}\b`  
   - Examples: *apple, class, table, train, model*  
   - Matches in Sample Doc: **43 occurrences** (28 unique words)
5. **Pattern 5: Words Starting with "pre"**  
   - Canonical Regex: `\bpre[A-Za-z]*\b`  
   - Examples: *prediction, preprocessing, prepare, preview*  
   - Matches in Sample Doc: **13 occurrences** (7 unique words)

---

## ⚙️ Deterministic Finite Automaton (Part B)

### Formal 5-Tuple Definition: $M = (Q, \Sigma, \delta, q_0, F)$
- **$Q = \{q_0, q_1, q_2, q_3, q_d\}$**: Five deterministic states.
- **$\Sigma = \{A-Z, a-z\}$**: Case-insensitive ASCII English alphabet.
- **$q_0$**: Initial state awaiting the first character of an ASCII word token.
- **$F = \{q_3\}$**: Accepting state (reached when prefix "com" is recognized).
- **$q_d$**: Rejection / Dead state for tokens beginning with any character other than "com".

### Transition Table:
| Current State | Input 'c, C' | Input 'o, O' | Input 'm, M' | Other Letters $[A-Za-z]$ | State Function |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **$\rightarrow q_0$** | **$q_1$** | $q_d$ | $q_d$ | $q_d$ | Initial state |
| **$q_1$** | $q_d$ | **$q_2$** | $q_d$ | $q_d$ | Prefix 'c' matched |
| **$q_2$** | $q_d$ | $q_d$ | **$q_3$** | $q_d$ | Prefix 'co' matched |
| **$* q_3$** | **$q_3$** | **$q_3$** | **$q_3$** | **$q_3$** | **Accepting state**; prefix 'com' matched |
| **$q_d$** | $q_d$ | $q_d$ | $q_d$ | $q_d$ | Dead state; self-loops until delimiter |

---

## ⚖️ RE vs. DFA Benchmark & Verification (Part C)

Tested on `sample_document.docx` (4,965 characters, 599 words) over 100 benchmark iterations:

| Metric | Regular Expression (`re`) | Deterministic Finite Automata (DFA) | Agreement / Verdict |
| :--- | :---: | :---: | :---: |
| **Total Matches Found** | **38** | **38** | **100% Match Agreement** |
| **Missing Matches** | 0 | 0 | None |
| **Extra Matches** | 0 | 0 | None |
| **Median Exec Time** | `0.0450 ms` | `0.4850 ms` | Both $O(n)$ Linear |
| **Mean Exec Time** | `0.0520 ms` | `0.5210 ms` | Fast sub-millisecond |
| **Min Exec Time** | `0.0410 ms` | `0.4420 ms` | Reliable across runs |
| **Max Exec Time** | `0.1180 ms` | `1.0450 ms` | Zero catastrophic spikes |
| **Source LOC** | ~95 lines | ~140 lines | RE is more concise |
| **Implementation Complexity** | Low (Declarative pattern) | Medium (Manual state loop) | DFA provides full transparency |

---

## 🧪 Academic Test Cases (Section 6)

The application includes an automated runner executing 15 mandatory academic test cases:

| TC # | Input Token | Expected Output | Status |
| :---: | :--- | :--- | :---: |
| **TC 01** | `computer` | Accepted ($q_0 \to q_1 \to q_2 \to q_3 \to q_3$) | **PASS** |
| **TC 02** | `communication` | Accepted (Terminates in $q_3$) | **PASS** |
| **TC 03** | `computation` | Accepted (Terminates in $q_3$) | **PASS** |
| **TC 04** | `complete` | Accepted (Terminates in $q_3$) | **PASS** |
| **TC 05** | `com` | Accepted (Minimal prefix token) | **PASS** |
| **TC 06** | `COMPUTER` | Accepted (Case-insensitivity verified) | **PASS** |
| **TC 07** | `information` | Rejected (Transitions to dead state $q_d$) | **PASS** |
| **TC 08** | `welcome` | Rejected (Internal substring rejected) | **PASS** |
| **TC 09** | `computer,` | Accepted ('computer' before punctuation) | **PASS** |
| **TC 10** | `""` (Empty string) | Rejected (Stays in $q_0$) | **PASS** |
| **TC 11** | `computer computer` | 2 distinct occurrences counted | **PASS** |
| **TC 12** | `computer\ncomputation` | Both tokens recognized across newlines | **PASS** |
| **TC 13** | `123computer456` | Extracted 'computer' (Digits are delimiters) | **PASS** |
| **TC 14** | Non-matching text | 0 matches recorded | **PASS** |
| **TC 15** | `computation` | Matched by Pattern 1 AND Pattern 3 | **PASS** |

---

## 📄 Deliverables Summary

- **Streamlit Application**: `app.py`
- **Case Study Report**: `reports/case_study_report.md` (28 complete sections)
- **Sample Document**: `sample_document.docx`
- **Pattern Results CSV**: `outputs/pattern_results.csv`
- **DFA Results CSV**: `outputs/dfa_results.csv`
- **Comparison CSV**: `outputs/comparison_results.csv`
- **DFA Transition Diagram**: `outputs/dfa_diagram.png`
- **Benchmark Chart**: `outputs/comparison_chart.png`
- **Application Screenshots**: `outputs/screenshots/` (9 live captured screenshots)

