#!/usr/bin/env python3
"""Assemble the Persian RTL HTML document from the parsed Markdown tree."""
import os, re, sys, shutil
sys.path.insert(0, "/home/z/my-project/scripts")
from fa_utils import fa
from mdparse import parse
from inliner import inline, inline_appx

BUILD = "/home/z/my-project/build"
DOWNLOAD = "/home/z/my-project/download"

CAPTIONS = {
    (3, 1): "دروس کلیدی برنامهٔ کارشناسی و کاربرد شغلی آن‌ها",
    (4, 1): "ترک‌های تخصصی: از درس اختیاری تا خانوادهٔ شغلی",
    (5, 1): "نقشهٔ شغلی به تفکیک مقطع (جدول اصلی)",
    (9, 1): "کشور به کشور: گشایش برای ایرانیان، فاند و اعداد کلیدی",
    (10, 1): "شغل‌های کمتر دیده‌شده و مقصدهای آن‌ها",
    (11, 1): "نقشهٔ راه سال‌به‌سال کارشناسی و ارشد",
}
LANDSCAPE = {5, 9, 10, 11}
COLW = {
    (3, 1): [20, 40, 40],
    (4, 1): [16, 27, 30, 27],
    (5, 1): [21, 26, 27, 26],
    (9, 1): [14, 26, 31, 29],
    (10, 1): [15, 21, 19, 19, 13, 13],
    (11, 1): [9, 24, 22, 22, 23],
}
CREDITS_NAMES = ["ابراهیم خسروانی", "محمدحسن شیری", "زهرا امیری", "امین عزیزی",
                 "بیتا قربانی", "یاسمین یزدانی", "سپهر طلایی"]
GROUP_LABEL = re.compile(r"\*\*([^*]+):\*\*\s*$")

def box(cls, title, body_html):
    return (f'<div class="box {cls}"><div class="bar">{title}</div>'
            f'<div class="bd">{body_html}</div></div>')

def render_p(text, green=False):
    stripped = text.replace("\ufe0f", "").replace("\ufe0e", "")
    if stripped.startswith("⚠"):
        return box("box-orange", "توجه", f"<p>{inline(stripped)}</p>")
    if text.startswith("**چطور"):
        return box("box-blue", "چطور بخوانید", f"<p>{inline(text)}</p>")
    if green:
        return box("box-green", "اقدام عملی", f"<p>{inline(text)}</p>")
    return f"<p>{inline(text)}</p>"

def render_table(b):
    key = (b["chap"], b["idx"])
    cap = CAPTIONS.get(key, "")
    cap_html = (f'<div class="tcap" id="tab-{b["chap"]}-{b["idx"]}">'
                f'جدول {fa(b["chap"])}-{fa(b["idx"])}: {cap}</div>')
    rows = b["rows"]
    head, body = rows[0], rows[1:]
    widths = COLW.get(key)
    colg = ""
    if widths:
        colg = "<colgroup>" + "".join(f'<col style="width:{w}%">' for w in widths) + "</colgroup>"
    ths = "".join(f"<th>{inline(c)}</th>" for c in head)
    trs = []
    for r in body:
        tds = "".join(f"<td>{inline(c)}</td>" for c in r)
        trs.append(f"<tr>{tds}</tr>")
    tbl = f'<table class="tbl">{colg}<thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
    inner = cap_html + tbl
    if b["chap"] in LANDSCAPE:
        inner = f'<div class="land">{inner}</div>'
    return inner

def render_myths(b):
    out = []
    for r in b["rows"][1:]:  # skip the header row («باور غلط | واقعیت»)
        myth = r[0] if r else ""
        reality = r[1] if len(r) > 1 else ""
        out.append(
            '<div class="myth">'
            f'<div class="myth-m"><p><span class="mlabel">باور غلط</span>{inline(myth)}</p></div>'
            f'<div class="myth-r"><p><span class="rlabel">واقعیت (با منبع)</span>{inline(reality)}</p></div>'
            "</div>")
    return "".join(out)

def render_ol(b):
    out = []
    for i, (tok, txt) in enumerate(b["items"], 1):
        out.append(f'<p class="oli"><span class="olin">{fa(i)}.</span> {inline(txt)}</p>')
    return "".join(out)

def render_ul(b):
    return "<ul>" + "".join(f"<li>{inline(it)}</li>" for it in b["items"]) + "</ul>"

