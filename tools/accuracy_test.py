"""
accuracy_test.py

Implements the accuracy test described in ACCURACY_REPORT_TEMPLATE.md /
brief section 14.

WHAT IT DOES
------------
1. Pulls every field from every *Verified* document (documents you've
   already uploaded, OCR'd, corrected on the verification screen, and
   approved) out of extracted_fields.
2. Compares ocr_value to corrected_value per field to decide whether the
   OCR was "correct" for that field.
3. Buckets fields into the same categories as the report template
   (Printed text, Handwritten names, Numbers, Dates, Addresses, Checkboxes,
   Signature presence) and computes accuracy per category, per form, and
   overall.
4. Prints a human-readable summary to the console AND writes a filled-in
   markdown report to accuracy_report_<timestamp>.md using the same table
   layout as ACCURACY_REPORT_TEMPLATE.md, so you can hand it in directly.

HOW TO USE
----------
1. Upload at least 10 real filled-in forms through upload.html (a mix of
   deposit and share applications), run OCR, and go through the
   verification screen for each one, correcting any wrong fields and
   clicking Approve/Verify. This is what makes them "Verified" and what
   generates the ground truth (corrected_value) this script needs -
   there's no separate ground-truth spreadsheet to fill in by hand,
   because the verification screen *is* the ground-truth entry step.
2. Run:
       python tools/accuracy_test.py
   from the project root (with the venv activated, same as the backend).

MATCHING RULE
-------------
A field counts as "correct" if ocr_value matches corrected_value after
trimming whitespace and ignoring case. This mirrors realistic usage: an
employee accepting the OCR value as-is (not touching the field) also
counts as correct, since corrected_value is seeded from ocr_value at
verification time and only overwritten if the employee edits it - check
database.py / your verification screen if that assumption doesn't match
your actual save behaviour.
"""

import datetime
import os
import sqlite3
import sys
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))
from database import DB_PATH  # noqa: E402


# ---------------------------------------------------------------------------
# Field -> report category mapping
# ---------------------------------------------------------------------------
# Anything not listed explicitly here falls back to a category based on its
# field_type in extracted_fields (checkbox -> Checkboxes, signature ->
# Signature presence, date -> Dates), and finally to "Printed text" for any
# remaining plain-text field. Adjust the explicit lists below if your real
# forms categorise a field differently.

HANDWRITTEN_NAME_FIELDS = {
    "applicant_name", "father_or_husband_name", "first_depositor_name",
    "second_depositor_name", "nominee_name", "witness_1", "witness_2",
    "introducer_name",
}

NUMBER_FIELDS = {
    "share_number", "folio_number", "deposit_amount_figures",
    "amount_received", "phone_number", "account_number",
    "cheque_or_draft_number", "maturity_amount", "age", "nominee_age",
    "first_depositor_age", "second_depositor_age", "pincode",
    "existing_fd_rd_number", "deposit_term",
}

ADDRESS_FIELDS = {
    "address", "postal_address", "door_number", "street_name",
    "introducer_address",
}


def categorise(field_name, field_type):
    if field_name in HANDWRITTEN_NAME_FIELDS:
        return "Handwritten names"
    if field_name in NUMBER_FIELDS:
        return "Numbers"
    if field_name in ADDRESS_FIELDS:
        return "Addresses"
    if field_type == "checkbox":
        return "Checkboxes"
    if field_type == "signature":
        return "Signature presence"
    if field_type == "date":
        return "Dates"
    return "Printed text"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

QUERY = """
SELECT d.document_id, d.document_number, d.form_type,
       ef.field_name, ef.field_type, ef.ocr_value, ef.corrected_value,
       ef.confidence_score
FROM extracted_fields ef
JOIN documents d ON d.document_id = ef.document_id
WHERE d.processing_status = 'Verified'
ORDER BY d.document_id, ef.field_id;
"""


def _norm(value):
    return (value or "").strip().lower()


def load_rows(db_path=DB_PATH):
    if not os.path.exists(db_path):
        raise SystemExit(f"Database not found at {db_path}. Run the backend at least once first.")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(QUERY).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Accuracy computation
# ---------------------------------------------------------------------------

def compute_accuracy(rows):
    """
    Returns:
      overall: dict(fields_tested, correct)
      by_category: {category: dict(fields_tested, correct)}
      by_form: {document_id: dict(document_number, form_type, fields_tested, correct)}
      mismatches: list of rows where ocr_value != corrected_value (for the
                  "observations" section - these are your worst offenders)
    """
    overall = {"fields_tested": 0, "correct": 0}
    by_category = defaultdict(lambda: {"fields_tested": 0, "correct": 0})
    by_form = {}
    mismatches = []

    for row in rows:
        category = categorise(row["field_name"], row["field_type"])
        is_correct = _norm(row["ocr_value"]) == _norm(row["corrected_value"])

        overall["fields_tested"] += 1
        overall["correct"] += int(is_correct)

        by_category[category]["fields_tested"] += 1
        by_category[category]["correct"] += int(is_correct)

        doc_id = row["document_id"]
        if doc_id not in by_form:
            by_form[doc_id] = {
                "document_number": row["document_number"],
                "form_type": row["form_type"],
                "fields_tested": 0,
                "correct": 0,
            }
        by_form[doc_id]["fields_tested"] += 1
        by_form[doc_id]["correct"] += int(is_correct)

        if not is_correct:
            mismatches.append(row)

    return overall, dict(by_category), by_form, mismatches


