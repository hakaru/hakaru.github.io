# Two-Pane Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert 144 app support HTML pages to a 2-pane layout with left sidebar navigation and automatic EN/JA language detection.

**Architecture:** A Python transformation script reads each HTML file, injects sidebar markup/CSS/JS, wraps existing content in a right pane, and removes the old inline nav. This avoids manually editing 144 files.

**Tech Stack:** Python 3 (BeautifulSoup4 for HTML parsing), vanilla CSS/JS for sidebar

---

## File Structure

| File | Responsibility |
|------|---------------|
| `scripts/sidebar-config.json` | App menu definitions (names, icons, sub-links, URL mappings) |
| `scripts/transform.py` | Reads config + HTML files, injects sidebar, writes output |
| `scripts/sidebar-template.html` | Sidebar HTML fragment template |
| `scripts/sidebar-styles.css` | Sidebar CSS (injected inline into each page) |
| `scripts/sidebar-script.js` | Sidebar JS: accordion, mobile menu, language detection |

All 144 `*-support/**/*.html` files are modified in-place by the script.

---

### Task 1: Create sidebar configuration

**Files:**
- Create: `scripts/sidebar-config.json`

- [ ] **Step 1: Create scripts directory**

```bash
mkdir -p /Users/hakaru/DEVELOP/hakaru.github.io/scripts
```

- [ ] **Step 2: Write sidebar-config.json**

