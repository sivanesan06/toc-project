"""
create_sample_doc.py
Script to generate the rich academic sample document: 'sample_document.docx'.
Ensures substantial occurrence counts for all five text patterns, mixed case, punctuation, and newlines.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


def generate_sample_docx(filename: str = "sample_document.docx"):
    doc = docx.Document()

    # Document Title
    title = doc.add_paragraph()
    title_run = title.add_run("Applications of Computer Science and Digital Technology")
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(27, 79, 114)  # Deep Navy
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_paragraph()
    sub_run = subtitle.add_run("A Comprehensive Case Study in Text Pattern Searching and Computational Linguistics")
    sub_run.font.size = Pt(13)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(86, 101, 115)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()  # Spacing

    paragraphs_data = [
        (
            "1. Introduction to Modern Computing and Digital Systems",
            "In modern digital society, computer systems and communication networks form the backbone of modern technological infrastructure. "
            "High-speed computation and distributed processing enable real-time information retrieval across vast digital libraries. "
            "Every modern computer relies on fundamental principles of discrete mathematics, formal language theory, and compiler design. "
            "Through advanced communication protocols, digital documents are transferred globally within milliseconds, fostering global education and scientific discovery. "
            "The computing paradigm continues evolving from classical centralized computation toward cloud-based parallel processing architectures, "
            "revolutionizing how students prepare for research and preview scholarly articles."
        ),
        (
            "2. Natural Language Processing and Digital Publishing",
            "Digital publishing enterprises manage extensive archives of books, journals, and articles. "
            "Efficient text searching, indexing, and pattern processing are indispensable for knowledge discovery. "
            "A digital publisher must prepare and preview text streams to identify structural patterns, verify typography, and classify terminology. "
            "Machine learning algorithms facilitate automated language understanding, sentiment classification, and semantic prediction. "
            "During preprocessing, tokenization converts raw text strings into structured tokens, while searching mechanisms evaluate regular expressions. "
            "Whether analyzing a classic text table or training an advanced neural class model, accurate pattern matching guarantees data integrity. "
            "Furthermore, modern publishing systems assist in communication between authors, editors, and reviewers across every educational domain."
        ),
        (
            "3. Automata Theory and Deterministic Pattern Recognition",
            "Automata theory provides the theoretical foundation for computer science, lexer design, and formal verification. "
            "A deterministic finite automaton (DFA) recognizes regular languages with guaranteed linear time efficiency. "
            "Consider searching for words starting with 'com': terms like computer, computation, communication, compiler, and complete are recognized instantly. "
            "The DFA transitions deterministically through states q0, q1, q2, and q3 without requiring backtracking or excessive memory allocation. "
            "In contrast, non-matching terms such as welcome, information, and education transition directly to the rejection state qd. "
            "This mathematical elegance ensures predictable performance even during heavy computational workloads. "
            "Publishing companies utilize these automata for high-throughput syntax checking, document classification, and stream filtering."
        ),
        (
            "4. Pattern Mining and Lexical Analysis in Book Archiving",
            "Document archiving requires scanning millions of words to discover statistical distributions and frequency trends. "
            "Lexical analysis identifies key vocabulary, such as words ending with 'ing' (computing, learning, searching, processing, reasoning, programming) "
            "and words containing 'tion' (information, education, application, communication, computation, automation). "
            "Short five-letter words like apple, table, class, train, model, and logic frequently serve as syntactic anchors or basic conceptual tokens. "
            "Meanwhile, words starting with 'pre' (preprocessing, prediction, preview, prepare) highlight methodological phases in scientific literature. "
            "Publishers must complete thorough quality audits before releasing digital publications to commercial markets."
        ),
        (
            "5. Experimental Evaluation and Case Study Observations",
            "To evaluate algorithmic effectiveness, benchmark experiments compare regular expressions against deterministic finite automata. "
            "Both methods process the same textual corpus containing mixed-case tokens like COMPUTER, Communication, and COMPUTATION. "
            "The system accurately detects isolated punctuation such as computer, complete, and computation! without misclassifying word boundaries. "
            "Even when words are adjacent to digits, such as 123computer456, or separated by newlines, tokenization remains robust and consistent. "
            "The empirical results confirm 100% exact match agreement between the two algorithms, proving that theoretical finite automata "
            "can match production-grade regular expressions in precision while offering transparent state inspection."
        ),
        (
            "6. Summary and Industrial Recommendations",
            "The combination of regular expressions and DFA modeling equips software engineers with powerful tools for text analytics. "
            "For rapid prototyping, regular expressions provide unparalleled agility and compact implementation. "
            "For mission-critical embedded systems and real-time network packet inspection, dedicated DFA engines deliver unmatched determinism and safety. "
            "Publishing platforms that combine both methodologies achieve optimal performance, reliability, and maintainability across all document processing pipelines."
        )
    ]

    for heading, text in paragraphs_data:
        h = doc.add_paragraph()
        h_run = h.add_run(heading)
        h_run.font.size = Pt(14)
        h_run.font.bold = True
        h_run.font.color.rgb = RGBColor(31, 97, 141)  # Steel Blue

        p = doc.add_paragraph()
        p_run = p.add_run(text)
        p_run.font.size = Pt(11)
        p_run.font.name = "Calibri"
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(12)

    # Add a concluding table for structural verification
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Light Shading Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Pattern ID"
    hdr_cells[1].text = "Target Pattern"
    hdr_cells[2].text = "Sample Words in Document"
    hdr_cells[3].text = "Application Domain"

    table_data = [
        ("Pattern 1", "Starts with 'com'", "computer, communication, computation, complete, computing", "Network & Hardware"),
        ("Pattern 2", "Ends with 'ing'", "learning, processing, searching, computing, programming", "Machine Intelligence"),
        ("Pattern 3", "Contains 'tion'", "information, education, application, communication, prediction", "Digital Publishing"),
        ("Pattern 4", "Exactly 5 Letters", "apple, class, table, train, model, logic", "Lexical Tokens"),
        ("Pattern 5", "Starts with 'pre'", "prediction, preprocessing, prepare, preview", "Data Science")
    ]

    for pid, pat, samples, domain in table_data:
        row_cells = table.add_row().cells
        row_cells[0].text = pid
        row_cells[1].text = pat
        row_cells[2].text = samples
        row_cells[3].text = domain

    doc.save(filename)
    print(f"Sample document successfully generated: {filename}")


if __name__ == "__main__":
    generate_sample_docx("sample_document.docx")

