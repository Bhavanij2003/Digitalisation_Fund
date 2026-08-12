# Architecture

## Component diagram

```
                         ┌─────────────────────────────┐
                         │        Frontend (SPA-ish)    │
                         │  index / upload / verify /   │
                         │  search  (HTML + CSS + JS)    │
                         └───────────────┬───────────────┘
                                          │ fetch() JSON / multipart
                                          ▼
                         ┌─────────────────────────────┐
                         │       FastAPI backend        │
                         │         (backend/main.py)    │
                         │                               │
                         │  /api/upload                  │
                         │  /api/document/{id}            │
                         │  /api/document/{id}/verify      │
                         │  /api/document/{id}/reprocess    │
                         │  /api/search                      │
                         │  /api/export/csv | excel           │
                         └───┬───────────┬───────────┬────────┘
                             │           │           │
             ┌───────────────┘           │           └───────────────┐
             ▼                           ▼                           ▼
 ┌───────────────────────┐  ┌────────────────────────┐  ┌─────────────────────┐
 │  preprocessing.py       │  │   ocr_engine.py         │  │  validation.py       │
 │  (OpenCV)                │  │   (pytesseract)          │  │  (business rules)    │
 │  - load image/PDF          │  │   - form type ID           │  │  - phone/pincode/age │
 │  - auto-rotate               │  │   - field OCR                │  │  - amount numeric      │
 │  - perspective correct        │  │   - checkbox detect             │  │  - date checks           │
 │  - deskew                       │  │   - signature detect              │  │  - duplicate share #      │
 │  - brightness/contrast            │  │   - confidence score                 │  └─────────────────────┘
 │  - denoise, resize                  │  └────────────────────────┘
 │  - align to blank template            │
 └───────────────────────┘                │
             │                             │
             ▼                             ▼
 ┌─────────────────────────────────────────────────────────┐
 │                     database.py (SQLite)                  │
 │  documents │ extracted_fields │ deposit_applications │       │
 │  share_applications │ audit_log                              │
 └─────────────────────────────────────────────────────────┘
             │
             ▼
 ┌─────────────────────────┐
 │   export_utils.py         │
 │   (pandas + openpyxl)      │
 │   CSV / XLSX export          │
 └─────────────────────────┘
```

## Data flow (matches brief section 12)

1. **Upload** — file saved to `data/uploads/`, a `documents` row is created
   with status `Uploaded`, then `Processing`.
2. **Preprocess** (`preprocessing.preprocess_pipeline`) — auto-rotate,
   perspective-correct, deskew, brightness/contrast correction, denoise,
   resize to a standard canvas size so field co-ordinates are consistent.
3. **Identify form type** (`ocr_engine.identify_form_type`) — OCRs the
   heading area and matches against known keywords, or uses the employee's
   manual selection if supplied.
4. **Align** (`preprocessing.align_to_reference`) — if a blank reference
   template exists for that form type, ORB feature matching + homography
   aligns the scan onto it, so fixed field boxes line up.
5. **Field-level extraction** (`ocr_engine.extract_fields`) — for every
   field defined in `templates_config.py`: crop → OCR (text fields),
   dark-pixel-ratio detection (checkboxes), ink-density/spread detection
   (signatures) → confidence score.
6. **Save extracted fields** — written to `extracted_fields`, status becomes
   `Pending Verification`.
7. **Verification screen** — employee reviews/corrects fields in the UI;
   corrections are written back to `extracted_fields.corrected_value`.
8. **Validation** (`validation.py`) — on Approve, business rules run; if any
   fail, the API returns 422 with the list of errors and nothing is saved
   to the typed table yet.
9. **Save to typed table** — once valid, data is upserted into
   `deposit_applications` or `share_applications`; `documents.processing_status`
   becomes `Verified`.
10. **Search / export** — `database.search_applications` joins documents with
    both typed tables; `export_utils` writes CSV/XLSX via pandas.

## Why this structure

- **Separation of concerns**: each backend module does one job
  (preprocessing / OCR / validation / persistence / export), so any one of
  them can be swapped (e.g. replace Tesseract with PaddleOCR) without
  touching the others.
- **Field-level crops, not full-page OCR**: per the brief's guidance
  (section 3, step 4), cropping and OCR-ing each field separately gives
  materially better accuracy than running OCR on the whole page at once,
  especially for short structured fields like phone numbers and pincodes.
- **Two-value storage** (`ocr_value` vs `corrected_value`) in
  `extracted_fields` preserves a full audit trail, satisfying section 6 of
  the brief and enabling future accuracy analysis without re-running OCR.
- **No cloud OCR calls**: everything runs locally, per the explicit
  instruction in section 18 not to send customer data to a web API without
  company approval.
