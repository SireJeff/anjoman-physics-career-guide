#!/usr/bin/env python3
"""v1.1 editorial pass: guide_v1_original.html -> guide.html.

Every edit is explicit and must match the expected number of times, so the
script fails loudly instead of silently skipping something.
"""
import os
import re
import sys

SRC = os.path.join("..", "provenance", "guide_v1_original.html")
OUT = "guide.html"
ZW = "‌"

h = open(SRC, encoding="utf-8").read()


def flex(s):
    """Regex for a literal that tolerates ZWNJ/space variation (Persian typing)."""
    out = []
    for ch in s:
        if ch in (" ", ZW):
            out.append(r"[ ‌]+" if ch == " " else r"[ ‌]?")
        else:
            out.append(re.escape(ch))
    return "".join(out)


def rep(old, new, count=1, region=None):
    """Replace a literal (ZWNJ-tolerant). count=None means 'at least one'."""
    global h
    pat = re.compile(flex(old))
    n = len(pat.findall(h))
    if (count is None and n == 0) or (count is not None and n != count):
        sys.exit(f"FAIL rep: expected {count}, found {n}: {old[:70]!r}")
    h = pat.sub(lambda m: new, h)


def appx_split():
    i = h.find('<section class="chapter appx"')
    assert i > 0
    return i


def sub_text(fn, body_only=True):
    """Apply fn to text nodes only (never inside tags), optionally body only."""
    global h
    stop = appx_split() if body_only else len(h)
    head, tail = h[:stop], h[stop:]
    parts = re.split(r"(<[^>]+>)", head)
    parts = [p if p.startswith("<") else fn(p) for p in parts]
    h = "".join(parts) + tail


# ------------------------------------------------------------------ 1. front matter
rep('<div class="cover-ver">نسخهٔ ۱٫۰</div>', '<div class="cover-ver">نسخهٔ ۱٫۲</div>')
rep('<div class="cover-en"><span class="lt">October 2026</span></div>\n', '')
rep('<p class="pref-lead"><strong>انجمن علمی دانشکدهٔ فیزیک، دانشگاه صنعتی شریف — '
    'نسخهٔ ۱٫۰ (مهر ۱۴۰۵ / اکتبر ۲۰۲۶)</strong></p>\n', '')
rep('این سند جمع‌بندی شش گزارش پژوهشی <bdi dir="ltr" class="lt">(R1</bdi> تا '
    '<bdi dir="ltr" class="lt">R6)</bdi> و برنامهٔ درسی رسمی کارشناسی فیزیک شریف است. ', '')

# ------------------------------------------------------------------ 2. internal report labels / editor leftovers
rep('هنگام تهیهٔ گزارش‌ها', 'هنگام تهیهٔ این راهنما')
rep('از شبکهٔ ما در دسترس نبود (تأییدشده ۹ اکتبر ۲۰۲۶). پیش از چاپ نهایی، فهرست دروس',
    'در دسترس نبود (بررسی‌شده در ۱۷ مهر ۱۴۰۵). پیش از انتخاب واحد، فهرست دروس')
rep('ارزیابی‌ها از شواهد شش گزارش آمده و', 'ارزیابی‌ها بر پایهٔ منابع این راهنماست و')
rep('گزارش <bdi dir="ltr" class="lt">R4</bdi> ادعای متفاوتی دارد', 'یک گزارش دیگر ادعای متفاوتی دارد')
rep('خلاصهٔ جدول‌های مقایسهٔ <bdi dir="ltr" class="lt">R4</bdi> با شواهد دیگر گزارش‌ها:',
    'خلاصهٔ مقایسه بر پایهٔ شواهد موجود:')
rep('توصیه‌های پراکندهٔ <bdi dir="ltr" class="lt">R1</bdi> تا <bdi dir="ltr" class="lt">R6</bdi> را',
    'توصیه‌های پراکندهٔ فصل‌های قبل را')
rep('همهٔ لینک‌ها در زمان تدوین (۹ اکتبر ۲۰۲۶) بازدید شده‌اند.',
    'همهٔ لینک‌ها در زمان تدوین (۱۷ مهر ۱۴۰۵) بازدید شده‌اند.')
rep('برای ردیابی، فهرست هر گزارش پژوهشی با شماره‌گذاری خودِ آن گزارش حفظ شده است.',
    'برای ردیابی، هر فهرست با شماره‌گذاری اصلی‌اش حفظ شده است.')
rep('لینک‌های آگهی‌های استخدام ممکن است منقضی شوند؛ برای نسخهٔ چاپی، بایگانی بگیرید.',
    'لینک‌های آگهی‌های استخدام ممکن است منقضی شده باشند.')

APPX = {  # old heading tail (after «منابع ») -> new heading tail
    'R1 (مرجع اصلی برنامه درسی، دکتری، اپلای، سربازی، تحریم)': 'برنامهٔ درسی، دکتری، اپلای، سربازی و تحریم',
    'R2 (بازار کار کارشناسی؛ [۱]–[۱۴۲])': 'بازار کار کارشناسی ([۱]–[۱۴۲])',
    'R3 (ارشد؛ S1–S85)': 'دورهٔ ارشد (S1–S85)',
    'R5 (بین‌المللی؛ ۱–۶۴)': 'مسیرهای بین‌المللی (۱–۶۴)',
    'R6 (مشاغل کمتر دیده‌شده؛ ۱–۵۱)': 'مشاغل کمتر دیده‌شده (۱–۵۱)',
}
for old, new in APPX.items():
    rep('منابع ' + old, 'منابع ' + new, 1)                       # data-bm attribute
    code, rest = old.split(' (', 1)
    rest = rest[:-1]
    if code == 'R3':
        tagged = f'منابع <bdi dir="ltr" class="lt">R3 (</bdi>ارشد؛ <bdi dir="ltr" class="lt">S1–S85)</bdi>'
    else:
        tagged = f'منابع <bdi dir="ltr" class="lt">{code} (</bdi>{rest})'
    new_tagged = 'منابع ' + new.replace('S1–S85', '<bdi dir="ltr" class="lt">S1–S85</bdi>')
    rep(tagged, new_tagged, 2)                                    # TOC + heading