```json
{
  "apps": [
    {
      "id": "1Take",
      "name": "1Take",
      "icon": "/1Take-support/assets/app-icon.png",
      "prefix": "/1Take-support",
      "links": {
        "en": [
          {"label": "Support", "href": "/1Take-support/"},
          {"label": "Manual", "href": "/1Take-support/manual/en/"},
          {"label": "Blog", "href": "/1Take-support/blog/en/"},
          {"label": "Changelog", "href": "/1Take-support/changelog"},
          {"label": "Privacy", "href": "/1Take-support/privacy"}
        ],
        "ja": [
          {"label": "サポート", "href": "/1Take-support/index-ja"},
          {"label": "マニュアル", "href": "/1Take-support/manual/ja/"},
          {"label": "ブログ", "href": "/1Take-support/blog/ja/"},
          {"label": "更新履歴", "href": "/1Take-support/changelog-ja"},
          {"label": "プライバシー", "href": "/1Take-support/privacy-ja"}
        ]
      },
      "langMap": {
        "/1Take-support/index.html": "/1Take-support/index-ja.html",
        "/1Take-support/index-ja.html": "/1Take-support/index.html",
        "/1Take-support/privacy.html": "/1Take-support/privacy-ja.html",
        "/1Take-support/privacy-ja.html": "/1Take-support/privacy.html",
        "/1Take-support/changelog.html": "/1Take-support/changelog-ja.html",
        "/1Take-support/changelog-ja.html": "/1Take-support/changelog.html",
        "/1Take-support/manual/en/": "/1Take-support/manual/ja/",
        "/1Take-support/manual/ja/": "/1Take-support/manual/en/",
        "/1Take-support/blog/en/": "/1Take-support/blog/ja/",
        "/1Take-support/blog/ja/": "/1Take-support/blog/en/",
        "blog/en/*/": "blog/ja/*/",
        "blog/ja/*/": "blog/en/*/"
      }
    },
    {
      "id": "GitInflow",
      "name": "GitInflow",
      "icon": "/assets/gitinflow-icon.png",
      "prefix": "/GitInflow-support",
      "links": {
        "en": [
          {"label": "Support", "href": "/GitInflow-support/"},
          {"label": "Manual", "href": "/GitInflow-support/manual/en/"},
          {"label": "Blog", "href": "/GitInflow-support/blog/en/"},
          {"label": "Changelog", "href": "/GitInflow-support/changelog"},
          {"label": "Privacy", "href": "/GitInflow-support/privacy"}
        ],
        "ja": [
          {"label": "サポート", "href": "/GitInflow-support/index-ja"},
          {"label": "マニュアル", "href": "/GitInflow-support/manual/ja/"},
          {"label": "ブログ", "href": "/GitInflow-support/blog/ja/"},
          {"label": "更新履歴", "href": "/GitInflow-support/changelog-ja"},
          {"label": "プライバシー", "href": "/GitInflow-support/privacy-ja"}
        ]
      },
      "langMap": {
        "/GitInflow-support/index.html": "/GitInflow-support/index-ja.html",
        "/GitInflow-support/index-ja.html": "/GitInflow-support/index.html",
        "/GitInflow-support/privacy.html": "/GitInflow-support/privacy-ja.html",
        "/GitInflow-support/privacy-ja.html": "/GitInflow-support/privacy.html",
        "/GitInflow-support/changelog.html": "/GitInflow-support/changelog-ja.html",
        "/GitInflow-support/changelog-ja.html": "/GitInflow-support/changelog.html",
        "/GitInflow-support/manual/en/": "/GitInflow-support/manual/ja/",
        "/GitInflow-support/manual/ja/": "/GitInflow-support/manual/en/",
        "blog/en/*/": "blog/ja/*/",
        "blog/ja/*/": "blog/en/*/"
      }
    },
    {
      "id": "SonicDNACollector",
      "name": "SonicDNA Collector",
      "icon": "/assets/sonicdna-icon.png",
      "prefix": "/SonicDNACollector-support",
      "links": {
        "en": [
          {"label": "Support", "href": "/SonicDNACollector-support/"},
          {"label": "Manual", "href": "/SonicDNACollector-support/manual/en/"},
          {"label": "Blog", "href": "/SonicDNACollector-support/blog/en/"},
          {"label": "Changelog", "href": "/SonicDNACollector-support/changelog/"},
          {"label": "Privacy", "href": "/SonicDNACollector-support/privacy"}
        ],
        "ja": [
          {"label": "サポート", "href": "/SonicDNACollector-support/index-ja"},
          {"label": "マニュアル", "href": "/SonicDNACollector-support/manual/ja/"},
          {"label": "ブログ", "href": "/SonicDNACollector-support/blog/ja/"},
          {"label": "更新履歴", "href": "/SonicDNACollector-support/changelog/"},
          {"label": "プライバシー", "href": "/SonicDNACollector-support/privacy-ja"}
        ]
      },
      "langMap": {
        "/SonicDNACollector-support/index.html": "/SonicDNACollector-support/index-ja.html",
        "/SonicDNACollector-support/index-ja.html": "/SonicDNACollector-support/index.html",
        "/SonicDNACollector-support/privacy.html": "/SonicDNACollector-support/privacy-ja.html",
        "/SonicDNACollector-support/privacy-ja.html": "/SonicDNACollector-support/privacy.html",
        "/SonicDNACollector-support/manual/en/": "/SonicDNACollector-support/manual/ja/",
        "/SonicDNACollector-support/manual/ja/": "/SonicDNACollector-support/manual/en/",
        "blog/en/*/": "blog/ja/*/",
        "blog/ja/*/": "blog/en/*/"
      }
    },
    {
      "id": "SonicDNAEngine",
      "name": "SonicDNA Engine",
      "icon": "/assets/sonicdna-icon.png",
      "prefix": "/SonicDNAEngine-support",
      "links": {
        "en": [
          {"label": "Support", "href": "/SonicDNAEngine-support/"},
          {"label": "Blog", "href": "/SonicDNAEngine-support/blog/en/"},
          {"label": "Changelog", "href": "/SonicDNAEngine-support/changelog"},
          {"label": "Privacy", "href": "/SonicDNAEngine-support/privacy"}
        ],
        "ja": [
          {"label": "サポート", "href": "/SonicDNAEngine-support/index-ja"},
          {"label": "ブログ", "href": "/SonicDNAEngine-support/blog/ja/"},
          {"label": "更新履歴", "href": "/SonicDNAEngine-support/changelog"},
          {"label": "プライバシー", "href": "/SonicDNAEngine-support/privacy-ja"}
        ]
      },
      "langMap": {
        "/SonicDNAEngine-support/index.html": "/SonicDNAEngine-support/index-ja.html",
        "/SonicDNAEngine-support/index-ja.html": "/SonicDNAEngine-support/index.html",
        "/SonicDNAEngine-support/privacy.html": "/SonicDNAEngine-support/privacy-ja.html",
        "/SonicDNAEngine-support/privacy-ja.html": "/SonicDNAEngine-support/privacy.html",
        "blog/en/*/": "blog/ja/*/",
        "blog/ja/*/": "blog/en/*/"
      }
    },
    {
      "id": "simpleMIDIController",
      "name": "simpleMIDI Controller",
      "icon": "/assets/simplemidi-icon.png",
      "prefix": "/simpleMIDIController-support",
      "links": {
        "en": [
          {"label": "Support", "href": "/simpleMIDIController-support/"},
          {"label": "Manual", "href": "/simpleMIDIController-support/manual/en/"},
          {"label": "Blog", "href": "/simpleMIDIController-support/blog/en/"},
          {"label": "Privacy", "href": "/simpleMIDIController-support/privacy/"}
        ],
        "ja": [
          {"label": "サポート", "href": "/simpleMIDIController-support/index-ja"},
          {"label": "マニュアル", "href": "/simpleMIDIController-support/manual/ja/"},
          {"label": "ブログ", "href": "/simpleMIDIController-support/blog/ja/"},
          {"label": "プライバシー", "href": "/simpleMIDIController-support/privacy/"}
        ]
      },
      "langMap": {
        "/simpleMIDIController-support/index.html": "/simpleMIDIController-support/index-ja.html",
        "/simpleMIDIController-support/index-ja.html": "/simpleMIDIController-support/index.html",
        "/simpleMIDIController-support/manual/en/": "/simpleMIDIController-support/manual/ja/",
        "/simpleMIDIController-support/manual/ja/": "/simpleMIDIController-support/manual/en/",
        "blog/en/*/": "blog/ja/*/",
        "blog/ja/*/": "blog/en/*/"
      }
    },
    {
      "id": "ChatArchive",
      "name": "ChatArchive",
      "icon": "/assets/chatarchive-icon.png",
      "prefix": "/ChatArchive-support",
      "links": {
        "ja": [
          {"label": "サポート", "href": "/ChatArchive-support/"},
          {"label": "ブログ", "href": "/ChatArchive-support/blog/"},
          {"label": "プライバシー", "href": "/ChatArchive-support/privacy"},
          {"label": "利用規約", "href": "/ChatArchive-support/terms"}
        ],
        "en": [
          {"label": "Support", "href": "/ChatArchive-support/en/"},
          {"label": "Blog", "href": "/ChatArchive-support/en/blog/"},
          {"label": "Privacy", "href": "/ChatArchive-support/en/privacy"},
          {"label": "Terms", "href": "/ChatArchive-support/en/terms"}
        ],
        "th": [
          {"label": "Support", "href": "/ChatArchive-support/th/"},
          {"label": "Blog", "href": "/ChatArchive-support/th/blog/"},
          {"label": "Privacy", "href": "/ChatArchive-support/th/privacy"},
          {"label": "Terms", "href": "/ChatArchive-support/th/terms"}
        ],
        "zh-Hant": [
          {"label": "Support", "href": "/ChatArchive-support/zh-Hant/"},
          {"label": "Blog", "href": "/ChatArchive-support/zh-Hant/blog/"},
          {"label": "Privacy", "href": "/ChatArchive-support/zh-Hant/privacy"},
          {"label": "Terms", "href": "/ChatArchive-support/zh-Hant/terms"}
        ]
      },
      "langMap": {
        "/ChatArchive-support/index.html": "/ChatArchive-support/en/index.html",
        "/ChatArchive-support/en/index.html": "/ChatArchive-support/index.html"
      }
    }
  ]
}
```

