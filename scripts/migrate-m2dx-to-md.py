#!/usr/bin/env python3
"""
M2DX-support の HTML ファイルを Docusaurus 用 Markdown に変換する。

入力:
  M2DX-support/{index,privacy}[-{lang}].html  (22 ファイル)

出力:
  M2DX-docs-src/docs/{index,privacy}.md                                          (EN)
  M2DX-docs-src/i18n/{lang}/docusaurus-plugin-content-docs/current/{...}.md      (10 言語)

使い方:
  python3 scripts/migrate-m2dx-to-md.py            # 全 22 ファイルを変換
  python3 scripts/migrate-m2dx-to-md.py --lang ja  # ja のみ
  python3 scripts/migrate-m2dx-to-md.py --page index  # index のみ
"""

import argparse
import re
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify as md

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "M2DX-support"
TARGET_BASE = REPO_ROOT / "M2DX-docs-src"

LOCALES = ["en", "de", "es", "fr", "it", "ja", "ko", "nl", "pt-BR", "sv", "zh-Hant"]
PAGES = ["index", "privacy"]


def source_path(lang: str, page: str) -> Path:
    if lang == "en":
        return SOURCE_DIR / f"{page}.html"
    return SOURCE_DIR / f"{page}-{lang}.html"


def target_path(lang: str, page: str) -> Path:
    if lang == "en":
        return TARGET_BASE / "docs" / f"{page}.md"
    return (
        TARGET_BASE
        / "i18n"
        / lang
        / "docusaurus-plugin-content-docs"
        / "current"
        / f"{page}.md"
    )


def extract_meta(soup: BeautifulSoup) -> dict:
    title = soup.title.get_text(strip=True) if soup.title else ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""
    return {"title": title, "description": description}


def extract_content(soup: BeautifulSoup) -> str:
    """`.container > .content` の中身を返す。`.hero` 内のアイコン・タイトルは別途処理。"""
    for tag in soup.select("style, script, .sidebar, .sidebar-toggle, .sidebar-overlay"):
        tag.decompose()

    container = soup.select_one(".container")
    if container is None:
        return ""

    hero = container.select_one(".hero")
    content = container.select_one(".content")

    parts = []
    if hero:
        icon = hero.select_one("img")
        if icon:
            alt = icon.get("alt", "M2DX")
            parts.append(f"![{alt}](/M2DX-docs/img/m2dx-icon.png)\n")
        tagline = hero.find("p")
        if tagline:
            parts.append(tagline.get_text(strip=True) + "\n")
        cta = hero.select_one("a.testflight-cta")
        if cta:
            label = cta.get_text(strip=True)
            href = cta.get("href", "#")
            parts.append(f"\n[{label}]({href})\n")

    if content:
        parts.append(md(str(content), heading_style="ATX", strip=["script", "style"]))

    return "\n".join(parts)


def convert_admonitions(markdown: str) -> str:
    """Current Status section を `:::info ... :::` に変換。

    マーカーは "— Why TestFlight" / "— Warum TestFlight" 等の言語別表現で揺れるので、
    ファイル内に対応する見出しが見つかったら、その見出しから次の同レベル見出しまでを
    admonition でラップする。
    """
    markers = [
        "Why TestFlight",
        "Warum TestFlight",
        "Por qué TestFlight",
        "Pourquoi TestFlight",
        "Perché TestFlight",
        "なぜ TestFlight",
        "왜 TestFlight",
        "Waarom TestFlight",
        "Por que TestFlight",
        "Varför TestFlight",
        "為什麼 TestFlight",
    ]
    pattern = re.compile(
        r"(^##\s+.*(?:"
        + "|".join(re.escape(m) for m in markers)
        + r").*$)([\s\S]*?)(?=^##\s+|\Z)",
        re.MULTILINE,
    )

    def repl(m):
        heading = m.group(1)
        body = m.group(2).strip()
        title = heading.lstrip("# ").strip()
        return f":::info {title}\n\n{body}\n\n:::\n"

    return pattern.sub(repl, markdown)


def build_frontmatter(page: str, meta: dict) -> str:
    title = meta["title"].split(" | ")[0].strip() or ("M2DX" if page == "index" else "Privacy Policy")
    description = meta["description"]
    slug = "/" if page == "index" else "/privacy"
    description_safe = description.replace('"', '\\"')
    return (
        "---\n"
        f'title: "{title}"\n'
        f'description: "{description_safe}"\n'
        f"slug: {slug}\n"
        "---\n\n"
    )


def convert_one(lang: str, page: str) -> Path:
    src = source_path(lang, page)
    if not src.exists():
        raise FileNotFoundError(src)
    html = src.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    meta = extract_meta(soup)
    body = extract_content(soup)
    body = convert_admonitions(body)

    out = build_frontmatter(page, meta) + body.strip() + "\n"

    dst = target_path(lang, page)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding="utf-8")
    return dst


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lang", choices=LOCALES, help="単一言語のみ変換")
    p.add_argument("--page", choices=PAGES, help="単一ページのみ変換")
    args = p.parse_args()

    langs = [args.lang] if args.lang else LOCALES
    pages = [args.page] if args.page else PAGES

    written = []
    for lang in langs:
        for page in pages:
            dst = convert_one(lang, page)
            written.append(dst)
            print(f"  {lang:8s} {page:8s} -> {dst.relative_to(REPO_ROOT)}")

    print(f"\nConverted {len(written)} file(s).")


if __name__ == "__main__":
    main()
