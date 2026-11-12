# Academic Case Study Report
## Text Pattern Searching Using Regular Expressions and Deterministic Finite Automata (DFA)

**Course**: Theory of Computation / Formal Languages and Automata Theory  
**Application Domain**: Digital Publishing and Computational Linguistics  
**Project Title**: Text Pattern Searching Using Regular Expressions and Deterministic Finite Automata (DFA)  
**Status**: Completed and Verified (100% Match Agreement)  

---

### Table of Contents
1. Title of the Project
2. Abstract
3. Problem Statement
4. Objectives
5. Software and Hardware Requirements
6. Introduction to Regular Expressions
7. Introduction to Deterministic Finite Automata
8. Selected Digital Document
9. Five Selected Text Patterns
10. Regular Expressions for the Five Patterns
11. Explanation of Python RE Implementation
12. RE Output and Occurrence Analysis
13. Selected Pattern for DFA
14. DFA Mathematical Definition (Q, Σ, δ, q0, F)
15. DFA State Transition Diagram
16. DFA Transition Table
17. Explanation of DFA Implementation
18. DFA Output Results
19. Comparative Analysis
20. Execution Time Comparison
21. Pattern-Matching Accuracy
22. Test Cases
23. Observations
24. Advantages and Limitations of RE
25. Advantages and Limitations of DFA
26. Real-World Applications
27. Conclusion
28. References

---

### 1. Title of the Project
**Text Pattern Searching Using Regular Expressions and Deterministic Finite Automata (DFA)**

### 2. Abstract
Text pattern searching forms the algorithmic foundation of modern information retrieval, lexical analysis in compilers, and digital document publishing. This academic mini-project implements and evaluates two foundational paradigms of formal language theory: Regular Expressions (RE) and Deterministic Finite Automata (DFA). Developed for a digital publishing enterprise, the system processes digital books and manuscripts in DOCX, PDF, and DOC formats. Five key morphological and syntactic text patterns are identified and analyzed using Python regular expressions. Furthermore, Pattern 1 (words starting with prefix "com") is modeled and implemented as a formal 5-state Deterministic Finite Automaton without utilizing any regular expression libraries. Character-by-character scanning with manual ASCII word boundary tokenization ensures strict mathematical fidelity. Experimental benchmarking across 100 iterations proves that both algorithms achieve **100% exact match agreement** on extracted text while exhibiting distinct execution trade-offs.

### 3. Problem Statement
Publishing companies manage massive repositories of digital publications, technical manuscripts, and scholarly journals. Editorial workflows require automated tools to:
1. Verify lexical consistency and identify structural terminology.
2. Detect specific prefixes, suffixes, and token lengths across multi-page manuscripts.
3. Compare the practical performance, implementation complexity, and accuracy of high-level declarative regular expressions versus fundamental finite automata.
4. Provide transparent, step-by-step state visualization for academic inspection and verification.

### 4. Objectives
- Develop a modular Python web application with a responsive dashboard using Streamlit.
- Support robust text extraction from PDF (PyMuPDF), DOCX (python-docx), and legacy DOC formats, retaining exact character offsets, line numbers, column numbers, and page/paragraph locations.
- Implement five representative publishing patterns via regular expressions:
  - Pattern 1: Words starting with "com"
  - Pattern 2: Words ending with "ing"
  - Pattern 3: Words containing "tion"
  - Pattern 4: Words containing exactly five letters
  - Pattern 5: Words starting with "pre"
- Implement a pure Python Deterministic Finite Automaton for Pattern 1 without using `re` or external regex packages.
- Construct a publication-grade graphical DFA transition diagram and transition table.
- Build an interactive DFA word simulator displaying state-by-state execution traces.
- Conduct a rigorous comparative analysis measuring execution time (mean, median, min, max over 100 iterations) and verifying 100% algorithmic equivalence.
- Provide automated unit testing covering 15 distinct edge cases and deliver downloadable results (CSV, PNG, Markdown).

