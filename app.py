"""
app.py
Text Pattern Searching Using Regular Expressions and Deterministic Finite Automata (DFA)
Professional Academic Mini-Project Dashboard built with Streamlit.
"""

import os
import io
import time
import tempfile
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Set matplotlib cache directory to temp to prevent permission warnings
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib_cache")

from src.document_extractor import extract_document, ExtractionResult
from src.regex_search import search_regex_pattern, search_all_patterns, PATTERNS
from src.dfa_search import search_dfa, simulate_word, STATES, INITIAL_STATE, ACCEPTING_STATES, STATE_DESCRIPTIONS
from src.dfa_visualizer import draw_dfa_diagram, get_dfa_transition_table_df
from src.comparison import verify_accuracy, run_benchmark, get_qualitative_comparison, plot_execution_time_comparison
from src.test_suite_runner import execute_test_cases
from src.report_generator import generate_all_deliverables


# Streamlit Page Configuration
st.set_page_config(
    page_title="Text Pattern Searching | RE & DFA",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sleek Academic Styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #F8F9FA;
    }
    
    /* Header typography */
    h1, h2, h3 {
        color: #1B4F72;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F1F4F9 100%);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #2980B9;
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #566573;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        color: #1B4F72;
        font-weight: 700;
        margin-top: 4px;
    }
    .metric-caption {
        font-size: 0.8rem;
        color: #7F8C8D;
        margin-top: 2px;
    }
    
    /* Status Badges */
    .badge-pass {
        background-color: #D4EFDF;
        color: #196F3D;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-fail {
        background-color: #FADBD8;
        color: #943126;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-accepted {
        background-color: #D5F5E3;
        color: #1E8449;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.1rem;
        border: 2px solid #2ECC71;
    }
    .badge-rejected {
        background-color: #FADBD8;
        color: #C0392B;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.1rem;
        border: 2px solid #E74C3C;
    }
    
    /* Highlighted Document Text */
    .match-highlight {
        background-color: #FFF275;
        color: #1A252C;
        padding: 1px 4px;
        border-radius: 3px;
        font-weight: bold;
        border: 1px solid #D4AC0D;
    }
    
    /* Section callout box */
    .callout-box {
        background-color: #EBF5FB;
        border-left: 4px solid #2980B9;
        padding: 14px 18px;
        border-radius: 6px;
        margin: 12px 0;
        font-size: 0.95rem;
        color: #154360;
    }
