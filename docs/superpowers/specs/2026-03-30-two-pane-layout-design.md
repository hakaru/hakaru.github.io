# Two-Pane Layout with Auto Language Detection

**Date:** 2026-03-30
**Status:** Approved

## Scope

All app support pages and their subpages (blog, manual, changelog, privacy). The root portfolio page (hakaru.net/) is NOT modified.

**Affected directories:**
- `1Take-support/` (36 HTML files)
- `GitInflow-support/` (10 HTML files)
- `SonicDNACollector-support/` (14 HTML files)
- `SonicDNAEngine-support/` (7 HTML files)
- `simpleMIDIController-support/` (20 HTML files)
- `ChatArchive-support/` (28 HTML files, 4 languages: ja/en/th/zh-Hant)

**Total:** ~115 HTML files

## Layout

Two-pane layout: fixed left sidebar (250px) + scrollable right content area.

### Left Sidebar

Top-to-bottom:
1. **hakaru logo** — links to hakaru.net/
2. **App accordion menu** — all apps listed, current app expanded with sub-links (Support, Manual, Blog, Changelog, Privacy), others collapsed
3. **Language switcher** — EN/JA toggle at bottom (ChatArchive also has TH/zh-Hant)

### Right Content Pane

The existing page content (hero, nav bar, content, footer) moves into this pane. The inline `support-nav` bar is removed since sidebar handles navigation.

### App Menu Items

| App | Sub-links |
|-----|-----------|
| 1Take | Support, Manual, Blog, Changelog, Privacy |
| GitInflow | Support, Manual, Blog, Changelog, Privacy |
| SonicDNA Collector | Support, Manual, Blog, Changelog, Privacy |
| SonicDNA Engine | Support, Blog, Changelog, Privacy |
| simpleMIDIController | Support, Manual, Blog, Privacy |
| ChatArchive | Support, Blog, Privacy, Terms |

## Language Auto-Detection

1. On page load, check `localStorage` for saved preference
2. If no saved preference, check `navigator.language`
3. If starts with `ja` → Japanese, else → English
4. Redirect to the appropriate language version of the current page
5. Save user's manual language switch to `localStorage`

### URL Mapping

Each page has a language counterpart:
- `index.html` ↔ `index-ja.html`
- `blog/en/` ↔ `blog/ja/`
- `manual/en/` ↔ `manual/ja/`
- `privacy.html` ↔ `privacy-ja.html`
- `changelog.html` ↔ `changelog-ja.html`
- Blog posts: `blog/en/{slug}/` ↔ `blog/ja/{slug}/`

ChatArchive has additional mappings for `th/` and `zh-Hant/`.

## Mobile Responsive

- Below 768px: sidebar collapses into hamburger menu
- Menu button fixed at top-left
- Tap to open/close sidebar as overlay
- Content area takes full width

## Visual Design

- Theme: existing dark gradient (`#1a1a2e → #16213e → #0f3460`)
- Accent: `#e94560`
- Sidebar background: slightly darker or semi-transparent with backdrop blur
- Active menu item highlighted with accent color
- Smooth accordion open/close transitions

## Implementation Approach

- No build tools — all HTML remains self-contained static files
- Sidebar HTML + CSS + JS inlined in each page
- A shared sidebar template is defined once and replicated across all files
- Existing content sections move into a `.content-pane` wrapper
- The existing `.support-nav` bar is removed (replaced by sidebar navigation)

## File Changes

Each of the ~115 HTML files needs:
1. Add sidebar HTML markup
2. Add sidebar CSS (inline `<style>`)
3. Add sidebar JS (language detection, accordion, mobile toggle)
4. Wrap existing content in `.content-pane` div
5. Remove existing `.support-nav` section
6. Update `<body>` to use flexbox layout
