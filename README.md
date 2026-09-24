# ProATS Resume Builder

Desktop GUI app (tkinter). ATS-compliant resume builder with live preview, ATS scoring, and PDF/DOCX/TXT export.

## Run

```bash
pip install python-docx fpdf2
python main.py
```

Requires Python 3.10+ with tkinter. Verified boot on Python 3.12 (Linux, xvfb, 2026-09-24) — window initializes with no errors.

Not a web/cloud app: it is a desktop tool. Package with PyInstaller for distribution.