# ------------------------------------------------------------------ 3. typos / artefacts
rep('системاتیکِ', 'سیستماتیکِ')
rep('<strong>رقم جعلیِ موثقی برای', '<strong>رقم موثقی برای')
rep('سکوی پرتعهای سوم', 'سکوی پرتاب سوم')
rep('فوتونیک/موارد/نیمه‌هادی', 'فوتونیک/مواد/نیمه‌هادی')
rep('استراتژی سربازی را شروع فکر کنید', 'به استراتژی سربازی فکر کنید')
rep('(تنتو)', '(ترنتو)')
h, n = re.subn('۵هزار‌?یِنی', '۵ هزار ینی', h)
assert n == 1, n

# ------------------------------------------------------------------ 4. currency signs -> Persian words
rep('(~<bdi dir="ltr" class="lt">€۲,۹۰۰</bdi>–۳,۷۰۰/ماه ناخالص)', '(حدود ۲,۹۰۰ تا ۳,۷۰۰ یورو در ماه، ناخالص)')
rep('حداقل حقوق <bdi dir="ltr" class="lt">€۳,۱۲۲</bdi>/ماه', 'حداقل حقوق ۳,۱۲۲ یورو در ماه')
rep('بورس دکتری ≈<strong><bdi dir="ltr" class="lt">€۱۸,۳۴۵</bdi>/سال</strong> (ترنتو) یا '
    '<bdi dir="ltr" class="lt">€۱۶,۲۴۳</bdi> (تریسته)',
    'بورس دکتری حدود <strong>۱۸,۳۴۵ یورو در سال</strong> (ترنتو) یا ۱۶,۲۴۳ یورو (تریسته)')
rep('قرارداد دکترا ~<bdi dir="ltr" class="lt">€۲,۱۰۰</bdi>–۲,۳۰۰/ماه ناخالص',
    'قرارداد دکترا حدود ۲,۱۰۰ تا ۲,۳۰۰ یورو در ماه (ناخالص)')
rep('(~<bdi dir="ltr" class="lt">SEK</bdi> ۳۴,۰۰۰+/ماه)', '(بیش از ۳۴,۰۰۰ کرون سوئد در ماه)')
rep('(~<bdi dir="ltr" class="lt">CHF</bdi> ۵۰–۶۰هزار/سال)', '(حدود ۵۰ تا ۶۰ هزار فرانک سوئیس در سال)')
rep('(~<bdi dir="ltr" class="lt">€۵۰</bdi>هزار/سال ناخالص)', '(حدود ۵۰ هزار یورو در سال، ناخالص)')
rep('<bdi dir="ltr" class="lt">€۱,۳۰۸٫۳۹</bdi>/ماه برای بالای ۲۴ سال (۲۰۲۶)',
    '۱,۳۰۸٫۳۹ یورو در ماه برای بالای ۲۴ سال (۱۴۰۵)')
rep('(≈۴,۵۰۰/۶,۵۰۰/۹,۰۰۰ لیر)', '(حدود ۴,۵۰۰، ۶,۵۰۰ و ۹,۰۰۰ لیر)')
rep('(مرجع: ~<bdi dir="ltr" class="lt">¥۱۱۷</bdi>–۱۴۴هزار/ماه بسته به مقطع)',
    '(مرجع: حدود ۱۱۷ تا ۱۴۴ هزار ین در ماه، بسته به مقطع)')
rep('(<bdi dir="ltr" class="lt">¥۲٫۶</bdi><bdi dir="ltr" class="lt">M</bdi> سال اول تا '
    '<bdi dir="ltr" class="lt">¥۳٫۶</bdi><bdi dir="ltr" class="lt">M)</bdi>',
    '(۲٫۶ میلیون ین در سال اول تا ۳٫۶ میلیون ین)')
rep('≈<bdi dir="ltr" class="lt">AUD</bdi> ۳۲هزار/سال', 'حدود ۳۲ هزار دلار استرالیا در سال')
rep('(شهریه + ~<bdi dir="ltr" class="lt">€۱,۴۰۰</bdi>/ماه + سفر)', '(شهریه + حدود ۱,۴۰۰ یورو در ماه + سفر)')
rep('کارت آبی اروپا با آستانهٔ ۲۰۲۶ <bdi dir="ltr" class="lt">€۵۰,۷۰۰</bdi> سالانه و '
    '<strong><bdi dir="ltr" class="lt">€۴۵,۹۳۴</bdi> برای مشاغل کمبود</strong>',
    'کارت آبی اروپا با آستانهٔ ۱۴۰۵: ۵۰,۷۰۰ یورو در سال و <strong>۴۵,۹۳۴ یورو برای مشاغل کمبود</strong>')
rep('حداقل <bdi dir="ltr" class="lt">€۳,۱۲۲</bdi>/ماه برای', 'حداقل ۳,۱۲۲ یورو در ماه برای')
rep('(ویزای فریلنس ۲ساله ≈<bdi dir="ltr" class="lt">AED</bdi> ۱۰,۵۰۰)', '(ویزای فریلنس ۲ساله، حدود ۱۰,۵۰۰ درهم)')
rep('۶۵–۱۰۵ دلار/ساعت', '۶۵ تا ۱۰۵ دلار در ساعت')
rep('مدیان ~۷۰ دلار/ساعت در ۱,۳۰۰+ نقش', 'میانهٔ حدود ۷۰ دلار در ساعت در بیش از ۱,۳۰۰ نقش')
rep('۲۳,۰۰۰+ مجوز تحصیلی', 'بیش از ۲۳,۰۰۰ مجوز تحصیلی')

