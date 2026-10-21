#!/usr/bin/env python3
"""Parse the Persian Markdown into an intermediate document tree."""
import re, sys
sys.path.insert(0, "/home/z/my-project/scripts")
from fa_utils import strip_vs

SRC = "/home/z/my-project/upload/SUT_Physics_Career_Guide_FA.md"

FA_NUM = "۰۱۲۳۴۵۶۷۸۹"

def is_h2(ln):  return ln.startswith("## ")
def is_h3(ln):  return ln.startswith("### ")
def is_h1(ln):  return ln.startswith("# ") and not ln.startswith("## ")
def is_table(ln): return ln.strip().startswith("|")
def is_hr(ln):  return re.fullmatch(r"-{3,}", ln.strip()) is not None
def is_ul(ln):  return ln.startswith("- ")
def is_ol(ln):  return re.match(r"^\d+\.\s", ln) is not None

def strip_h2_number(title):
    """«۱۱. عنوان» -> (11, 'عنوان')"""
    m = re.match(r"^([۰-۹]+)\.\s*(.*)$", title.strip())
    if m:
        num = int("".join(str(FA_NUM.index(c)) for c in m.group(1)))
        return num, m.group(2).strip()
    return None, title.strip()

def strip_h3_number(title):
    """«۶٫۱ عنوان» -> ((6,1), 'عنوان') ; unnumbered -> (None, title)"""
    m = re.match(r"^([۰-۹]+)٫([۰-۹]+)\s*(.*)$", title.strip())
    if m:
        a = int("".join(str(FA_NUM.index(c)) for c in m.group(1)))
        b = int("".join(str(FA_NUM.index(c)) for c in m.group(2)))
        return (a, b), m.group(3).strip()
    return None, title.strip()

def parse_table(lines, i):
    """Parse pipe-table starting at lines[i]; return (rows, next_i).
    rows = list of list-of-cells; separator row removed."""
    rows = []
    while i < len(lines) and is_table(lines[i]):
        raw = lines[i].strip().strip("|")
        cells = [c.strip() for c in raw.split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            rows.append(cells)
        i += 1
    return rows, i

def parse():
    text = open(SRC, encoding="utf-8").read()
    lines = text.split("\n")

    # ---- split off Editor's Notes (verbatim) ----
    en_start = None
    for idx, ln in enumerate(lines):
        if ln.strip() == "# Editor's Notes (English)":
            en_start = idx
            break
    assert en_start is not None, "Editor's Notes heading not found"
    editors_notes = "\n".join(lines[en_start:])
    lines = lines[:en_start]
    # drop trailing hr/blank
    while lines and (lines[-1].strip() in ("", "---")):
        lines.pop()

    doc = {"title": "", "subtitle": "", "preface": [], "chapters": [], "appendix": None}

    i = 0
    # ---- head matter: h1 title, h3 subtitle, preface paragraphs until first hr ----
    while i < len(lines):
        ln = lines[i]
        if is_h1(ln) and not doc["title"]:
            doc["title"] = ln[2:].strip(); i += 1; continue
        if is_h3(ln) and not doc["subtitle"]:
            doc["subtitle"] = ln[3:].strip(); i += 1; continue
        if is_hr(ln):
            i += 1; break
        if ln.strip():
            doc["preface"].append(ln.strip())
        i += 1

    # ---- chapters ----
    cur = None          # current chapter dict
    sec = None          # current section dict or None
    blocks = None       # current block list
    table_order = []    # (chapter_num, table_idx_in_chapter)

    def flush_table_context():
        pass

    while i < len(lines):
        ln = lines[i]

        if is_h2(ln):
            num, title = strip_h2_number(ln[3:])
            cur = {"num": num, "title": title, "secs": [], "intro": [], "tables": 0}
            doc["chapters"].append(cur)
            sec = None
            blocks = cur["intro"]
            i += 1
            continue

        if is_h3(ln) and cur is not None:
            snum, stitle = strip_h3_number(ln[3:])
            sec = {"num": snum, "title": stitle, "blocks": []}
            cur["secs"].append(sec)
            blocks = sec["blocks"]
            i += 1
            continue

        if is_table(ln):
            rows, i = parse_table(lines, i)
            cur["tables"] += 1
            kind = "table"
            if cur["num"] == 13:
                kind = "myths"
            blocks.append({"t": kind, "rows": rows,
                           "idx": cur["tables"], "chap": cur["num"]})
            continue

        if is_hr(ln):
            blocks.append({"t": "hr"})
            i += 1
            continue

        if is_ul(ln):
            items = []
            while i < len(lines) and is_ul(lines[i]):
                items.append(lines[i][2:].strip()); i += 1
            blocks.append({"t": "ul", "items": items})
            continue

        if is_ol(ln):
            items = []
            while i < len(lines) and is_ol(lines[i]):
                m = re.match(r"^(\d+\.)\s+(.*)$", lines[i])
                items.append((m.group(1), m.group(2).strip()))
                i += 1
            blocks.append({"t": "ol", "items": items})
            continue

        if ln.strip():
            blocks.append({"t": "p", "text": ln.strip()})

        i += 1

    # ---- extract appendix (chapter 14) ----
    for ch in doc["chapters"]:
        if ch["num"] == 14:
            doc["appendix"] = ch
    doc["chapters"] = [c for c in doc["chapters"] if c["num"] != 14]
    if doc["appendix"]:
        doc["appendix"]["num"] = None  # becomes پیوست الف

    return doc, editors_notes

if __name__ == "__main__":
    doc, notes = parse()
    print("title:", doc["title"])
    print("subtitle:", doc["subtitle"])
    print("preface paras:", len(doc["preface"]))
    print("chapters:", [(c["num"], c["title"][:30], len(c["intro"]), len(c["secs"]), c["tables"]) for c in doc["chapters"]])
    a = doc["appendix"]
    print("appendix: intro", len(a["intro"]), "secs", [(s["num"], s["title"][:40], len(s["blocks"])) for s in a["secs"]])
    print("editors notes chars:", len(notes))