- [ ] **Step 3: Commit**

```bash
git add scripts/sidebar-config.json
git commit -m "feat: add sidebar menu configuration for all apps"
```

---

### Task 2: Create sidebar CSS

**Files:**
- Create: `scripts/sidebar-styles.css`

- [ ] **Step 1: Write sidebar CSS**

This CSS will be injected into the `<style>` tag of every page. Key layout: `body` becomes flexbox with sidebar (250px fixed) + content pane (flex: 1).

```css
/* --- Sidebar Layout --- */
body {
    display: flex;
    min-height: 100vh;
}
.sidebar {
    width: 250px;
    min-width: 250px;
    background: rgba(10, 10, 30, 0.95);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.08);
    padding: 20px 0;
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    overflow-y: auto;
    z-index: 100;
}
.sidebar-logo {
    padding: 10px 20px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 10px;
}
.sidebar-logo a {
    color: #fff;
    text-decoration: none;
    font-size: 1.2em;
    font-weight: 700;
}
.sidebar-logo a:hover { color: #e94560; }
.sidebar-app {
    margin-bottom: 2px;
}
.sidebar-app-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 20px;
    cursor: pointer;
    color: #a0a0a0;
    font-size: 0.95em;
    font-weight: 500;
    transition: all 0.2s;
    border: none;
    background: none;
    width: 100%;
    text-align: left;
    font-family: inherit;
}
.sidebar-app-header:hover { color: #fff; background: rgba(255,255,255,0.05); }
.sidebar-app-header.active { color: #e94560; }
.sidebar-app-header img {
    width: 24px;
    height: 24px;
    border-radius: 6px;
}
.sidebar-app-header .arrow {
    margin-left: auto;
    font-size: 0.7em;
    transition: transform 0.2s;
}
.sidebar-app-header.expanded .arrow {
    transform: rotate(90deg);
}
.sidebar-app-links {
    display: none;
    padding: 4px 0 8px;
}
.sidebar-app-links.show { display: block; }
.sidebar-app-links a {
    display: block;
    padding: 6px 20px 6px 54px;
    color: #808080;
    text-decoration: none;
    font-size: 0.85em;
    transition: all 0.2s;
}
.sidebar-app-links a:hover { color: #fff; background: rgba(255,255,255,0.05); }
.sidebar-app-links a.active { color: #e94560; }
.sidebar-lang {
    padding: 15px 20px;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin-top: 10px;
}
.sidebar-lang-btn {
    display: inline-block;
    padding: 4px 12px;
    color: #808080;
    text-decoration: none;
    font-size: 0.85em;
    border-radius: 4px;
    transition: all 0.2s;
}
.sidebar-lang-btn:hover { color: #fff; }
.sidebar-lang-btn.active { color: #e94560; font-weight: 600; }
.content-pane {
    flex: 1;
    margin-left: 250px;
    min-height: 100vh;
}
.content-pane .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 60px 20px;
}
/* Mobile hamburger */
.sidebar-toggle {
    display: none;
    position: fixed;
    top: 15px;
    left: 15px;
    z-index: 200;
    background: rgba(10, 10, 30, 0.9);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    color: #fff;
    font-size: 1.3em;
    padding: 8px 12px;
    cursor: pointer;
}
.sidebar-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    z-index: 90;
}
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-100%);
        transition: transform 0.3s;
    }
    .sidebar.open { transform: translateX(0); }
    .sidebar-toggle { display: block; }
    .sidebar-overlay.show { display: block; }
    .content-pane {
        margin-left: 0;
        padding-top: 60px;
    }
}
```