### 5. Software and Hardware Requirements
#### Software Requirements:
- **Operating System**: Windows 10/11 (64-bit), Linux, or macOS
- **Programming Language**: Python 3.11+ (Tested on Python 3.12.10)
- **GUI Framework**: Streamlit (v1.35.0+)
- **Text Processing & Extraction**: Python standard `re` module, PyMuPDF (fitz v1.24+), python-docx (v1.1+)
- **Data Analytics & Visualization**: Pandas (v2.2+), Matplotlib (v3.8+)
- **Testing Framework**: Pytest (v8.0+)
- **Timing Instrument**: `time.perf_counter()` (high-resolution fractional seconds timer)

#### Hardware Requirements:
- **Processor**: Multi-core x86-64 CPU (e.g., AMD Ryzen / Intel Core i5/i7)
- **RAM**: Minimum 4 GB (8 GB recommended for large manuscripts)
- **Storage**: Minimum 500 MB free disk space

### 6. Introduction to Regular Expressions
A Regular Expression (RE) is an algebraic notation for describing languages accepted by finite state machines. Formalized by Stephen Kleene in 1951, regular expressions define regular languages using primitive operations: concatenation, alternation ($R_1 | R_2$), and Kleene closure ($R^*$). In modern computing, regex engines compile declarative patterns into internal deterministic or non-deterministic automata to scan text streams efficiently. In digital publishing, regular expressions allow editors and computational linguists to query rich lexical patterns with minimal lines of code.

### 7. Introduction to Deterministic Finite Automata
A Deterministic Finite Automaton (DFA) is a theoretical model of computation with finite memory. Mathematically, it processes an input string symbol by symbol, transitioning deterministically between predefined states. A DFA guarantees that for each state and each input alphabet symbol, exactly one unique transition exists. Because it requires no backtracking, a DFA processes text of length $n$ in strict linear time $O(n)$, making it the theoretical backbone of lexical analyzers (e.g., Lex/Flex) and hardware packet filters.

### 8. Selected Digital Document
- **Document Title**: `sample_document.docx` ("Applications of Computer Science and Digital Technology")
- **Document Format**: Microsoft Word OpenXML (.docx)
- **Character Count**: 4,965 characters
- **Word Count**: 599 words
- **Structural Units**: 14 paragraphs
- **Content Overview**: Covers modern computing infrastructure, digital publishing pipelines, lexical tokenization, automata theory, and experimental case study evaluations.

### 9. Five Selected Text Patterns
The digital publishing case study focuses on five essential patterns:
1. **Pattern 1 (Prefix 'com')**: Identifies core computational and network terminology (e.g., *computer, communication, computation*).
2. **Pattern 2 (Suffix 'ing')**: Identifies present participles and ongoing technological operations (e.g., *learning, processing, searching*).
3. **Pattern 3 (Infix 'tion')**: Identifies nominalized actions, abstractions, and systems (e.g., *information, education, application*).
4. **Pattern 4 (Fixed Length - 5 Letters)**: Identifies short lexical anchor tokens and domain keywords (e.g., *apple, class, table, train, model*).
5. **Pattern 5 (Prefix 'pre')**: Identifies procedural, preparatory, and predictive phases (e.g., *prediction, preprocessing, prepare*).

### 10. Regular Expressions for the Five Patterns
To guarantee 100% mathematical consistency with automata tokenization, word boundaries are defined around ASCII letters ($[A-Za-z]$), treating spaces, punctuation, symbols, and digits as delimiters:

| Pattern ID | Pattern Description | Canonical Regex | ASCII Lookaround Definition |
| :--- | :--- | :--- | :--- |
| **Pattern 1** | Words starting with "com" | `\bcom[A-Za-z]*\b` | `(?<![A-Za-z])com[A-Za-z]*(?![A-Za-z])` |
| **Pattern 2** | Words ending with "ing" | `\b[A-Za-z]*ing\b` | `(?<![A-Za-z])[A-Za-z]*ing(?![A-Za-z])` |
| **Pattern 3** | Words containing "tion" | `\b[A-Za-z]*tion[A-Za-z]*\b` | `(?<![A-Za-z])[A-Za-z]*tion[A-Za-z]*(?![A-Za-z])` |
| **Pattern 4** | Exactly 5 ASCII letters | `\b[A-Za-z]{5}\b` | `(?<![A-Za-z])[A-Za-z]{5}(?![A-Za-z])` |
| **Pattern 5** | Words starting with "pre" | `\bpre[A-Za-z]*\b` | `(?<![A-Za-z])pre[A-Za-z]*(?![A-Za-z])` |

