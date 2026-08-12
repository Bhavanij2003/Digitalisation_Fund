# Suryan Benefit Fund — Deposit &amp; Share Application Digitisation


Watch demonstration video
https://drive.google.com/file/d/1bbduYhds5xCdiragIcZ1Y8qiok_DnFiG/view?usp=drive_link


A prototype system that turns manually filled Deposit Application Forms and
Share Application forms into searchable digital records, using OCR with a
mandatory human verification step.

This implements the full workflow from the brief:

```
upload → preprocess/align → identify form type → crop fields →
OCR + checkbox/signature detection → confidence scoring → validation →
verification screen → employee corrects & approves → save to database →
search, view, export
```

## 1. What's in this folder

```
project/
├── backend/
│   ├── main.py               FastAPI app — all API endpoints
│   ├── database.py           SQLite access layer
│   ├── preprocessing.py      OpenCV: rotation, perspective, alignment, etc.
│   ├── ocr_engine.py         Tesseract OCR, checkbox & signature detection
│   ├── templates_config.py   Field co-ordinates per form type (needs calibration)
│   └── validation.py         Section-8 validation rules
├── frontend/
│   ├── index.html            Dashboard / processing queue
│   ├── upload.html           Upload screen
│   ├── verify.html           Two-pane verification screen
│   ├── search.html           Search + CSV/Excel export
│   ├── style.css, app.js
├── tools/
│   └── calibrate_template.py Click-to-define field regions on a blank form
├── data/
│   ├── uploads/               original uploaded files (created at runtime)
│   ├── processed/              preprocessed images (created at runtime)
│   ├── templates/               put blank reference form images here
│   └── exports/                  CSV/XLSX exports land here
├── schema.sql                  full database schema
├── requirements.txt
├── ARCHITECTURE.md              architecture diagram + notes
├── ACCURACY_REPORT_TEMPLATE.md  fill in after testing with real sample forms
└── README.md                    this file
```

## 2. Setup

### 2.1 System requirements
- Python 3.10+
- **Tesseract OCR** installed at the OS level (pytesseract is just a wrapper):
  - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`
  - Windows: install from https://github.com/UB-Mannheim/tesseract/wiki and
    add the install directory to PATH.
- For Tamil handwriting support later (optional advanced feature), also
  install the Tamil language pack: `sudo apt-get install tesseract-ocr-tam`.

### 2.2 Python environment

```bash
cd project
python -m venv venv
source venv/bin/activate          # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2.3 Initialise the database

The database is created automatically on first run (see `startup` event in
`backend/main.py`), but you can also create it explicitly:

```bash
python -c "import sys; sys.path.append('backend'); import database; database.init_db()"
```

This creates `data/sbf_digitisation.db` using `schema.sql`.

### 2.4 Run the backend API

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The API is now at `http://127.0.0.1:8000`. Interactive API docs (Swagger UI)
are automatically available at `http://127.0.0.1:8000/docs`.

### 2.5 Run the frontend

The frontend is plain HTML/CSS/JS with no build step. The simplest way to
serve it (so the browser doesn't block `fetch()` calls under a `file://`
URL) is:

```bash
cd frontend
python -m http.server 5500
```

Then open `http://127.0.0.1:5500/index.html` in a browser.

If you deploy the API somewhere other than `127.0.0.1:8000`, change
`API_BASE` at the top of `frontend/app.js`.

## 3. Calibrating field positions (important, one-time step)

The field regions shipped in `backend/templates_config.py` are reasonable
placeholders based on the layout described in the brief, but every printed
form has small differences in exact placement. Before relying on field-level
accuracy:

1. Scan the two **blank** forms and save them as:
   - `data/templates/deposit_blank.png`
   - `data/templates/share_blank.png`
2. Run the calibration tool for each:
   ```bash
   python tools/calibrate_template.py data/templates/deposit_blank.png deposit
   python tools/calibrate_template.py data/templates/share_blank.png share
   ```
3. Drag a box over each field on the image, type its name (matching the keys
   already used in `templates_config.py`) in the terminal, and press Enter.
4. Press `q` when done — the tool prints ready-to-paste JSON with correctly
   scaled fractional coordinates. Paste it over the corresponding entries in
   `backend/templates_config.py`.

