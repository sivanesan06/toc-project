"""
document_extractor.py
Module for extracting text and structural metadata from PDF, DOCX, and DOC documents.
Maintains exact character indices, line/column tracking, and page/paragraph mapping.
"""

import os
import bisect
from typing import Dict, Any, List, Tuple, Optional


class ExtractionResult:
    """Encapsulates extracted text and associated document metadata."""

    def __init__(
        self,
        full_text: str,
        filename: str,
        file_format: str,
        total_chars: int,
        total_words: int,
        total_units: int,  # pages for PDF, paragraphs for DOCX/DOC
        unit_type: str,    # "Pages" or "Paragraphs"
        unit_ranges: List[Tuple[int, int, int]],  # (start_char, end_char, unit_number)
        is_scanned: bool = False,
        error_message: Optional[str] = None
    ):
        self.full_text = full_text
        self.filename = filename
        self.file_format = file_format
        self.total_chars = total_chars
        self.total_words = total_words
        self.total_units = total_units
        self.unit_type = unit_type
        self.unit_ranges = unit_ranges
        self.is_scanned = is_scanned
        self.error_message = error_message
        self.line_offsets = self._compute_line_offsets(full_text)

    @staticmethod
    def _compute_line_offsets(text: str) -> List[int]:
        """Calculates starting character offset of every line (0-based)."""
        offsets = [0]
        for i, char in enumerate(text):
            if char == '\n':
                offsets.append(i + 1)
        return offsets

    def get_position_metadata(self, start_idx: int) -> Tuple[int, int, Optional[int], Optional[int]]:
        """
        Returns (line_number, column_number, page_number, paragraph_number).
        Line and column are 1-based.
        """
        # Find line number (1-based)
        line_idx = bisect.bisect_right(self.line_offsets, start_idx) - 1
        line_num = max(1, line_idx + 1)
        col_num = start_idx - self.line_offsets[line_idx] + 1

        page_num = None
        para_num = None

        unit_num = None
        for start, end, u_num in self.unit_ranges:
            if start <= start_idx < end:
                unit_num = u_num
                break
        if unit_num is None and self.unit_ranges:
            # Fallback to closest unit
            unit_num = self.unit_ranges[-1][2]

        if self.unit_type == "Pages":
            page_num = unit_num
        else:
            para_num = unit_num

        return line_num, col_num, page_num, para_num


def extract_from_pdf(file_source) -> ExtractionResult:
    """
    Extracts text from a PDF file using PyMuPDF (fitz).
    Accepts file path (str) or file-like object (BytesIO).
    """
    import fitz  # PyMuPDF

    doc = None
    try:
        if isinstance(file_source, str):
            doc = fitz.open(file_source)
            filename = os.path.basename(file_source)
        else:
            file_bytes = file_source.read() if hasattr(file_source, 'read') else file_source
            filename = getattr(file_source, 'name', 'uploaded_document.pdf')
            doc = fitz.open(stream=file_bytes, filetype="pdf")

        total_pages = len(doc)
        full_text_parts = []
        unit_ranges: List[Tuple[int, int, int]] = []
        current_offset = 0

        for page_idx in range(total_pages):
            page = doc[page_idx]
            page_text = page.get_text("text")
            # Normalize line endings
            page_text = page_text.replace("\r\n", "\n").replace("\r", "\n")
            if not page_text.endswith("\n") and page_text:
                page_text += "\n"

            start_char = current_offset
            full_text_parts.append(page_text)
            current_offset += len(page_text)
            end_char = current_offset
            unit_ranges.append((start_char, end_char, page_idx + 1))

        full_text = "".join(full_text_parts)
        total_chars = len(full_text)
        total_words = len([w for w in full_text.split() if w])

        is_scanned = (total_pages > 0 and total_chars < 20)

        return ExtractionResult(
            full_text=full_text,
            filename=filename,
            file_format="PDF",
            total_chars=total_chars,
            total_words=total_words,
            total_units=total_pages,
            unit_type="Pages",
            unit_ranges=unit_ranges,
            is_scanned=is_scanned,
            error_message="Image-only scanned PDF detected. Requires OCR." if is_scanned else None
        )
    finally:
        if doc is not None:
            doc.close()


