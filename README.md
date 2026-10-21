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
  (SIL OFL 1.1). See `guide/fonts/vazirmatn/LICENSE.txt`,
  `guide/fonts/texgyretermes-LICENSE.txt`, and `guide/fonts/fa-solid-LICENSE.txt`.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) — includes a note on why versioning
starts at v1.0 despite earlier "v1.2"-labelled internal drafts.

## Contact

**[@Anjoman_Elmi_Phys_sut](https://t.me/Anjoman_Elmi_Phys_sut)** on Telegram.