def render_block(b, green=False, appx=False):
    t = b["t"]
    if t == "hr":
        return ""
    if t == "p":
        if appx:
            g = GROUP_LABEL.match(b["text"])
            if g:
                return f'<div class="appx-group">{inline(g.group(1))}:</div>'
            return f'<div class="appx-item">{inline_appx(b["text"])}</div>'
        return render_p(b["text"], green=green)
    if t == "ul":
        if appx:
            return "".join(f'<div class="appx-item">{inline_appx(it)}</div>' for it in b["items"])
        return render_ul(b)
    if t == "ol":
        if appx:
            return "".join(
                f'<div class="appx-item">{esc_tok(tok)} {inline_appx(txt)}</div>'
                for tok, txt in b["items"])
        return render_ol(b)
    if t == "table":
        return render_table(b)
    if t == "myths":
        return render_myths(b)
    return ""

def esc_tok(tok):
    return tok.replace("&", "&amp;").replace("<", "&lt;")

def toc_entries(doc):
    ents = [("preface", "پیش‌گفتار", 1)]
    for ch in doc["chapters"]:
        ents.append((f"ch{ch['num']}", f"{fa(ch['num'])}. {ch['title']}", 1))
        for j, s in enumerate(ch["secs"]):
            if s["num"] is None:
                ents.append((f"s{ch['num']}-{j}", s["title"], 2))
            else:
                sn = f"{fa(s['num'][0])}٫{fa(s['num'][1])}"
                ents.append((f"s{ch['num']}-{j}", f"{sn} {s['title']}", 2))
    ents.append(("appx", "پیوست الف: منابع", 1))
    for j, s in enumerate(doc["appendix"]["secs"], 1):
        ents.append((f"a{j}", f"الف٫{fa(j)} {s['title']}", 2))
    return ents

def toc_nav(entries, tocnum):
    out = ['<nav class="toc-list">']
    for anchor, label, lvl in entries:
        num = (tocnum or {}).get(anchor, "۰۰")
        cls = "toc-l1" if lvl == 1 else "toc-l2"
        dots = "" if lvl == 1 else '<span class="dots"></span>'
        out.append(f'<a class="{cls}" href="#{anchor}"><span class="t">{inline(label)}</span>{dots}<span class="n">{num}</span></a>')
    out.append("</nav>")
    return "".join(out)

def lot_nav(doc, tocnum):
    out = ['<nav class="toc-list">']
    for ch in doc["chapters"]:
        for b in ch["intro"] + [x for s in ch["secs"] for x in s["blocks"]]:
            if b["t"] == "table":
                key = (b["chap"], b["idx"])
                anchor = f"tab-{b['chap']}-{b['idx']}"
                num = (tocnum or {}).get(anchor, "۰۰")
                label = f"جدول {fa(b['chap'])}-{fa(b['idx'])}: {CAPTIONS.get(key, '')}"
                out.append(f'<a class="toc-l2" href="#{anchor}"><span class="t">{label}</span>'
                           f'<span class="dots"></span><span class="n">{num}</span></a>')
    out.append("</nav>")
    return "".join(out)

HEAD_META = f"""<meta charset="utf-8">
<title>راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف</title>
<meta name="author" content="انجمن علمی دانشکدهٔ فیزیک دانشگاه صنعتی شریف">
<meta name="description" content="مسیرهای شغلی و تحصیلی پس از کارشناسی، کارشناسی ارشد و دکتری فیزیک">
<meta name="keywords" content="فیزیک، شریف، مسیر شغلی، اپلای، سربازی، برنامه درسی">
<meta name="generator" content="انجمن علمی دانشکدهٔ فیزیک دانشگاه صنعتی شریف">
<link rel="stylesheet" href="style.css">"""

