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
    "1Take-support",
    "GitInflow-support",
    "SonicDNACollector-support",
    "SonicDNAEngine-support",
    "simpleMIDIController-support",
    "ChatArchive-support",
    "TineModeler-support",
    "M2DX-Core-support",
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


def detect_language(rel_path, app):
    """Detect the current page language based on path rules."""
    app_id = app["id"]

    if app_id == "ChatArchive":
        if "/en/" in rel_path:
            return "en"
        if "/th/" in rel_path:
            return "th"
        if "/zh-Hant/" in rel_path:
            return "zh-Hant"
        return "ja"  # root is JA for ChatArchive
    else:
        # Standard apps: JA indicators
        if (
            "index-ja" in rel_path
            or "privacy-ja" in rel_path
            or "changelog-ja" in rel_path
            or "/ja/" in rel_path
        ):
            return "ja"
        return "en"


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
        "blog": ["blog", "ブログ"],
        "manual": ["manual", "マニュアル"],
        "changelog": ["changelog", "更新履歴"],
        "privacy": ["privacy", "プライバシー"],
        "terms": ["terms", "利用規約"],
        "support": ["support", "サポート"],
    }
    return label_lower in [x.lower() for x in mapping.get(section, [])]


def compute_lang_switch_url(rel_path, app, current_lang):
    """Compute the URL to switch language for the current page."""
    app_id = app["id"]

    if app_id == "ChatArchive":
        # ChatArchive: JA is root, others have lang prefix
        if current_lang == "ja":
            prefix = app["prefix"]
            path_within = rel_path[len("ChatArchive-support"):].lstrip("/")
            if path_within in ("", "index.html"):
                return prefix + "/en/"
            if path_within.startswith("blog/"):
                return prefix + "/en/" + path_within
            if path_within in ("privacy.html", "privacy"):
                return prefix + "/en/privacy"
            if path_within in ("terms.html", "terms"):
                return prefix + "/en/terms"
            return prefix + "/en/"
        else:
            prefix = app["prefix"]
            path_within = rel_path[len("ChatArchive-support"):].lstrip("/")
            for lang_seg in ("en/", "th/", "zh-Hant/"):
                if path_within.startswith(lang_seg):
                    path_within = path_within[len(lang_seg):]
                    break
            if path_within in ("", "index.html"):
                return prefix + "/"
            if path_within.startswith("blog/"):
                return prefix + "/" + path_within
            if path_within in ("privacy.html", "privacy"):
                return prefix + "/privacy"
            if path_within in ("terms.html", "terms"):
                return prefix + "/terms"
            return prefix + "/"
    else:
        # Standard apps
        prefix = "/" + app["prefix"].lstrip("/")
        path_within = rel_path[len(app["prefix"].lstrip("/") + "/"):]

        if current_lang == "en":
            # Switch to JA
            if "/blog/en/" in rel_path:
                return "/" + rel_path.replace("/blog/en/", "/blog/ja/")
            if "/manual/en/" in rel_path:
                return "/" + rel_path.replace("/manual/en/", "/manual/ja/")
            if "index.html" in path_within or path_within == "":
                return prefix + "/index-ja"
            if "privacy.html" in path_within or path_within == "privacy.html":
                return prefix + "/privacy-ja"
            if "changelog.html" in path_within or path_within == "changelog.html":
                return prefix + "/changelog-ja"
            return prefix + "/index-ja"
        else:
            # Switch to EN
            if "/blog/ja/" in rel_path:
                return "/" + rel_path.replace("/blog/ja/", "/blog/en/")
            if "/manual/ja/" in rel_path:
                return "/" + rel_path.replace("/manual/ja/", "/manual/en/")
            if "index-ja.html" in path_within or "index-ja" in path_within:
                return prefix + "/"
            if "privacy-ja.html" in path_within or "privacy-ja" in path_within:
                return prefix + "/privacy"
            if "changelog-ja.html" in path_within or "changelog-ja" in path_within:
                return prefix + "/changelog"
            return prefix + "/"


def build_sidebar_html(config, current_app, current_lang, active_section, lang_switch_url):
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

    # For standard apps (non-ChatArchive), only show en/ja
    if current_app["id"] != "ChatArchive":
        available_langs = [l for l in available_langs if l in ("en", "ja")]

    for lang in available_langs:
        label = LANG_LABELS.get(lang, lang.upper())
        if lang == current_lang:
            lines.append(
                f'    <span class="sidebar-lang-btn active" data-lang="{lang}">{label}</span>'
            )
        else:
            if current_app["id"] != "ChatArchive" or lang != current_lang:
                switch_url = lang_switch_url if len(available_langs) == 2 else "#"
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

        # Compute language switch URL
        lang_switch_url = compute_lang_switch_url(rel_path, app, current_lang)

        # Build new sidebar HTML
        new_sidebar = build_sidebar_html(
            config, app, current_lang, active_section, lang_switch_url
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
