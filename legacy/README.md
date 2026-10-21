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
