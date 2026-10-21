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
