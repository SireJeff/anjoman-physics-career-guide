#!/usr/bin/env python3
"""Persian typography utilities: digits, LTR-run wrapping, icons, arrows."""
import re

FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"

def fa(n):
    """int -> Persian digit string"""
    return "".join(FA_DIGITS[int(d)] for d in str(n))

VS_CHARS = "\ufe0e\ufe0f"

def strip_vs(text):
    """Strip Unicode variation selectors (U+FE0E/U+FE0F)."""
    return re.sub(f"[{VS_CHARS}]", "", text)

ICON_CHECK = '<span class="fa ic-check" aria-label="✔"></span>'
ICON_WARN = '<span class="fa ic-warn" aria-label="⚠"></span>'

def icons(text):
    """Replace check/warning marks with FontAwesome icon spans."""
    text = text.replace("\u2714", ICON_CHECK)
    text = text.replace("\u26a0", ICON_WARN)
    return text

def flip_arrows(text):
    """Flip → to ← so arrows point in RTL reading direction.
    (Source wrote them LTR-style; in RTL flow the arrow must point left
    to read naturally: «الف ← ب» = الف leads to ب.)"""
    return text.replace("\u2192", "\u2190")

# ----- LTR island wrapping (xepersian \lr{} equivalent) -----

# chars allowed inside a Latin run (incl. space, en-dash, currency, punct)
_LAT_CH = "A-Za-z0-9\u00c0-\u024f\u2013$€¥£‰%.,:;!?&/+=_#@'’()\\[\\]\\-*"
_LAT_RUN = re.compile(f"[{_LAT_CH}][{_LAT_CH} ]*[{_LAT_CH}]|[{_LAT_CH}]")
_HAS_LETTER = re.compile(r"[A-Za-z\u00c0-\u024f]")
_HAS_DIGIT = re.compile(r"[0-9]")
_CURRENCY_TOKEN = re.compile(r"[€$¥£][۰-۹][۰-۹٫,]*(?:[A-Za-z]{1,3})?")

def _qualifies(core):
    """A run qualifies if it has a Latin letter, or is a currency amount."""
    if _HAS_LETTER.search(core):
        return True
    return core[:1] in "$€¥£" and _HAS_DIGIT.search(core)

TAG_SPLIT = re.compile(r"(<[^>]+>)")

def _wrap_runs(text):
    """Wrap maximal Latin runs of a plain-text segment in <bdi dir="ltr" class="lt">."""
    out = []
    last = 0
    for m in _LAT_RUN.finditer(text):
        s, e = m.span()
        run = m.group(0)
        # trim outer spaces
        core = run.strip()
        lead = len(run) - len(run.lstrip())
        trail = len(run) - len(run.rstrip())
        cs, ce = s + lead, e - trail
        if not _qualifies(core):
            continue
        out.append(text[last:cs])
        out.append(f'<bdi dir="ltr" class="lt">{core}</bdi>')
        last = ce
    out.append(text[last:])
    return "".join(out)

def wrap_ltr(text):
    """Tag-aware LTR wrapping: process text between tags, skip inside <bdi>."""
    parts = TAG_SPLIT.split(text)
    out = []
    in_bdi = 0
    for part in parts:
        if part.startswith("<"):
            low = part.lower()
            if low.startswith("<bdi"):
                in_bdi += 1
            elif low.startswith("</bdi") and in_bdi:
                in_bdi -= 1
            out.append(part)
            continue
        if in_bdi:
            out.append(part)
        else:
            out.append(_wrap_runs(part))
    return "".join(out)

def wrap_currency(text):
    """Wrap currency + Persian-digit tokens (e.g. €۲,۹۰۰ / ¥۲٫۶M) in LTR bdi."""
    parts = TAG_SPLIT.split(text)
    out = []
    in_bdi = 0
    for part in parts:
        if part.startswith("<"):
            low = part.lower()
            if low.startswith("<bdi"):
                in_bdi += 1
            elif low.startswith("</bdi") and in_bdi:
                in_bdi -= 1
            out.append(part)
            continue
        if in_bdi:
            out.append(part)
        else:
            out.append(_CURRENCY_TOKEN.sub(
                lambda m: f'<bdi dir="ltr" class="lt">{m.group(0)}</bdi>', part))
    return "".join(out)