- [ ] **Step 2: Commit**

```bash
git add scripts/sidebar-styles.css
git commit -m "feat: add sidebar CSS with responsive mobile support"
```

---

### Task 3: Create sidebar JavaScript

**Files:**
- Create: `scripts/sidebar-script.js`

- [ ] **Step 1: Write sidebar JS**

Handles: accordion toggle, mobile menu, language auto-detection, active link highlighting.

```javascript
(function() {
    // Language auto-detection
    var savedLang = localStorage.getItem('hakaru-lang');
    var currentPath = window.location.pathname;

    function detectLang() {
        if (savedLang) return savedLang;
        var navLang = (navigator.language || navigator.userLanguage || 'en').toLowerCase();
        return navLang.startsWith('ja') ? 'ja' : 'en';
    }

    function isJaPage() {
        return currentPath.includes('/index-ja') ||
               currentPath.includes('/privacy-ja') ||
               currentPath.includes('/changelog-ja') ||
               currentPath.includes('/manual/ja/') ||
               currentPath.includes('/blog/ja/') ||
               (currentPath.includes('/ChatArchive-support/') &&
                !currentPath.includes('/en/') &&
                !currentPath.includes('/th/') &&
                !currentPath.includes('/zh-Hant/'));
    }

    function getCurrentPageLang() {
        if (currentPath.includes('/th/')) return 'th';
        if (currentPath.includes('/zh-Hant/')) return 'zh-Hant';
        if (currentPath.includes('/en/') && currentPath.includes('/ChatArchive-support/')) return 'en';
        return isJaPage() ? 'ja' : 'en';
    }

    // Auto-redirect on first visit (no saved preference)
    var pageLang = getCurrentPageLang();
    var userLang = detectLang();
    if (!savedLang && !document.referrer.includes('hakaru.net') && pageLang !== userLang) {
        var langAlt = document.querySelector('.sidebar-lang-btn[data-lang="' + userLang + '"]');
        if (langAlt && langAlt.href) {
            window.location.href = langAlt.href;
            return;
        }
    }

    // Accordion
    document.querySelectorAll('.sidebar-app-header').forEach(function(header) {
        header.addEventListener('click', function() {
            var links = this.nextElementSibling;
            var wasExpanded = this.classList.contains('expanded');
            // Collapse all
            document.querySelectorAll('.sidebar-app-header').forEach(function(h) {
                h.classList.remove('expanded');
                h.nextElementSibling.classList.remove('show');
            });
            // Toggle clicked
            if (!wasExpanded) {
                this.classList.add('expanded');
                links.classList.add('show');
            }
        });
    });

    // Auto-expand current app
    var currentApp = document.querySelector('.sidebar-app-header.active');
    if (currentApp) {
        currentApp.classList.add('expanded');
        currentApp.nextElementSibling.classList.add('show');
    }

    // Mobile toggle
    var toggle = document.querySelector('.sidebar-toggle');
    var sidebar = document.querySelector('.sidebar');
    var overlay = document.querySelector('.sidebar-overlay');
    if (toggle) {
        toggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('show');
        });
    }
    if (overlay) {
        overlay.addEventListener('click', function() {
            sidebar.classList.remove('open');
            overlay.classList.remove('show');
        });
    }

    // Language switch saves preference
    document.querySelectorAll('.sidebar-lang-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            localStorage.setItem('hakaru-lang', this.dataset.lang);
        });
    });
})();
```

