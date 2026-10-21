# GitHub Publication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the flat, non-git `SUT_Physics_Career_Guide_deliverables` folder into a clean public GitHub repo (`SireJeff/anjoman-physics-career-guide`) with separated live/provenance/legacy content, real license files, a changelog that resolves the confusing version history, bilingual READMEs, CI, and a tagged v1.0.0 release.

**Architecture:** Reorganize the existing folder **in place** (it becomes the repo root — no new location) via plain filesystem moves across Tasks 1–8, building the complete tree on disk with no git safety net yet; Task 9 is the only task that touches git — `git init`, one deliberate initial commit (explicit paths, never `-A`), `gh repo create`, push, tag, release. Every content file (licenses, changelog, READMEs) is drafted with real text pulled from the actual guide, not placeholders.

**Tech Stack:** Git + GitHub CLI (`gh`, already authenticated as `SireJeff`), Python 3.11 (WeasyPrint + PyMuPDF, already proven), Bash tool for all file operations (not PowerShell — matches this project's established working pattern).

**Spec:** `docs/superpowers/specs/2026-10-21-github-publication-design.md` — read it first; the plan argues from it.

## Global Constraints

- **Reorganize in place.** The repo root IS `C:\Users\Surface Laptop 3\Downloads\SUT_Physics_Career_Guide_deliverables`. Do not create a second copy elsewhere.
- **Never delete anything.** Items excluded from the new repo (`channel_post.md`, `.superpowers/`, the Persian-filename PDF on disk, the now-partially-empty `docs/superpowers/` tree) are left physically in place, untouched, simply never `git add`ed. `.gitignore` lists them so a future `git add -A` doesn't sweep them in by accident.
- **All file operations via the Bash tool** (not PowerShell) — this project's commands consistently use POSIX paths (`/c/Program Files/...`) and that pattern is proven stable here. Python: `"/c/Program Files/Python311/python"`. Git: `"/c/Program Files/Git/cmd/git.exe"`. GitHub CLI: `"/c/Program Files/GitHub CLI/gh.exe"` (or bare `gh` — confirmed on PATH, but prefer the absolute path for consistency with git/python).
- **git identity:** already configured globally (`user.name = SireJeff`, `user.email = sandmanshiri@gmail.com`) — no per-commit override needed.
- **Commit message trailer:** every commit message ends with `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
- **No content edits to the guide.** `guide.html`'s text, `style.css`'s rules, and `refine.py`'s logic are moved verbatim — byte-identical before and after the move (verified in Task 1).
- **Real text, not placeholders.** Every doc task below contains the actual content to write — license texts, chapter lists, changelog entries — not instructions to "fill in" content.

---

### Task 1: Directory reorganization + build.py path fix + pipeline verification

**Files:**
- Create dirs: `guide/`, `guide/fonts/`, `provenance/`, `dist/`, `docs/design/`, `legacy/pipeline/`, `legacy/pdfs/`, `.github/workflows/`, `.github/ISSUE_TEMPLATE/`
- Move: `source/guide.html` → `guide/guide.html`; `source/style.css` → `guide/style.css`; `source/refine.py` → `guide/refine.py`; `source/build.py` → `guide/build.py`; `source/anjoman_logo.png` → `guide/anjoman_logo.png`; `source/fonts/` → `guide/fonts/`
- Move: `source/guide_v1_original.html` → `provenance/guide_v1_original.html`; `source/style_v1_original.css` → `provenance/style_v1_original.css`
- Move: `source/fa_utils.py`, `source/finalize.py`, `source/inliner.py`, `source/md2html.py`, `source/mdparse.py` → `legacy/pipeline/`
- Move: `SUT_Physics_Career_Guide_build_report.md` → `legacy/build-report-v1.md`
- Move: `SUT_Physics_Career_Guide_v1.pdf`, `SUT_Physics_Career_Guide_v1.1.pdf`, `SUT_Physics_Career_Guide_v1.2.pdf` → `legacy/pdfs/`
- Move: `editors_notes.txt` → `docs/methodology.md` (content preserved, new header prepended — see Step 5)
- Modify: `guide/build.py:18` — `OUT` path

**Note — design docs stay put for now:** `docs/superpowers/specs/*.md` and `docs/superpowers/plans/*.md` (including *this plan file itself*) are **not** moved here. The controller executing this plan re-reads the plan from its original path for every task dispatch; moving it mid-execution would break that. Task 9 (the last task, after nothing needs to re-slice the plan) moves all four design docs into `docs/design/` as its final step, right before the git commit.
- Leave untouched (do not move, do not delete): `channel_post.md`, `.superpowers/`, `راهنمای_مسیرهای_حرفه‌ای_پس_از_فیزیک_شریف.pdf`, the now-empty `source/` dir and `docs/superpowers/` dir (leave as empty husks — do not `rmdir`, not worth the risk)

**Interfaces:**
- Produces: `guide/build.py` writing to `../dist/SUT_Physics_Career_Guide_v1.0.pdf`; `dist/SUT_Physics_Career_Guide_v1.0.pdf` (49 pp, all-portrait) consumed by Task 9's release step; `docs/methodology.md` consumed by Task 6's READMEs (link target — the file exists after this task; Task 6 only references it in prose, doesn't need to open it). `docs/design/` is created empty here (Step 1) and populated later, by Task 9 — Task 6's README table row describing it is a forward reference to the finished repo, not a same-task dependency.

- [ ] **Step 1: Create the new directory skeleton**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
mkdir -p guide/fonts provenance dist docs/design legacy/pipeline legacy/pdfs .github/workflows .github/ISSUE_TEMPLATE
```

- [ ] **Step 2: Move the live pipeline into `guide/`**

```bash
mv source/guide.html guide/guide.html
mv source/style.css guide/style.css
mv source/refine.py guide/refine.py
mv source/build.py guide/build.py
mv source/anjoman_logo.png guide/anjoman_logo.png
mv source/fonts/* guide/fonts/
```

- [ ] **Step 3: Move provenance, legacy pipeline, legacy build artifacts**

```bash
mv source/guide_v1_original.html provenance/guide_v1_original.html
mv source/style_v1_original.css provenance/style_v1_original.css
mv source/fa_utils.py source/finalize.py source/inliner.py source/md2html.py source/mdparse.py legacy/pipeline/
mv SUT_Physics_Career_Guide_build_report.md legacy/build-report-v1.md
mv SUT_Physics_Career_Guide_v1.pdf SUT_Physics_Career_Guide_v1.1.pdf SUT_Physics_Career_Guide_v1.2.pdf legacy/pdfs/
```

- [ ] **Step 4: Fix build.py's output path**

In `guide/build.py`, change line 18 from:
```python
OUT = os.path.join(HERE, "..", "SUT_Physics_Career_Guide_v1.0.pdf")
```
to:
```python
OUT = os.path.join(HERE, "..", "dist", "SUT_Physics_Career_Guide_v1.0.pdf")
```

- [ ] **Step 5: Promote editors_notes.txt into docs/methodology.md with a new header**

```bash
"/c/Program Files/Python311/python" - <<'EOF'
header = """# روش‌شناسی و یادداشت‌های ویرایشی — Methodology & Editorial Notes

این سند فرایند راستی‌آزمایی ادعاهای راهنما را مستند می‌کند: تناقض میان گزارش‌های
منبع (R1 تا R6)، نحوهٔ حل آن‌ها، و مواردی که هنوز نیاز به تأیید نهایی دارند. انتشار
این یادداشت‌ها همسو با اصل راهنماست: «هیچ عددی بدون منبع نیامده».

This document records the fact-checking process behind the guide: conflicts
between the six source research reports (R1–R6), how each was resolved, and
open items still needing final confirmation. Publishing these notes matches
the guide's own rule — no number appears without a source.

---

"""
orig = open("editors_notes.txt", encoding="utf-8").read()
open("docs/methodology.md", "w", encoding="utf-8").write(header + orig)
import os
os.remove("editors_notes.txt")
print("wrote docs/methodology.md,", len(header + orig), "bytes")
EOF
```

- [ ] **Step 6: Verify the pipeline builds from its new location**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables/guide"
PYTHONUTF8=1 "/c/Program Files/Python311/python" refine.py 2>&1 | tail -4
PYTHONUTF8=1 "/c/Program Files/Python311/python" build.py 2>&1 | grep -E "pass|wrote|front"
```
Expected: `refine.py` prints its usual checks ending `written guide.html`; `build.py` prints `pass 1/2: 49 pages` then `wrote …\dist\SUT_Physics_Career_Guide_v1.0.pdf (… MB, 49 pages)` and `front matter from page 3 | chapter 1 = page 7`.

- [ ] **Step 7: Verify content survived the move byte-identical and the final tree is clean**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
"/c/Program Files/Python311/python" - <<'EOF'
import fitz, os
d = fitz.open("dist/SUT_Physics_Career_Guide_v1.0.pdf")
land = [i + 1 for i, p in enumerate(d) if p.rect.width > p.rect.height]
print("pages:", len(d), "| landscape:", land)
assert not land and len(d) == 49
for p in ("guide/guide.html", "guide/style.css", "guide/refine.py", "guide/build.py",
          "guide/anjoman_logo.png", "provenance/guide_v1_original.html",
          "provenance/style_v1_original.css", "legacy/pipeline/md2html.py",
          "legacy/pdfs/SUT_Physics_Career_Guide_v1.2.pdf", "docs/methodology.md"):
    assert os.path.exists(p), p
# docs/design/ content is populated by Task 9, not here — not checked in this task
for gone in ("source", "SUT_Physics_Career_Guide_v1.pdf", "editors_notes.txt",
             "SUT_Physics_Career_Guide_build_report.md"):
    assert not os.path.exists(gone) or os.path.isdir(gone) and not os.listdir(gone), gone
for kept in ("channel_post.md", "راهنمای_مسیرهای_حرفه‌ای_پس_از_فیزیک_شریف.pdf"):
    assert os.path.exists(kept), kept
print("tree OK")
EOF
```
Expected: `pages: 49 | landscape: []` then `tree OK`.

---

### Task 2: Licensing — LICENSE, LICENSE-CODE, font license files

**Files:**
- Create: `LICENSE`, `LICENSE-CODE`, `guide/fonts/vazirmatn/LICENSE.txt`, `guide/fonts/fa-solid-LICENSE.txt`, `guide/fonts/texgyretermes-LICENSE.txt`

**Interfaces:**
- Produces: the four license files Task 6's READMEs summarize and link to.

- [ ] **Step 1: Write LICENSE (CC BY-NC-SA 4.0, content)**

Create `LICENSE`:

```markdown
راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف
Copyright © 1405 (2026) انجمن علمی دانشکدهٔ فیزیک، دانشگاه صنعتی شریف
(Sharif Physics Students' Scientific Association)

This work (the guide's text, data, and PDF content — everything under
`guide/guide.html`, `docs/`, and `dist/`) is licensed under the
**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
License (CC BY-NC-SA 4.0)**.

## You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

## Under the following terms:
- **Attribution** — You must give appropriate credit to انجمن علمی دانشکدهٔ
  فیزیک، دانشگاه صنعتی شریف, provide a link to this repository, and indicate
  if changes were made.
- **NonCommercial** — You may not use the material for commercial purposes.
- **ShareAlike** — If you remix, transform, or build upon the material, you
  must distribute your contributions under the same license as the original.
- **No additional restrictions** — You may not apply legal terms or
  technological measures that legally restrict others from doing anything
  the license permits.

This is a human-readable summary of (and not a substitute for) the full
legal code, which governs: **https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode**

The pipeline code (`*.py`, `style.css`, GitHub Actions workflows) is
licensed separately under MIT — see `LICENSE-CODE`. Bundled fonts carry
their own licenses — see `guide/fonts/*/LICENSE.txt`.
```

- [ ] **Step 2: Write LICENSE-CODE (MIT)**

Create `LICENSE-CODE`:

```
MIT License

Copyright (c) 1405 (2026) انجمن علمی دانشکدهٔ فیزیک، دانشگاه صنعتی شریف
(Sharif Physics Students' Scientific Association)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This license covers the build pipeline only (*.py, style.css, and the
.github/ workflows). The guide's text content is licensed separately under
CC BY-NC-SA 4.0 — see LICENSE. Bundled fonts carry their own licenses — see
guide/fonts/*/LICENSE.txt.
```

- [ ] **Step 3: Write the Vazirmatn font license**

Create `guide/fonts/vazirmatn/LICENSE.txt`:

```
SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide development of collaborative font projects, to support the font creation efforts of academic and linguistic communities, and to provide a free and open framework in which fonts may be shared and improved in partnership with others.

The OFL allows the licensed fonts to be used, studied, modified and redistributed freely as long as they are not sold by themselves. The fonts, including any derivative works, can be bundled, embedded, redistributed and/or sold with any software provided that any reserved names are not used by derivative works. The fonts and derivatives, however, cannot be released under any other type of license. The requirement for fonts to remain under this license does not apply to any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright Holder(s) under this license and clearly marked as such. This may include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the copyright statement(s).

"Original Version" refers to the collection of Font Software components as distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to, deleting, or substituting -- in part or in whole -- any of the components of the Original Version, by changing formats or by porting the Font Software to a new environment.

"Author" refers to any designer, engineer, programmer, technical writer or other person who contributed to the Font Software.

PERMISSION & CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining a copy of the Font Software, to use, study, copy, merge, embed, modify, redistribute, and sell modified and unmodified copies of the Font Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components, in Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled, redistributed and/or sold with any software, provided that each copy contains the above copyright notice and this license. These can be included either as stand-alone text files, human-readable headers or in the appropriate machine-readable metadata fields within text or binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font Name(s) unless explicit written permission is granted by the corresponding Copyright Holder. This restriction only applies to the primary font name as presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font Software shall not be used to promote, endorse or advertise any Modified Version, except to acknowledge the contribution(s) of the Copyright Holder(s) and the Author(s) or with their explicit written permission.

5) The Font Software, modified or unmodified, in part or in whole, must be distributed entirely under this license, and must not be distributed under any other license. The requirement for fonts to remain under this license does not apply to any document created using the Font Software.

TERMINATION
This license becomes null and void if any of the above conditions are not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM OTHER DEALINGS IN THE FONT SOFTWARE.

---
Font: Vazirmatn. Upstream: https://github.com/rastikerdar/vazirmatn
Copyright holder per upstream release: Saber Rastikerdar.
```

- [ ] **Step 4: Write the Font Awesome (fa-solid.otf) font license**

Create `guide/fonts/fa-solid-LICENSE.txt` with the same SIL OFL 1.1 body as Step 3 (identical license text — only the trailing attribution block differs), replacing the trailing block with:

```
---
Font: Font Awesome 6 Free Solid (fa-solid.otf) — icon glyphs only (✔ U+F00C, ⚠ U+F071).
Copyright (c) 2024 Fonticons, Inc. with Reserved Font Name "Font Awesome".
Upstream: https://fontawesome.com — Fonts: SIL OFL 1.1 · Icons (SVG/JS): CC BY 4.0 · Code: MIT.
Only the OFL-licensed font file is bundled in this repository.
```

- [ ] **Step 5: Write the TeX Gyre Termes font license**

Create `guide/fonts/texgyretermes-LICENSE.txt`:

```
% This is version 1.0, dated 22 June 2009, of the GUST Font License.
% (GUST is the Polish TeX Users Group, https://www.gust.org.pl)
%
% For the most recent version of this license see
% https://www.gust.org.pl/fonts/licenses/GUST-FONT-LICENSE.txt
% or
% https://tug.org/fonts/licenses/GUST-FONT-LICENSE.txt
%
% This work may be distributed and/or modified under the conditions
% of the LaTeX Project Public License, either version 1.3c of this
% license or (at your option) any later version.
%
% Please also observe the following clause:
% 1) it is requested, but not legally required, that derived works be
%    distributed only after changing the names of the fonts comprising this
%    work and given in an accompanying "manifest", and that the
%    files comprising the Work, as listed in the manifest, also be given
%    new names. Any exceptions to this request are also given in the
%    manifest.
%
%    We recommend the manifest be given in a separate file named
%    MANIFEST-<fontid>.txt, where <fontid> is some unique identification
%    of the font family. If a separate "readme" file accompanies the Work,
%    we recommend a name of the form README-<fontid>.txt.
%
% The latest version of the LaTeX Project Public License is in
% https://www.latex-project.org/lppl.txt and version 1.3c or later
% is part of all distributions of LaTeX version 2006/05/20 or later.

---
Font family: TeX Gyre Termes (texgyretermes-regular/italic/bold/bolditalic.otf)
Upstream: https://www.gust.org.pl/projects/e-foundry/tex-gyre
Copyright (c) 2007-2015 by B. Jackowski and J.M. Nowacki (for the GUST e-foundry).
```

- [ ] **Step 6: Verify all five files exist and are non-empty**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
"/c/Program Files/Python311/python" -c "
import os
for f in ('LICENSE', 'LICENSE-CODE', 'guide/fonts/vazirmatn/LICENSE.txt',
          'guide/fonts/fa-solid-LICENSE.txt', 'guide/fonts/texgyretermes-LICENSE.txt'):
    sz = os.path.getsize(f)
    assert sz > 200, (f, sz)
    print(f, sz, 'bytes')
"
```
Expected: five lines, all sizes > 200 bytes.

---

### Task 3: CHANGELOG.md

**Files:**
- Create: `CHANGELOG.md`

**Interfaces:**
- Consumes: the real chapter list (13 chapters + پیوست الف, confirmed against `guide/guide.html`'s TOC in Step 1 below).
- Produces: version-history record linked from both READMEs (Task 6).

- [ ] **Step 1: Re-confirm the chapter list against the moved guide.html**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
"/c/Program Files/Python311/python" -c "
import re
h = open('guide/guide.html', encoding='utf-8').read()
toc = h[h.find('class=\"toc-list\"'):h.find('</nav>', h.find('class=\"toc-list\"'))]
rows = re.findall(r'<a class=\"toc-l1\"[^>]*>.*?<span class=\"t\">(.*?)</span>', toc, re.S)
for r in rows: print(re.sub(r'<[^>]+>', '', r).strip())
"
```
Expected (14 lines, matches what's used in Step 2 below):
```
پیش‌گفتار
۱. مقدمه: چرا این راهنما
۲. فیزیک شریف در یک نگاه: هفت خوشهٔ پژوهشی
۳. رمزگشایی برنامهٔ درسی: هر درس چه می‌آموزد و کجا به کار می‌آید
۴. مسیرهای تخصصی (ترک‌های اختیاری): از درس اختیاری تا خانوادهٔ شغلی
۵. نقشهٔ شغلی به تفکیک مقطع: جدول اصلی
۶. بعد از کارشناسی: چهار درِ واقعی
۷. بعد از کارشناسی ارشد: پلی که به دو سمت وصل است
۸. بعد از دکتری: بازارِ ساختارمند اما قطبی‌شده
۹. مسیرهای بین‌المللی: نقشهٔ واقعیِ ۱۴۰۴–۱۴۰۵
۱۰. شغل‌هایی که کمتر به آن‌ها فکر می‌کنیم
۱۱. نقشهٔ راه سال‌به‌سال
۱۲. مهارت‌هایی که برنامهٔ درسی نمی‌دهد و راه یادگیری‌شان
۱۳. باورهای غلط رایج دربارهٔ آیندهٔ شغلی فیزیک
پیوست الف: منابع
```

- [ ] **Step 2: Write CHANGELOG.md**

Create `CHANGELOG.md`:

```markdown
# Changelog — تاریخچهٔ تغییرات

> **دربارهٔ شماره‌گذاری نسخه‌ها:** در توسعهٔ داخلی، نسخه‌های ۱، ۱٫۱ و ۱٫۲ برچسب‌های
> تکرار داخلی بودند و هرگز منتشر نشدند. این مخزن اولین انتشار عمومی راهنماست،
> بنابراین شماره‌گذاری از ۱٫۰ آغاز می‌شود. برای شفافیت، آن سه تکرار داخلی در
> «تاریخچهٔ پیش از انتشار» زیر خلاصه شده‌اند.
>
> **On versioning:** internal development used v1, v1.1, and v1.2 as iteration
> labels; none were ever published. This repository is the guide's first
> public release, so numbering restarts at v1.0. For transparency, those
> three internal iterations are summarized under "Pre-release history" below.

تمام نسخه‌های نشانه‌گذاری‌شده بر پایهٔ [Semantic Versioning](https://semver.org/) هستند:
وصله (`v1.0.x`) برای اصلاح اشتباه یا به‌روزرسانی عددی، نسخهٔ فرعی (`v1.x.0`) برای
محتوای تازه یا فصل جدید، نسخهٔ اصلی (`v2.0.0`) برای بازطراحی ساختاری.

Tags follow [Semantic Versioning](https://semver.org/): patch (`v1.0.x`) for
corrections/data updates, minor (`v1.x.0`) for new content or a new chapter,
major (`v2.0.0`) for a structural rework.

## [1.0.0] — 2026-10-13

اولین انتشار عمومی. / First public release.

### افزوده‌شده / Added
- راهنمای کامل مسیرهای حرفه‌ای پس از فیزیک شریف، ۴۹ صفحه، شامل:
  - پیش‌گفتار و اصل راهنما: «هیچ عددی بدون منبع نیامده»
  - فصل ۱ — مقدمه: چرا این راهنما
  - فصل ۲ — فیزیک شریف در یک نگاه: هفت خوشهٔ پژوهشی
  - فصل ۳ — رمزگشایی برنامهٔ درسی
  - فصل ۴ — مسیرهای تخصصی (ترک‌های اختیاری)
  - فصل ۵ — نقشهٔ شغلی به تفکیک مقطع (جدول اصلی)
  - فصل ۶ — بعد از کارشناسی: چهار درِ واقعی
  - فصل ۷ — بعد از کارشناسی ارشد
  - فصل ۸ — بعد از دکتری: بازارِ ساختارمند اما قطبی‌شده
  - فصل ۹ — مسیرهای بین‌المللی: نقشهٔ واقعیِ ۱۴۰۴–۱۴۰۵
  - فصل ۱۰ — شغل‌هایی که کمتر به آن‌ها فکر می‌کنیم
  - فصل ۱۱ — نقشهٔ راه سال‌به‌سال
  - فصل ۱۲ — مهارت‌هایی که برنامهٔ درسی نمی‌دهد
  - فصل ۱۳ — باورهای غلط رایج دربارهٔ آیندهٔ شغلی فیزیک
  - پیوست الف — منابع (۶ گزارش پژوهشی زمینه‌ای، ادغام‌شده و ارجاع‌داده‌شده)
- طرح انتشار: جلد با نوار سری، شناسنامهٔ انتشار (ناشر، تاریخ، نسخه)، فهرست
  مطالب با شمارهٔ صفحهٔ واقعی، سرصفحه و شمارهٔ صفحهٔ فارسی در تمام صفحات.
- یادداشت‌های روش‌شناسی (`docs/methodology.md`) — فرایند راستی‌آزمایی و
  تناقض‌های حل‌شدهٔ میان شش گزارش منبع.

A complete career-paths guide for physics graduates of Sharif University,
49 pages, covering the department's seven research clusters, the curriculum,
specialization tracks, a career map by degree level, four real post-BSc
paths, the MSc/PhD job markets, international paths (current as of
۱۴۰۴–۱۴۰۵ / 2025–2026), under-considered careers, a year-by-year roadmap,
skills the curriculum doesn't teach, and common misconceptions — plus a
sourced bibliography appendix. Publication-edition front matter (cover
band, publication/شناسنامه page, real TOC page numbers, Persian folios on
every page). Methodology notes documenting how conflicts between the six
source research reports were resolved.

## Pre-release history (not separately released) — تاریخچهٔ پیش از انتشار

- **v1.2 (2026-10-12):** تبدیل تمام جدول‌های landscape به portrait (جمع‌فشرده،
  جدول ۱۰.۱ از ۶ به ۴ ستون ادغام شد)، ویرایش طبیعی فارسی (نزدیک به ۹۸ اصلاح،
  حذف واژه‌های ناخوشایند و تنوین نابجا)، به‌روزرسانی جلد به «نسخهٔ ۱٫۲».
  / Portrait conversion of all four landscape tables (جدول ۱۰.۱ merged
  6→4 columns), a ~98-edit natural-Persian line edit, cover bumped to
  نسخهٔ ۱٫۲. See `docs/design/2026-10-12-v1.2-portrait-natural-persian-design.md`.
- **v1.1 (2026-10-09):** تبدیل تاریخ‌ها به شمسی، اعداد و ارز به فارسی/کلمه،
  اصلاح شمارهٔ بخش‌ها (۸٫۲ به‌جای ۸٫۲ با ویرگول عربی).
  / Dates converted to Shamsi, digits and currency to Persian-word form,
  section-numbering punctuation fixed.
- **v1 (2026-10-09):** اولین نسخهٔ تولیدشده، از طریق خط لولهٔ مبتنی بر Markdown
  (در `legacy/` بایگانی شده)، ۵۶ صفحه، جدول‌های landscape، بر پایهٔ ترکیب
  شش گزارش پژوهشی (R1–R6).
  / First generated draft via the markdown-based pipeline (archived in
  `legacy/`), 56 pp, landscape tables, synthesized from six source research
  reports (R1–R6). See `legacy/build-report-v1.md`.
```

- [ ] **Step 3: Verify**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
"/c/Program Files/Python311/python" -c "
h = open('CHANGELOG.md', encoding='utf-8').read()
for s in ('[1.0.0]', 'Pre-release history', '۱۳. باورهای', 'semver.org', 'legacy/build-report-v1.md'):
    assert s in h, s
print('CHANGELOG OK,', len(h), 'bytes')
"
```

---

### Task 4: provenance/README.md and legacy/README.md

**Files:**
- Create: `provenance/README.md`, `legacy/README.md`

**Interfaces:** none (standalone explanatory docs).

- [ ] **Step 1: Write provenance/README.md**

Create `provenance/README.md`:

```markdown
# Provenance — خاستگاه سند

## فارسی

این دو فایل، ورودی منجمد خط لولهٔ ویرایشی هستند و **هرگز دست‌خورده نمی‌شوند**:

- `guide_v1_original.html` — نسخهٔ اولیهٔ تولیدشده، پیش از هر ویرایش.
- `style_v1_original.css` — شیوه‌نامهٔ اولیه.

تمام تغییرات رسمی (نسخه‌های ۱٫۱، ۱٫۲ و شناسنامهٔ انتشار ۱٫۰) به‌صورت یک رشته
تبدیل‌های قطعی و قابل بازاجرا در `guide/refine.py` ثبت شده‌اند — نه با دستی
ویرایش این دو فایل. این الگو یک ضمانت را فراهم می‌کند: هر تغییری در محتوا
قابل ردیابی تا منبعش است.

اگر در آینده یک دور ویرایشی بزرگ (نه فقط چند جمله) با همین ضمانت audit-trail
لازم شد، نقطهٔ شروع باید همین دو فایل باشند — نه `guide/guide.html` که خودش
محصول نهاییِ قابل‌ویرایش مستقیم است (رجوع کنید به `CONTRIBUTING.md`).

## English

These two files are the frozen input to the editorial pipeline and are
**never edited**:

- `guide_v1_original.html` — the first generated draft, before any pass.
- `style_v1_original.css` — the original stylesheet.

Every official change (v1.1, v1.2, and the v1.0 publication-edition front
matter) is recorded as a chain of deterministic, re-runnable transforms in
`guide/refine.py` — never by hand-editing these two files. This pattern
gives one guarantee: every content change traces back to its source.

If a future large editorial pass (not just a sentence or two) needs that
same audit-trail guarantee, these two files are the starting point — not
`guide/guide.html`, which is itself the directly-editable current state
(see `CONTRIBUTING.md`).
```

- [ ] **Step 2: Write legacy/README.md**

Create `legacy/README.md`:

```markdown
# Legacy — بایگانی

## فارسی

محتوای این پوشه **غیرفعال و جایگزین‌شده** است؛ فقط برای شفافیت تاریخی نگه
داشته شده:

- `pipeline/` — نسل اول خط لولهٔ ساخت سند (`md2html.py` → `finalize.py`)،
  مبتنی بر ورودی Markdown که دیگر در این مخزن وجود ندارد. این اسکریپت‌ها
  مسیر sandbox غیرموجودی (`/home/z/my-project/scripts`) را import می‌کنند و
  **اجرا نمی‌شوند**. جایگزین شدند با `guide/refine.py` + `guide/build.py`
  که مستقیماً از `guide/guide.html` کار می‌کنند.
- `build-report-v1.md` — گزارش ساخت اولین نسخه (۵۶ صفحه، جدول‌های landscape).
- `pdfs/` — سه تکرار داخلی پیش از انتشار عمومی (v1، v1.1، v1.2) —
  جزئیات هرکدام در `CHANGELOG.md`، بخش «تاریخچهٔ پیش از انتشار».

## English

Everything in this folder is **superseded and non-functional**, kept only
for historical transparency:

- `pipeline/` — the first-generation build pipeline (`md2html.py` →
  `finalize.py`), driven by Markdown source that no longer exists in this
  repository. These scripts import a nonexistent sandbox path
  (`/home/z/my-project/scripts`) and **will not run**. Replaced by
  `guide/refine.py` + `guide/build.py`, which work directly from
  `guide/guide.html`.
- `build-report-v1.md` — the build report for the very first render (56 pp,
  landscape tables).
- `pdfs/` — the three internal pre-release iterations (v1, v1.1, v1.2) —
  see `CHANGELOG.md`'s "Pre-release history" section for what each contains.
```

- [ ] **Step 3: Verify**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
"/c/Program Files/Python311/python" -c "
for f in ('provenance/README.md', 'legacy/README.md'):
    h = open(f, encoding='utf-8').read()
    assert len(h) > 300, (f, len(h))
    print(f, len(h), 'bytes')
"
```

---

### Task 5: CONTRIBUTING.md

**Files:**
- Create: `CONTRIBUTING.md`

**Interfaces:** none (standalone doc; references `provenance/README.md`'s guidance on when to use refine.py vs. direct edits).

- [ ] **Step 1: Write CONTRIBUTING.md**

Create `CONTRIBUTING.md`:

```markdown
# Contributing — مشارکت

## فارسی

بیشتر مشارکت‌های مفید در این مخزن، **اصلاح یک واقعیت یا عدد** هستند، نه کد.
این سند هر دو مسیر را توضیح می‌دهد.

### اصلاح یک واقعیت یا عدد

1. یک [Issue](../../issues/new?template=fact-correction.md) با الگوی
   «اصلاح واقعیت» باز کنید: بخش/صفحه، چه چیزی اشتباه است، و **منبع معتبر
   برای اصلاح** (این مهم‌ترین قسمت است — راهنما قولِ «هیچ عددی بدون منبع»
   داده؛ یک اصلاح بدون منبع هم همان مشکل را دارد).
2. یا مستقیماً یک Pull Request بزنید: `guide/guide.html` را ویرایش کنید
   (متن قابل‌جست‌وجو و خوانا است)، سپس طبق بخش «بازساخت محلی» زیر، PDF را
   بسازید و بررسی کنید که هنوز درست رندر می‌شود.
3. برای تغییرات بزرگ‌تر (یک فصل کامل، بازطراحی یک بخش)، به جای ویرایش مستقیم
   `guide.html`، یک تبدیل جدید و قطعی در `guide/refine.py` اضافه کنید —
   همان الگویی که نسخه‌های ۱٫۱ و ۱٫۲ از آن استفاده کردند (به `provenance/README.md`
   مراجعه کنید). این الگو تضمین می‌کند تغییر از ابتدا تا انتها قابل‌ردیابی بماند.

### بازساخت محلی

```bash
pip install -r requirements.txt
cd guide
python refine.py   # فقط اگر refine.py را تغییر داده‌اید
python build.py    # -> ../dist/SUT_Physics_Career_Guide_v1.0.pdf
```
پیش‌نیاز: Python 3.11+‎، هیچ فونتی از سیستم لازم نیست (همه در `guide/fonts/`
بسته‌بندی شده‌اند).

### قوانین محتوایی

- هر عدد یا ادعای تازه باید منبع داشته باشد.
- تاریخ‌ها فقط شمسی، اعداد فارسی، واحد پول به کلمهٔ فارسی.
- کارفرمایان تحریم‌شده یا مرتبط با حوزهٔ دفاعی هرگز به‌عنوان مقصد پیشنهادی
  معرفی نمی‌شوند؛ فقط با نشان هشدار مشخص می‌شوند.

### نسخه‌گذاری

برچسب‌ها طبق Semantic Versioning: `v1.0.x` برای اصلاح، `v1.x.0` برای محتوای
تازه، `v2.0.0` برای بازطراحی ساختاری. جزئیات در `CHANGELOG.md`.

## English

Most useful contributions here are **a fact or number correction**, not
code. Both paths:

### Correcting a fact or number

1. Open a [fact-correction Issue](../../issues/new?template=fact-correction.md):
   which section/page, what's wrong, and **a credible source for the fix**
   (this is the important part — the guide promises no number without a
   source; an uncited correction has the same problem it's fixing).
2. Or open a Pull Request directly: edit `guide/guide.html` (it's readable,
   searchable plain HTML), then rebuild per "Local rebuild" below and check
   it still renders correctly.
3. For larger changes (a whole chapter, a section redesign), add a new
   deterministic transform to `guide/refine.py` instead of hand-editing
   `guide.html` — the same pattern v1.1 and v1.2 used (see
   `provenance/README.md`). This keeps the change traceable end to end.

### Local rebuild

```bash
pip install -r requirements.txt
cd guide
python refine.py   # only if you changed refine.py
python build.py    # -> ../dist/SUT_Physics_Career_Guide_v1.0.pdf
```
Requires Python 3.11+. No system fonts needed — everything is bundled
under `guide/fonts/`.

### Content rules

- Every new number or claim needs a source.
- Shamsi dates only, Persian digits, currency spelled in Persian words.
- Sanctioned or defense-adjacent employers are never presented as a
  suggested destination — only flagged with a warning mark.

### Versioning

Tags follow Semantic Versioning: `v1.0.x` for corrections, `v1.x.0` for new
content, `v2.0.0` for a structural rework. Details in `CHANGELOG.md`.
```

- [ ] **Step 2: Verify**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
"/c/Program Files/Python311/python" -c "
h = open('CONTRIBUTING.md', encoding='utf-8').read()
for s in ('fact-correction.md', 'refine.py', 'python build.py', 'Semantic Versioning'):
    assert s in h, s
print('CONTRIBUTING OK,', len(h), 'bytes')
"
```

---

### Task 6: Bilingual READMEs

**Files:**
- Create: `README.md` (English-primary), `README.fa.md` (Persian-primary)

**Interfaces:**
- Consumes: the chapter list confirmed in Task 3 Step 1; `LICENSE`/`LICENSE-CODE` from Task 2; `CHANGELOG.md` from Task 3; `CONTRIBUTING.md` from Task 5; `dist/SUT_Physics_Career_Guide_v1.0.pdf` from Task 1.

- [ ] **Step 1: Write README.md (English)**

Create `README.md`:

```markdown
# راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف
### A Career-Paths Guide for Sharif Physics Graduates

**[برای نسخهٔ فارسی کامل، به README.fa.md مراجعه کنید → Full Persian README](README.fa.md)**

---

A complete, source-cited guide to career and academic paths after a
physics degree at Sharif University of Technology — written by and for
the department's own student community. Published by **انجمن علمی
دانشکدهٔ فیزیک، دانشگاه صنعتی شریف** (the Sharif Physics Students'
Scientific Association), a non-profit student body.

📄 **[Download the latest PDF](dist/SUT_Physics_Career_Guide_v1.0.pdf)** (49 pages, Persian, A4)

## What's inside

13 chapters + a sourced bibliography appendix: the department's seven
research clusters, how to read the curriculum, specialization tracks, a
career map by degree level, four real post-BSc paths, the MSc/PhD job
markets, international paths (current as of 1404–1405 / 2025–2026),
under-considered careers, a year-by-year roadmap, skills the curriculum
doesn't teach, and common misconceptions about physics career prospects.

The guide's one rule, stated in its preface: **every claim is linked to a
source; every career path carries a confidence level; where no reliable
figure exists, it says so plainly** rather than inventing one. Sanctioned
or defense-adjacent employers are flagged, never recommended.

## Repository map

| Path | What it is |
|---|---|
| `guide/` | The live document — `guide.html` + `style.css` are what you edit; `refine.py`/`build.py` are the build pipeline |
| `provenance/` | Frozen original HTML/CSS the pipeline's edit history traces back to — never edited directly |
| `dist/` | The built PDF |
| `docs/methodology.md` | Fact-checking notes: how conflicts between the six source research reports were resolved |
| `docs/design/` | Design specs and implementation plans from past editorial rounds |
| `legacy/` | A superseded first-generation build pipeline and the three pre-release PDF iterations, kept for history |

## Rebuild it yourself

```bash
pip install -r requirements.txt
cd guide
python build.py    # -> ../dist/SUT_Physics_Career_Guide_v1.0.pdf
```
Requires Python 3.11+. No system fonts needed (Vazirmatn, TeX Gyre Termes,
and Font Awesome icons are bundled under `guide/fonts/`).

## Contributing

Most contributions are fact or number corrections — see
[CONTRIBUTING.md](CONTRIBUTING.md). Every correction needs a cited source.

## Licensing

- **Guide content** (`guide/guide.html`, `docs/`, the PDF) —
  [CC BY-NC-SA 4.0](LICENSE): share and adapt with attribution, no
  commercial use, share-alike.
- **Pipeline code** (`*.py`, `style.css`, `.github/`) —
  [MIT](LICENSE-CODE).
- **Bundled fonts** — each under its own license: Vazirmatn (SIL OFL 1.1),
  TeX Gyre Termes (GUST Font License / LPPL), Font Awesome 6 Free Solid
  (SIL OFL 1.1). See `guide/fonts/*/LICENSE.txt`.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) — includes a note on why versioning
starts at v1.0 despite earlier "v1.2"-labelled internal drafts.

## Contact

**[@Anjoman_Elmi_Phys_sut](https://t.me/Anjoman_Elmi_Phys_sut)** on Telegram.
```

- [ ] **Step 2: Write README.fa.md (Persian)**

Create `README.fa.md`:

```markdown
# راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف

**[English README](README.md)**

---

راهنمایی کامل و منبع‌دار از مسیرهای شغلی و تحصیلی پس از فیزیک شریف — نوشته‌شده
توسط و برای دانشجویان خودِ این دانشکده. منتشرشده توسط **انجمن علمی دانشکدهٔ
فیزیک، دانشگاه صنعتی شریف**، یک تشکل دانشجویی غیرانتفاعی.

📄 **[دانلود آخرین نسخهٔ PDF](dist/SUT_Physics_Career_Guide_v1.0.pdf)** (۴۹ صفحه، فارسی، A4)

## این راهنما برای کیست؟

برای دبیرستانی‌هایی که می‌خواهند بدانند فیزیک به کجا می‌رسد، و دانشجویان
فیزیک شریف که می‌خواهند هر ترم آگاهانه‌تر تصمیم بگیرند.

## محتوا

۱۳ فصل به‌علاوهٔ پیوست منابع:

۱. مقدمه: چرا این راهنما · ۲. فیزیک شریف در یک نگاه: هفت خوشهٔ پژوهشی ·
۳. رمزگشایی برنامهٔ درسی · ۴. مسیرهای تخصصی (ترک‌های اختیاری) ·
۵. نقشهٔ شغلی به تفکیک مقطع (جدول اصلی) · ۶. بعد از کارشناسی: چهار درِ واقعی ·
۷. بعد از کارشناسی ارشد · ۸. بعد از دکتری: بازارِ ساختارمند اما قطبی‌شده ·
۹. مسیرهای بین‌المللی: نقشهٔ واقعیِ ۱۴۰۴–۱۴۰۵ · ۱۰. شغل‌هایی که کمتر به
آن‌ها فکر می‌کنیم · ۱۱. نقشهٔ راه سال‌به‌سال · ۱۲. مهارت‌هایی که برنامهٔ
درسی نمی‌دهد · ۱۳. باورهای غلط رایج دربارهٔ آیندهٔ شغلی فیزیک · پیوست الف:
منابع.

اصل حاکم بر راهنما، از پیش‌گفتار: **همهٔ ادعاها به منبع متصل‌اند؛ هر مسیر
شغلی سطح اطمینان (بالا / متوسط / پایین) دارد؛ هیچ عددی بدون منبع نیامده و
جایی که آمار معتبری پیدا نشد، صادقانه نوشته‌ایم «رقم معتبری یافت نشد».**
کارفرمایانِ تحریم‌شده یا مرتبط با حوزهٔ دفاعی فقط با نشان هشدار مشخص
می‌شوند و هرگز به‌عنوان مقصد پیشنهادی معرفی نمی‌شوند.

## نقشهٔ مخزن

| مسیر | توضیح |
|---|---|
| `guide/` | سند زنده — `guide.html` و `style.css` قابل‌ویرایش هستند؛ `refine.py`/`build.py` خط لولهٔ ساخت‌اند |
| `provenance/` | HTML/CSS اولیهٔ منجمد که تاریخچهٔ ویرایش خط لوله از آن آغاز می‌شود — هرگز مستقیم ویرایش نمی‌شود |
| `dist/` | فایل PDF ساخته‌شده |
| `docs/methodology.md` | یادداشت‌های راستی‌آزمایی: نحوهٔ حل تناقض میان شش گزارش پژوهشی منبع |
| `docs/design/` | اسناد طراحی و برنامه‌های اجرای دورهای ویرایشی گذشته |
| `legacy/` | خط لولهٔ ساخت نسل اول (غیرفعال) و سه تکرار داخلی پیش از انتشار، برای تاریخچه |

## بازساخت محلی

```bash
pip install -r requirements.txt
cd guide
python build.py    # -> ../dist/SUT_Physics_Career_Guide_v1.0.pdf
```
نیازمند Python 3.11+‎. نیازی به فونت سیستمی نیست (Vazirmatn، TeX Gyre
Termes و آیکون‌های Font Awesome همگی در `guide/fonts/` بسته‌بندی شده‌اند).

## مشارکت

بیشتر مشارکت‌ها اصلاح یک واقعیت یا عدد است — به [CONTRIBUTING.md](CONTRIBUTING.md)
مراجعه کنید. هر اصلاحی به یک منبع معتبر نیاز دارد.

## مجوزها

- **محتوای راهنما** (`guide/guide.html`، `docs/`، فایل PDF) —
  [CC BY-NC-SA 4.0](LICENSE): اشتراک‌گذاری و تغییر با ذکر منبع آزاد است،
  استفادهٔ تجاری ممنوع، انتشار مجدد باید با همین مجوز باشد.
- **کد خط لوله** (`*.py`، `style.css`، `.github/`) — [MIT](LICENSE-CODE).
- **فونت‌های بسته‌بندی‌شده** — هرکدام با مجوز خودشان: Vazirmatn (SIL OFL 1.1)،
  TeX Gyre Termes (GUST Font License / LPPL)، Font Awesome 6 Free Solid
  (SIL OFL 1.1). به `guide/fonts/*/LICENSE.txt` مراجعه کنید.

## تاریخچهٔ تغییرات

به [CHANGELOG.md](CHANGELOG.md) مراجعه کنید — شامل توضیحی دربارهٔ اینکه چرا
شماره‌گذاری از ۱٫۰ شروع می‌شود، با وجود تکرارهای داخلی قبلی با برچسب «۱٫۲».

## ارتباط

کانال تلگرام: **[@Anjoman_Elmi_Phys_sut](https://t.me/Anjoman_Elmi_Phys_sut)**
```

- [ ] **Step 3: Verify**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
"/c/Program Files/Python311/python" -c "
for f, needle in (('README.md', 'README.fa.md'), ('README.fa.md', 'README.md')):
    h = open(f, encoding='utf-8').read()
    assert needle in h, (f, needle)
    assert 'CC BY-NC-SA' in h and 'CONTRIBUTING.md' in h and 'CHANGELOG.md' in h, f
    print(f, len(h), 'bytes, cross-links OK')
"
```

---

### Task 7: .gitignore, .gitattributes, requirements.txt

**Files:**
- Create: `.gitignore`, `.gitattributes`, `requirements.txt`

**Interfaces:**
- Produces: the exclusion rules Task 9's `git add` relies on not needing to special-case manually (belt-and-braces — Task 9 still uses explicit paths, never `-A`, but `.gitignore` protects future contributors who do use `-A`).

- [ ] **Step 1: Write .gitignore**

Create `.gitignore`:

```
# internal agent/process scratch — never public
.superpowers/

# superseded top-level files, left in place but not tracked
/channel_post.md
/راهنمای_مسیرهای_حرفه‌ای_پس_از_فیزیک_شریف.pdf

# now-empty husks left behind by the repo reorg
/source/
/docs/superpowers/

# build scratch the pipeline sometimes leaves behind
__pycache__/
*.pyc
_*.png
_*.json
_*.html
!guide/guide.html
!provenance/guide_v1_original.html
```

- [ ] **Step 2: Write .gitattributes**

Create `.gitattributes`:

```
# Force LF on the pipeline's text sources — a CRLF checkout changes byte
# sizes for any future fingerprint/integrity check (lesson learned on a
# sibling project: never trust core.autocrlf for Persian RTL HTML).
*.html text eol=lf
*.css text eol=lf
*.py text eol=lf
*.md text eol=lf
*.txt text eol=lf
.gitignore text eol=lf
.gitattributes text eol=lf

# binary, never diff/convert
*.pdf binary
*.png binary
*.ttf binary
*.otf binary
```

- [ ] **Step 3: Write requirements.txt**

Create `requirements.txt`:

```
weasyprint>=68,<69
pymupdf>=1.24
```

- [ ] **Step 4: Verify**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
"/c/Program Files/Python311/python" -c "
for f in ('.gitignore', '.gitattributes', 'requirements.txt'):
    h = open(f, encoding='utf-8').read()
    assert len(h) > 20, f
    print(f, len(h), 'bytes')
"
```

---

### Task 8: GitHub Actions CI + issue template

**Files:**
- Create: `.github/workflows/build-check.yml`, `.github/workflows/release.yml`, `.github/ISSUE_TEMPLATE/fact-correction.md`

**Interfaces:**
- Consumes: `requirements.txt` (Task 7); `guide/build.py` (Task 1) writing to `../dist/SUT_Physics_Career_Guide_v1.0.pdf`.

- [ ] **Step 1: Write build-check.yml**

Create `.github/workflows/build-check.yml`:

```yaml
name: Build check

on:
  push:
    paths: ["guide/**", "requirements.txt"]
  pull_request:
    paths: ["guide/**", "requirements.txt"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install system deps for WeasyPrint
        run: |
          sudo apt-get update
          sudo apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libharfbuzz-subset0
      - name: Install Python deps
        run: pip install -r requirements.txt
      - name: Build the guide
        run: |
          cd guide
          python refine.py
          python build.py
      - name: Verify output
        run: |
          python -c "
          import fitz
          d = fitz.open('dist/SUT_Physics_Career_Guide_v1.0.pdf')
          land = [i + 1 for i, p in enumerate(d) if p.rect.width > p.rect.height]
          assert not land, land
          assert len(d) >= 40, len(d)
          print('build-check OK:', len(d), 'pages, all portrait')
          "
```

- [ ] **Step 2: Write release.yml**

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags: ["v*"]

jobs:
  build-and-release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install system deps for WeasyPrint
        run: |
          sudo apt-get update
          sudo apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libharfbuzz-subset0
      - name: Install Python deps
        run: pip install -r requirements.txt
      - name: Build the guide
        run: |
          cd guide
          python refine.py
          python build.py
      - name: Attach PDF to the release
        uses: softprops/action-gh-release@v2
        with:
          files: dist/SUT_Physics_Career_Guide_v1.0.pdf
          generate_release_notes: true
```

- [ ] **Step 3: Write the fact-correction issue template**

Create `.github/ISSUE_TEMPLATE/fact-correction.md`:

```markdown
---
name: اصلاح واقعیت / Fact correction
about: گزارش یک عدد یا ادعای نادرست در راهنما / Report an incorrect number or claim in the guide
title: "[اصلاح] "
labels: fact-correction
---

**بخش/صفحه — Section/page**
<!-- مثال: فصل ۹، بخش ۹.۳ / e.g. Chapter 9, section 9.3 -->

**چه چیزی اشتباه است؟ — What's wrong?**

**منبع معتبر برای اصلاح — Credible source for the correction**
<!-- این بخش الزامی است — راهنما قول «هیچ عددی بدون منبع» داده.
     Required — the guide promises no number without a source. -->
```

- [ ] **Step 4: Verify**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
"/c/Program Files/Python311/python" -c "
import yaml
for f in ('.github/workflows/build-check.yml', '.github/workflows/release.yml'):
    with open(f, encoding='utf-8') as fh:
        d = yaml.safe_load(fh)
    assert 'jobs' in d, f
    print(f, 'parses as valid YAML')
h = open('.github/ISSUE_TEMPLATE/fact-correction.md', encoding='utf-8').read()
assert 'fact-correction' in h and 'منبع معتبر' in h
print('issue template OK')
" 2>&1 || "/c/Program Files/Python311/python" -c "
# fallback if pyyaml isn't installed: just confirm the files are non-empty and start with the expected key
for f in ('.github/workflows/build-check.yml', '.github/workflows/release.yml'):
    h = open(f, encoding='utf-8').read()
    assert h.startswith('name:') and 'jobs:' in h, f
    print(f, len(h), 'bytes, structurally OK')
"
```

---

### Task 9: git init, initial commit, create + push GitHub repo, tag + release v1.0.0

**Files:** none created — this task only runs git/gh commands over the tree built by Tasks 1–8.

**Interfaces:**
- Consumes: the complete file tree from Tasks 1–8, plus the plan/spec files still sitting at `docs/superpowers/{specs,plans}/` (deferred from Task 1 — see its note).
- Produces: the public repo `SireJeff/anjoman-physics-career-guide`, tag `v1.0.0`, a GitHub Release with the PDF attached.

- [ ] **Step 1: Promote the design docs (deferred from Task 1)**

This is the last task — nothing after this re-reads the plan from its original path, so it's now safe to move it.

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
mv docs/superpowers/specs/2026-10-12-v1.2-portrait-natural-persian-design.md docs/design/
mv docs/superpowers/plans/2026-10-12-v1.2-portrait-natural-persian.md docs/design/
mv docs/superpowers/specs/2026-10-21-github-publication-design.md docs/design/
mv docs/superpowers/plans/2026-10-21-github-publication.md docs/design/
ls docs/design/
```
Expected: four files listed.

- [ ] **Step 2: Initialize git and inspect what's on disk before staging**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
GIT="/c/Program Files/Git/cmd/git.exe"
"$GIT" init
"$GIT" branch -m main
"/c/Program Files/Python311/python" -c "
import os
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', '.superpowers', 'source')]
    for f in files:
        print(os.path.relpath(os.path.join(root, f), '.'))
" | sort
```
Review the printed list against the Global Constraints exclusion list before Step 3 — confirm `channel_post.md`, the Persian-filename PDF, and anything under `.superpowers/`/`source/`/`docs/superpowers/` do NOT appear (the walk already skips `.superpowers` and `source`, but re-confirm `docs/superpowers/` is now empty — both its subdirectories were just emptied by Step 1 — and the two loose files are visible-but-about-to-be-excluded).

- [ ] **Step 3: Stage explicit paths only and commit**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
GIT="/c/Program Files/Git/cmd/git.exe"
"$GIT" add README.md README.fa.md CHANGELOG.md CONTRIBUTING.md LICENSE LICENSE-CODE \
  .gitignore .gitattributes requirements.txt \
  guide/ provenance/ dist/ docs/methodology.md docs/design/ legacy/ .github/
"$GIT" status --short | head -30
"$GIT" commit -m "feat: first public release — راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف v1.0.0

Publication-edition guide (49 pp, A4, all-portrait), live refine.py/build.py
pipeline, frozen provenance originals, bilingual READMEs, CC BY-NC-SA 4.0
content license + MIT pipeline license, CI build-check + tag-triggered
release workflow, archived first-generation pipeline and pre-release
iterations (v1/v1.1/v1.2) under legacy/.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```
Expected: `git status --short` before the commit shows only `A` (added) entries under the intended paths — no `channel_post.md`, no Persian-filename PDF, no `.superpowers/`.

- [ ] **Step 4: Verify the commit's tree matches Task 1's final-state check**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
GIT="/c/Program Files/Git/cmd/git.exe"
"$GIT" ls-files | wc -l
"$GIT" ls-files | grep -c "^legacy/pdfs/"
"$GIT" log -1 --format="%H %s"
```
Expected: a nonzero file count; exactly 3 files under `legacy/pdfs/`; one commit logged.

- [ ] **Step 5: Create the GitHub repo and push**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
GH="/c/Program Files/GitHub CLI/gh.exe"
"$GH" repo create anjoman-physics-career-guide --public --source=. --remote=origin \
  --description "راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف — a sourced career-paths guide for Sharif physics graduates, published by the department's student association" \
  --push
```
Expected: creates `SireJeff/anjoman-physics-career-guide` on GitHub, sets `origin`, pushes `main`.

- [ ] **Step 6: Confirm CI passes on the initial push**

```bash
GH="/c/Program Files/GitHub CLI/gh.exe"
"$GH" run list --repo SireJeff/anjoman-physics-career-guide --limit 3
```
Wait for the `build-check` run to reach `completed`/`success` (poll every ~30s, up to 5 minutes — WeasyPrint's apt install + font setup takes a couple of minutes on a fresh Ubuntu runner). If it fails, read the log (`"$GH" run view --repo SireJeff/anjoman-physics-career-guide --log-failed`) and fix before proceeding — do not tag a release on top of a known-broken CI run.

- [ ] **Step 7: Tag and release v1.0.0**

```bash
cd "/c/Users/Surface Laptop 3/Downloads/SUT_Physics_Career_Guide_deliverables"
GIT="/c/Program Files/Git/cmd/git.exe"
GH="/c/Program Files/GitHub CLI/gh.exe"
"$GIT" tag -a v1.0.0 -m "راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف — نسخهٔ ۱٫۰، اولین انتشار عمومی

First public release. See CHANGELOG.md."
"$GIT" push origin v1.0.0
```
Pushing the tag triggers `release.yml`. Poll `"$GH" run list --repo SireJeff/anjoman-physics-career-guide --limit 3` until the `Release` run completes, then confirm:
```bash
"$GH" release view v1.0.0 --repo SireJeff/anjoman-physics-career-guide
```
Expected: shows the release with `SUT_Physics_Career_Guide_v1.0.pdf` listed as an asset.

- [ ] **Step 8: Verify both READMEs render on GitHub**

```bash
GH="/c/Program Files/GitHub CLI/gh.exe"
"$GH" api repos/SireJeff/anjoman-physics-career-guide/readme --jq '.name'
"$GH" api repos/SireJeff/anjoman-physics-career-guide/contents/README.fa.md --jq '.name'
```
Expected: `README.md` then `README.fa.md` — confirms GitHub picked up `README.md` as the repo's default rendered readme and that `README.fa.md` exists and is fetchable (both responses succeeding, rather than a 404, is the actual render check available without a browser).

- [ ] **Step 9: Final report**

Report to the user: the repo URL, the release URL, confirmation CI is green, and a one-line reminder of what's left physically on disk but outside the repo (`channel_post.md`, the Persian-filename PDF, `.superpowers/`) in case they want those cleaned up separately.
