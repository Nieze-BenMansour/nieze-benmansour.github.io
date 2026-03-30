# Fetches AZ-400 Learn data for a locale (en-us or fr-fr).
# Snippets: az400_learn_snippets.py or az400_learn_snippets_fr.py
# Unit excerpts: az400_learn_unit_excerpts.py or az400_learn_unit_excerpts_fr.py
# Run from study-guide/: python fetch_az400_locale_data.py --locale fr-fr
from __future__ import annotations

import argparse
import re
import time
import urllib.error
import urllib.request
from html import unescape

from az400_learn_snippets import LEARN

UA = "Mozilla/5.0 (compatible; AZ400-study-guide/1.0)"
SKIP_SUBSTR = ("knowledge-check",)
MAX_UNITS = 12
MAX_TEXT_PER_UNIT = 950
SLEEP_SEC = 0.35


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def strip_tags(s: str) -> str:
    t = re.sub(r"<[^>]+>", " ", s)
    t = unescape(re.sub(r"\s+", " ", t)).strip()
    return t


def parse_module_landing(html: str) -> dict:
    """Extract title, summary, objectives, prerequisites from a Learn module landing page."""
    title_m = re.search(r"<h1[^>]*>\s*([^<]+?)\s*</h1>", html, re.I)
    title = unescape(title_m.group(1).strip()) if title_m else ""
    summary = ""
    for pat in (
        r'property="og:description" content="([^"]*)"',
        r'name="description" content="([^"]*)"',
    ):
        m = re.search(pat, html)
        if m:
            summary = unescape(m.group(1).strip())
            break
    objectives: list[str] = []
    prereq: list[str] = []
    # Section headers vary by locale
    for obj_header in (
        r"Objectifs d'apprentissage",
        r"Learning objectives",
    ):
        sec = re.search(
            obj_header + r"[\s\S]{0,800}?<ul[^>]*>([\s\S]*?)</ul>",
            html,
            re.I,
        )
        if sec:
            objectives = [
                strip_tags(x)
                for x in re.findall(r"<li[^>]*>([\s\S]*?)</li>", sec.group(1))
                if strip_tags(x)
            ]
            break
    for pre_header in (r"Prérequis", r"Prerequisites"):
        sec = re.search(
            pre_header + r"[\s\S]{0,400}?<ul[^>]*>([\s\S]*?)</ul>", html, re.I
        )
        if sec:
            prereq = [
                strip_tags(x)
                for x in re.findall(r"<li[^>]*>([\s\S]*?)</li>", sec.group(1))
                if strip_tags(x)
            ]
            break
    return {
        "title": title,
        "summary": summary,
        "objectives": objectives,
        "prerequisites": prereq,
    }


def fetch_snippets(locale: str) -> dict[str, dict]:
    base = f"https://learn.microsoft.com/{locale}/training/modules"
    out: dict[str, dict] = {}
    slugs = sorted(LEARN.keys())
    for i, slug in enumerate(slugs, 1):
        print(f"[snippets {i}/{len(slugs)}] {slug}")
        url = f"{base}/{slug}/"
        try:
            html = fetch(url)
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            print("  failed:", e)
            fb = LEARN.get(slug, {})
            out[slug] = {
                "title": slug,
                "summary": fb.get("summary", ""),
                "objectives": fb.get("objectives", []),
                "prerequisites": fb.get("prerequisites", []),
            }
            time.sleep(SLEEP_SEC)
            continue
        meta = parse_module_landing(html)
        fb = LEARN.get(slug, {})
        out[slug] = {
            "title": meta.get("title") or fb.get("title", "") or slug,
            "summary": meta.get("summary") or fb.get("summary", ""),
            "objectives": meta.get("objectives") or fb.get("objectives", []),
            "prerequisites": meta.get("prerequisites") or fb.get("prerequisites", []),
        }
        time.sleep(SLEEP_SEC)
    return out


def module_units(module_slug: str, locale: str) -> list[tuple[str, str]]:
    base = f"https://learn.microsoft.com/{locale}/training/modules"
    d = fetch(f"{base}/{module_slug}/")
    pairs: list[tuple[str, str]] = []

    def scan(pat: str) -> None:
        nonlocal pairs
        for m in re.finditer(pat, d):
            pairs.append((m.group(1), unescape(m.group(2)).strip()))

    scan(r'<a class="unit-title[^"]*"[^>]*href="(\d+-[^"]+)"[^>]*>([^<]+)</a>')
    if not pairs:
        scan(
            r'<a[^>]*href="(\d+-[^"]+)"[^>]*class="unit-title[^"]*"[^>]*>([^<]+)</a>'
        )
    return pairs