- [ ] **Step 2: Commit**

```bash
git add scripts/sidebar-script.js
git commit -m "feat: add sidebar JS with accordion, mobile menu, and language detection"
```

---

### Task 4: Create the HTML transformation script

**Files:**
- Create: `scripts/transform.py`

- [ ] **Step 1: Install BeautifulSoup4**

```bash
pip3 install beautifulsoup4
```

- [ ] **Step 2: Write transform.py**

The script:
1. Reads `sidebar-config.json` to know app menu structure
2. Reads `sidebar-styles.css` and `sidebar-script.js` for injection
3. For each HTML file in `*-support/` directories:
   - Determines which app this file belongs to (by path prefix)
   - Determines the current page language
   - Builds sidebar HTML with the correct active states
   - Injects sidebar CSS into the existing `<style>` tag
   - Wraps `<body>` content: adds sidebar + wraps existing content in `.content-pane`
   - Removes the old `.support-nav` element
   - Removes the `.back-link` element (sidebar replaces it)
   - Adds hamburger button + overlay for mobile
   - Injects JS before `</body>`
   - Writes the file back

```python
#!/usr/bin/env python3
"""Transform support pages to two-pane layout with sidebar."""

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPTS_DIR / 'sidebar-config.json'
CSS_PATH = SCRIPTS_DIR / 'sidebar-styles.css'
JS_PATH = SCRIPTS_DIR / 'sidebar-script.js'


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_css():
    with open(CSS_PATH) as f:
        return f.read()


def load_js():
    with open(JS_PATH) as f:
        return f.read()


def detect_app(filepath, config):
    """Determine which app this file belongs to."""
    rel = '/' + str(filepath.relative_to(REPO_ROOT))
    for app in config['apps']:
        if rel.startswith(app['prefix']):
            return app
    return None


def detect_page_lang(filepath, app):
    """Determine the language of the current page."""
    rel = str(filepath.relative_to(REPO_ROOT))

    if app['id'] == 'ChatArchive':
        if '/en/' in rel:
            return 'en'
        if '/th/' in rel:
            return 'th'
        if '/zh-Hant/' in rel:
            return 'zh-Hant'
        return 'ja'

    if 'index-ja' in rel or 'privacy-ja' in rel or 'changelog-ja' in rel:
        return 'ja'
    if '/ja/' in rel:
        return 'ja'
    return 'en'


def get_lang_switch_url(filepath, app, page_lang):
    """Get the URL for the other language version of this page."""
    rel = '/' + str(filepath.relative_to(REPO_ROOT))

    # Try exact match in langMap
    lang_map = app.get('langMap', {})
    if rel in lang_map:
        return lang_map[rel]

    # Try pattern match for blog posts
    if app['id'] != 'ChatArchive':
        if '/blog/en/' in rel and rel.count('/') > 3:
            return rel.replace('/blog/en/', '/blog/ja/')
        if '/blog/ja/' in rel and rel.count('/') > 3:
            return rel.replace('/blog/ja/', '/blog/en/')

    return None


def detect_active_link(filepath, app, page_lang):
    """Determine which sub-link should be marked active."""
    rel = '/' + str(filepath.relative_to(REPO_ROOT))
    links = app['links'].get(page_lang, app['links'].get('en', []))

    # Check blog posts first (they match blog link)
    if '/blog/' in rel:
        for link in links:
            if '/blog/' in link['href']:
                return link['href']

    # Check manual
    if '/manual/' in rel:
        for link in links:
            if '/manual/' in link['href']:
                return link['href']

    # Check exact matches
    for link in links:
        href = link['href'].rstrip('/')
        rel_clean = rel.rstrip('/').replace('/index.html', '').replace('/index-ja.html', '').replace('.html', '')
        if href.rstrip('/') == rel_clean:
            return link['href']

    # Default to first link (Support)
    return links[0]['href'] if links else None


def build_sidebar_html(app, page_lang, active_href, lang_switch_url, config):
    """Build the sidebar HTML for this page."""
    lines = []
    lines.append('<button class="sidebar-toggle" aria-label="Menu">&#9776;</button>')
    lines.append('<div class="sidebar-overlay"></div>')
    lines.append('<nav class="sidebar">')
    lines.append('  <div class="sidebar-logo"><a href="/">hakaru</a></div>')

    for a in config['apps']:
        is_current = (a['id'] == app['id'])
        header_cls = 'sidebar-app-header'
        if is_current:
            header_cls += ' active'

        lines.append(f'  <div class="sidebar-app">')
        lines.append(f'    <button class="{header_cls}">')
        lines.append(f'      <img src="{a["icon"]}" alt="{a["name"]}" width="24" height="24">')
        lines.append(f'      {a["name"]}')
        lines.append(f'      <span class="arrow">&#9654;</span>')
        lines.append(f'    </button>')

        link_lang = page_lang if page_lang in a['links'] else 'en'
        links = a['links'].get(link_lang, a['links'].get('en', []))
        links_cls = 'sidebar-app-links'
        if is_current:
            links_cls += ' show'
        lines.append(f'    <div class="{links_cls}">')
        for link in links:
            link_cls = ' class="active"' if (is_current and link['href'] == active_href) else ''
            lines.append(f'      <a href="{link["href"]}"{link_cls}>{link["label"]}</a>')
        lines.append(f'    </div>')
        lines.append(f'  </div>')

    # Language switcher
    lines.append('  <div class="sidebar-lang">')
    available_langs = list(app['links'].keys())
    lang_labels = {'en': 'EN', 'ja': 'JA', 'th': 'TH', 'zh-Hant': '繁體'}
    for lang in available_langs:
        cls = ' active' if lang == page_lang else ''
        if lang == page_lang:
            lines.append(f'    <span class="sidebar-lang-btn active" data-lang="{lang}">{lang_labels.get(lang, lang.upper())}</span>')
        elif lang_switch_url:
            lines.append(f'    <a href="{lang_switch_url}" class="sidebar-lang-btn" data-lang="{lang}">{lang_labels.get(lang, lang.upper())}</a>')
        else:
            lines.append(f'    <span class="sidebar-lang-btn" data-lang="{lang}">{lang_labels.get(lang, lang.upper())}</span>')
    lines.append('  </div>')

    lines.append('</nav>')
    return '\n'.join(lines)


def transform_file(filepath, config, css_content, js_content):
    """Transform a single HTML file to two-pane layout."""
    app = detect_app(filepath, config)
    if not app:
        print(f'  SKIP (no app match): {filepath}')
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already transformed
    if 'sidebar' in html and 'content-pane' in html:
        print(f'  SKIP (already transformed): {filepath}')
        return False

    page_lang = detect_page_lang(filepath, app)
    active_href = detect_active_link(filepath, app, page_lang)
    lang_switch_url = get_lang_switch_url(filepath, app, page_lang)
    sidebar_html = build_sidebar_html(app, page_lang, active_href, lang_switch_url, config)

    # 1. Inject CSS into <style> tag
    # Find the closing </style> and inject sidebar CSS before it
    html = html.replace('</style>', '\n/* --- Sidebar Layout --- */\n' + css_content + '\n</style>', 1)

    # 2. Remove .support-nav
    html = re.sub(r'<nav class="support-nav">.*?</nav>', '', html, flags=re.DOTALL)

    # 3. Remove .back-link
    html = re.sub(r'<a[^>]*class="back-link"[^>]*>.*?</a>', '', html, flags=re.DOTALL)

    # 4. Wrap body content: sidebar + content-pane
    # Find <body...> and the first <div class="container">
    body_match = re.search(r'(<body[^>]*>)', html)
    if not body_match:
        print(f'  ERROR (no body tag): {filepath}')
        return False

    body_tag = body_match.group(1)
    body_pos = body_match.end()

    # Insert sidebar + content-pane wrapper after <body>
    new_body = body_tag + '\n' + sidebar_html + '\n<div class="content-pane">\n'
    html = html[:body_match.start()] + new_body + html[body_pos:]

    # Close content-pane before </body>
    html = html.replace('</body>', '</div>\n<script>\n' + js_content + '\n</script>\n</body>')

    # 5. Update body CSS to remove conflicting styles
    # The body already has background set; we need to keep it but add flex

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'  OK: {filepath} ({page_lang})')
    return True


def main():
    config = load_config()
    css_content = load_css()
    js_content = load_js()

    support_dirs = [
        '1Take-support',
        'GitInflow-support',
        'SonicDNACollector-support',
        'SonicDNAEngine-support',
        'simpleMIDIController-support',
        'ChatArchive-support',
    ]

    total = 0
    transformed = 0

    for support_dir in support_dirs:
        full_dir = REPO_ROOT / support_dir
        if not full_dir.exists():
            print(f'Directory not found: {full_dir}')
            continue

        print(f'\n--- {support_dir} ---')
        for html_file in sorted(full_dir.rglob('*.html')):
            total += 1
            if transform_file(html_file, config, css_content, js_content):
                transformed += 1

    print(f'\nDone: {transformed}/{total} files transformed')


if __name__ == '__main__':
    main()
```