Once `data/templates/deposit_blank.png` / `share_blank.png` exist, the
preprocessing pipeline will also automatically align every uploaded scan to
that blank template using ORB feature matching (see
`preprocessing.align_to_reference`), which significantly improves field-crop
accuracy for skewed or slightly-offset photographs.

## 4. Using the system

1. **Upload** (`upload.html`) — drag in a JPG/PNG/PDF of a completed form.
   The backend preprocesses it, identifies the form type, extracts fields,
   and returns a document ready for review.
2. **Verify** (`verify.html`) — the left pane shows the scanned form (zoom,
   rotate, toggle original/processed); the right pane shows every extracted
   field as an editable box, colour-coded by confidence (green ≥ 90%,
   orange 70–90%, red < 70%). Correct any field, then **Approve**, **Save
   draft**, **Reprocess OCR**, **Mark duplicate**, or **Reject**.
3. **Search & export** (`search.html`) — search by name, phone, share
   number, account number, date, deposit type, nominee, or status, and
   export the result set to CSV or Excel.

## 5. Database

See `schema.sql` for the full DDL. Summary:

- `documents` — one row per uploaded file, its status, and file paths.
- `deposit_applications` / `share_applications` — the approved, structured
  data for each form type (one row per document, created on Approve).
- `extracted_fields` — every OCR'd field for a document, keeping both the
  original OCR value and the employee-corrected value, plus its confidence
  score — this is the audit trail described in section 6 of the brief.
- `audit_log` — who did what and when (upload, OCR, approve, reject, etc.)

## 6. Security notes (section 18 of the brief)

This prototype demonstrates the workflow end-to-end but is **not**
hardened for production:
- No authentication/login is implemented yet — add an auth layer (e.g.
  FastAPI's `OAuth2PasswordBearer` + a `users` table with hashed passwords)
  before any real customer data is processed.
- `/files/uploads` and `/files/processed` are currently mounted without
  access control for ease of local development — in production these must
  require a valid session and should not be publicly reachable.
- No cloud OCR API is called anywhere in this codebase — everything runs
  locally via Tesseract, per the brief's instruction not to send customer
  data to a web API without company approval.
- Add field-level masking for phone numbers/PAN/Aadhaar in list/export views
  if required by company policy (see "Optional Advanced Features").
- Add regular backups of `data/sbf_digitisation.db` and the `data/uploads`
  and `data/processed` folders.

## 7. Known limitations

- Field regions require the one-time calibration step in section 3 above —
  without it, extraction still runs but crop boxes are approximate.
- Handwriting recognition accuracy with Tesseract is moderate; see
  `ACCURACY_REPORT_TEMPLATE.md` for how to measure it against real samples,
  and consider trying EasyOCR/PaddleOCR or a handwriting-specific model as a
  drop-in replacement inside `ocr_engine.ocr_text_with_confidence`.
- "Amount in figures vs amount in words" cross-validation
  (`validation.amounts_roughly_match`) is a placeholder heuristic — a full
  Indian-English number-words parser would be needed for a strict check.
- No authentication/role-based access yet (see Security notes).
- Multi-page PDFs only use page 1; batch upload and PDF page-splitting are
  listed as optional advanced features, not yet implemented.
- Tamil handwriting is not specifically tuned for; the Tamil Tesseract
  language pack can be enabled but was not benchmarked here.

## 8. Suggestions for improving the system

- Swap Tesseract for a stronger handwriting model (e.g. a cloud handwriting
  API used only after company approval and with sensitive fields masked, or
  a locally-hosted TrOCR model) for the handwritten-name and address fields,
  which typically have the lowest confidence.
- Add role-based login (data-entry clerk vs. verifier vs. admin) matching
  the "Clerk approval / Cashier approval / Secretary-MD approval" fields
  already present on the Share Application form.
- Add an audit-trail view in the UI (the `audit_log` table already captures
  every action) so managers can see who corrected what.
- Add batch upload and automatic multi-page PDF splitting for scanning many
  forms at once.
- Add automatic maturity-date calculation from deposit date + term, to
  cross-check the OCR'd maturity date.