def extract_module_unit_content(page_html: str) -> str:
    marker = 'id="module-unit-content">'
    start = page_html.find(marker)
    if start == -1:
        return ""
    sub = page_html[start + len(marker) :]
    depth = 1
    i = 0
    n = len(sub)
    while i < n:
        if sub.startswith("<div", i):
            depth += 1
            ie = sub.find(">", i)
            if ie == -1:
                break
            i = ie + 1
            continue
        if sub.startswith("</div>", i):
            depth -= 1
            i += 6
            if depth == 0:
                return sub[: i - 6]
            continue
        i += 1
    return ""


def paragraphs_from_inner(inner: str) -> str:
    chunks = [
        strip_tags(m.group(1))
        for m in re.finditer(r"<p[^>]*>(.*?)</p>", inner, re.S | re.I)
    ]
    chunks = [c for c in chunks if c and len(c) > 15]
    for m in re.finditer(r"<li[^>]*>(.*?)</li>", inner, re.S | re.I):
        t = strip_tags(m.group(1))
        if t and len(t) > 15:
            chunks.append(t)
    if not chunks:
        t = strip_tags(inner)
        return t[:MAX_TEXT_PER_UNIT] if t else ""
    text = " ".join(chunks[:12])
    if len(text) > MAX_TEXT_PER_UNIT:
        text = text[: MAX_TEXT_PER_UNIT - 1].rsplit(" ", 1)[0] + "…"
    return text


def should_skip_unit(unit_path: str) -> bool:
    low = unit_path.lower()
    return any(s in low for s in SKIP_SUBSTR)


def excerpt_for_unit(
    module_slug: str, unit_path: str, title: str, locale: str
) -> dict | None:
    base = f"https://learn.microsoft.com/{locale}/training/modules"
    url = f"{base}/{module_slug}/{unit_path}/"
    try:
        page = fetch(url)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None
    inner = extract_module_unit_content(page)
    text = paragraphs_from_inner(inner)
    if not text:
        return None
    return {"path": unit_path, "title": title, "url": url, "text": text}


def fetch_unit_excerpts(locale: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    slugs = sorted(LEARN.keys())
    for si, slug in enumerate(slugs, 1):
        print(f"[units {si}/{len(slugs)}] {slug}")
        try:
            pairs = module_units(slug, locale)
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            print("  module index failed:", e)
            out[slug] = []
            time.sleep(SLEEP_SEC)
            continue
        rows: list[dict] = []
        for unit_path, title in pairs:
            if should_skip_unit(unit_path):
                continue
            if len(rows) >= MAX_UNITS:
                break
            time.sleep(SLEEP_SEC)
            row = excerpt_for_unit(slug, unit_path, title, locale)
            if row:
                rows.append(row)
                print(f"  ok {unit_path}")
            else:
                print(f"  skip {unit_path}")
        out[slug] = rows
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Fetch French (fr-fr) Learn data. Does not overwrite English az400_learn_snippets.py."
    )
    ap.add_argument(
        "--locale",
        default="fr-fr",
        choices=["fr-fr"],
        help="Only fr-fr supported (writes *_fr.py files)",
    )
    ap.add_argument(
        "--snippets-only",
        action="store_true",
        help="Only regenerate az400_learn_snippets_fr.py",
    )
    ap.add_argument(
        "--units-only",
        action="store_true",
        help="Only regenerate az400_learn_unit_excerpts_fr.py",
    )
    args = ap.parse_args()
    loc = args.locale.lower()
    snippets_path = "az400_learn_snippets_fr.py"
    excerpts_path = "az400_learn_unit_excerpts_fr.py"

    if not args.units_only:
        data = fetch_snippets(loc)
        with open(snippets_path, "w", encoding="utf-8") as f:
            f.write(
                f"# AUTO-GENERATED by fetch_az400_locale_data.py --locale {loc}\n\nLEARN = "
            )
            f.write(repr(data))
            f.write("\n")
        print("Wrote", snippets_path)

    if not args.snippets_only:
        data_u = fetch_unit_excerpts(loc)
        with open(excerpts_path, "w", encoding="utf-8") as f:
            f.write(
                f"# AUTO-GENERATED by fetch_az400_locale_data.py --locale {loc}\n\nUNIT_EXCERPTS = "
            )
            f.write(repr(data_u))
            f.write("\n")
        print("Wrote", excerpts_path)


if __name__ == "__main__":
    main()
