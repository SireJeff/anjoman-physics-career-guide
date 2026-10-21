# گزارش ساخت — Build Report
راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف — نسخهٔ ۱٫۰
Deliverable: `SUT_Physics_Career_Guide_v1.pdf` (56 pages, A4, ~0.76 MB)

## 1. Toolchain and fonts
- **Route: HTML/CSS + WeasyPrint 68.0** (the sanctioned fallback — XeLaTeX was not
  installed; only Tectonic 0.15 was available, and the bidi/xltabular/tcolorbox RTL
  combination is fragile there. State: HTML route used, as permitted by the brief.)
- Persian font: **Vazirmatn** (Regular 400 / Medium 500 / Bold 700 / ExtraBold 800 —
  embedded and subsetted). Tahoma is not available on this system; Vazirmatn is the
  brief's named fallback.
- Latin font: **TeX Gyre Termes** (regular/italic/bold/bold-italic — embedded), the
  brief's named Times New Roman fallback.
- Icons: **Font Awesome 6 Free Solid** — ✔ → `\f00c` (green), ⚠ → `\f071` (amber);
  the 47+15 variation selectors (U+FE0E/U+FE0F) were stripped as instructed.
- Shaping/bidi: Pango/HarfBuzz (full Unicode bidi algorithm incl. bracket pairing).
- Arabic-script shaping verified visually and programmatically; ZWNJ (U+200C,
  1126 occurrences) preserved — spot-checked می‌شود / دانش‌بنیان / سند‌شده.

## 2. Structure delivered
1. Cover (no page number) — logo, association name, title, subtitle, «نسخهٔ ۱٫۰»،
   «۱۸ مهر ۱۴۰۵» + «October 2026».
2. Credits (no number) — logo, «با تشکر از:» + the 7 names, summary line, channel handle.
3. پیش‌گفتار — the two paragraphs that follow the subtitle (verbatim).
4. فهرست مطالب — chapters bold, dark blue, bold Persian page numbers on the left;
   sections with dotted leaders; clickable (291 named-destination link annotations).
5. فهرست جدول‌ها — 6 short captions.
6. Chapters فصل ۱…۱۳ from Markdown sections ۱…۱۳; «###» → sections (۶٫۱ … ۹٫۵).
   Chapter openers on new pages with ~5 cm top space, no running header.
7. پیوست الف: منابع (section ۱۴), subsections numbered الف٫۱…الف٫۵.
8. Editor's Notes excluded from the PDF; returned verbatim as `editors_notes.txt`
   (byte-identical to the source slice — verified).

## 3. Numbering and folios
- Headings renumbered by the generator; resulting numbers match the original ones
  (chapter 1 = مقدمه …, 6.1 = ادامهٔ تحصیل …). Persian digits everywhere.
- Front matter footers: الف (preface), ب، پ (فهرست مطالب), ت (فهرست جدول‌ها).
- Main matter restarts at ۱ (chapter 1 = global page 7).
- Running header on non-opening pages: «فصل N. عنوان» top-right with a thin rule,
  implemented with `string(chap, first-except)`; page numbers centred at the bottom.
- Because WeasyPrint 68 does not support mid-document `counter-reset: page`, the
  folios were stamped post-render from a second WeasyPrint-generated overlay
  (vector text, same font); TOC/LOT numbers were computed from measured anchors and
  injected as text, so TOC numbers, folios and targets agree.

## 3b. Tables set in landscape
- جدول ۵-۱ (master table, section 5) — landscape, 10 pt, own pages, running header
  kept, header row repeats.
- جدول ۹-۱ (country-by-country, section 9.2) — landscape (very long cells).
- جدول ۱۰-۱ (six columns, section 10) — landscape.
- جدول ۱۱-۱ (five columns, section 11) — landscape.
- جدول ۳-۱ and ۴-۱ set portrait (readable at 10 pt).
- Section 13's myth/reality table rendered as 10 two-part boxes (myth on light red,
  reality on light green) — the pairs were unambiguous, as permitted by the brief;
  therefore the list of tables has 6 entries.

## 4. Boxes and ornaments
- Blue «چطور بخوانید» around the section-5 reading instructions (kept verbatim inside).
- Orange «توجه» around the five ⚠-flagged caveat paragraphs (L65, L109, L151, L187,
  L270 of the source) — sanctions/defence/military-service caveats.
- Green «اقدام عملی» around the self-contained action paragraph in 7.6.
- Markdown `---` rules all coincided with chapter breaks and were absorbed by them.
- Bold source text rendered bold in the house dark blue.

## 5. Links and bookmarks
- All body links render as clickable text only (dark blue, no boxes); appendix raw
  URLs are printed, wrapped with `word-break`, each an LTR run, and clickable
  (hrefs percent-encoded where paths contain Persian characters/spaces).
- 1392 link annotations in total; PDF outline (41 entries, Persian) matches
  chapters/sections and opens correctly in phone PDF viewers.
- PDF /Lang = fa-IR; metadata Title/Author/Subject/Keywords set exactly as specified.

## 6. Not rendered perfectly (known limitations)
1. **Copy-paste of لا-words**: WeasyPrint's ToUnicode maps the lam-alef ligature and
   some combining marks (هٔ) in reversed order, so text *extracted* from the PDF
   (e.g. searching «بالا» inside a viewer) can miss those words. This is an engine
   level behaviour (reproduced identically with FreeSerif/DejaVu) — the rendered
   glyphs are correct. XeLaTeX/xepersian does not have this issue; relevant only if
   copy-paste fidelity becomes important.
2. The last page of each landscape table section ends mid-page (blank lower half) —
   a consequence of rotating to landscape for those pages only.
3. Justification is space-based (no kashida); standard for web-engine Persian text.
4. Appendix lines whose URLs contain raw spaces/commas (e.g. the Karpishe entry,
   source line 411) keep the visible text verbatim; their clickable href is a
   best-effort percent-encoded form.

## 7. Content issues noticed (NOT fixed, per the absolute rule)
1. **Citation artefact**: `【turn0searchN】` occurs once, in source line 715 — inside
   the excluded Editor's Notes section, so it never entered the PDF. Not removed
   anywhere else because it does not occur elsewhere.
2. **«۵هزار‌یِنی»** (source line 224, OIST row): unusual ZWNJ placement inside the
   compound; presumably intended «۵ هزار ینی» (5,000-yen). Rendered verbatim.
3. **«سکوی پرتعهای سوم»** (source line 236): the word «پرتعهای» looks like a typo
   (perhaps «پرتعدّی»/«پرتعهد» or «سکوی پرتاب سوم» was meant). Rendered verbatim.
4. **Appendix numbering mixes digit systems**: heading ۱۴٫۲ says «[۱]–[۱۴۲]» (Persian
   digits) while the entries themselves are «[1]…[142]» (ASCII). Both kept exactly
   as in the source, per the "keep source numbering" rule.
5. **Unnumbered heading** «پنج پروفایل واقعی (سند‌شده)» (chapter 10) has no number in
   the source; rendered as an unnumbered section (no «۱۰٫۱») and included in the
   TOC/bookmarks without a number.
6. The 13 in-text arrows written as «→» in the Markdown were flipped to «←» so they
   point in the RTL reading direction, per the brief's instruction; the source's own
   «←» chains were kept unchanged.