# ------------------------------------------------------------------ 5. dates -> Shamsi
rep('(تأییدشده ۹ اکتبر ۲۰۲۶)', '(بررسی‌شده در ۱۷ مهر ۱۴۰۵)')
rep('نقشهٔ واقعیِ ۲۰۲۵–۲۶', 'نقشهٔ واقعیِ ۱۴۰۴–۱۴۰۵', 3)
rep('در ۲۰۲۶ محدودیت‌ها', 'در ۱۴۰۵ محدودیت‌ها')
rep('(۱۳ ویزا در تابستان ۲۰۲۵ در برابر ~۱۳۰۰ در ۲۰۲۴؛', '(۱۳ ویزا در تابستان ۱۴۰۴ در برابر حدود ۱,۳۰۰ در ۱۴۰۳؛')
rep('، مه ۲۰۲۵؛', '، اردیبهشت–خرداد ۱۴۰۴؛')
rep('فرمان دسامبر ۲۰۲۵ (اجرایی از ۱ ژانویهٔ ۲۰۲۶)', 'فرمان آذر ۱۴۰۴ (اجرایی از ۱۱ دی ۱۴۰۴)')
rep('تا دسامبر ۲۰۲۴', 'تا دی ۱۴۰۳')
rep('که ۲۰۲۵ اعلام شد، ژوئن ۲۰۲۶ <strong>لغو شد</strong>', 'که در ۱۴۰۴ اعلام شد، در خرداد–تیر ۱۴۰۵ <strong>لغو شد</strong>')
rep('ددلاین‌های ژانویه–فوریه؛', 'ددلاین‌های اواسط دی تا اوایل اسفند؛')
rep('ددلاین اواخر فوریه</td>', 'ددلاین اوایل اسفند</td>')
rep('ددلاین چرخهٔ ۲۰۲۶–۲۷: ۲۸ فوریهٔ ۲۰۲۶', 'ددلاین چرخهٔ ۱۴۰۵–۱۴۰۶: ۹ اسفند ۱۴۰۴')
rep('(سال منتهی به مارس ۲۰۲۶؛', '(دوازده ماهِ منتهی به فروردین ۱۴۰۵؛')
rep('(۲۰۰۵–۲۰۲۱)', '(۱۳۸۴–۱۴۰۰)')
rep('۱۹۰۲–۱۹۰۹ «کارشناس فنی»', '۱۲۸۱–۱۲۸۸ «کارشناس فنی»')
rep('مقالات ۱۹۰۵ را', 'مقالات مشهور سال ۱۲۸۴ را')
rep('ددلاین‌های دسامبر–فوریه؛ <bdi dir="ltr" class="lt">ICTP (</bdi>اواخر فوریه)؛ '
    '<bdi dir="ltr" class="lt">MEXT (</bdi>بهار از سفارت)؛ ترکیه <bdi dir="ltr" class="lt">Bursları (</bdi>ژانویه–فوریه)',
    'ددلاین‌های اواسط آذر تا اوایل اسفند؛ <bdi dir="ltr" class="lt">ICTP</bdi> (اوایل اسفند)؛ '
    '<bdi dir="ltr" class="lt">MEXT</bdi> (بهار، از سفارت)؛ <bdi dir="ltr" class="lt">Türkiye Bursları</bdi> (اواسط دی تا اوایل اسفند)')
rep('محدودیت ۲۰۱۹، بازگشت با لایسنس عمومی ۲۰۲۱', 'محدودیت تیر ۱۳۹۸، بازگشت با لایسنس عمومی دی ۱۳۹۹')
rep('از ۲۰۲۶ تعلیق است', 'از دی ۱۴۰۴ تعلیق است')
rep('(۲۰۲۵–۲۶)</th>', '(۱۴۰۴–۱۴۰۵)</th>')

YEARS = {"۲۰۱۸": "۱۳۹۷", "۲۰۲۰": "۱۳۹۹", "۲۰۲۳": "۱۴۰۲", "۲۰۲۴": "۱۴۰۳", "۲۰۲۵": "۱۴۰۴", "۲۰۲۶": "۱۴۰۵"}


def years(t):
    t = t.replace("۲۰۲۵–۲۶", "۱۴۰۴–۱۴۰۵")
    return re.sub(r"(?<![۰-۹])(۲۰[۰-۹]{2})(?![۰-۹])", lambda m: YEARS.get(m.group(1), m.group(1)), t)


sub_text(years)

# ------------------------------------------------------------------ 6. section numbering ۸٫۲ -> ۸.۲
h, n = re.subn(r'<span class="sn">([^<]+)</span>',
               lambda m: '<span class="sn">' + m.group(1).replace("٫", ".") + '</span> ', h)
print("heading numbers:", n)
# data-bm and TOC labels: «۶٫۱ عنوان» / «الف٫۱ عنوان»
h, n = re.subn(r'((?:data-bm="|<span class="t">)(?:[۰-۹]{1,2}|الف))٫([۰-۹])', r'\1.\2', h)
print("bookmark/TOC numbers:", n)
# cross-references «بخش ۶٫۴» / «بخش ۳ و ۶٫۱» / «بخش ۶٫۲ و ۷٫۲»


def xref(t):
    return re.sub(r"بخش(?:‌های)? [۰-۹]+(?:٫[۰-۹])?(?: و [۰-۹]+(?:٫[۰-۹])?)*",
                  lambda m: m.group(0).replace("٫", "."), t)