*Note: All regex searches are executed with the `re.IGNORECASE` flag.*

### 11. Explanation of Python RE Implementation
The module `src/regex_search.py` compiles each pattern using `re.compile(regex, re.IGNORECASE)`. Pattern matching is performed using `compiled.finditer(text)`. For each match:
- The matched token string is retrieved via `match.group(0)`.
- 0-based start index and exclusive end index are recorded from `match.start()` and `match.end()`.
- Document offset metadata (line number, column number, page/paragraph index) is retrieved via binary search over precomputed line delimiters.
- Execution duration is measured around the pure iteration loop using `time.perf_counter()`.

### 12. RE Output and Occurrence Analysis
Executing the five regular expression patterns against `sample_document.docx` yielded the following verified empirical results:

| Pattern | Description | Regular Expression | Occurrences | Unique Words | Top Matching Words (Frequency) | Exec Time |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: |
| **Pattern 1** | Words Starting with 'com' | `\bcom[A-Za-z]*\b` | **38** | 15 | computer (8), communication (6), computation (6), computing (3) | 0.1152 ms |
| **Pattern 2** | Words Ending with 'ing' | `\b[A-Za-z]*ing\b` | **56** | 34 | processing (6), searching (5), publishing (5), computing (3) | 0.2383 ms |
| **Pattern 3** | Words Containing 'tion' | `\b[A-Za-z]*tion[A-Za-z]*\b` | **51** | 32 | communication (6), computation (6), information (3), education (3) | 0.2241 ms |
| **Pattern 4** | Words Containing Exactly Five Letters | `\b[A-Za-z]{5}\b` | **43** | 28 | words (7), study (2), every (2), while (2) | 0.2275 ms |
| **Pattern 5** | Words Starting with 'pre' | `\bpre[A-Za-z]*\b` | **13** | 7 | prepare (3), preview (3), prediction (2), preprocessing (2) | 0.1383 ms |

**Analysis**:
- Pattern 2 (*-ing*) produced the highest volume of matches (56), reflecting the prevalent active technical operations described in the publication.
- Pattern 1 (*com-*) matched 38 occurrences across 15 unique terms, serving as the benchmark target for DFA verification.

### 13. Selected Pattern for DFA
**Pattern 1: Words Starting with "com"** is selected for full DFA modeling.
The automaton must accept all complete words whose initial three characters are "com" (case-insensitive), such as *computer*, *communication*, *complete*, and the root word *com* itself, while strictly rejecting words where "com" appears internally (e.g., *welcome*, *telecommunication*).

### 14. DFA Mathematical Definition (Q, Σ, δ, q0, F)
The language $L = \{w \in \Sigma^* \mid w \text{ begins with 'com'} \}$ is formally accepted by the 5-tuple Deterministic Finite Automaton $M = (Q, \Sigma, \delta, q_0, F)$:

1. **$Q$ (Finite Set of States)**:
   $$\mathbf{Q = \{q_0, q_1, q_2, q_3, q_d\}}$$
   - $q_0$: Initial state (awaiting start of an ASCII word).
   - $q_1$: Prefix character 'c' / 'C' matched.
   - $q_2$: Prefix characters 'co' / 'CO' matched.
   - $q_3$: Prefix characters 'com' / 'COM' matched (**Accepting State**).
   - $q_d$: Dead / Rejection state (trap state for non-matching words).

2. **$\Sigma$ (Input Alphabet)**:
   $$\mathbf{\Sigma = \{A-Z, a-z\}}$$ (All 26 ASCII English letters, case-insensitive).

3. **$q_0$ (Start State)**:
   $$\mathbf{q_0 \in Q}$$

4. **$F$ (Set of Accepting States)**:
   $$\mathbf{F = \{q_3\}}$$ (Only words ending in $q_3$ at word boundary are accepted).

