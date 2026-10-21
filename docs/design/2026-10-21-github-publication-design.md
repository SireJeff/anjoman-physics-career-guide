# GitHub Publication — Repository Structure & Governance Design

**Date:** 2026-10-21 · **Status:** approved in chat · **Target:** public repo `SireJeff/anjoman-physics-career-guide`

## Context

The guide has shipped three internal iterations (v1 → v1.1 → v1.2) inside a flat, non-git `Downloads/SUT_Physics_Career_Guide_deliverables/` folder, plus a just-finished "publication edition" restyle (cover band + شناسنامه page) built as the first public-facing release. The folder also carries a dead first-generation pipeline (`md2html.py`/`finalize.py`/`mdparse.py`/`inliner.py` — imports a nonexistent sandbox path, no Markdown source left) and internal agent scratch (`.superpowers/sdd/`). None of this has a public home, a license, a changelog, or a contribution path, and the user wants the guide "updated through the years to come" — i.e. a structure a future maintainer (not necessarily this session) can pick up.

## Goals

1. A clean public GitHub repo: live pipeline separated from frozen provenance, separated from archived dead pipeline.
2. Clear licensing — content and code licensed separately, with real license files bundled (not just referenced).
3. A changelog that resolves the confusing version history honestly (old v1/v1.1/v1.2 were internal iteration labels; this release restarts numbering at v1.0 as the actual first public release).
4. Bilingual documentation — Persian for the actual audience, English for GitHub's default audience and future contributors.
5. A rebuild path any future maintainer can run (`pip install -r requirements.txt && python guide/build.py`), plus CI that catches breakage and automates PDF attachment to tagged releases.

## Non-goals

No content edits to the guide itself · no new design work on the PDF (the publication-edition restyle is already done) · no attempt to resurrect the dead markdown pipeline · no org/team setup beyond the single personal-account repo.

## Approved decisions

| Question | Decision |
|---|---|
| Repo | `SireJeff/anjoman-physics-career-guide`, public (matches the `anjoman-accounting` precedent on the same account) |
| Content license | CC BY-NC-SA 4.0 |
| Code license | MIT, in a separate `LICENSE-CODE` file |
| PDF distribution | Committed in `dist/` **and** attached to GitHub Releases |
| Dead pipeline + old iteration PDFs | Kept, moved to `legacy/`, clearly marked non-functional/superseded |

## Design

### 1. Directory structure

```
anjoman-physics-career-guide/
├── README.md               English-primary, links to README.fa.md
├── README.fa.md             Persian-primary — the real front door
├── CHANGELOG.md
├── LICENSE                  CC BY-NC-SA 4.0 (content)
├── LICENSE-CODE              MIT (pipeline)
├── CONTRIBUTING.md
├── requirements.txt
├── .gitattributes
├── .gitignore
├── guide/                   the LIVE document
│   ├── guide.html            editable source — direct edits are a supported workflow
│   ├── style.css
│   ├── refine.py              deterministic editorial-pass log (audit trail, re-runnable from provenance/)
│   ├── build.py                guide.html -> ../dist/*.pdf
│   ├── anjoman_logo.png
│   └── fonts/
│       ├── vazirmatn/ (+ LICENSE.txt, SIL OFL 1.1)
│       ├── texgyretermes-*.otf (+ LICENSE.txt, GUST Font License / LPPL)
│       └── fa-solid.otf (+ LICENSE.txt, SIL OFL 1.1)
├── provenance/               frozen originals, never edited — refine.py's input
│   ├── README.md
│   ├── guide_v1_original.html
│   └── style_v1_original.css
├── dist/
│   └── SUT_Physics_Career_Guide_v1.0.pdf
├── docs/
│   ├── methodology.md         editors_notes.txt, promoted (R1-R6 fact-check cross-references, open questions)
│   └── design/                 the v1.2 spec + plan, promoted from docs/superpowers/
├── legacy/                    dead pipeline + old iteration PDFs
│   ├── README.md
│   ├── pipeline/                fa_utils.py, finalize.py, inliner.py, md2html.py, mdparse.py
│   ├── build-report-v1.md
│   └── pdfs/                    v1.pdf, v1.1.pdf, v1.2.pdf
└── .github/
    ├── workflows/
    │   ├── build-check.yml       CI: runs build.py on push/PR touching guide/
    │   └── release.yml            on a version tag: builds + attaches the PDF to the GitHub Release
    └── ISSUE_TEMPLATE/
        └── fact-correction.md
```