before = h.count("٫")
sub_text(xref)
print("cross-references fixed:", before - h.count("٫"))
# table captions «جدول ۳-۱» -> «جدول ۳.۱»
h, n = re.subn(r"جدول ([۰-۹]+)-([۰-۹]+)", r"جدول \1.\2", h)
print("table captions:", n)

# ------------------------------------------------------------------ 7. approximations, thousands separator
sub_text(lambda t: re.sub(r"[~≈]\s?(?=[۰-۹])", "حدود ", t))
sub_text(lambda t: re.sub(r"(?<=[۰-۹]),(?=[۰-۹]{3}(?![۰-۹]))", "٬", t), body_only=False)

# ------------------------------------------------------------------ 8. punctuation trapped inside LTR islands
PAIRS = {"(": ")", "[": "]"}
EDGE = ":;,./،؛"


def unmatched(c):
    """Indices of brackets in c that have no partner inside c."""
    stack, bad = [], set()
    for i, ch in enumerate(c):
        if ch in PAIRS:
            stack.append(i)
        elif ch in PAIRS.values():
            if stack and PAIRS[c[stack[-1]]] == ch:
                stack.pop()
            else:
                bad.add(i)
    return bad | set(stack)


def fix_bdi(m):
    """Move punctuation that belongs to the Persian sentence out of an LTR island."""
    c = m.group(1)
    pre = post = ""
    while c:
        c0 = c
        if c != c.lstrip():
            pre += " "; c = c.lstrip(); continue
        if c != c.rstrip():
            post = " " + post; c = c.rstrip(); continue
        if c[-1] == "-" or (c[-1] == "+" and c[-2:-1] == " "):
            post = c[-1] + post; c = c[:-1]; continue
        if c[0] in "-+":
            pre += c[0]; c = c[1:]; continue
        bad = unmatched(c)
        if c[0] in EDGE or 0 in bad:
            pre += c[0]; c = c[1:]; continue
        if (c[-1] in EDGE and not re.search(r"(?:[A-Za-z]|etc|Inc|al)\.$", c)) or len(c) - 1 in bad:
            post = c[-1] + post; c = c[:-1]; continue
        if c[0] in PAIRS and c[-1] == PAIRS[c[0]] and not unmatched(c[1:-1]):
            depth = 0
            for i, ch in enumerate(c):
                depth += (ch == c[0]) - (ch == PAIRS[c[0]])
                if depth == 0:
                    break
            if i == len(c) - 1:
                pre += c[0]; post = c[-1] + post; c = c[1:-1]; continue
        if c == c0:
            break
    if not re.search(r"[A-Za-z0-9]", c):
        return pre + c + post
    return f'{pre}<bdi dir="ltr" class="lt">{c}</bdi>{post}'


h, n = re.subn(r'<bdi dir="ltr" class="lt">([^<]*)</bdi>', fix_bdi, h)
print("LTR islands checked:", n)

# ------------------------------------------------------------------ 9. break up wall-of-text paragraphs
SPLITS = [
    "دو قانون مهم دیگر:", "مقیاس دانشکده در دورهٔ کاتالوگ:",
    "درِ دوم، ",
    "نمونه‌های شاغل در این فضا", "واقعیت بورس کار",
    "اعداد حقوقیِ موجود", "نرم‌افزار هم همین‌طور است",
    "سازوکار <strong>امریهٔ دانش‌بنیان", "<strong>امریهٔ دانشگاهی",
    "ترتیب‌های عملی رایج",
    "دو مسیر خاص:",
    "در سلامت، ", "در خارج، دادهٔ",
    "آنچه کمیته‌ها می‌خوانند",
    "<strong>ویزای آمریکا:</strong>", "<strong>پول:</strong>",
    "حقوق — با تعارض منابع",
    "بر اساس جست‌وجوی مستقیم", "در مقابل، <strong>شریف",
    "در اروپا پست‌داکتری",
    "مقطع شما تعیین می‌کند", "مقیاس جریان:",
    "دو استثنای مهم:",
    "اما: این پلتفرم‌ها", "الگوی عملی که بین",
    "در مقابل، <strong>کم‌خطرترین", "قاعدهٔ عملی:",
]


def split_before(phrase):
    global h
    ms = list(re.finditer(flex(phrase), h))
    if len(ms) != 1:
        sys.exit(f"FAIL split: {len(ms)} matches for {phrase!r}")
    i = ms[0].start()
    while h[:i].endswith("<strong>"):
        i -= len("<strong>")
    ps = h.rfind("<p", 0, i)
    assert h.rfind("</p>", 0, i) < ps, phrase
    seg = h[ps:i]
    for t in ("strong", "a", "bdi", "em", "span"):
        assert len(re.findall(f"<{t}[ >]", seg)) == seg.count(f"</{t}>"), (phrase, t)
    tag = re.match(r"<p[^>]*>", h[ps:]).group(0)
    h = h[:i].rstrip() + "</p>\n" + tag + h[i:]


for s in SPLITS:
    split_before(s)

# ------------------------------------------------------------------ 10. portrait layout (v1.2)
# unwrap the four landscape divs; compact class; merge جدول ۱۰.۱ 6->4 columns
for tid in ("tab-5-1", "tab-9-1", "tab-10-1", "tab-11-1"):
    i = h.find(f'<div class="land"><div class="tcap" id="{tid}">')
    assert i > 0, tid
    j = h.find("</table>", i) + len("</table>")
    assert h[j:j + 6] == "</div>", tid
    h = h[:i] + h[i + len('<div class="land">'):j] + h[j + len("</div>"):]
    k = h.find(f'<div class="tcap" id="{tid}">')
    m = h.find('</div><table class="tbl">', k)
    h = h[:m] + '</div><table class="tbl tbl-c">' + h[m + len('</div><table class="tbl">'):]

