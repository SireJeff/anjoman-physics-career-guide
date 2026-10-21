# Rebuild guide — راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف

## Contents
- `guide.html` + `style.css` — the typeset document (dir="rtl", lang="fa-IR").
  `guide.html` is the final render-ready source: the TOC/list-of-tables page
  numbers are already injected as text (they match the shipped PDF exactly).
- `anjoman_logo.png` — association logo (referenced by the cover and credits page).
- `fonts/` — Vazirmatn (Regular/Medium/Bold/ExtraBold, OFL licence, see
  `fonts/vazirmatn/OFL.txt` in the upstream release), TeX Gyre Termes
  (GUST Font Licence), Font Awesome 6 Free Solid (OFL/CC BY 4.0 — icons only).
- `*.py` — the build pipeline (optional; needed only when the Markdown changes).

## Publication edition (current) — v1.0, first release
```bash
python refine.py   # guide_v1_original.html -> guide.html (v1.1 + v1.2 passes + section 12: series-style cover + شناسنامه)
python build.py    # -> ../SUT_Physics_Career_Guide_v1.0.pdf (49 pp)
```
Publication furniture (band «انتشار اول · ۱۴۰۵», تهیه و تدوین line, date/نسخه facts)
lives in `refine.py` section 12 and the `publication edition` block at the end of
`style.css`. Body content is unchanged from v1.2; v1/v1.1/v1.2 PDFs stay untouched.

## v1.2 build (previous)
```bash
pip install weasyprint pymupdf
python refine.py   # guide_v1_original.html -> guide.html (v1.1 + v1.2 editorial passes)
python build.py    # -> ../SUT_Physics_Career_Guide_v1.2.pdf (all-portrait)
```
v1.2 changes: landscape pages removed (compact `tbl-c` tables, جدول ۱۰.۱ merged 6→4 columns),
natural-Persian prose pass, cover at نسخهٔ ۱٫۲. Edits still belong in `refine.py`
(sections 10–11 are the v1.2 pass), or edit `guide.html` directly and run only `build.py`.

## v1.1 build (Windows/local, no Markdown needed)
```bash
pip install weasyprint pymupdf
python refine.py   # guide_v1_original.html -> guide.html (v1.1 editorial pass)
python build.py    # two-pass render, TOC numbers, folios -> ../SUT_Physics_Career_Guide_v1.1.pdf
```
`refine.py` always starts from `guide_v1_original.html`, so further edits belong
in `refine.py` (or edit `guide.html` directly and run only `build.py`).

## Render the PDF (no content changes)
```bash
python3 -m weasyprint guide.html SUT_Physics_Career_Guide_v1.pdf
```
This produces the PDF *without* the stamped page-number footers (layout is identical).

## Full pipeline (after editing the Markdown)
```bash
pip install weasyprint pikepdf
python3 md2html.py     # rebuilds build/guide.html + download/editors_notes.txt
python3 finalize.py    # two-pass render + Persian-letter/digit footer stamping + metadata
```
Expected: ~56 pages, preface anchored at global page 3 (footer الف), first chapter
at global page 7 (footer ۱), four landscape table sections.

## Layout notes
- Page numbers are stamped post-render (WeasyPrint 68 does not support mid-document
  `counter-reset: page`); `finalize.py` computes the الف/ب/پ front-matter and the
  restarted ۱/۲/۳ main-matter footers and overlays them via pikepdf `add_overlay`.
- Arabic-script shaping is done by Pango/HarfBuzz — no reordering is done in code;
  Latin runs are wrapped in `<bdi dir="ltr">` (the HTML equivalent of xepersian `\lr{}`).
- ✔/⚠ appear as Font Awesome glyphs (`\f00c`, `\f071`) with variation selectors stripped.
