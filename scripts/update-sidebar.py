#!/usr/bin/env python3
"""
update-sidebar.py — Regenerates the sidebar HTML in all existing support pages.

Reads sidebar-config.json (now including TineModeler) and replaces the sidebar
block in every HTML file across all support directories.
"""

import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

TARGET_DIRS = [
    "EraVerb-support",
    "P73-support",
    "1Take-support",
    "GitInflow-support",
    "SonicDNACollector-support",
    "SonicDNAEngine-support",
    "simpleMIDIController-support",
    "ChatArchive-support",
    "TineModeler-support",
    "M2DX-Core-support",
    "M2DX-support",
    "PeerClockMetronome-support",
]

LANG_LABELS = {
    "en": "EN",
    "ja": "JA",
    "th": "TH",
    "zh-Hant": "繁體",
}


def load_config():
    with open(os.path.join(SCRIPT_DIR, "sidebar-config.json"), encoding="utf-8") as f:
        return json.load(f)


def get_app_for_path(rel_path, config):
    """Return the app config entry matching the file's path prefix."""
    for app in config:
        prefix = app["prefix"].lstrip("/")  # e.g. "1Take-support"
        if rel_path.startswith(prefix + "/") or rel_path == prefix:
            return app
    return None


def get_subpath(rel_path, app):
    prefix = app["prefix"].lstrip("/")
    if rel_path == prefix:
        return ""
    if rel_path.startswith(prefix + "/"):
        return rel_path[len(prefix) + 1 :]
    return rel_path


def detect_language(rel_path, app):
    """Detect the current page language based on path rules."""
    subpath = get_subpath(rel_path, app)
    available_langs = list(app["links"].keys())

    for lang in sorted(available_langs, key=len, reverse=True):
        if lang == "en":
            continue
        if subpath.startswith(f"{lang}/") or f"/{lang}/" in f"/{subpath}":
            return lang
        if re.search(
            rf"(?:^|/)(?:index|privacy|terms|changelog)-{re.escape(lang)}(?:\.html)?$",
            subpath,
        ):
            return lang

    if app["id"] == "ChatArchive" and "ja" in app["links"]:
        return "ja"
    if "en" in app["links"]:
        return "en"
    return available_langs[0]


def get_active_section(rel_path):
    """Return the active section key based on the path."""
    if "/blog/" in rel_path:
        return "blog"
    if "/manual/" in rel_path:
        return "manual"
    if "changelog" in rel_path:
        return "changelog"
    if "privacy" in rel_path:
        return "privacy"
    if "terms" in rel_path:
        return "terms"
    return "support"  # default: first link (Support)


def label_matches_section(label, section):
    """Check if a link label corresponds to the active section."""
    label_lower = label.lower()
    mapping = {
        "blog": [
            "blog", "ブログ", "blogg", "部落格", "블로그",
        ],
        "manual": [
            "manual", "マニュアル", "handbuch", "guia", "guide", "guida", "manuale",
            "handleiding", "manual", "手冊", "매뉴얼",
        ],
        "changelog": [
            "changelog", "更新履歴", "versionsverlauf", "registro de cambios",
            "journal des modifications", "registro modifiche", "wijzigingslog",
            "registro de alterações", "andringslogg", "變更記錄", "변경 기록",
        ],
        "privacy": [
            "privacy", "プライバシー", "datenschutz", "privacidad", "confidentialité",
            "privacybeleid", "privacidade", "integritet", "隱私", "개인정보",
        ],
        "terms": [
            "terms", "利用規約", "bedingungen", "términos", "conditions",
            "termini", "voorwaarden", "termos", "villkor", "條款", "약관",
        ],
        "support": [
            "support", "サポート", "soporte", "supporto", "suporte", "支援", "지원",
        ],
    }
    return label_lower in [x.lower() for x in mapping.get(section, [])]


def get_section_fallback_url(app, target_lang, active_section):
    links = app["links"].get(target_lang) or app["links"].get("en") or []
    for link in links:
        if label_matches_section(link["label"], active_section):
            return link["href"]
    if links:
        return links[0]["href"]
    return app["prefix"] + "/"


def compute_lang_switch_url(rel_path, app, current_lang, target_lang, active_section):
    """Compute the URL to switch language for the current page."""
    if target_lang == current_lang:
        return None

    prefix = app["prefix"]
    subpath = get_subpath(rel_path, app)

    if app["id"] == "ChatArchive":
        path_without_lang = subpath
        for lang in sorted(app["links"].keys(), key=len, reverse=True):
            lang_prefix = f"{lang}/"
            if path_without_lang.startswith(lang_prefix):
                path_without_lang = path_without_lang[len(lang_prefix) :]
                break

        if target_lang == "ja":
            if path_without_lang in ("", "index.html"):
                return prefix + "/"
            if path_without_lang in ("privacy", "privacy.html"):
                return prefix + "/privacy"
            if path_without_lang in ("terms", "terms.html"):
                return prefix + "/terms"
            return prefix + "/" + path_without_lang

        if path_without_lang in ("", "index.html"):
            return prefix + f"/{target_lang}/"
        if path_without_lang in ("privacy", "privacy.html"):
            return prefix + f"/{target_lang}/privacy"
        if path_without_lang in ("terms", "terms.html"):
            return prefix + f"/{target_lang}/terms"
        return prefix + f"/{target_lang}/" + path_without_lang

    if subpath in ("", "index.html") or re.fullmatch(r"index-[^/]+(?:\.html)?", subpath):
        return prefix + "/" if target_lang == "en" else prefix + f"/index-{target_lang}"

    for section in ("blog", "manual"):
        match = re.match(rf"{section}/([^/]+)/(.*)", subpath)
        if match:
            _, rest = match.groups()
            return prefix + f"/{section}/{target_lang}/{rest}"

    for section in ("privacy", "support", "changelog"):
        match = re.match(rf"{section}/([^/]+)/(.*)", subpath)
        if match:
            _, rest = match.groups()
            if target_lang == "en":
                return prefix + f"/{section}/{rest}"
            return prefix + f"/{section}/{target_lang}/{rest}"

    file_match = re.fullmatch(r"([a-zA-Z0-9-]+?)(?:-([A-Za-z0-9-]+))?(?:\.html)?", subpath)
    if file_match:
        stem, maybe_lang = file_match.groups()
        if maybe_lang in app["links"]:
            return prefix + f"/{stem}" if target_lang == "en" else prefix + f"/{stem}-{target_lang}"
        if target_lang == "en":
            return prefix + f"/{stem}"
        return prefix + f"/{stem}-{target_lang}"

    return get_section_fallback_url(app, target_lang, active_section)