# جدول ۱۰.۱: 6 columns -> 4 (ایران/خارج merged, ورود/اطمینان merged)
i = h.find('id="tab-10-1"')
t0 = h.find("<table", i)
t1 = h.find("</table>", t0) + len("</table>")
tbl = h[t0:t1]
old_cg = ('<colgroup><col style="width:15%"><col style="width:21%"><col style="width:19%">'
          '<col style="width:19%"><col style="width:13%"><col style="width:13%"></colgroup>')
new_cg = ('<colgroup><col style="width:15%"><col style="width:27%"><col style="width:40%">'
          '<col style="width:18%"></colgroup>')
assert tbl.count(old_cg) == 1
tbl = tbl.replace(old_cg, new_cg, 1)
old_th = ('<thead><tr><th>شغل</th><th>چرا فیزیک‌دان می‌خواهد</th><th>داخل ایران</th>'
          '<th>خارج</th><th>مقطع ورود</th><th>اطمینان</th></tr></thead>')
new_th = ('<thead><tr><th>شغل</th><th>چرا فیزیک‌دان می‌خواهد</th><th>ایران / خارج</th>'
          '<th>ورود و اطمینان</th></tr></thead>')
assert tbl.count(old_th) == 1
tbl = tbl.replace(old_th, new_th, 1)
head_end = tbl.find("</thead>") + len("</thead>")
head, body10 = tbl[:head_end], tbl[head_end:]


def merge_row(m):
    cells = re.findall(r"<td>(.*?)</td>", m.group(0), re.S)
    assert len(cells) == 6, m.group(0)[:100]
    return ("<tr><td>" + cells[0] + "</td><td>" + cells[1] +
            "</td><td><strong>ایران:</strong> " + cells[2] +
            "<br><strong>خارج:</strong> " + cells[3] +
            "</td><td>" + cells[4] + " · " + cells[5] + "</td></tr>")


body10, nmerged = re.subn(r"<tr><td>.*?</td></tr>", merge_row, body10, flags=re.S)
assert nmerged == 15, nmerged
h = h[:t0] + head + body10 + h[t1:]

# ------------------------------------------------------------------ 11. v1.2 prose: natural-Persian pass
def sweep(old, new):
    """Literal ZWNJ-tolerant replace; fails on zero matches; prints the count."""
    global h
    pat = re.compile(flex(old))
    n = len(pat.findall(h))
    if n == 0:
        sys.exit(f"FAIL sweep: {old[:60]!r}")
    h = pat.sub(lambda m: new, h)
    print(f"sweep {old[:28]!r}: {n}")


# ch1 opening — the sentence ENZO dissected word by word
rep('اضطرابی که دانشجویان ما دربارهٔ آینده و فرایند اپلای گزارش می‌کنند واقعی است و ساختارش هم واقعی است: '
    'چند ضرب‌الاجل هم‌زمان، یک لایهٔ تحریم که می‌تواند شبی یک برنامه را به‌هم بریزد، سربازی برای برادران، و محیطی پر از شایعه.',
    'اضطرابی که دانشجویان ما دربارهٔ آینده و اپلای دارند واقعی است، و دلایلش هم واقعی‌اند: '
    'چند ددلاین هم‌زمان، تحریم‌هایی که ممکن است شبی همه‌چیز را به‌هم بریزند، سربازی برای برادران، و محیطی پر از شایعه.')
rep('این راهنما عمداً شواهدمحور نوشته شده نه انگیزشی؛', 'این راهنما آگاهانه شواهدمحور نوشته شده، نه انگیزشی؛')

# mechanical word sweeps (occurrence lines verified against guide_v1_original.html)
sweep('فیزیکدان', 'فیزیک‌دان')                       # 1 line
sweep('مهارتمحور', 'مهارت‌محور')                     # 7 matches
sweep('دانش‌گاه', 'دانشگاه')                         # 1 line
sweep('ریز‌عدسی', 'ریزعدسی')                         # 1 line
sweep('در حال بدتر‌شدن', 'در حال بدتر شدن')          # 1 line
sweep('سافتهای', 'سافت‌های')                         # 1 line
sweep('فکرتانک‌ها', 'اندیشکده‌ها')                    # 1 line
sweep('(اپلیکیشن‌فی، آزمون، لایسنس)', '(هزینهٔ درخواست، آزمون، لایسنس)')
sweep('هم‌دوره تحریم شده', 'هم‌زمان با دورهٔ تحریم شده')
sweep('فرایند پواسون مزدوج', 'فرایند پواسون مرکب')

# credits page: drop the internal-report sentence (round-1 leftover)
rep('<div class="cr-note">این راهنما جمع‌بندی شش گزارش پژوهشی و برنامهٔ درسی رسمی کارشناسی فیزیک شریف است.</div>', '')

# ------------------------------------------------------------------ 11b. task-5 line-edit, batch 1 (front matter + ch1-5)
# front matter / TOC
rep('صادقانه نوشته شده «رقم معتبری یافت نشد»', 'صادقانه نوشته‌ایم «رقم معتبری یافت نشد»')
sweep('پنج پروفایل واقعی (سند‌شده)', 'پنج پروفایل واقعی (مستند)')        # TOC + bookmark + h2

# ch1
sweep('شواهدمحور', 'شواهد‌محور')                                        # مثل مهارت‌محور

