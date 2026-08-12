# Accuracy Report — Suryan Benefit Fund Form Digitisation

*(Template — fill in after running the accuracy test in section 14 of the
brief against at least 10 real, manually filled sample forms.)*

## Method

1. Collect at least 10 manually filled sample forms (a mix of Deposit
   Application Forms and Applications for Share).
2. For each form, manually type the correct value for every field into a
   reference spreadsheet (this is your ground truth).
3. Upload each form through `upload.html` and let the system run OCR.
4. On the verification screen, record — for every field — whether the OCR
   value matched the reference data exactly, or needed correction.
5. Tally results using the categories below.

## Overall accuracy

| Metric                     | Value |
|-----------------------------|-------|
| Forms tested                  |       |
| Total fields tested             |       |
| Correctly extracted               |       |
| Fields requiring correction         |       |
| Overall field-level accuracy          | __ % |

## Accuracy by field category (section 14 requirement)

| Category            | Fields tested | Correct | Accuracy |
|-----------------------|--------------|---------|----------|
| Printed text             |              |         |          |
| Handwritten names           |              |         |          |
| Numbers                        |              |         |          |
| Dates                              |              |         |          |
| Addresses                             |              |         |          |
| Checkboxes                               |              |         |          |
| Signature presence                          |              |         |          |

## Per-form breakdown

| Form # | Form type | Fields tested | Correct | Accuracy | Notes |
|--------|-----------|----------------|---------|----------|-------|
| 1      |           |                |         |          |       |
| 2      |           |                |         |          |       |
| ...    |           |                |         |          |       |

## Observations

- Which fields most often needed correction, and why (e.g. cursive
  handwriting, faint ink, overlapping table lines)?
- Did perspective correction / alignment noticeably help or hurt accuracy on
  photographed (vs. scanned) forms?
- Any consistent OCR misreads worth a validation rule (e.g. "O" vs "0" in
  amounts, as shown in the brief's own example)?

## How to regenerate this data quickly

The `extracted_fields` table already stores both `ocr_value` and
`corrected_value` for every verified document, which is exactly the data
needed for this report. A simple query to pull it after testing:

```sql
SELECT d.form_type, ef.field_name, ef.ocr_value, ef.corrected_value,
       ef.confidence_score,
       (ef.ocr_value = ef.corrected_value) AS matched
FROM extracted_fields ef
JOIN documents d ON d.document_id = ef.document_id
WHERE d.processing_status = 'Verified';
```

Export that with `sqlite3` or pandas and pivot by field category to fill in
the tables above automatically for future test batches.