def extract_from_docx(file_source) -> ExtractionResult:
    """
    Extracts text from a DOCX file using python-docx.
    Accepts file path (str) or file-like object (BytesIO).
    """
    import docx
    import io

    if isinstance(file_source, str):
        doc = docx.Document(file_source)
        filename = os.path.basename(file_source)
    else:
        file_bytes = file_source.read() if hasattr(file_source, 'read') else file_source
        if hasattr(file_source, 'seek'):
            file_source.seek(0)
        filename = getattr(file_source, 'name', 'uploaded_document.docx')
        doc = docx.Document(io.BytesIO(file_bytes))

    full_text_parts = []
    unit_ranges: List[Tuple[int, int, int]] = []
    current_offset = 0
    para_count = 0

    for idx, p in enumerate(doc.paragraphs):
        text = p.text.replace("\r\n", "\n").replace("\r", "\n")
        # Keep paragraph delimiter
        text_with_newline = text + "\n"
        start_char = current_offset
        full_text_parts.append(text_with_newline)
        current_offset += len(text_with_newline)
        end_char = current_offset
        unit_ranges.append((start_char, end_char, idx + 1))
        if text.strip():
            para_count += 1

    full_text = "".join(full_text_parts)
    total_chars = len(full_text)
    total_words = len([w for w in full_text.split() if w])

    return ExtractionResult(
        full_text=full_text,
        filename=filename,
        file_format="DOCX",
        total_chars=total_chars,
        total_words=total_words,
        total_units=max(1, para_count),
        unit_type="Paragraphs",
        unit_ranges=unit_ranges,
        is_scanned=False,
        error_message=None
    )


def extract_from_doc(file_source) -> ExtractionResult:
    """
    Extracts text from legacy binary DOC format.
    Attempts extraction via Windows COM Word if available, or provides a detailed message.
    """
    filename = getattr(file_source, 'name', 'document.doc') if not isinstance(file_source, str) else os.path.basename(file_source)

    # Check if win32com is available
    try:
        import win32com.client
        import tempfile

        if not isinstance(file_source, str):
            temp_doc = tempfile.NamedTemporaryFile(delete=False, suffix=".doc")
            temp_doc.write(file_source.read())
            temp_doc.close()
            doc_path = temp_doc.name
        else:
            doc_path = os.path.abspath(file_source)

        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(doc_path)
        full_text = doc.Content.Text
        doc.Close()
        word.Quit()

        if not isinstance(file_source, str):
            os.remove(doc_path)

        full_text = full_text.replace("\r\n", "\n").replace("\r", "\n")
        total_chars = len(full_text)
        total_words = len([w for w in full_text.split() if w])

        return ExtractionResult(
            full_text=full_text,
            filename=filename,
            file_format="DOC (Legacy)",
            total_chars=total_chars,
            total_words=total_words,
            total_units=1,
            unit_type="Paragraphs",
            unit_ranges=[(0, total_chars, 1)],
            is_scanned=False
        )
    except Exception as e:
        # Fallback informative notice for legacy binary DOC
        error_msg = (
            f"Legacy binary DOC format detected ({filename}). "
            "Native direct parsing requires Microsoft Word or LibreOffice conversion. "
            "Please convert this file to .docx or .pdf for full fidelity parsing."
        )
        return ExtractionResult(
            full_text="",
            filename=filename,
            file_format="DOC (Legacy)",
            total_chars=0,
            total_words=0,
            total_units=0,
            unit_type="Paragraphs",
            unit_ranges=[],
            is_scanned=False,
            error_message=error_msg
        )


def extract_document(file_source, filename: Optional[str] = None) -> ExtractionResult:
    """
    Unified entry point for document text extraction.
    Determines document type by extension and applies appropriate extractor.
    """
    if filename is None:
        filename = getattr(file_source, 'name', 'document') if not isinstance(file_source, str) else os.path.basename(file_source)

    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return extract_from_pdf(file_source)
    elif ext == ".docx":
        return extract_from_docx(file_source)
    elif ext == ".doc":
        return extract_from_doc(file_source)
    elif ext == ".txt":
        # Provide TXT support as convenient utility
        if isinstance(file_source, str):
            with open(file_source, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        else:
            raw = file_source.read() if hasattr(file_source, 'read') else file_source
            text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        return ExtractionResult(
            full_text=text,
            filename=filename,
            file_format="TXT",
            total_chars=len(text),
            total_words=len(text.split()),
            total_units=len([line for line in text.split("\n") if line.strip()]),
            unit_type="Lines",
            unit_ranges=[(0, len(text), 1)],
            is_scanned=False
        )
    else:
        return ExtractionResult(
            full_text="",
            filename=filename,
            file_format=ext.upper().replace(".", ""),
            total_chars=0,
            total_words=0,
            total_units=0,
            unit_type="Unknown",
            unit_ranges=[],
            is_scanned=False,
            error_message=f"Unsupported format '{ext}'. Supported formats: .docx, .pdf, .doc, .txt."
        )