# ch2
rep('در خلأ و با دستگاه‌هایی مثل تبخیر و پوشش‌دهی', 'در خلأ و با دستگاه‌هایی برای تبخیر و پوشش‌دهی')
rep('این خوشه در ایران شغلی‌ترین خوشهٔ آزمایشگاهی است',
    'در ایران این خوشه از میان خوشه‌های آزمایشگاهی بیشترین فرصت شغلی را دارد')
rep('پشت‌بندان ریاضی سنگین است (جبر خطی، مکانیک کوانتومی، نظریه گروه‌ها)',
    'پشتوانه‌اش ریاضیِ سنگین است (جبر خطی، مکانیک کوانتومی، نظریهٔ گروه‌ها)')
rep('هم‌پوشانی مستقیم صنعتیِ آن کم‌ترین است', 'هم‌پوشانی مستقیم آن با صنعت کمترین است')
rep('اغلب به سمت داده و کمیّت مالی (<bdi dir="ltr" class="lt">Quant</bdi>) چرخش مهارتی می‌دهند',
    'اغلب مسیرشان را به داده و کمیّت مالی (<bdi dir="ltr" class="lt">Quant</bdi>) تغییر می‌دهند')
rep('به خط لولهٔ آکادمیک و صنایع مجاور وابسته‌اند', 'به مسیر آکادمیک و صنایع مجاور وابسته‌اند')

# ch3
rep('مبنای ورودی‌های از ۱۳۹۳ به بعد', 'مبنای ورودی‌های ۱۳۹۳ به بعد')
rep('هشدار به‌روزبودن:', 'هشدار به‌روز بودن:')
rep('فیزیکِ سیستم‌های زنده', 'فیزیکِ سامانه‌های زنده')
rep('آشنایی با پروسهٔ قرارداد و قیمت‌گذاری', 'آشنایی با فرایند قرارداد و قیمت‌گذاری')

# ch4
rep('فیزیک‌دانان پروسه', 'فیزیک‌دانان فرایند')
rep('عملاً همان تحقیق مواد است', 'عملاً همان پژوهش مواد است')

# ch5
rep('ستون «ایران» مستقیم اجرا می‌شود', 'ستون «ایران» مستقیماً اعمال می‌شود')
rep('، مالکیت صنعتی، سیاست علم', '، مالکیت صنعتی، سیاست‌گذاری علم')
sweep('خارج: ناپذیرفتنی', 'خارج: موضوعیت ندارد')                      # ۳ خانهٔ ردیف استخدام دولتی
sweep('مجوز-محور', 'مجوز‌محور')                                        # با خط ربط ناجور؛ مثل مهارت‌محور
sweep('کم‌ترین', 'کمترین')                                             # باقیماندهٔ ch7 پس از rep بالا

# ------------------------------------------------------------------ 11c. task-5 line-edit, batch 2 (ch6-9)
# NOTE: «هیأت‌عملی» (ch8, منبع مهر) عمداً دست‌نخورده ماند؛ همان رشته در پیوست هم هست و پیوست byte-identical می‌ماند.
# ch6
rep('فارغ‌التحصیلانِ به‌موقعِ تقریباً ', 'فارغ‌التحصیلان به‌موقع تقریباً ')   #kasra
rep('سازوکار پایدار است، عدد‌ها نه', 'سازوکار پایدار است، عددها نه')
rep('(با کارآموزیِ پردرآمدِ تحلیل داده)', '(با کارآموزی پردرآمد تحلیل داده)')
rep('برای کارشناسیِ فیزیکِ صرف،', 'برای کارشناسی فیزیکِ صرف،')
rep('متخصص داده/هوش مصنوعیِ ارشدی در تهران', 'متخصص داده/هوش مصنوعی ارشدی در تهران')
rep('میدلول', 'میان‌رده')
rep('با سیستم امتیاز است', 'با سامانهٔ امتیاز است')
rep('دورهٔ آموزشی ۲ماههٔ نظام', 'دورهٔ آموزشی ۲ ماههٔ نظام')
rep('سراغ‌تان می‌آید و بدون <strong>کارت پایان خدمت یا معافیت</strong>، استخدام دولتی ممنوع، گواهینامه',
    'سراغ‌تان می‌آید. بدون <strong>کارت پایان خدمت یا معافیت</strong>، استخدام دولتی ممنوع است، گواهینامه')

# ch7
rep('پس از ارشد، پنج کاربرد واقعی دارد', 'ارشد پنج کاربرد واقعی دارد')
rep('<bdi dir="ltr" class="lt">CV</bdi> هسته‌ای-نزدیک', '<bdi dir="ltr" class="lt">CV</bdi> نزدیک به حوزهٔ هسته‌ای')
rep('این راهنما آن را مقصد پیشنهادی نمی‌داند؛', 'این راهنما آن را به‌عنوان مقصد پیشنهاد نمی‌کند؛')
rep('تنها پروکسی حقوقیِ تاریخ‌دار', 'تنها نشانگر حقوقیِ تاریخ‌دار')
rep('تفسیرش را با نمک: ', 'با احتیاط تفسیرش کنید: ')
rep('پایان‌نامه‌مقیاس پژوهش،', 'پژوهش در مقیاس پایان‌نامه،')
rep('در عمل کاندیداها به', 'در عمل داوطلب‌ها به')
rep('توالی سربازی را قبل از ترم آخر', 'ترتیب سربازی را قبل از ترم آخر')
rep('اما همه‌اش همان بخشی از پروسه است', 'اما همه‌اش همان بخشی از فرایند است')

# ch8
rep('جذب مرکزی‌رانده و', 'جذب متمرکز و')
rep('از هیأت اجرایی جذب', 'از هیئت اجرایی جذب')
rep('باز است ولی اکثرشان ارشد کفایت می‌کند', 'باز است ولی برای اکثرشان ارشد کافی است')
rep('پیامدش مرزی و بلندمدت است', 'پیامدش بلندمدت است و از مرز هم عبور می‌کند')
rep('مدرک شما خودش بار منفی ندارد؛ کارفرمای آینده‌تان می‌تواند داشته باشد.',
    'مدرک شما خودش بار منفی ندارد؛ بار منفی می‌تواند از کارفرمای آینده‌تان بیاید.')