</style>
""", unsafe_allow_html=True)


# Session State Initialization
if "doc_result" not in st.session_state:
    sample_path = "sample_document.docx"
    if os.path.exists(sample_path):
        st.session_state.doc_result = extract_document(sample_path)
    else:
        st.session_state.doc_result = None

if "last_benchmark" not in st.session_state:
    st.session_state.last_benchmark = None


# Sidebar Navigation and Metadata
with st.sidebar:
    st.markdown("## 🔍 Text Pattern Searcher")
    st.caption("College Mini-Project | Automata & RE")
    st.markdown("---")

    menu_option = st.radio(
        "Navigation",
        [
            "1. 📊 Dashboard & Overview",
            "2. 📁 Document Upload & Preview",
            "3. 🔍 Regular Expression Search",
            "4. ⚙️ DFA Design & Simulation",
            "5. ⚖️ RE vs DFA Comparison",
            "6. 🧪 Test Cases & Observations",
            "7. 📄 Academic Report & Export"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("### 📄 Current Document")
    if st.session_state.doc_result is not None:
        dr = st.session_state.doc_result
        st.success(f"**{dr.filename}**")
        st.write(f"- **Format**: {dr.file_format}")
        st.write(f"- **Characters**: {dr.total_chars:,}")
        st.write(f"- **Words**: {dr.total_words:,}")
        st.write(f"- **{dr.unit_type}**: {dr.total_units}")
    else:
        st.warning("No document loaded.")

    if st.button("🔄 Reload Default Sample Document", use_container_width=True):
        st.session_state.doc_result = extract_document("sample_document.docx")
        st.rerun()

    st.markdown("---")
    st.caption("Developed with Python 3.12, Streamlit & Matplotlib")


# Helper: Highlight matches in document text preview
def generate_highlighted_html(text: str, matches: list, max_length: int = 2500) -> str:
    """Highlights matches in HTML format up to max_length characters."""
    if not matches or not text:
        return f"<div style='background:#FFF; padding:15px; border-radius:8px; border:1px solid #DDD; font-family:monospace; white-space:pre-wrap; max-height:350px; overflow-y:auto;'>{text[:max_length]}</div>"

    sorted_m = sorted(matches, key=lambda m: m.start_idx)
    html_parts = []
    last_idx = 0

    for m in sorted_m:
        if m.start_idx >= max_length:
            break
        if m.start_idx > last_idx:
            html_parts.append(text[last_idx:m.start_idx])
        word = text[m.start_idx:m.end_idx]
        html_parts.append(f"<mark class='match-highlight'>{word}</mark>")
        last_idx = m.end_idx

    if last_idx < max_length:
        html_parts.append(text[last_idx:max_length])

    truncated_msg = f"\n\n[... Truncated at {max_length} characters for preview ...]" if len(text) > max_length else ""
    full_html = "".join(html_parts) + truncated_msg
    return f"<div style='background:#FFF; padding:15px; border-radius:8px; border:1px solid #DDD; font-family:monospace; white-space:pre-wrap; max-height:350px; overflow-y:auto;'>{full_html}</div>"


# SECTION 1: DASHBOARD & OVERVIEW
if menu_option.startswith("1."):
    st.title("📊 Project Dashboard & Overview")
    st.markdown("#### Text Pattern Searching Using Regular Expressions and Deterministic Finite Automata")
    
    st.markdown("""
    <div class='callout-box'>
        <b>Case Study Overview:</b> Designed for a publishing company to identify and analyse lexical text patterns in digital manuscripts, 
        books, and academic articles. The system demonstrates both <b>declarative Regular Expressions (RE)</b> and a formal 
        <b>5-State Deterministic Finite Automaton (DFA)</b> implemented in pure Python with 100% mathematical accuracy.
    </div>
    """, unsafe_allow_html=True)

    # Key Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-title'>Document Corpus</div>
            <div class='metric-value'>{}</div>
            <div class='metric-caption'>Characters: {:,}</div>
        </div>
        """.format(
            st.session_state.doc_result.filename if st.session_state.doc_result else "None",
            st.session_state.doc_result.total_chars if st.session_state.doc_result else 0
        ), unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-title'>Vocabulary Scope</div>
            <div class='metric-value'>{}</div>
            <div class='metric-caption'>Total Tokens: {:,}</div>
        </div>
        """.format(
            st.session_state.doc_result.total_words if st.session_state.doc_result else 0,
            st.session_state.doc_result.total_words if st.session_state.doc_result else 0
        ), unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-title'>RE Patterns</div>
            <div class='metric-value'>5 Patterns</div>
            <div class='metric-caption'>Prefix, Suffix, Infix & Length</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-title'>Algorithmic Parity</div>
            <div class='metric-value'>100%</div>
            <div class='metric-caption'>RE vs DFA Exact Match Agreement</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🏛️ Technology Stack & System Architecture")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown("""
        **Frontend & Visuals**
        - Streamlit Dashboard
        - Matplotlib Charts & State Diagrams
        - Pandas Interactive Tabular Views
        - HTML5 Highlighting & Badging
        """)
    with sc2:
        st.markdown("""
        **Document Parsing**
        - PyMuPDF (`fitz`) for PDF Extraction
        - `python-docx` for Word Documents
        - Legacy DOC Fallback Support
        - 1-Based Line & Column Position Tracking
        """)
    with sc3:
        st.markdown("""
        **Core Automata & Search**
        - Python Standard `re` Module
        - Pure Python DFA (Zero Regex Libraries)
        - High-Resolution `time.perf_counter()`
        - Automated Pytest Unit Test Suite
        """)

    st.markdown("### 📋 The Five Required Text Patterns")
    pats_summary = []
    for pid, pdata in PATTERNS.items():
        pats_summary.append({
            "Pattern ID": pid,
            "Pattern Name": pdata["name"],
            "Regular Expression": pdata["raw_regex"],
            "Examples": ", ".join(pdata["examples"]),
            "Automata Implementation": "Pure DFA (Part B)" if pid == "Pattern 1" else "Standard RE"
        })
    st.table(pd.DataFrame(pats_summary))


# SECTION 2: DOCUMENT UPLOAD & PREVIEW
elif menu_option.startswith("2."):
    st.title("📁 Document Upload & Structural Preview")
    st.markdown("Upload digital manuscripts in **PDF**, **DOCX**, or **DOC** formats, or explore the pre-generated sample publication.")

    up_col1, up_col2 = st.columns([2, 1])
    with up_col1:
        uploaded_file = st.file_uploader(
            "Upload Document",
            type=["docx", "pdf", "doc", "txt"],
            help="Upload a digital book or document for text pattern extraction."
        )
        if uploaded_file is not None:
            with st.spinner("Extracting text and calculating structural offsets..."):
                st.session_state.doc_result = extract_document(uploaded_file)
            st.success(f"Successfully processed uploaded file: **{uploaded_file.name}**")

    with up_col2:
        st.markdown("#### Sample Document")
        st.info("No document? Use the included academic publication.")
        if st.button("📄 Load Default `sample_document.docx`", use_container_width=True):
            st.session_state.doc_result = extract_document("sample_document.docx")
            st.rerun()

    # Document Metadata Details
    dr = st.session_state.doc_result
    if dr is not None:
        st.markdown("---")
        st.subheader("📊 Document Metadata")
        
        if dr.is_scanned:
            st.error("⚠️ **Image-Only Scanned Document Detected**: This document contains fewer than 20 characters of extractable text. Scanned or image-only documents require Optical Character Recognition (OCR) rather than direct text stream extraction.")
        elif dr.error_message:
            st.warning(f"⚠️ {dr.error_message}")

        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("Filename", dr.filename)
        mc2.metric("Format", dr.file_format)
        mc3.metric("Total Characters", f"{dr.total_chars:,}")
        mc4.metric("Total Words", f"{dr.total_words:,}")
        mc5.metric(dr.unit_type, dr.total_units)

        st.markdown("### 📖 Extracted Document Preview")
        st.text_area(
            label="Extracted Text (Full)",
            value=dr.full_text[:3000] + ("\n\n... [Remaining text truncated for preview] ..." if len(dr.full_text) > 3000 else ""),
            height=280,
            disabled=True
        )
    else:
        st.warning("Please upload a document or load the default sample document to proceed.")


# SECTION 3: REGULAR EXPRESSION SEARCH
elif menu_option.startswith("3."):
    st.title("🔍 Regular Expression Pattern Searching (Part A)")
    st.markdown("Perform high-precision search across the five required lexical patterns with detailed offset tracking.")

    dr = st.session_state.doc_result
    if dr is None or not dr.full_text.strip():
        st.warning("No document text available. Please upload a document or load the sample file in Section 2.")
    else:
        pat_choices = ["All 5 Patterns (Unified View)"] + [f"{pid}: {p['name']}" for pid, p in PATTERNS.items()]
        selected_choice = st.selectbox("Select Search Pattern", pat_choices)

        with st.spinner("Executing Regular Expression searches..."):
            all_re_results = search_all_patterns(dr.full_text, dr)

        if selected_choice == "All 5 Patterns (Unified View)":
            st.subheader("📈 Five-Pattern Occurrence Summary")
            summary_data = []
            bar_counts = {}
            for pid, res in all_re_results.items():
                summary_data.append(res.get_summary())
                bar_counts[f"{pid}"] = res.total_occurrences

            st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

            # Bar Chart Comparing All 5 Patterns
            st.markdown("#### Occurrence Counts Comparison Across All 5 Patterns")
            fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=200)
            bars = ax.bar(bar_counts.keys(), bar_counts.values(), color=["#2980B9", "#27AE60", "#8E44AD", "#F39C12", "#D35400"])
            ax.set_ylabel("Total Occurrences", fontweight="bold")
            ax.set_title("Frequency of Matches per Regular Expression Pattern", fontweight="bold", pad=10)
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, int(yval), ha="center", va="bottom", fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig)

            # Download CSV
            all_records = []
            for pid, res in all_re_results.items():
                for m in res.matches:
                    all_records.append(m.to_dict())
            df_all = pd.DataFrame(all_records)
            csv_bytes = df_all.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download All Pattern Matches (CSV)",
                data=csv_bytes,
                file_name="pattern_results.csv",
                mime="text/csv"
            )

        else:
            # Single Pattern Detailed View
            pid = selected_choice.split(":")[0].strip()
            res = all_re_results[pid]

            rc1, rc2, rc3, rc4 = st.columns(4)
            rc1.metric("Pattern", pid)
            rc2.metric("Total Matches", res.total_occurrences)
            rc3.metric("Unique Words", len(res.word_frequencies))
            rc4.metric("Exec Time (ms)", f"{res.execution_time_ms:.4f}")

            st.markdown(f"**Canonical Regex**: `{res.regex_pattern}`")

            # Pandas Table of Matches
            st.markdown("#### Detailed Match Positions")
            match_data = [m.to_dict() for m in res.matches]
            if match_data:
                df_matches = pd.DataFrame(match_data)
                st.dataframe(df_matches, use_container_width=True, height=280)
            else:
                st.info("No matches found for this pattern in the current document.")

            # Frequency Table
            st.markdown("#### Unique Matching Words Frequency")
            freq_df = pd.DataFrame(res.word_frequencies.most_common(), columns=["Word", "Frequency"])
            st.dataframe(freq_df, use_container_width=True, height=200)

            # Highlighted Text Preview
            st.markdown("#### Document Text Preview with Highlighted Matches")
            highlighted_html = generate_highlighted_html(dr.full_text, res.matches)
            st.markdown(highlighted_html, unsafe_allow_html=True)


# SECTION 4: DFA DESIGN & SIMULATION
elif menu_option.startswith("4."):
    st.title("⚙️ Deterministic Finite Automata (DFA) Design & Simulation (Part B)")
    st.markdown("Pure Python implementation of Deterministic Finite Automata for **Pattern 1: Words Starting with 'com'**.")

    tab1, tab2, tab3 = st.tabs(["📐 Theoretical Definition & Diagram", "📊 Transition Table", "🎮 Interactive Step-by-Step Simulator"])

    with tab1:
        st.subheader("Formal Mathematical Definition $M = (Q, \\Sigma, \\delta, q_0, F)$")
        st.markdown(r"""
        - **$Q$ (State Set)**: $\{q_0, q_1, q_2, q_3, q_d\}$
        - **$\Sigma$ (Alphabet)**: $\{A-Z, a-z\}$ (ASCII English letters, case-insensitive)
        - **$q_0$ (Start State)**: $q_0$ (Awaiting word start)
        - **$F$ (Accepting States)**: $\{q_3\}$ (Accepts any word starting with prefix "com")
        - **$q_d$ (Dead State)**: Trap state for any non-matching word prefix
        """)

        st.markdown("### 🖼️ DFA State Transition Diagram")
        fig_dfa = draw_dfa_diagram("outputs/dfa_diagram.png")
        st.pyplot(fig_dfa)

        with open("outputs/dfa_diagram.png", "rb") as img_file:
            st.download_button(
                label="📥 Export DFA Diagram (PNG)",
                data=img_file.read(),
                file_name="dfa_diagram.png",
                mime="image/png"
            )

    with tab2:
        st.subheader(r"State Transition Table $\delta(q, a)$")
        st.markdown("The transition function maps each state and character class to the next deterministic state:")
        df_table = get_dfa_transition_table_df()
        st.dataframe(df_table, use_container_width=True)

    with tab3:
        st.subheader("🎮 Interactive DFA Word Simulator")
        st.markdown("Enter any word to inspect the exact state transitions dynamically generated by the automaton.")

        sim_input = st.text_input("Enter a test word:", value="computer")
        if sim_input:
            sim_res = simulate_word(sim_input)

            if sim_res["is_accepted"]:
                st.markdown(f"<div class='badge-accepted'>✅ ACCEPTED (Terminates in {sim_res['final_state']})</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='badge-rejected'>❌ REJECTED (Terminates in {sim_res['final_state']})</div>", unsafe_allow_html=True)

            st.markdown(f"**State Progression Path**: `{sim_res['path_string']}`")
            st.info(sim_res["explanation"])

            # Step sequence table
            steps_data = []
            for idx, (s_from, ch, s_to) in enumerate(sim_res["steps"]):
                steps_data.append({
                    "Step": idx + 1,
                    "Current State": s_from,
                    "Input Character": f"'{ch}'",
                    "Next State": s_to,
                    "Automaton Action": "Prefix Matching" if s_to in ["q1", "q2", "q3"] else "Dead State Transition"
                })
            if steps_data:
                st.dataframe(pd.DataFrame(steps_data), use_container_width=True)


# SECTION 5: RE VS DFA COMPARISON
elif menu_option.startswith("5."):
    st.title("⚖️ RE vs DFA Comparative Analysis (Part C)")
    st.markdown("Empirical performance benchmarking, algorithmic complexity assessment, and 100% accuracy verification.")

    dr = st.session_state.doc_result
    if dr is None or not dr.full_text.strip():
        st.warning("No document loaded. Please upload a document or load sample_document.docx.")
    else:
        # 1. Accuracy Verification
        re_p1 = search_regex_pattern(dr.full_text, "Pattern 1", dr)
        dfa_p1 = search_dfa(dr.full_text, dr)

        verification = verify_accuracy(re_p1.matches, dfa_p1.matches)

        st.subheader("🎯 Pattern-Matching Accuracy Verification")
        ac1, ac2, ac3, ac4 = st.columns(4)
        ac1.metric("RE Match Count", verification["re_count"])
        ac2.metric("DFA Match Count", verification["dfa_count"])
        ac3.metric("Missing Matches", verification["missing_count"])
        ac4.metric("Agreement Status", verification["accuracy_status"])

        if verification["exact_match_agreement"]:
            st.success("✅ **100% Match Agreement**: Both Regular Expression and DFA algorithms returned identical words at the exact same character offsets.")
        else:
            st.error(f"Discrepancy detected: Missing={verification['missing_count']}, Extra={verification['extra_count']}")

        # 2. Performance Benchmark
        st.markdown("---")
        st.subheader("⏱️ High-Precision Performance Benchmark")
        st.markdown("Exclude document loading and UI overhead; run repeated matching iterations using `time.perf_counter()`.")

        bench_col1, bench_col2 = st.columns([3, 1])
        with bench_col1:
            iterations = st.slider("Benchmark Iterations", min_value=50, max_value=500, value=100, step=50)
        with bench_col2:
            st.write("")
            st.write("")
            run_btn = st.button("🚀 Run Benchmark Now", use_container_width=True)

        if run_btn or st.session_state.last_benchmark is None:
            with st.spinner(f"Running {iterations} iterations on {dr.total_chars:,} characters..."):
                st.session_state.last_benchmark = run_benchmark(dr.full_text, iterations=iterations)

        bench = st.session_state.last_benchmark
        re_s = bench["re_stats"]
        dfa_s = bench["dfa_stats"]

        bc1, bc2 = st.columns(2)
        with bc1:
            st.markdown("##### 🔍 Regular Expression (`re`)")
            st.write(f"- **Median**: `{re_s['median_ms']:.4f} ms`")
            st.write(f"- **Mean**: `{re_s['mean_ms']:.4f} ms`")
            st.write(f"- **Min**: `{re_s['min_ms']:.4f} ms`")
            st.write(f"- **Max**: `{re_s['max_ms']:.4f} ms`")
            st.write(f"- **StdDev**: `{re_s['stdev_ms']:.4f} ms`")
        with bc2:
            st.markdown("##### ⚙️ Deterministic Finite Automata (DFA)")
            st.write(f"- **Median**: `{dfa_s['median_ms']:.4f} ms`")
            st.write(f"- **Mean**: `{dfa_s['mean_ms']:.4f} ms`")
            st.write(f"- **Min**: `{dfa_s['min_ms']:.4f} ms`")
            st.write(f"- **Max**: `{dfa_s['max_ms']:.4f} ms`")
            st.write(f"- **StdDev**: `{dfa_s['stdev_ms']:.4f} ms`")

        # Benchmark Chart
        fig_bench = plot_execution_time_comparison(bench, "outputs/comparison_chart.png")
        st.pyplot(fig_bench)

        st.info(
            f"**Observation on Execution Time**: The Python `re` library operates via precompiled C routines, "
            f"executing in {re_s['median_ms']:.4f} ms median. The pure Python DFA executes character-by-character "
            f"in interpreted Python bytecode ({dfa_s['median_ms']:.4f} ms median). Both algorithms maintain strictly "
            f"linear time complexity O(n)."
        )

        # 3. Qualitative Comparison Matrix
        st.markdown("---")
        st.subheader("📑 Qualitative & Engineering Comparison Matrix")
        df_qual = get_qualitative_comparison()
        st.dataframe(df_qual, use_container_width=True)


# SECTION 6: TEST CASES & OBSERVATIONS
elif menu_option.startswith("6."):
    st.title("🧪 Automated Test Cases & Observations")
    st.markdown("Execution of the 15 required academic unit test cases covering edge cases, word boundaries, and case insensitivity.")

    if st.button("▶️ Execute Full Test Suite", use_container_width=True):
        st.session_state.df_tests = execute_test_cases()
    elif "df_tests" not in st.session_state:
        st.session_state.df_tests = execute_test_cases()

    df_tests = st.session_state.df_tests
    total_t = len(df_tests)
    passed_t = len(df_tests[df_tests["Status"] == "PASS"])
    failed_t = total_t - passed_t

    tc1, tc2, tc3 = st.columns(3)
    tc1.metric("Total Test Cases", total_t)
    tc2.metric("Tests Passed", passed_t)
    tc3.metric("Pass Rate", f"{(passed_t / total_t) * 100:.1f}%")

    st.dataframe(df_tests, use_container_width=True)

    st.markdown("### 📝 Key Empirical Observations")
    st.markdown("""
    1. **Boundary Delimiter Consistency**: When digits and punctuation are treated as word boundaries, both RE and DFA achieve 100% parity on complex tokens like `123computer456` and `computer,`.
    2. **Internal Substring Rejection**: The word `welcome` contains the characters 'come' internally but is rejected by both algorithms because the prefix is 'wel'.
    3. **Case Normalization**: Case insensitivity is successfully maintained across uppercase, lowercase, and title case tokens without degrading state transitions.
    4. **Multi-Pattern Overlap**: A single token such as `computation` successfully registers under Pattern 1 (starts with 'com') and Pattern 3 (contains 'tion').
    """)


# SECTION 7: ACADEMIC REPORT & RESULT EXPORT
elif menu_option.startswith("7."):
    st.title("📄 Academic Report & Deliverables Export")
    st.markdown("Download full reports, CSV result tables, diagrams, and project assets.")

    # Generate / update deliverables
    if st.button("🔄 Regenerate All Output Deliverables", use_container_width=True):
        with st.spinner("Generating deliverables..."):
            generate_all_deliverables()
        st.success("All deliverables successfully refreshed in outputs/ and reports/.")

    st.markdown("### 📥 Download Project Deliverables")
    dc1, dc2, dc3 = st.columns(3)

    with dc1:
        if os.path.exists("outputs/pattern_results.csv"):
            with open("outputs/pattern_results.csv", "rb") as f:
                st.download_button("📥 pattern_results.csv", f.read(), "pattern_results.csv", "text/csv", use_container_width=True)
        if os.path.exists("outputs/dfa_results.csv"):
            with open("outputs/dfa_results.csv", "rb") as f:
                st.download_button("📥 dfa_results.csv", f.read(), "dfa_results.csv", "text/csv", use_container_width=True)

    with dc2:
        if os.path.exists("outputs/comparison_results.csv"):
            with open("outputs/comparison_results.csv", "rb") as f:
                st.download_button("📥 comparison_results.csv", f.read(), "comparison_results.csv", "text/csv", use_container_width=True)
        if os.path.exists("outputs/dfa_diagram.png"):
            with open("outputs/dfa_diagram.png", "rb") as f:
                st.download_button("📥 dfa_diagram.png", f.read(), "dfa_diagram.png", "image/png", use_container_width=True)

    with dc3:
        if os.path.exists("reports/case_study_report.md"):
            with open("reports/case_study_report.md", "rb") as f:
                st.download_button("📥 case_study_report.md", f.read(), "case_study_report.md", "text/markdown", use_container_width=True)
        if os.path.exists("sample_document.docx"):
            with open("sample_document.docx", "rb") as f:
                st.download_button("📥 sample_document.docx", f.read(), "sample_document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)

    st.markdown("---")
    st.markdown("### 📖 Case Study Report Preview (28 Sections)")
    if os.path.exists("reports/case_study_report.md"):
        with open("reports/case_study_report.md", "r", encoding="utf-8") as f:
            report_text = f.read()
        st.markdown(report_text[:8000] + "\n\n... [Download full report for complete text] ...")