Excluded from the new repo entirely: `.superpowers/` (internal agent scratch — ledgers, briefs, review packages from the SDD round; not meant for a public audience and not useful without the session that produced it), `channel_post.md` and `SUT_Physics_Career_Guide_build_report.md`'s sibling marketing copy (channel_post.md folds into README context instead, not carried as a standalone file), the currently-on-disk Persian-filename PDF (`راهنمای_مسیرهای_حرفه‌ای_پس_از_فیزیک_شریف.pdf` — superseded by a fresh `dist/` build under the ASCII filename for repo/CI hygiene).

### 2. build.py path adjustment

Currently `OUT = os.path.join(HERE, "..", "SUT_Physics_Career_Guide_v1.0.pdf")` (repo-root sibling of `source/`). In the new layout `guide/build.py` must write to `../dist/SUT_Physics_Career_Guide_v1.0.pdf` — one-line change, `HERE` stays `guide/`, and `dist/` is created if missing. No other pipeline logic changes; `refine.py`'s `SRC`/relative paths are unaffected since it reads from the same directory it's invoked from.

### 3. Licensing

- `LICENSE` — full CC BY-NC-SA 4.0 legal text, copyright line: "© 2026 انجمن علمی دانشکدهٔ فیزیک، دانشگاه صنعتی شریف (Sharif Physics Students' Scientific Association)". Covers `guide.html`'s text content, `docs/`, and the PDF's content.
- `LICENSE-CODE` — full MIT text, same copyright line. Covers `*.py`, `style.css`, the GitHub Actions workflows.
- `guide/fonts/vazirmatn/LICENSE.txt`, `guide/fonts/fa-solid-LICENSE.txt` — SIL OFL 1.1 full text (fetched from upstream, bundled verbatim).
- `guide/fonts/texgyretermes-LICENSE.txt` — the GUST Font License header (which itself normatively points to LPPL 1.3c) — matches the convention TeX Gyre's own distributions use.
- `README.md`/`README.fa.md` each carry a short "Licensing" section summarizing which license covers what, since CC BY-NC-SA + MIT + two font licenses in one repo needs a one-paragraph map for a reader who won't read four license files.

### 4. CHANGELOG.md

Opens with a plain-language note resolving the version-numbering confusion: internal development used v1 → v1.1 → v1.2 as iteration labels before any public release; this is the first public release, numbered v1.0 to mark that restart. Structure:

```markdown
# Changelog
<note explaining the renumbering, as above>

## [1.0.0] — 2026-10-13
### Added
- First public release: portrait-only layout, natural-Persian prose pass,
  publication-edition cover + شناسنامه (publisher/date/version block).
- [full bullet list of what's in the guide: chapter coverage, the seven
  research clusters, international-path content, sourcing discipline —
  written as one comprehensive "what's in v1.0" list, since nothing before
  it was public]

## Pre-release history (not separately released)
- v1.2 (2026-10-12): portrait conversion (4 tables un-landscaped),
  ~98-edit natural-Persian line edit, جدول ۱۰.۱ merged 6→4 columns.
- v1.1 (2026-10-09): Shamsi dates, Persian digits/currency words, section
  numbering fixes.
- v1 (2026-10-09): first generated draft via the markdown pipeline (archived
  in legacy/), 56 pp, landscape tables, R1–R6 source-report synthesis.
```