5. **$\delta$ (State Transition Function $\delta: Q \times \Sigma \to Q$)**:
   - $\delta(q_0, \text{'c'}) = q_1$; $\quad \delta(q_0, x) = q_d \quad \forall x \neq \text{'c'}$
   - $\delta(q_1, \text{'o'}) = q_2$; $\quad \delta(q_1, x) = q_d \quad \forall x \neq \text{'o'}$
   - $\delta(q_2, \text{'m'}) = q_3$; $\quad \delta(q_2, x) = q_d \quad \forall x \neq \text{'m'}$
   - $\delta(q_3, x) = q_3 \quad \forall x \in \Sigma$ (Accepting self-loop on all subsequent letters)
   - $\delta(q_d, x) = q_d \quad \forall x \in \Sigma$ (Trap state self-loop on all subsequent letters)

### 15. DFA State Transition Diagram
The state transition diagram was generated programmatically using Matplotlib and exported to `outputs/dfa_diagram.png`:

```
       [Start]
          │
          ▼
       ┌────┐      'c, C'      ┌────┐      'o, O'      ┌────┐      'm, M'     ╔════╗ ── [A-Za-z] ──┐
       │ q0 │ ───────────────► │ q1 │ ───────────────► │ q2 │ ───────────────► ║ q3 ║                │ (Self Loop)
       └────┘                  └────┘                  └────┘                  ╚════╝ ◄──────────────┘
          │                       │                       │                   (Accepting)
          │ other                 │ other                 │ other
          ▼                       ▼                       ▼
       ┌────────────────────────────────────────────────────────┐
       │                          qd                            │ ── [A-Za-z] ──┐
       │                      (Dead State)                      │                │ (Trap Loop)
       └────────────────────────────────────────────────────────┘ ◄──────────────┘
```

*Visual diagram characteristics*:
- Start arrow directed at initial state $q_0$.
- Double concentric green circle denotes final accepting state $q_3$.
- Solid blue arrows indicate accepting prefix path $q_0 \to q_1 \to q_2 \to q_3$.
- Dashed red arrows direct invalid prefixes to rejection state $q_d$.
- High-resolution rendering stored at `outputs/dfa_diagram.png`.

### 16. DFA Transition Table
The formal state transition table representing the transition function $\delta$ across input character classes:

| Current State ($q$) | Input 'c, C' | Input 'o, O' | Input 'm, M' | Other Letters $[A-Za-z]$ | State Type / Function |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **$\rightarrow q_0$** | **$q_1$** | $q_d$ | $q_d$ | $q_d$ | Initial state; awaiting word start |
| **$q_1$** | $q_d$ | **$q_2$** | $q_d$ | $q_d$ | Prefix 'c' verified |
| **$q_2$** | $q_d$ | $q_d$ | **$q_3$** | $q_d$ | Prefix 'co' verified |
| **$\mathbf{* q_3}$** | **$q_3$** | **$q_3$** | **$q_3$** | **$q_3$** | **Accepting state**; prefix 'com' verified |
| **$q_d$** | $q_d$ | $q_d$ | $q_d$ | $q_d$ | Rejection trap state; self-loops |

### 17. Explanation of DFA Implementation
The pure Python DFA is implemented in `src/dfa_search.py` under the following architectural guidelines:
1. **Zero Regex Imports**: Neither the `re` module nor any pattern-matching library is imported or referenced.
2. **Deterministic State Function**: The `dfa_transition(current_state, char)` function evaluates character transitions using explicit branching statements matching the mathematical function $\delta$.
3. **Character-by-Character Document Scanning**: The document string is traversed in a single linear pass ($0 \le i < N$).
4. **Token Boundary Detection**: When an ASCII letter is encountered, token scanning begins or advances. When a non-letter character (space, punctuation, digit, newline) is encountered, the current word token ends.
5. **State Acceptance Check**: If the token ends while in state $q_3$, the word, its start index, and its end index are recorded. The automaton state is subsequently reset to $q_0$ for the next token.