- [ ] **Step 3: Commit**

```bash
git add scripts/transform.py
git commit -m "feat: add HTML transformation script for two-pane sidebar injection"
```

---

### Task 5: Test with a single file first

**Files:**
- Modify: `1Take-support/index.html`

- [ ] **Step 1: Back up the file**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
cp 1Take-support/index.html 1Take-support/index.html.bak
```

- [ ] **Step 2: Run transform on just this file (dry test)**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
python3 scripts/transform.py
```

Review terminal output. Verify `1Take-support/index.html` shows `OK`.

- [ ] **Step 3: Open in browser to verify**

```bash
open 1Take-support/index.html
```

Verify:
- Left sidebar appears with all 6 apps
- 1Take is expanded with sub-links
- Current page (Support) is highlighted with accent color
- Other apps are collapsed
- Language switcher shows EN/JA
- Mobile: resize to <768px, verify hamburger menu appears
- Content displays correctly in right pane

- [ ] **Step 4: Fix any issues found during visual review**

If sidebar layout is broken, adjust CSS in `scripts/sidebar-styles.css` and re-run the script after restoring from backup:

```bash
cp 1Take-support/index.html.bak 1Take-support/index.html
python3 scripts/transform.py
```

- [ ] **Step 5: Verify language auto-detection**

