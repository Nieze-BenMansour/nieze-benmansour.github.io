# Builds study-guide/fr/az104.html from az104.html (machine translation of text nodes; preserves code/pre).
# Run after editing the English source: python study-guide/_translate_az104_fr.py
# Requires: pip install beautifulsoup4 deep-translator lxml
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator

DIR = Path(__file__).resolve().parent
SRC = DIR / "az104.html"
OUT = DIR / "fr" / "az104.html"

SKIP_PARENT_TAG = frozenset({"script", "style", "code", "pre", "kbd", "samp", "textarea"})
SKIP_ANCESTOR = frozenset({"code", "pre"})


def should_translate_text(node: NavigableString) -> bool:
    if not str(node).strip():
        return False
    p = node.parent
    if not p or not p.name:
        return False
    for anc in p.parents:
        if anc.name in SKIP_ANCESTOR:
            return False
    if p.name in SKIP_PARENT_TAG:
        return False
    return True


def chunk_text(text: str, max_len: int = 4500) -> list[str]:
    text = text.strip()
    if len(text) <= max_len:
        return [text]
    parts = []
    rest = text
    while rest:
        if len(rest) <= max_len:
            parts.append(rest)
            break
        cut = rest.rfind(". ", 0, max_len)
        if cut < max_len // 2:
            cut = rest.rfind(" ", 0, max_len)
        if cut < max_len // 2:
            cut = max_len
        parts.append(rest[: cut + 1].strip())
        rest = rest[cut + 1 :].strip()
    return parts


def translate_cached(translator: GoogleTranslator, cache: dict, text: str) -> str:
    if text in cache:
        return cache[text]
    chunks = chunk_text(text)
    out_parts = []
    for ch in chunks:
        for attempt in range(4):
            try:
                tr = translator.translate(ch)
                out_parts.append(tr if tr is not None else ch)
                break
            except Exception as e:
                if attempt == 3:
                    print("Translate failed, keeping EN:", repr(ch[:120]), e, file=sys.stderr)
                    out_parts.append(ch)
                else:
                    time.sleep(2 * (attempt + 1))
        time.sleep(0.05)
    merged = " ".join(out_parts) if len(out_parts) > 1 else (out_parts[0] if out_parts else text)
    if not merged:
        merged = text
    cache[text] = merged
    return merged


def translate_attrs(tag, translator: GoogleTranslator, cache: dict) -> None:
    for attr in ("aria-label", "title"):
        if not tag.has_attr(attr):
            continue
        val = tag[attr]
        if not val or not str(val).strip():
            continue
        tag[attr] = translate_cached(translator, cache, str(val))


def main():
    html = SRC.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    if soup.html:
        soup.html["lang"] = "fr"
    if soup.title:
        soup.title.string = "Guide d’étude AZ-104"
    head = soup.head
    if head:
        m = head.find("meta", attrs={"name": "description"})
        if m:
            m["content"] = (
                "Notes de révision pour l’examen AZ-104 Microsoft Azure Administrator — identités, stockage, calcul, réseau, supervision."
            )
        else:
            t = head.find("title")
            if t:
                meta = soup.new_tag(
                    "meta",
                    attrs={
                        "name": "description",
                        "content": "Notes de révision pour l’examen AZ-104 Microsoft Azure Administrator — identités, stockage, calcul, réseau, supervision.",
                    },
                )
                t.insert_after(meta)

    nav_html = """  <header class="top-nav" id="topNav">
    <a href="az104.html" class="site-title">Guide AZ-104</a>
    <button type="button" class="menu-toggle" id="menuToggle" aria-label="Ouvrir le menu">☰</button>
    <div class="nav-wrap">
      <ul class="nav-links">
        <li><a href="../../index.html" class="back-link">← Retour au portfolio</a></li>
        <li><a href="../az400-all.html">Guide AZ-400 (EN)</a></li>
        <li><a href="az400-all.html">Guide AZ-400 (FR)</a></li>
        <li><a href="../az104.html">English version</a></li>
        <li><a href="#identities">1. Identités</a></li>
        <li><a href="#storage">2. Stockage</a></li>
        <li><a href="#compute">3. Calcul</a></li>
        <li><a href="#networking">4. Réseau</a></li>
        <li><a href="#monitor">5. Supervision</a></li>
      </ul>
      <div class="nav-right">
        <button type="button" class="theme-toggle" id="themeToggle" aria-label="Basculer le mode sombre" title="Basculer clair / sombre">☀</button>
      </div>
    </div>
  </header>
"""
    header = soup.find("header", class_="top-nav")
    if header:
        header.replace_with(BeautifulSoup(nav_html, "html.parser"))

    fold = soup.find("div", class_="fold-unfold")
    if fold:
        frag = BeautifulSoup(
            """<div class="fold-unfold">
          <button type="button" id="foldAll" aria-label="Tout replier">Tout replier</button>
          <button type="button" id="unfoldAll" aria-label="Tout déplier">Tout déplier</button>
        </div>""",
            "html.parser",
        ).div
        fold.replace_with(frag)

    main = soup.find("main")
    if not main:
        raise SystemExit("no main")

    translator = GoogleTranslator(source="en", target="fr")
    cache: dict[str, str] = {}

    to_translate: list[NavigableString] = []
    for node in main.descendants:
        if isinstance(node, NavigableString) and should_translate_text(node):
            to_translate.append(node)

    unique_texts = list(dict.fromkeys(str(n) for n in to_translate))
    print("Text nodes:", len(to_translate), "unique strings:", len(unique_texts), file=sys.stderr)

    for i, ut in enumerate(unique_texts):
        if i % 50 == 0:
            print(f"  translating {i}/{len(unique_texts)}", file=sys.stderr)
        translate_cached(translator, cache, ut)

    for node in to_translate:
        t = str(node)
        node.replace_with(cache[t])

    for tag in main.find_all(True):
        translate_attrs(tag, translator, cache)

    for script in soup.find_all("script"):
        s = script.string
        if not s or "az104-theme" not in s:
            continue
        s = s.replace("Switch to light mode", "Passer en mode clair")
        s = s.replace("Switch to dark mode", "Passer en mode sombre")
        s = s.replace("Close menu", "Fermer le menu")
        s = s.replace("Open menu", "Ouvrir le menu")
        s = s.replace("Expand section", "Développer la section")
        s = s.replace("Collapse section", "Réduire la section")
        script.string = s

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(soup.prettify(), encoding="utf-8")
    print("Wrote", OUT, "chars", len(soup.prettify()))


if __name__ == "__main__":
    main()