def build_sidebar_html(config, current_app, rel_path, current_lang, active_section):
    """Build the full sidebar navigation HTML."""
    lines = []
    lines.append('<button class="sidebar-toggle" aria-label="Menu">&#9776;</button>')
    lines.append('<div class="sidebar-overlay"></div>')
    lines.append('<nav class="sidebar">')
    lines.append('  <div class="sidebar-logo"><a href="/">hakaru</a></div>')

    for app in config:
        is_current = app["id"] == current_app["id"]
        header_classes = "sidebar-app-header"
        if is_current:
            header_classes += " active expanded"

        links_classes = "sidebar-app-links"
        if is_current:
            links_classes += " show"

        lines.append('  <div class="sidebar-app">')
        lines.append(f'    <button class="{header_classes}">')
        lines.append(
            f'      <img src="{app["icon"]}" alt="{app["name"]}" width="24" height="24">'
        )
        lines.append(f'      {app["name"]}')
        lines.append('      <span class="arrow">&#9654;</span>')
        lines.append('    </button>')
        lines.append(f'    <div class="{links_classes}">')

        # Determine which language to show links in
        if is_current:
            display_lang = current_lang
        else:
            if current_lang in app["links"]:
                display_lang = current_lang
            else:
                display_lang = "en"

        app_links = app["links"].get(display_lang, app["links"].get("en", []))
        for link in app_links:
            is_active_link = is_current and label_matches_section(link["label"], active_section)
            active_attr = ' class="active"' if is_active_link else ""
            lines.append(f'      <a href="{link["href"]}"{active_attr}>{link["label"]}</a>')

        lines.append('    </div>')
        lines.append('  </div>')

    # Language switcher
    lines.append('  <div class="sidebar-lang">')

    available_langs = list(current_app["links"].keys())

    for lang in available_langs:
        label = LANG_LABELS.get(lang, lang.upper())
        if lang == current_lang:
            lines.append(
                f'    <span class="sidebar-lang-btn active" data-lang="{lang}">{label}</span>'
            )
        else:
            switch_url = compute_lang_switch_url(
                rel_path, current_app, current_lang, lang, active_section
            )
            lines.append(
                f'    <a href="{switch_url}" class="sidebar-lang-btn" data-lang="{lang}">{label}</a>'
            )

    lines.append('  </div>')
    lines.append('</nav>')

    return "\n".join(lines)


def collect_html_files():
    """Collect all HTML files in the target directories."""
    files = []
    for target_dir in TARGET_DIRS:
        dir_path = os.path.join(REPO_ROOT, target_dir)
        if not os.path.isdir(dir_path):
            continue
        for root, dirs, filenames in os.walk(dir_path):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for filename in filenames:
                if filename.endswith(".html"):
                    files.append(os.path.join(root, filename))
    return sorted(files)


# Regex to match the entire sidebar block
SIDEBAR_PATTERN = re.compile(
    r'<button class="sidebar-toggle"[^>]*>.*?</nav>',
    re.DOTALL,
)


def main():
    config = load_config()

    html_files = collect_html_files()
    print(f"Found {len(html_files)} HTML files to process")

    updated = 0
    skipped = 0
    errors = 0

    for file_path in html_files:
        rel_path = os.path.relpath(file_path, REPO_ROOT)

        with open(file_path, encoding="utf-8") as f:
            html = f.read()

        # Skip files that don't have a sidebar yet
        if 'class="sidebar-toggle"' not in html:
            print(f"  SKIP (no sidebar): {rel_path}", file=sys.stderr)
            skipped += 1
            continue

        # Determine which app
        app = get_app_for_path(rel_path, config)
        if app is None:
            print(f"  WARNING: Could not determine app for {rel_path}", file=sys.stderr)
            errors += 1
            continue

        # Detect language
        current_lang = detect_language(rel_path, app)
        if current_lang not in app["links"]:
            current_lang = list(app["links"].keys())[0]

        # Determine active section
        active_section = get_active_section(rel_path)

        # Build new sidebar HTML
        new_sidebar = build_sidebar_html(
            config, app, rel_path, current_lang, active_section
        )

        # Replace the old sidebar block
        new_html, count = SIDEBAR_PATTERN.subn(new_sidebar, html, count=1)
        if count == 0:
            print(f"  WARNING: Pattern not matched in {rel_path}", file=sys.stderr)
            errors += 1
            continue

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_html)

        print(f"  [OK] {rel_path} (app={app['id']}, lang={current_lang}, section={active_section})")
        updated += 1

    print(f"\nDone: {updated} updated, {skipped} skipped (no sidebar), {errors} errors")


if __name__ == "__main__":
    main()
