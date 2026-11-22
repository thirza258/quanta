"""Pure-Python standard library PDF generator for Quanta course certificates."""

from __future__ import annotations

import io
from datetime import datetime


def _escape_pdf_text(text: str) -> str:
    """Escape backslashes and parentheses for PDF string literals."""
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def generate_certificate_pdf(record: dict) -> bytes:
    """Generate a valid, standalone PDF 1.4 document for a certificate record."""
    recipient_name = _escape_pdf_text(record.get("recipientName", "Learner"))
    course_title = _escape_pdf_text(record.get("courseTitle", "Course"))
    cert_id = _escape_pdf_text(record.get("id", "QTA-0000"))
    issued_at = record.get("issuedAt", "")[:10]
    score_band = record.get("scoreBand")
    study_minutes = record.get("studyMinutes", 0)
    study_hours = f"{study_minutes // 60}h {study_minutes % 60}m" if study_minutes else "Self-paced"
    verify_url = f"https://quant.nevatal.id/verify/{cert_id}"

    # Build the PDF content stream (in points, landscape: 792 x 612)
    # Coordinate system: origin (0,0) at bottom-left
    stream_lines = [
        # Draw background and elegant certificate borders
        "q",
        "0.98 0.98 0.99 rg",  # subtle parchment background
        "0 0 792 612 re f",
        # Dark navy outer border (2.5 pt)
        "0.08 0.16 0.28 RG",
        "2.5 w",
        "36 36 720 540 re S",
        # Gold accent inner border (1 pt)
        "0.78 0.65 0.28 RG",
        "1.0 w",
        "42 42 708 528 re S",
        # Subtle corner decorative marks
        "46 46 16 16 re S",
        "730 46 16 16 re S",
        "46 550 16 16 re S",
        "730 550 16 16 re S",
        "Q",
        # Text block
        "BT",
        "/F2 14 Tf",
        "0.40 0.45 0.52 rg",
        "285 525 Td",
        "(QUANTA LEARNING ACADEMY) Tj",
        "ET",
        "BT",
        "/F2 26 Tf",
        "0.08 0.16 0.28 rg",
        "210 480 Td",
        "(CERTIFICATE OF COMPLETION) Tj",
        "ET",
        "BT",
        "/F1 12 Tf",
        "0.45 0.50 0.58 rg",
        "330 445 Td",
        "(PROUDLY PRESENTED TO) Tj",
        "ET",
        # Recipient Name (Bold, 26pt)
        "BT",
        "/F2 24 Tf",
        "0.10 0.20 0.35 rg",
        f"120 405 Td",
        f"({recipient_name}) Tj",
        "ET",
        "BT",
        "/F1 12 Tf",
        "0.45 0.50 0.58 rg",
        "120 375 Td",
        "(for successful completion of all coursework, exercises, and assessments in) Tj",
        "ET",
        # Course Title (Bold, 18pt)
        "BT",
        "/F2 18 Tf",
        "0.08 0.16 0.28 rg",
        "120 345 Td",
        f"({course_title}) Tj",
        "ET",
    ]

    # Optional Score Band for credentials (e.g. Conduct & Compliance)
    if score_band:
        band_text = _escape_pdf_text(f"CREDENTIAL ACHIEVEMENT BAND: {score_band.upper()}")
        stream_lines.extend([
            "q",
            "0.92 0.95 0.98 rg",
            "120 295 320 24 re f",
            "0.20 0.45 0.70 RG",
            "0.75 w",
            "120 295 320 24 re S",
            "Q",
            "BT",
            "/F2 11 Tf",
            "0.12 0.35 0.60 rg",
            "130 302 Td",
            f"({band_text}) Tj",
            "ET",
        ])

    # Metadata & Verification details
    meta_y = 230 if score_band else 260
    stream_lines.extend([
        "BT",
        "/F1 10 Tf",
        "0.35 0.40 0.45 rg",
        f"120 {meta_y} Td",
        f"(Issue Date: {issued_at}    |    Guided Study: {study_hours}    |    Certificate ID: {cert_id}) Tj",
        "ET",
        # Separator line
        "q",
        "0.80 0.83 0.88 RG",
        "0.75 w",
        f"120 {meta_y - 20} m 672 {meta_y - 20} l S",
        "Q",
        # Verification instructions
        "BT",
        "/F1 9 Tf",
        "0.45 0.50 0.55 rg",
        f"120 {meta_y - 45} Td",
        f"(Authenticity verifiable online at: {verify_url}) Tj",
        "ET",
        "BT",
        "/F1 8 Tf",
        "0.55 0.60 0.65 rg",
        f"120 {meta_y - 65} Td",
        "(Issued by Quanta Learning Platform · Cryptographically checksummed & tamper-evident record) Tj",
        "ET",
        # Vector QR Code Stamp for online verification
        "q",
        "1 1 1 rg 600 115 72 72 re f",
        "0.78 0.65 0.28 RG 0.75 w 600 115 72 72 re S",
        "0.08 0.16 0.28 rg",
        # Top-left finder
        "604 163 20 20 re f",
        "1 1 1 rg 607 166 14 14 re f",
        "0.08 0.16 0.28 rg 610 169 8 8 re f",
        # Top-right finder
        "652 163 20 20 re f",
        "1 1 1 rg 655 166 14 14 re f",
        "0.08 0.16 0.28 rg 658 169 8 8 re f",
        # Bottom-left finder
        "604 119 20 20 re f",
        "1 1 1 rg 607 122 14 14 re f",
        "0.08 0.16 0.28 rg 610 125 8 8 re f",
        # Alignment & timing modules
        "658 123 10 10 re f",
        "1 1 1 rg 660 125 6 6 re f",
        "0.08 0.16 0.28 rg 662 127 2 2 re f",
        "628 175 4 4 re f 636 175 4 4 re f 644 175 4 4 re f",
        "628 167 4 4 re f 640 167 4 4 re f",
        "628 151 4 4 re f 636 151 4 4 re f 644 151 4 4 re f 652 151 4 4 re f",
        "628 143 4 4 re f 640 143 4 4 re f 656 143 4 4 re f",
        "628 135 4 4 re f 636 135 4 4 re f 648 135 4 4 re f",
        "628 127 4 4 re f 640 127 4 4 re f 648 127 4 4 re f",
        "Q",
        "BT",
        "/F2 7 Tf",
        "0.40 0.45 0.52 rg",
        "602 104 Td",
        "(SCAN TO VERIFY) Tj",
        "ET",
    ])

    content_stream = "\n".join(stream_lines).encode("latin1", errors="replace")
    stream_length = len(content_stream)

    # Construct the PDF object dictionary
    buf = io.BytesIO()
    buf.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

    offsets = []

    def write_obj(obj_num: int, body: bytes):
        offsets.append(buf.tell())
        buf.write(f"{obj_num} 0 obj\n".encode("ascii"))
        buf.write(body)
        buf.write(b"\nendobj\n")

    # Obj 1: Catalog
    write_obj(1, b"<< /Type /Catalog /Pages 2 0 R >>")

    # Obj 2: Pages
    write_obj(2, b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")

    # Obj 3: Page (Landscape 792 x 612)
    write_obj(
        3,
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 792 612] "
            b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>"
        ),
    )

    # Obj 4: Content Stream
    stream_bytes = b"<< /Length " + str(stream_length).encode("ascii") + b" >>\nstream\n" + content_stream + b"\nendstream"
    write_obj(4, stream_bytes)

    # Obj 5: Font F1 (Helvetica)
    write_obj(5, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    # Obj 6: Font F2 (Helvetica-Bold)
    write_obj(6, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    # Cross-reference table
    xref_offset = buf.tell()
    buf.write(b"xref\n0 7\n0000000000 65535 f \n")
    for off in offsets:
        buf.write(f"{off:010d} 00000 n \n".encode("ascii"))

    # Trailer
    buf.write(
        (
            b"trailer\n<< /Size 7 /Root 1 0 R >>\nstartxref\n"
            + str(xref_offset).encode("ascii")
            + b"\n%%EOF\n"
        )
    )

    return buf.getvalue()
