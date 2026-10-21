#!/usr/bin/env python3
"""Local build: guide.html -> ../SUT_Physics_Career_Guide_v1.0.pdf

Same scheme as finalize.py, but works straight from guide.html (no Markdown
source needed) and stamps folios with PyMuPDF instead of pikepdf:
  1. render, read anchor pages, inject TOC/LOT page numbers, repeat until stable;
  2. render a folio overlay (الف/ب/... for front matter, ۱/۲/... from chapter 1);
  3. overlay it page by page and set PDF metadata.
"""
import os
import re
import sys

import fitz
import weasyprint

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "dist", "SUT_Physics_Career_Guide_v1.0.pdf")
HTML = os.path.join(HERE, "guide.html")

LETTERS = ["الف", "ب", "پ", "ت", "ث", "ج", "چ", "ح", "خ", "د", "ذ", "ر", "ز", "ژ", "س", "ش"]
FA = "۰۱۲۳۴۵۶۷۸۹"
META = {
    "title": "راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف",
    "author": "انجمن علمی دانشکدهٔ فیزیک دانشگاه صنعتی شریف",
    "subject": "مسیرهای شغلی و تحصیلی پس از کارشناسی، کارشناسی ارشد و دکتری فیزیک",
    "keywords": "فیزیک، شریف، مسیر شغلی، اپلای، سربازی، برنامه درسی",
    "creator": "WeasyPrint (HTML/CSS, RTL)",
}
TOC_ROW = re.compile(r'(<a class="toc-l[12]" href="#([^"]+)">.*?<span class="n">)([^<]*)(</span></a>)')


def fa(n):
    return "".join(FA[int(d)] for d in str(n))


def render(html):
    return weasyprint.HTML(string=html, base_url=HERE).render()


def anchor_pages(doc):
    pages = {}
    for i, pg in enumerate(doc.pages):
        for name in pg.anchors:
            pages.setdefault(name, i)
    return pages


def inject_numbers(html, pages):
    main = pages["ch1"]
    missing = []

    def num(m):
        a = m.group(2)
        if a == "preface":
            return m.group(1) + "الف" + m.group(4)
        if a not in pages:
            missing.append(a)
            return m.group(0)
        return m.group(1) + fa(pages[a] - main + 1) + m.group(4)

    html = TOC_ROW.sub(num, html)
    if missing:
        sys.exit(f"missing anchors: {missing}")
    return html


def overlay(labels, sizes, path):
    css = (
        "@font-face{font-family:V;src:url('fonts/vazirmatn/Vazirmatn-Regular.ttf')}"
        "html,body{margin:0;padding:0}"
        "@page p{size:210mm 297mm;margin:0}@page l{size:297mm 210mm;margin:0}"
        ".p{page:p;break-after:page}.l{page:l;break-after:page}"
        ".p span,.l span{display:block;text-align:center;font-family:V;font-size:10pt;color:#3a3f45;line-height:1.2}"
        ".p span{padding-top:283.2mm}.l span{padding-top:196.2mm}"
    )
    body = "".join(
        f'<div class="{"p" if h > w else "l"}"><span>{lab or "&#8203;"}</span></div>'
        for lab, (w, h) in zip(labels, sizes)
    )
    weasyprint.HTML(string=f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head>'
                    f"<body>{body}</body></html>", base_url=HERE).write_pdf(path)


def main():
    html = open(HTML, encoding="utf-8").read()
    for attempt in range(5):
        doc = render(html)
        pages = anchor_pages(doc)
        new = inject_numbers(html, pages)
        print(f"pass {attempt + 1}: {len(doc.pages)} pages")
        if new == html:
            break
        html = new
    else:
        sys.exit("TOC numbers did not converge")
    open(HTML, "w", encoding="utf-8").write(html)

    base = os.path.join(HERE, "_base.pdf")
    ov = os.path.join(HERE, "_overlay.pdf")
    doc.write_pdf(base)

    pre, main_ = pages["preface"], pages["ch1"]
    labels = ["" if i < pre else LETTERS[i - pre] if i < main_ else fa(i - main_ + 1)
              for i in range(len(doc.pages))]
    sizes = [(p.width, p.height) for p in doc.pages]
    overlay(labels, sizes, ov)

    pdf, ovl = fitz.open(base), fitz.open(ov)
    assert len(pdf) == len(ovl)
    for i, page in enumerate(pdf):
        if labels[i]:
            page.show_pdf_page(page.rect, ovl, i, overlay=True)
    pdf.set_metadata({**pdf.metadata, **META})
    pdf.xref_set_key(pdf.pdf_catalog(), "Lang", "(fa-IR)")
    pdf.save(OUT, garbage=3, deflate=True)
    pdf.close(); ovl.close()
    os.remove(base); os.remove(ov)
    print("wrote", os.path.normpath(OUT), f"({os.path.getsize(OUT) / 1e6:.2f} MB, {len(labels)} pages)")
    print("front matter from page", pre + 1, "| chapter 1 = page", main_ + 1)


if __name__ == "__main__":
    main()