rep('در اروپا پست‌داکتری و دکتری «کارمزد حقوق» مقیاس عمومی‌اند',
    'در اروپا پست‌داکتری و دکتری قرارداد کاریِ حقوق‌بگیر با مقیاس عمومی‌اند')
rep('خط لولهٔ استادی طولانی است', 'مسیر استادی طولانی است')
rep('بازار استادی طراحی‌شده رقیق است', 'بازار استادی ذاتاً رقیق است')
rep('جذب‌کنندهٔ سنتی ماده‌چگال‌ها و پروسه‌ای‌ها', 'جذب‌کنندهٔ سنتی فارغ‌التحصیلان مادهٔ چگال و مهندسان فرایند')
rep('برای کارفرمای خارجی پرچم‌دارند', 'برای کارفرمای خارجی پرچم قرمز بالا می‌دهند')
rep('این آمار به‌سنگینی به دکتری وزن دارد', 'در این آمار دکتری وزن سنگینی دارد')

# ch9
rep('مردانِ مجرد ۲۳–۳۵ ساله بررسی اضافه می‌بینند', 'مردان مجرد ۲۳–۳۵ ساله با بررسی سخت‌گیرانه‌تری روبه‌رو می‌شوند')
rep('باز و ساختاراً مهمان‌نواز', 'باز و از نظر ساختاری مهمان‌نواز')
rep('به‌دلیل قواعد کنترل صادراتِ آمریکایی از استخدام ایرانیان معاف شناخته شده‌اند',
    'مجاز شناخته شده‌اند که طبق قواعد کنترل صادرات آمریکا ایرانیان را استخدام نکنند')
rep('موقتاً بسته بود و صف اضافه داد', 'موقتاً بسته بود و صف‌ها را طولانی‌تر کرد')
rep('شرطش ارشد + استادِ موافقت‌شده است', 'شرطش ارشد + استادی است که موافقت کرده باشد')
rep('دکتری ۵سالهٔ کاملاً فاندشده', 'دکتری ۵ سالهٔ کاملاً فاندشده')
rep('دکتری ۵سالهٔ تمام‌فاند', 'دکتری ۵ سالهٔ تمام‌فاند')
rep('ویزای فریلنس ۲ساله،', 'ویزای فریلنس ۲ ساله،')
rep('مقاله و رونویسی شما می‌سازند', 'مقاله و کارنامهٔ شما می‌سازند')
rep('برند شریف در این پرونده‌ها کمکی است که خودش می‌کند', 'برند شریف در این پرونده‌ها خودش کمک می‌کند')
rep('استخدام ایرانی: خط لولهٔ شریف', 'استخدام ایرانی: مسیر شریف')
rep('مهندسی پروسهٔ نیمه‌هادی و لیتوگرافی', 'مهندسی فرایند نیمه‌هادی و لیتوگرافی')
rep('فوتونیک دفاعی‌نزدیک', 'فوتونیک نزدیک به حوزهٔ دفاع')
sweep('هزینهٔ اپلیکیشن', 'هزینهٔ درخواست')                             # ۳ مورد؛ application fee

# ------------------------------------------------------------------ 11d. task-5 line-edit, batch 3 (ch10-13 + boxes)
# ch10
rep('، سابقهٔ پژوهش، رونویسی منسجم،', '، سابقهٔ پژوهش، کارنامهٔ منسجم،')   # رونویسی = کارنامه (ترنسکریپت)
rep('خواندن فنیِ اول‌اصولی دربارهٔ «این ادعا واقعاً چی می‌گوید»',
    'خواندن فنی و اول‌اصولیِ ادعاها: «این ادعا واقعاً چه می‌گوید»')
rep('سافت‌های ایرانی', 'نرم‌افزارهای ایرانی')
rep('استدلال مرتبه‌مقداری', 'استدلال مرتبهٔ بزرگی')
sweep('فرضیهمحور', 'فرضیه‌محور')                                       # مثل مهارت‌محور
rep('بورس انرژی و سازمان‌های تجدیدپذیر', 'بورس انرژی و شرکت‌های انرژی تجدیدپذیر')
rep('سنتز شواهد و برقراری عدم‌قطعیت', 'سنتز شواهد و انتقال عدم‌قطعیت')
rep('هرکدام پژوهشِ شهودیِ فیزیکی', 'هرکدام شهودِ فیزیکی می‌خواهد')
rep('وجودش واقعی است؛ قیمت مرزی‌اش هم واقعی است.', 'وجودش واقعی است؛ هزینهٔ مرزی‌اش هم واقعی است.')
rep('همساز مدل نرخ بهرهٔ', 'هم‌ساز مدل نرخ بهرهٔ')
rep('سیاست علم و دیپلماسی علمی', 'سیاست‌گذاری علم و دیپلماسی علمی')

# ch11
rep('مزه‌مزهٔ «فیزیک یا مهندسی؟» را', 'سؤال «فیزیک یا مهندسی؟» را')
rep('قوی‌ترین تک‌پیش‌بینِ اپلای موفق', 'قوی‌ترین پیش‌بینِ اپلای موفق')
rep('در صورت معدل≥۱۷،', 'در صورت معدل ≥۱۷،')
rep('نامه–سابقه–رونویسی', 'نامه–سابقه–کارنامه')
rep('توالی سربازی را قطعی کنید', 'ترتیب سربازی را قطعی کنید')
rep('کم‌لرزش‌ترین برای ایرانیان', 'کم‌ریسک‌ترین برای ایرانیان')
rep('قواعدش سالانه می‌خزد', 'قواعدش هر سال عوض می‌شود')
rep('نمره‌های این ترم‌ها در رونویسی دیده می‌شوند', 'نمره‌های این ترم‌ها در کارنامه دیده می‌شوند')