Going forward: semver tags — `v1.0.x` for fact corrections/typos, `v1.x.0` for new content/sections, `v2.0.0` for a structural rework.

### 5. README strategy

- `README.md` (English): guide identity/purpose in 2-3 sentences, prominent link to `README.fa.md`, licensing summary, quickstart (`pip install -r requirements.txt && python guide/build.py`), repo map (one line per top-level directory), contribution pointer, changelog link.
- `README.fa.md` (Persian, RTL prose — GitHub's renderer doesn't apply `dir=rtl` to markdown, a known platform limitation, nothing to engineer around): the actual front door — what the guide is, who it's for, download link to the latest release PDF, how to report a factual error, credits (شناسنامه content mirrored), license summary in Persian.

### 6. CONTRIBUTING.md

Content-first framing (most contributions will be factual corrections, not code): cite-a-source rule for any factual change; how to propose a correction via Issue (template) or PR directly on `guide/guide.html`; how to rebuild locally to verify a PDF still renders; brief pointer to `refine.py` for anyone who wants to understand the edit history mechanism (not a requirement to use it — direct `guide.html` edits are the normal path going forward).

### 7. CI (`.github/workflows/`)

- `build-check.yml`: on push/PR touching `guide/**`, installs `requirements.txt`, runs `python guide/build.py`, fails the check if it errors (refine.py/build.py are already fail-loud by design, so this just surfaces that in CI).
- `release.yml`: on a pushed tag matching `v*`, builds the PDF and attaches it to the GitHub Release for that tag via `gh release upload` (or the `softprops/action-gh-release` action) — so a future maintainer's workflow is: edit → commit → tag → push tag → release PDF appears automatically.

### 8. Legacy archive

`legacy/README.md` states plainly: these files are superseded, the markdown pipeline is non-functional (imports a nonexistent path, no `.md` source remains), kept only for historical provenance of how v1 was first generated. `legacy/pdfs/` holds the three internal-iteration PDFs with one line each explaining what they were (cross-referenced from CHANGELOG's pre-release history section).

### 9. provenance/README.md

States the content law this project has run under since round one: `guide_v1_original.html` and `style_v1_original.css` are the frozen inputs `refine.py` transforms; they are never edited; any future large-scale editorial pass that wants the same audit-trail guarantee `refine.py` provided should treat these as its starting point, not `guide/guide.html`.

## Verification (definition of done)

- [ ] `python guide/build.py` succeeds from a fresh clone (after `pip install -r requirements.txt`) and produces a 49-page, all-portrait PDF matching the current `dist/` content
- [ ] `git log` shows a clean history (no `.superpowers/` scratch, no stray binaries)
- [ ] All four license texts present and non-empty; README license-summary paragraph matches them
- [ ] CHANGELOG's two sections (1.0.0 + pre-release history) are internally consistent with the actual file contents in `legacy/pdfs/`
- [ ] Both READMEs render correctly on GitHub (checked via `gh repo view --web` or the repo page after push)
- [ ] CI `build-check.yml` passes on the initial push
- [ ] Repo created, pushed, and (if a tag is cut) `release.yml` successfully attaches the PDF

## Risks & mitigations

| Risk | Mitigation |
|---|---|
| Font redistribution terms violated | Full license texts bundled per font family; OFL explicitly permits bundling/redistribution; GUST/LPPL permits redistribution with the license intact |
| CI `release.yml` requires repo secrets/permissions it doesn't have by default | `GITHUB_TOKEN` (automatic, repo-scoped) is sufficient for attaching release assets to the same repo — no new secret needed |
| guide/build.py path change breaks on first run after move | Build + verify immediately after the directory move, before first commit |
| Bilingual README drift (English falls behind Persian edits over time) | Out of scope to prevent structurally; CONTRIBUTING.md asks PR authors touching one to check the other |