def build_html(doc, tocnum=None):
    parts = ['<!DOCTYPE html>\n<html dir="rtl" lang="fa-IR">\n<head>', HEAD_META, "</head>\n<body>"]

    # 1) cover
    parts.append(f"""<section class="cover">
<img class="logo" src="anjoman_logo.png" alt="نشان انجمن علمی">
<div class="assoc">انجمن علمی دانشکدهٔ فیزیک دانشگاه صنعتی شریف</div>
<h1 class="cover-title">{doc['title']}</h1>
<div class="cover-sub">{doc['subtitle']}</div>
<div class="cover-ver">نسخهٔ ۱٫۰</div>
<div class="cover-date">۱۸ مهر ۱۴۰۵</div>
<div class="cover-en"><span class="lt">October 2026</span></div>
</section>""")

    # 2) credits
    names = "".join(f'<div class="cr-name">{n}</div>' for n in CREDITS_NAMES)
    parts.append(f"""<section class="credits">
<img class="logo-s" src="anjoman_logo.png" alt="نشان انجمن علمی">
<div class="cr-assoc">انجمن علمی فیزیک دانشگاه صنعتی شریف</div>
<div class="cr-thanks">با تشکر از:</div>
{names}
<div class="cr-note">این راهنما جمع‌بندی شش گزارش پژوهشی و برنامهٔ درسی رسمی کارشناسی فیزیک شریف است.</div>
<div class="cr-channel"><bdi dir="ltr" class="lt">@Anjoman_Elmi_Phys_sut</bdi></div>
</section>""")

    # 3) preface
    p0, p1 = doc["preface"][0], doc["preface"][1]
    parts.append(f"""<section class="preface" id="preface">
<h1 class="fm-title" data-bm="پیش‌گفتار">پیش‌گفتار</h1>
<p class="pref-lead">{inline(p0)}</p>
<p>{inline(p1)}</p>
</section>""")

    # 4) TOC
    ents = toc_entries(doc)
    parts.append(f"""<section class="toc" id="toc">
<h1 class="fm-title" data-bm="فهرست مطالب">فهرست مطالب</h1>
{toc_nav(ents, tocnum)}
</section>""")

    # 5) LOT
    parts.append(f"""<section class="lot" id="lot">
<h1 class="fm-title" data-bm="فهرست جدول‌ها">فهرست جدول‌ها</h1>
{lot_nav(doc, tocnum)}
</section>""")

    # 6) chapters
    for ch in doc["chapters"]:
        n = ch["num"]
        bm = f"فصل {fa(n)}. {ch['title']}"
        parts.append(f"""<section class="chapter" id="ch{n}">
<div class="chap-open">
<div class="chap-num">فصل {fa(n)}</div>
<h1 class="chap-title" data-bm="{bm}" style='string-set: chap "فصل {fa(n)}. " content()'>{inline(ch['title'])}</h1>
</div>""")
        for b in ch["intro"]:
            parts.append(render_block(b))
        for j, s in enumerate(ch["secs"]):
            a = f"s{n}-{j}"
            if s["num"] is None:
                parts.append(f'<h2 class="sec" id="{a}" data-bm="{s["title"]}">{inline(s["title"])}</h2>')
            else:
                sn = f"{fa(s['num'][0])}٫{fa(s['num'][1])}"
                parts.append(f'<h2 class="sec" id="{a}" data-bm="{sn} {s["title"]}">'
                             f'<span class="sn">{sn}</span>{inline(s["title"])}</h2>')
            green = (n == 7 and s["num"] == (7, 6))
            for b in s["blocks"]:
                parts.append(render_block(b, green=green))
        parts.append("</section>")

    # 7) appendix
    appx = doc["appendix"]
    parts.append(f"""<section class="chapter appx" id="appx">
<div class="chap-open">
<div class="chap-num">پیوست الف</div>
<h1 class="chap-title" data-bm="پیوست الف: منابع" style='string-set: chap "پیوست الف. " content()'>منابع</h1>
</div>""")
    for b in appx["intro"]:
        parts.append(render_block(b))
    for j, s in enumerate(appx["secs"], 1):
        sn = f"الف٫{fa(j)}"
        parts.append(f'<h2 class="appxs" id="a{j}" data-bm="{sn} {s["title"]}">'
                     f'<span class="sn">{sn}</span>{inline(s["title"])}</h2>')
        parts.append('<div class="appx-list">')
        for b in s["blocks"]:
            parts.append(render_block(b, appx=True))
        parts.append("</div>")
    parts.append("</section>")

    parts.append("</body>\n</html>")
    return "\n".join(parts)

def main():
    doc, notes = parse()
    html = build_html(doc, None)
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(DOWNLOAD, exist_ok=True)
    with open(f"{BUILD}/guide.html", "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy("/home/z/my-project/upload/anjoman_logo.png", f"{BUILD}/anjoman_logo.png")
    nl = "\n" if not notes.endswith("\n") else ""
    with open(f"{DOWNLOAD}/editors_notes.txt", "w", encoding="utf-8") as f:
        f.write(notes + nl)
    print("guide.html written:", len(html), "chars")
    print("editors_notes.txt written:", len(notes), "chars")

if __name__ == "__main__":
    main()