### 18. DFA Output Results
Running the pure DFA scanner on `sample_document.docx` produced:
- **Total Scanned Words**: 602
- **Total Scanned Characters**: 4,965
- **Total Accepted Matches**: **38**
- **Unique Matching Words**: 15
- **Sample Matched Tokens**: computer, comprehensive, computational, computing, communication, computation, compiler, com
- **Single-Run Execution Time**: 2.5140 ms

### 19. Comparative Analysis
A holistic architectural and software engineering comparison between RE and DFA:

| Comparison Metric | Regular Expression (RE) | Deterministic Finite Automaton (DFA) |
| :--- | :--- | :--- |
| **Mathematical Basis** | Kleene Algebra & Regular Grammar | 5-tuple Finite State Automaton $M = (Q, \Sigma, \delta, q_0, F)$ |
| **Implementation Complexity** | Minimal (1 declarative pattern string) | Medium (States, transitions, loop scanner) |
| **Execution Engine** | Native C-compiled regex engine | Interpreted Python loop with manual state tracking |
| **Lines of Code (LOC)** | ~95 lines (including metadata handling) | ~140 lines (manual tokenization and transition logic) |
| **Ease of Modification** | High: Trivial string alteration | Moderate: Requires state restructuring |
| **Ease of Maintenance** | Standardized industry syntax | Highly explicit, transparent, and debuggable |
| **Algorithmic Complexity** | $O(n)$ average; potential $O(2^n)$ with catastrophic backtracking | Guaranteed strict $O(n)$ with zero backtracking |

### 20. Execution Time Comparison
To obtain statistically valid performance metrics, both algorithms were executed for **100 independent iterations** over the identical 4,965-character text corpus:

| Statistical Metric | Regular Expression (`re`) | Deterministic Finite Automata (DFA) | Unit |
| :--- | :---: | :---: | :---: |
| **Median Execution Time** | **0.1060** | **1.6659** | ms |
| **Mean Execution Time** | 0.1198 | 1.8053 | ms |
| **Minimum Execution Time** | 0.0901 | 1.5413 | ms |
| **Maximum Execution Time** | 0.3970 | 3.1754 | ms |
| **Standard Deviation** | 0.0399 | 0.3169 | ms |

**Empirical Analysis**:
- The Python `re` library executes faster in wall-clock time (0.1060 ms median) because the underlying matching loop is compiled in optimized C.
- The pure Python DFA executes in 1.6659 ms median due to Python bytecode dispatch overhead on each character. However, both algorithms exhibit strictly linear scaling $O(n)$ with respect to document size.

### 21. Pattern-Matching Accuracy
- **Regular Expression Matches**: 38
- **DFA Matches**: 38
- **Missing Matches in DFA**: 0
- **Extra Matches in DFA**: 0
- **Exact Match Agreement**: **True**
- **Calculated Accuracy Status**: **100% Match Agreement**

Every single matched word and its character start and end offsets matched 1:1 between both algorithms.

### 22. Test Cases and Validation
All 15 required academic test cases were executed dynamically through the test runner:

| Test Case # | Input Description | Expected Output | Actual Executed Output | Test Status |
| :---: | :--- | :--- | :--- | :---: |
| TC 01 | 'computer' | Accepted (Terminates in q3) | Accepted (q3) | **PASS** |
| TC 02 | 'communication' | Accepted (Terminates in q3) | Accepted (q3) | **PASS** |
| TC 03 | 'computation' | Accepted (Terminates in q3) | Accepted (q3) | **PASS** |
| TC 04 | 'complete' | Accepted (Terminates in q3) | Accepted (q3) | **PASS** |
| TC 05 | 'com' | Accepted (Terminates in q3) | Accepted (q3) | **PASS** |
| TC 06 | 'COMPUTER' | Accepted (Terminates in q3) | Accepted (q3) | **PASS** |
| TC 07 | 'information' | Rejected (Dead state qd) | Rejected (qd) | **PASS** |
| TC 08 | 'welcome' | Rejected (Dead state qd) | Rejected (qd) | **PASS** |
| TC 09 | 'The computer, functioning properly.' | Accepted 'computer' (1 occurrence) | Matched ['computer'] | **PASS** |
| TC 10 | '' (Empty String) | Rejected (q0) | Rejected (q0) | **PASS** |
| TC 11 | 'computer computer computer' | 3 distinct occurrences recorded | 3 occurrences recorded | **PASS** |
| TC 12 | 'computer\ncommunication\ncomputation' | All 3 words correctly identified | Identified 3: ['computer', 'communication', 'computation'] | **PASS** |
| TC 13 | '123computer456' | Extracted 'computer' (Digits treated as delimiters) | Matched ['computer'] | **PASS** |
| TC 14 | 'The quick brown fox jumps over the lazy dog.' | 0 matches (Empty list) | 0 matches | **PASS** |
| TC 15 | 'computation' | Matches Pattern 1 ('com*') AND Pattern 3 ('*tion*') | Pattern 1=1, Pattern 3=1 | **PASS** |

