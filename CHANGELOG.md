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
