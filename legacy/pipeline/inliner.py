#!/usr/bin/env python3
"""Inline Markdown→HTML transforms with Persian bidi handling."""
import re
from urllib.parse import quote
from fa_utils import strip_vs, flip_arrows, icons, wrap_ltr, wrap_currency

MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
TOKEN = re.compile("\x00(\\d+)\x00")
BOLD = re.compile(r"\*\*(.+?)\*\*")
EM = re.compile(r"\*([^*\n]+)\*")
URL_START = re.compile(r"https?://")
URL_TERMS = (" و ", " — ", "، ", "؛ ")

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def url_attr(url):
    """Percent-encode non-ASCII (Persian paths, spaces) for reliable PDF URIs."""
    q = quote(url, safe="!#$&'()*+,/:;=?@[]~%-._")
    return esc(q)

def _bold(t):
    return BOLD.sub(r"<strong>\1</strong>", t)

def _em(t):
    return EM.sub(r"<em>\1</em>", t)

def inline_rich(text):
    """Escape + bold + em for small fragments (link text)."""
    t = esc(text)
    t = _bold(t)
    t = _em(t)
    return t

def _inline_common(t, store, putback):
    t = esc(t)
    t = _bold(t)
    t = _em(t)
    t = icons(t)
    t = TOKEN.sub(putback, t)
    t = wrap_ltr(t)
    t = wrap_currency(t)
    return t

def inline(text):
    """Full pipeline for body text (Markdown links only, no raw URLs)."""
    t = strip_vs(text)
    t = flip_arrows(t)
    store = []
    def keep_txt(m):
        store.append((m.group(1), m.group(2)))
        return f"\x00{len(store)-1}\x00"
    t = MD_LINK.sub(keep_txt, t)
    def putback(m):
        txt, url = store[int(m.group(1))]
        return f'<a href="{url_attr(url)}">{inline_rich(txt)}</a>'
    return _inline_common(t, store, putback)

def inline_appx(text):
    """Pipeline for appendix items: Markdown links + raw URL linkification."""
    t = strip_vs(text)
    t = flip_arrows(t)
    store = []
    def add(txt=None, url=None):
        store.append((txt, url))
        return f"\x00{len(store)-1}\x00"
    t = MD_LINK.sub(lambda m: add(txt=m.group(1), url=m.group(2)), t)
    # raw URLs: span from https:// to first terminator (all terminators
    # contain a space, so they necessarily end the URL token)
    out, pos = [], 0
    while True:
        m = URL_START.search(t, pos)
        if not m:
            out.append(t[pos:])
            break
        s = m.start()
        out.append(t[pos:s])
        rest = t[s:]
        end = len(rest)
        for term in URL_TERMS:
            k = rest.find(term, 9)
            if k != -1:
                end = min(end, k)
        url = rest[:end].rstrip("،.؛")
        out.append(add(url=url))
        pos = s + end
    t = "".join(out)
    def putback(m):
        txt, url = store[int(m.group(1))]
        if txt is not None:
            return f'<a href="{url_attr(url)}">{inline_rich(txt)}</a>'
        return f'<a class="url" href="{url_attr(url)}"><bdi dir="ltr" class="url">{esc(url)}</bdi></a>'
    return _inline_common(t, store, putback)