Open browser DevTools, go to Application > Local Storage, clear `hakaru-lang`. Reload with browser set to Japanese. Verify it redirects to `index-ja.html`.

- [ ] **Step 6: Remove backup, commit**

```bash
rm 1Take-support/index.html.bak
git add -A
git commit -m "feat: verify two-pane layout on 1Take support page"
```

---

### Task 6: Run full transformation on all 144 files

**Files:**
- Modify: All 144 `*-support/**/*.html` files

- [ ] **Step 1: Run the transform script**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
python3 scripts/transform.py
```

Expected output: `Done: 144/144 files transformed`

- [ ] **Step 2: Spot-check pages across different apps**

Open and verify each:
- `1Take-support/blog/en/2026-03-29-1take-v14-released/index.html` (blog post EN)
- `1Take-support/blog/ja/2026-03-29-1take-v14-released/index.html` (blog post JA)
- `GitInflow-support/index.html` (different app)
- `ChatArchive-support/index.html` (JA root app)
- `ChatArchive-support/en/index.html` (ChatArchive EN)
- `simpleMIDIController-support/manual/en/index.html` (manual page)

For each, verify:
- Sidebar shows with correct active app expanded
- Correct sub-link highlighted
- Language switcher works
- Content displays properly

- [ ] **Step 3: Commit all transformed files**

```bash
git add -A
git commit -m "feat: apply two-pane sidebar layout to all 144 support pages"
```

---

### Task 7: Deploy to Netlify and verify

**Files:**
- No file changes

- [ ] **Step 1: Deploy to Netlify**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
npx netlify-cli deploy --prod --dir=.
```

- [ ] **Step 2: Verify live site**

Check these URLs:
- `https://hakaru.net/1Take-support/`
- `https://hakaru.net/1Take-support/blog/en/2026-03-29-1take-v14-released/`
- `https://hakaru.net/GitInflow-support/`
- `https://hakaru.net/ChatArchive-support/`

Verify sidebar, navigation, language switching, and mobile responsiveness all work.

- [ ] **Step 3: Push to GitHub**

```bash
git push origin main
```