def pct(correct, total):
    return (correct / total * 100.0) if total else 0.0


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

REPORT_CATEGORY_ORDER = [
    "Printed text", "Handwritten names", "Numbers", "Dates",
    "Addresses", "Checkboxes", "Signature presence",
]


def print_console_summary(overall, by_category, by_form, mismatches):
    print("=" * 70)
    print("ACCURACY TEST SUMMARY")
    print("=" * 70)

    print(f"\nForms tested: {len(by_form)}")
    print(f"Total fields tested: {overall['fields_tested']}")
    print(f"Correctly extracted: {overall['correct']}")
    print(f"Overall field-level accuracy: {pct(overall['correct'], overall['fields_tested']):.1f}%")

    print("\n--- By field category ---")
    for cat in REPORT_CATEGORY_ORDER:
        stats = by_category.get(cat, {"fields_tested": 0, "correct": 0})
        print(f"{cat:<20} {stats['correct']:>4}/{stats['fields_tested']:<4} "
              f"({pct(stats['correct'], stats['fields_tested']):.1f}%)")

    print("\n--- By form ---")
    for doc_id, stats in sorted(by_form.items()):
        acc = pct(stats["correct"], stats["fields_tested"])
        print(f"[{doc_id}] {stats['document_number']} ({stats['form_type']}): "
              f"{stats['correct']}/{stats['fields_tested']} ({acc:.1f}%)")

    if mismatches:
        print(f"\n--- {len(mismatches)} field(s) OCR got wrong (worth reviewing) ---")
        for m in mismatches[:30]:  # cap console output; full list goes in the .md report
            print(f"  doc {m['document_id']} [{m['field_name']}]: "
                  f"OCR={m['ocr_value']!r}  ->  corrected={m['corrected_value']!r}")
        if len(mismatches) > 30:
            print(f"  ... and {len(mismatches) - 30} more (see the generated report)")


def write_markdown_report(overall, by_category, by_form, mismatches, out_path):
    lines = []
    lines.append("# Accuracy Report — Suryan Benefit Fund Form Digitisation")
    lines.append("")
    lines.append(f"*(Auto-generated by tools/accuracy_test.py on "
                 f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})*")
    lines.append("")
    lines.append("## Overall accuracy")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Forms tested | {len(by_form)} |")
    lines.append(f"| Total fields tested | {overall['fields_tested']} |")
    lines.append(f"| Correctly extracted | {overall['correct']} |")
    lines.append(f"| Fields requiring correction | {overall['fields_tested'] - overall['correct']} |")
    lines.append(f"| Overall field-level accuracy | {pct(overall['correct'], overall['fields_tested']):.1f}% |")
    lines.append("")

    lines.append("## Accuracy by field category")
    lines.append("")
    lines.append("| Category | Fields tested | Correct | Accuracy |")
    lines.append("|---|---|---|---|")
    for cat in REPORT_CATEGORY_ORDER:
        stats = by_category.get(cat, {"fields_tested": 0, "correct": 0})
        lines.append(f"| {cat} | {stats['fields_tested']} | {stats['correct']} | "
                     f"{pct(stats['correct'], stats['fields_tested']):.1f}% |")
    lines.append("")

    lines.append("## Per-form breakdown")
    lines.append("")
    lines.append("| Form # | Document number | Form type | Fields tested | Correct | Accuracy |")
    lines.append("|---|---|---|---|---|---|")
    for i, (doc_id, stats) in enumerate(sorted(by_form.items()), start=1):
        acc = pct(stats["correct"], stats["fields_tested"])
        lines.append(f"| {i} | {stats['document_number']} | {stats['form_type']} | "
                     f"{stats['fields_tested']} | {stats['correct']} | {acc:.1f}% |")
    lines.append("")

    lines.append("## Fields OCR got wrong")
    lines.append("")
    if mismatches:
        lines.append("| Document | Field | OCR value | Corrected value |")
        lines.append("|---|---|---|---|")
        for m in mismatches:
            ocr_val = (m["ocr_value"] or "").replace("|", "\\|")
            corr_val = (m["corrected_value"] or "").replace("|", "\\|")
            lines.append(f"| {m['document_number']} | {m['field_name']} | {ocr_val} | {corr_val} |")
    else:
        lines.append("None — every field matched on this test run.")
    lines.append("")

    lines.append("## Observations")
    lines.append("")
    lines.append("- Fill in manually: which fields most often needed correction, and why "
                 "(cursive handwriting, faint ink, overlapping table lines)?")
    lines.append("- Fill in manually: did perspective correction / alignment noticeably "
                 "help or hurt accuracy on photographed vs. scanned forms?")
    lines.append("- Fill in manually: any consistent OCR misreads worth a validation rule?")
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    rows = load_rows()
    if not rows:
        print("No Verified documents found yet. Upload and verify at least 10 forms "
              "(a mix of deposit and share applications) before running this test - "
              "see the docstring at the top of this file.")
        return

    overall, by_category, by_form, mismatches = compute_accuracy(rows)
    print_console_summary(overall, by_category, by_form, mismatches)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(out_dir, f"accuracy_report_{timestamp}.md")
    write_markdown_report(overall, by_category, by_form, mismatches, out_path)
    print(f"\nFull markdown report written to: {out_path}")


if __name__ == "__main__":
    main()