# ch12
rep('بومی‌محلیِ آن کارفرماها و کمیته‌ها آن را نمی‌فهمند', 'این‌ها برای کارفرما و کمیتهٔ مقصد ناآشناست')

# ch13
rep('اکثریتِ ارشدِ فیزیک از آکادمی', 'اکثریت فارغ‌التحصیلان ارشد فیزیک از آکادمی')
rep('اپتیک بلیت نقش‌های واقعی', 'اپتیک بلیتِ نقش‌های واقعی')
rep('مقیاس اکوسیستم به ۱۰هزار شرکت رسیده', 'مقیاس اکوسیستم به ۱۰ هزار شرکت رسیده')
rep('پیامد مرزی‌شان (ویزا، بانک، همکاری بین‌المللی) مادام‌العمر است',
    'پیامدشان در مرزها (ویزا، بانک، همکاری بین‌المللی) مادام‌العمر است')
rep('فقط هزینهٔ کامل در را نشان می‌دهد', 'فقط هزینهٔ کاملِ این در را نشان می‌دهد')

# ------------------------------------------------------------------ 12. publication edition: series-style cover + شناسنامه
# cover -> band / logo+title / foot; credits -> تهیه و تدوین + facts; names & channel verbatim
i = h.find('<section class="cover">')
assert i > 0, "cover section missing"
j = h.find("</section>", i)
assert j > i, "cover end missing"
h = (h[:i]
     + '<section class="cover">'
     + '<div class="pub-band"><span class="pub-org">انجمن علمی دانشکدهٔ فیزیک · دانشگاه صنعتی شریف</span>'
     + '<span class="pub-ed">انتشار اول · ۱۴۰۵</span></div>'
     + '<div class="cv-main">'
     + '<img class="logo" src="anjoman_logo.png" alt="نشان انجمن علمی">'
     + '<h1 class="cover-title">راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف</h1>'
     + '<div class="cover-sub">از دانشکده تا بازار کار: برای دبیرستانی‌ها و دانشجویان فیزیک</div>'
     + '</div>'
     + '<div class="pub-foot"><div class="cover-date">۲۱ مهر ۱۴۰۵</div></div>'
     + "</section>"
     + h[j:])

i = h.find('<section class="credits">')
assert i > 0, "credits section missing"
j = h.find("</section>", i)
assert j > i, "credits end missing"
old_cr = h[i:j]
names = re.findall(r'<div class="cr-name">(.*?)</div>', old_cr)
assert len(names) == 7, len(names)
chan = re.search(r'<div class="cr-channel">(.*?)</div>', old_cr)
assert chan, "channel missing"
h = (h[:i]
     + '<section class="credits">'
     + '<img class="logo-s" src="anjoman_logo.png" alt="نشان انجمن علمی">'
     + '<div class="cr-assoc">تهیه و تدوین: انجمن علمی دانشکدهٔ فیزیک، دانشگاه صنعتی شریف</div>'
     + '<div class="cr-sub">انجمنی دانشجویی و غیرانتفاعی</div>'
     + '<div class="cr-doc">راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف</div>'
     + '<dl class="cr-facts">'
     + "<div><dt>تاریخ</dt><dd>۲۱ مهر ۱۴۰۵</dd></div>"
     + "<div><dt>نسخه</dt><dd>نسخهٔ ۱٫۰</dd></div>"
     + "</dl>"
     + '<div class="cr-thanks">با تشکر از:</div>'
     + "".join(f'<div class="cr-name">{n}</div>' for n in names)
     + f'<div class="cr-channel">{chan.group(1)}</div>'
     + "</section>"
     + h[j:])
print("publication edition: cover + شناسنامه rebuilt;", len(names), "names kept")

open(OUT, "w", encoding="utf-8").write(h)

# ------------------------------------------------------------------ checks
body = re.sub(r"<[^>]+>", "", h[:appx_split()])
left = re.findall(r"(?:ژانویه|فوریه|مارس|آوریل|ژوئن|ژوئیه|اوت|سپتامبر|اکتبر|نوامبر|دسامبر|"
                  r"October|[€¥$£]|(?<![۰-۹])۲۰[۰-۹]{2}|(?<![۰-۹])۱۹[۰-۹]{2}|\bR[1-6]\b)", body)
print("leftover gregorian/currency/R-labels in body:", left)
print("section-number ٫ left:", re.findall(r"(?:بخش|جدول) [۰-۹]+٫[۰-۹]", body))
BANNED = ["ضرب‌الاجل", "لایهٔ تحریم", "فرآیند", "مهارتمحور", "سافتهای",
          "اپلیکیشنفی", "فکرتانک", "عمداً شواهدمحور", "پواسون مزدوج",
          # task-5 batch 1
          "شواهدمحور", "ناپذیرفتنی", "مجوز-محور", "کم‌ترین", "سند‌شده", "سند شده",
          # task-5 batch 2 (هیأت عمداً آزاد است: «هیأت‌عملی» در پیوست هم هست)
          "پروسه", "خط لوله", "خط‌لوله", "میدلول", "کاندیدا", "پروکسی",
          # task-5 batch 3
          "رونویسی", "فرضیهمحور"]
bad = [b for b in BANNED if b in h[:appx_split()]]
assert not bad, bad
print("banned-phrase check: clean")
print("written", OUT)
