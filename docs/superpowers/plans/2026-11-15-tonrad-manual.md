# Tonrad Manual Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a source-verified Tonrad user manual in the site's 11 languages.

**Architecture:** Static HTML under `Tonrad-support/manual/<lang>/index.html`, matching existing manual URLs. Shared manual CSS and the existing sidebar generator provide navigation. Keep support/privacy in their existing two languages, with explicit English fallback links from other locales and section-specific language switching.

**Tech Stack:** HTML/CSS, existing Python sidebar generators, browser verification.

**Spec:** User request: 「Tonradのマニュアルを作り１１言語対応して」. Covers first sound, all shipping controls, USB MIDI in 0.2.0, saved settings and troubleshooting. The App Store currently distributes 0.1.0; distinguish 0.2.0 features without claiming its release.

## Global Constraints

- Locales: en, ja, de, es, fr, it, ko, nl, pt-BR, sv, zh-Hant.
- Use the Standard edition only; no user instructions for unavailable PRESET/TUNE.
- Keep literal on-screen labels, version numbers, MIDI values and anchor IDs consistent across translations.
- Generated sidebar edits come from `scripts/sidebar-config.json`; regenerate all existing sidebars.
- Use clean internal URLs. No new analytics or dependencies.
- Execute Python through `uv run python3` from the marketing workspace.

## Review Focus

- Version mismatch: MIDI, background audio and rotary controls need version qualifiers.
- Silent organ: explain drawbars, expression, output volume and connected audio route.
- Partial localization: language switching on support/privacy must never invent missing pages.
- Long translations and tables: mobile width, wrapping and keyboard navigation.
- Generated changes: unrelated page bodies must remain byte-for-byte unchanged.

### Task 1: Source and master copy

- [x] Audit current Standard UI and 0.1.0 history; record source evidence in the marketing worklog.
- [x] Author Japanese and English manuals with matching sections and concrete steps.

### Task 2: Translation and integration

- [x] Translate the approved factual master into nine additional languages in disjoint files.
- [x] Create manual HTML/CSS, canonical/hreflang tags, TOC and language links.
- [x] Add localized manual links to the homepage, support pages and sidebar config.
- [x] In both sidebar generators, honor optional `sectionLanguages` so support/privacy retain EN/JA while manuals offer all 11 locales.
- [x] Regenerate sidebars and add manual URLs to the sitemap.

### Task 3: Verify and publish

- [x] Check all section IDs, language links, local assets, active navigation, sitemap and translated section parity.
- [x] Verify generated changes outside Tonrad only touch sidebar blocks.
- [x] Review source facts and translations; inspect desktop/mobile display and language switching in the browser.
- [x] Commit/push to main, verify all 11 public manual URLs, and record the change in the worklog and memdream.