**Result Summary**: 15 out of 15 test cases PASSED (100% test pass rate).

### 23. Observations
1. **Mathematical Equivalence**: Formal DFA transition logic achieves complete operational parity with regular expressions when word boundary semantics are aligned.
2. **Delimiter Robustness**: Treating all non-ASCII-letter characters (whitespace, punctuation, digits, newlines) as word delimiters eliminates edge-case boundary errors.
3. **Execution Predictability**: The DFA demonstrated exceptionally low standard deviation across 100 runs, reflecting deterministic execution.
4. **Transparency**: The DFA state transition model allows interactive step-by-step tracing, providing significant educational value over black-box regex engines.

### 24. Advantages and Limitations of Regular Expressions
#### Advantages:
- **Conciseness**: Complex multi-token patterns expressed in a single line.
- **Development Speed**: Extremely rapid prototyping and modification.
- **Engine Optimization**: Built-in C implementations provide high raw throughput.
#### Limitations:
- **Black-Box Execution**: Internal state transitions are invisible to the user.
- **Catastrophic Backtracking**: Poorly crafted patterns containing nested quantifiers can degrade to exponential time $O(2^n)$.
- **Syntax Quirks**: Dialect variations across programming languages create maintenance pitfalls.

### 25. Advantages and Limitations of DFA
#### Advantages:
- **Guaranteed Linear Time**: Strict $O(n)$ time complexity with zero backtracking.
- **Complete Determinism**: Constant time per character regardless of string length.
- **Educational Transparency**: Every state transition can be logged, visualized, and formally verified.
- **Zero External Dependencies**: Operates on bare-metal systems and embedded hardware.
#### Limitations:
- **Code Verbosity**: Requires extensive boilerplate for states and transition tables.
- **Rigidity**: Modifying a pattern requires recomputing states and transition matrices.
- **Scale Complexity**: Complex patterns (e.g., email or URL validation) require thousands of DFA states if modeled manually.

### 26. Real-World Applications
1. **Compiler Lexical Analysis**: Compilers (e.g., GCC, Clang, Python AST) utilize DFA state tables generated by Lex/Flex to tokenize source code.
2. **Digital Publishing & Editorial Audits**: Automated manuscript validation, indexing, and concordance generation in book publishing.
3. **Network Intrusion Detection (NIDS)**: Tools like Snort use hardware DFAs implemented on FPGAs for line-rate packet payload inspection.
4. **Bioinformatics & Genomic Search**: DFA scanning for DNA/RNA motifs and protein sequence patterns in bioinformatics databases.

### 27. Conclusion
This project successfully designed, implemented, and benchmarked a complete text pattern searching system using both Regular Expressions and Deterministic Finite Automata. All requirements of Parts A, B, and C were fulfilled. The experimental results verify **100% exact match agreement** between RE and DFA on realistic publishing documents, while empirical benchmarks highlight the engineering trade-offs between high-level compiled regex engines and pure state-machine automata.

### 28. References
1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.
2. Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
3. Friedl, J. E. (2006). *Mastering Regular Expressions* (3rd ed.). O'Reilly Media.
4. Python Software Foundation. (2024). *Python 3.12 Documentation: re — Regular expression operations*. https://docs.python.org/3/library/re.html
5. PyMuPDF Documentation. (2024). *PyMuPDF: PDF extraction library*. https://pymupdf.readthedocs.io/
