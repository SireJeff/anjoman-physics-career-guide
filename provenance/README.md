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
