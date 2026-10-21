#!/usr/bin/env python3
"""Two-pass render: measure anchors, inject restarted page numbers, stamp footers."""
import sys, os
sys.path.insert(0, "/home/z/my-project/scripts")
import weasyprint, pikepdf
from fa_utils import fa
from mdparse import parse
from md2html import build_html, toc_entries, BUILD, DOWNLOAD

LETTERS = ["الف", "ب", "پ", "ت", "ث", "ج", "چ", "ح", "خ", "د", "ذ", "ر", "ز", "ژ", "س", "ش"]

TITLE = "راهنمای مسیرهای حرفه‌ای پس از فیزیک شریف"
AUTHOR = "انجمن علمی دانشکدهٔ فیزیک دانشگاه صنعتی شریف"
SUBJECT = "مسیرهای شغلی و تحصیلی پس از کارشناسی، کارشناسی ارشد و دکتری فیزیک"
KEYWORDS = "فیزیک، شریف، مسیر شغلی، اپلای، سربازی، برنامه درسی"

def find_anchor_page(doc, name):
    for i, pg in enumerate(doc.pages):
        if name in pg.anchors:
            return i
    return None

def compute_tocnum(doc_tree, doc):
    preface_start = find_anchor_page(doc, "preface")
    main_start = find_anchor_page(doc, "ch1")
    tocnum = {}
    for anchor, label, lvl in toc_entries(doc_tree):
        if anchor == "preface":
            tocnum[anchor] = "الف"
            continue
        p = find_anchor_page(doc, anchor)
        if p is None:
            print("WARN missing anchor:", anchor)
            continue
        tocnum[anchor] = fa(p - main_start + 1) if p >= main_start else "?"
    for ch in doc_tree["chapters"]:
        for b in ch["intro"] + [x for s in ch["secs"] for x in s["blocks"]]:
            if b["t"] == "table":
                a = f"tab-{b['chap']}-{b['idx']}"
                p = find_anchor_page(doc, a)
                if p is not None:
                    tocnum[a] = fa(p - main_start + 1)
    return tocnum, preface_start, main_start

def render_html(html, path_pdf, path_html=None):
    if path_html:
        with open(path_html, "w", encoding="utf-8") as f:
            f.write(html)
    d = weasyprint.HTML(string=html, base_url=BUILD).render()
    d.write_pdf(path_pdf)
    return d

def build_overlay(labels, sizes, out_pdf):
    css, body = [], []
    css.append("@font-face { font-family: Vazirmatn; src: url('fonts/vazirmatn/Vazirmatn-Regular.ttf'); }")
    css.append("html,body{margin:0;padding:0}")
    css.append("@page ovp { size: 210mm 297mm; margin: 0; }")
    css.append("@page ovl { size: 297mm 210mm; margin: 0; }")
    css.append(".ovp { page: ovp; break-after: page; }")
    css.append(".ovl { page: ovl; break-after: page; }")
    css.append(".ovp span { display: block; padding-top: 283.2mm; text-align: center;"
               " font-family: Vazirmatn; font-size: 10pt; color: #3a3f45; line-height: 1.2; }")
    css.append(".ovl span { display: block; padding-top: 196.2mm; text-align: center;"
               " font-family: Vazirmatn; font-size: 10pt; color: #3a3f45; line-height: 1.2; }")
    for i, (lab, (w, h)) in enumerate(zip(labels, sizes)):
        cls = "ovp" if h > w else "ovl"
        body.append(f'<div class="{cls}"><span>{lab}</span></div>')
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
            + "".join(css) + "</style></head><body>"
            + "".join(body) + "</body></html>")
    weasyprint.HTML(string=html, base_url=BUILD).write_pdf(out_pdf)

def merge(base_pdf, overlay_pdf, labels, out_pdf):
    pdf = pikepdf.open(base_pdf)
    ov = pikepdf.open(overlay_pdf)
    for i, page in enumerate(pdf.pages):
        if labels[i]:
            page.add_overlay(ov.pages[i])
    pdf.docinfo["/Title"] = pikepdf.String(TITLE)
    pdf.docinfo["/Author"] = pikepdf.String(AUTHOR)
    pdf.docinfo["/Subject"] = pikepdf.String(SUBJECT)
    pdf.docinfo["/Keywords"] = pikepdf.String(KEYWORDS)
    pdf.docinfo["/Creator"] = pikepdf.String("WeasyPrint 68 (HTML/CSS, RTL)")
    try:
        pdf.Root["/Lang"] = pikepdf.String("fa-IR")
    except Exception as e:
        print("lang set failed:", e)
    pdf.save(out_pdf)

def main():
    doc_tree, notes = parse()
    tocnum = {}
    d = None
    for attempt in range(4):
        html = build_html(doc_tree, tocnum)
        d = render_html(html, f"{BUILD}/base.pdf", f"{BUILD}/guide.html")
        new_tocnum, preface_start, main_start = compute_tocnum(doc_tree, d)
        if new_tocnum == tocnum:
            break
        print(f"pass {attempt+1}: pages={len(d.pages)} preface@{preface_start} main@{main_start} — numbers updated, re-rendering")
        tocnum = new_tocnum
    N = len(d.pages)
    sizes = [(pg.width, pg.height) for pg in d.pages]
    labels = []
    for i in range(N):
        if i < preface_start:
            labels.append("")
        elif i < main_start:
            labels.append(LETTERS[i - preface_start])
        else:
            labels.append(fa(i - main_start + 1))
    build_overlay(labels, sizes, f"{BUILD}/overlay.pdf")
    out = f"{DOWNLOAD}/SUT_Physics_Career_Guide_v1.pdf"
    merge(f"{BUILD}/base.pdf", f"{BUILD}/overlay.pdf", labels, out)
    print("final pages:", N, "| size:", round(os.path.getsize(out) / 1e6, 2), "MB")
    print("footer map: p1-2 none, letters from p", preface_start + 1, ", digits from p", main_start + 1)

if __name__ == "__main__":
    main()
