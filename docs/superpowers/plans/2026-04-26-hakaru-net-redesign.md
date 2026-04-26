# hakaru.net Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace 800+ hand-maintained HTML files with a single Astro project (Warm Editorial Light visual direction, 11-language i18n) and ship via parallel construction on a `redesign` branch with single-PR cutover to `main`.

**Architecture:** Astro SSG under `apps/web/`. Content lives in typed Astro Content Collections (Markdown). Auto-converted from existing HTML by a Claude-powered migration script. Cloudflare Pages serves the static build with `_redirects` providing full 301 coverage from legacy URLs. The current site stays live on `main` while building proceeds on `redesign`; cutover is a single merge.

**Tech Stack:** Astro (latest), Node 20+, Astro `i18n`, Astro Content Collections (`zod` schemas), `@astrojs/sitemap`, Anthropic SDK (`@anthropic-ai/sdk`) for the migration script (Python invokes it), Cloudflare Pages.

**Reference spec:** `docs/superpowers/specs/2026-04-26-hakaru-net-redesign-design.md`

---

## File Structure

| File / Directory | Responsibility |
|---|---|
| `apps/web/package.json` | Astro project deps & scripts |
| `apps/web/astro.config.mjs` | Astro + i18n + integrations |
| `apps/web/src/content.config.ts` | Zod schemas for `apps`, `support`, `blog`, `manual` collections |
| `apps/web/src/styles/tokens.css` | Design tokens (colors, typography variables) |
| `apps/web/src/styles/global.css` | Reset + base typography + element defaults |
| `apps/web/src/layouts/RootLayout.astro` | `<html>` shell, head meta, hreflang, gtag, sidebar slot |
| `apps/web/src/layouts/AppPageLayout.astro` | App support/privacy page chrome (hero + content slot) |
| `apps/web/src/layouts/BlogLayout.astro` | Blog post page chrome |
| `apps/web/src/components/Sidebar.astro` | App nav + lang switcher (auto from collections) |
| `apps/web/src/components/LangSwitcher.astro` | 11-lang button row |
| `apps/web/src/components/AppCard.astro` | Top page app card |
| `apps/web/src/components/FeatureCard.astro` | M2DX-style feature grid item |
| `apps/web/src/components/StatusCard.astro` | "Current Status" disclosure card |
| `apps/web/src/components/TestFlightCTA.astro` | TestFlight button |
| `apps/web/src/components/AppStoreCTA.astro` | App Store / GitHub button |
| `apps/web/src/components/PostList.astro` | Blog index list |
| `apps/web/src/components/PostMeta.astro` | Post metadata (date, lang) |
| `apps/web/src/content/apps/<app>.json` | App metadata (icon, badge, accent, links, per-lang category/desc) |
| `apps/web/src/content/support/<app>/<section>.<lang>.md` | Support / privacy / terms / changelog Markdown |
| `apps/web/src/content/blog/<app>/<slug>.<lang>.md` | Blog posts |
| `apps/web/src/content/manual/<app>/<slug>.<lang>.md` | Manual pages |
| `apps/web/src/pages/index.astro` | Root redirect to `/[detected-lang]/` |
| `apps/web/src/pages/[lang]/index.astro` | Top page (app cards) |
| `apps/web/src/pages/[lang]/[app]/index.astro` | App support page |
| `apps/web/src/pages/[lang]/[app]/privacy.astro` | App privacy page |
| `apps/web/src/pages/[lang]/[app]/blog/index.astro` | Blog index |
| `apps/web/src/pages/[lang]/[app]/blog/[...slug].astro` | Blog post |
| `apps/web/src/pages/[lang]/[app]/manual/[...slug].astro` | Manual page |
| `apps/web/public/_redirects` | Cloudflare Pages 301 rules |
| `apps/web/public/CNAME` | hakaru.net |
| `apps/web/public/robots.txt` | Robots policy |
| `apps/web/public/assets/**` | Site-wide images (icons, logos) |
| `apps/web/public/apps/<app>/**` | Per-app icons consolidated |
| `scripts/migrate-to-md.py` | HTML → Markdown converter (calls Anthropic API) |
| `scripts/build-redirects.py` | Generates legacy → new URL 301 entries |
| `scripts/check-migration.py` | Word-count / link-count diff old vs new |

---

## Pre-flight: Branch & Environment Setup

### Task 0: Create the `redesign` branch and verify Node/npm

**Files:** none

- [ ] **Step 1: Confirm current branch is clean**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git status
```
Expected: only the pre-existing unrelated modifications (`scripts/sidebar-script.js`, `scripts/transform.py`, etc.) shown earlier. No new tracked changes.

- [ ] **Step 2: Create and switch to `redesign` branch**

```bash
git checkout -b redesign
git push -u origin redesign
```
Expected: branch created and pushed. Cloudflare Pages preview build will trigger (will fail until P0 lands — that's OK).

- [ ] **Step 3: Verify Node.js 20+ is available**

```bash
node --version
```
Expected: `v20.x.x` or higher. If lower, install via fnm/nvm.

---

## Phase 0: Astro Scaffold + Design System + Hand-Built M2DX Page

### Task 1: Initialize Astro project under `apps/web/`

**Files:**
- Create: `apps/web/package.json`
- Create: `apps/web/astro.config.mjs`
- Create: `apps/web/tsconfig.json`
- Create: `apps/web/src/env.d.ts`

- [ ] **Step 1: Create Astro project (non-interactive)**

```bash
mkdir -p apps && cd apps
npm create astro@latest web -- --template minimal --typescript strict --no-install --no-git --skip-houston
cd ..
```
Expected: `apps/web/` populated with starter files.

- [ ] **Step 2: Install dependencies**

```bash
cd apps/web
npm install
npm install @astrojs/sitemap
cd ../..
```
Expected: `apps/web/node_modules/` exists, no errors.

- [ ] **Step 3: Replace `apps/web/astro.config.mjs` with i18n + sitemap config**

```js
// apps/web/astro.config.mjs
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://hakaru.net',
  trailingSlash: 'always',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ja', 'de', 'es', 'fr', 'it', 'ko', 'nl', 'pt-BR', 'sv', 'zh-Hant'],
    routing: { prefixDefaultLocale: true, redirectToDefaultLocale: false },
  },
  integrations: [sitemap()],
});
```

- [ ] **Step 4: Verify build succeeds with empty pages dir**

```bash
cd apps/web && npm run build && cd ../..
```
Expected: build succeeds (may produce 0 pages — fine for now).

- [ ] **Step 5: Commit**

```bash
git add apps/web/ apps/.gitignore 2>/dev/null
git commit -m "feat(redesign): scaffold Astro project with i18n config"
```

### Task 2: Add design tokens and global styles

**Files:**
- Create: `apps/web/src/styles/tokens.css`
- Create: `apps/web/src/styles/global.css`

- [ ] **Step 1: Create `apps/web/src/styles/tokens.css`**

```css
:root {
  --bg: #faf9f7;
  --bg-subtle: #f5f4f1;
  --bg-card: #ffffff;
  --border: #e7e5e4;
  --border-strong: #d6d3d1;
  --text: #18181b;
  --text-muted: #57534e;
  --text-subtle: #78716c;
  --accent: #18181b;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 12px;
  --shadow-sm: 0 1px 2px rgba(24, 24, 27, 0.04);
  --shadow-md: 0 4px 12px rgba(24, 24, 27, 0.06);
  --font-sans: -apple-system, BlinkMacSystemFont, "Inter", "Hiragino Sans", "Noto Sans JP", system-ui, sans-serif;
  --font-mono: "SF Mono", "Fira Code", ui-monospace, monospace;
  --container-max: 720px;
  --sidebar-width: 220px;
}
```

- [ ] **Step 2: Create `apps/web/src/styles/global.css`**

```css
@import './tokens.css';

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; }
body {
  font-family: var(--font-sans);
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
h1, h2, h3, h4 { letter-spacing: -0.025em; font-weight: 700; line-height: 1.15; }
h1 { font-size: 2.4em; }
h2 { font-size: 1.5em; }
h3 { font-size: 1.15em; }
a { color: var(--text); text-decoration: underline; text-decoration-color: var(--border-strong); text-underline-offset: 3px; }
a:hover { text-decoration-color: var(--text); }
hr { border: none; border-top: 1px solid var(--border); margin: 32px 0; }
code { font-family: var(--font-mono); font-size: 0.92em; background: var(--bg-subtle); padding: 2px 6px; border-radius: 4px; }
pre { font-family: var(--font-mono); background: var(--bg-subtle); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 16px 20px; overflow-x: auto; margin: 16px 0; }
pre code { background: transparent; padding: 0; }
table { width: 100%; border-collapse: collapse; margin: 16px 0; }
th, td { padding: 10px 14px; text-align: left; border-bottom: 1px solid var(--border); }
th { font-weight: 600; }
```

- [ ] **Step 3: Commit**

```bash
git add apps/web/src/styles/
git commit -m "feat(redesign): add design tokens and global styles"
```

### Task 3: Define Content Collection schemas

**Files:**
- Create: `apps/web/src/content.config.ts`

- [ ] **Step 1: Write `apps/web/src/content.config.ts`**

```ts
import { defineCollection, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

const LOCALES = ['en','ja','de','es','fr','it','ko','nl','pt-BR','sv','zh-Hant'] as const;
const Locale = z.enum(LOCALES);

const apps = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/apps' }),
  schema: z.object({
    id: z.string(),
    name: z.string(),
    icon: z.string(),
    badge: z.enum(['NEW', 'COMING', 'TESTFLIGHT']).optional(),
    accentColor: z.string(),
    order: z.number().default(100),
    sections: z.array(z.enum(['support','privacy','terms','changelog','blog','manual'])).default(['support','privacy']),
    category: z.record(Locale, z.string()),
    description: z.record(Locale, z.string()),
    links: z.object({
      appStore: z.string().url().optional(),
      testFlight: z.string().url().optional(),
      github: z.string().url().optional(),
    }).default({}),
  }),
});

const support = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/support' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    lang: Locale,
    app: z.string(),
    section: z.enum(['support','privacy','terms','changelog']),
    date: z.coerce.date().optional(),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    lang: Locale,
    app: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
  }),
});

const manual = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/manual' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    lang: Locale,
    app: z.string(),
    order: z.number().default(100),
  }),
});

export const collections = { apps, support, blog, manual };
```

- [ ] **Step 2: Verify schemas type-check**

```bash
cd apps/web && npx astro sync && cd ../..
```
Expected: `astro sync` completes without TS errors. Generates `.astro/` types.

- [ ] **Step 3: Commit**

```bash
git add apps/web/src/content.config.ts
git commit -m "feat(redesign): define content collection schemas (apps/support/blog/manual)"
```

### Task 4: Create RootLayout

**Files:**
- Create: `apps/web/src/layouts/RootLayout.astro`

- [ ] **Step 1: Write `apps/web/src/layouts/RootLayout.astro`**

```astro
---
import '../styles/global.css';
import Sidebar from '../components/Sidebar.astro';

interface Props {
  title: string;
  description?: string;
  lang: string;
  currentApp?: string;
  currentSection?: 'support' | 'privacy' | 'blog' | 'manual' | 'home';
  pathWithoutLang: string; // e.g. "/m2dx/" — for lang switcher
}

const { title, description, lang, currentApp, currentSection = 'home', pathWithoutLang } = Astro.props;
const canonical = `https://hakaru.net/${lang}${pathWithoutLang}`;

const LOCALES = ['en','ja','de','es','fr','it','ko','nl','pt-BR','sv','zh-Hant'];
---
<!DOCTYPE html>
<html lang={lang}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{description && <meta name="description" content={description}>}
<meta property="og:title" content={title}>
{description && <meta property="og:description" content={description}>}
<meta property="og:type" content="website">
<meta property="og:url" content={canonical}>
<link rel="canonical" href={canonical}>
{LOCALES.map((l) => (
  <link rel="alternate" hreflang={l} href={`https://hakaru.net/${l}${pathWithoutLang}`}>
))}
<link rel="alternate" hreflang="x-default" href={`https://hakaru.net/en${pathWithoutLang}`}>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-N0830V28FD"></script>
<script is:inline>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-N0830V28FD');
</script>
</head>
<body>
  <button class="sidebar-toggle" aria-label="Menu">&#9776;</button>
  <div class="sidebar-overlay"></div>
  <Sidebar lang={lang} currentApp={currentApp} currentSection={currentSection} pathWithoutLang={pathWithoutLang} />
  <main class="content-pane">
    <slot />
  </main>
  <script>
    const toggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    toggle?.addEventListener('click', () => {
      sidebar?.classList.toggle('open');
      overlay?.classList.toggle('show');
    });
    overlay?.addEventListener('click', () => {
      sidebar?.classList.remove('open');
      overlay?.classList.remove('show');
    });
  </script>
  <style is:global>
    body { display: flex; min-height: 100vh; }
    .content-pane { flex: 1; margin-left: var(--sidebar-width); min-height: 100vh; }
    .content-pane .container { max-width: var(--container-max); margin: 0 auto; padding: 56px 64px; }
    .sidebar-toggle { display: none; position: fixed; top: 15px; left: 15px; z-index: 200; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; color: var(--text); font-size: 1.3em; padding: 8px 12px; cursor: pointer; }
    .sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(24,24,27,0.4); z-index: 90; }
    @media (max-width: 768px) {
      .content-pane { margin-left: 0; padding-top: 60px; }
      .content-pane .container { padding: 40px 24px; }
      .sidebar-toggle { display: block; }
      .sidebar-overlay.show { display: block; }
    }
  </style>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add apps/web/src/layouts/RootLayout.astro
git commit -m "feat(redesign): RootLayout with hreflang, gtag, sidebar slot, mobile drawer"
```

### Task 5: Create Sidebar component

**Files:**
- Create: `apps/web/src/components/Sidebar.astro`

- [ ] **Step 1: Write `apps/web/src/components/Sidebar.astro`**

```astro
---
import { getCollection } from 'astro:content';
import LangSwitcher from './LangSwitcher.astro';

interface Props {
  lang: string;
  currentApp?: string;
  currentSection?: string;
  pathWithoutLang: string;
}

const { lang, currentApp, currentSection, pathWithoutLang } = Astro.props;
const apps = (await getCollection('apps')).sort((a, b) => a.data.order - b.data.order);

function sectionLabel(section: string, lang: string): string {
  const labels: Record<string, Record<string, string>> = {
    support: { en: 'Support', ja: 'サポート', de: 'Support', es: 'Soporte', fr: 'Support', it: 'Supporto', ko: '지원', nl: 'Support', 'pt-BR': 'Suporte', sv: 'Support', 'zh-Hant': '支援' },
    privacy: { en: 'Privacy', ja: 'プライバシー', de: 'Datenschutz', es: 'Privacidad', fr: 'Confidentialité', it: 'Privacy', ko: '개인정보', nl: 'Privacy', 'pt-BR': 'Privacidade', sv: 'Integritet', 'zh-Hant': '隱私' },
    blog: { en: 'Blog', ja: 'ブログ', de: 'Blog', es: 'Blog', fr: 'Blog', it: 'Blog', ko: '블로그', nl: 'Blog', 'pt-BR': 'Blog', sv: 'Blogg', 'zh-Hant': '部落格' },
    manual: { en: 'Manual', ja: 'マニュアル', de: 'Handbuch', es: 'Manual', fr: 'Manuel', it: 'Manuale', ko: '매뉴얼', nl: 'Handleiding', 'pt-BR': 'Manual', sv: 'Manual', 'zh-Hant': '手冊' },
    changelog: { en: 'Changelog', ja: '更新履歴', de: 'Änderungen', es: 'Cambios', fr: 'Modifications', it: 'Modifiche', ko: '변경 기록', nl: 'Wijzigingen', 'pt-BR': 'Alterações', sv: 'Ändringar', 'zh-Hant': '變更記錄' },
  };
  return labels[section]?.[lang] ?? section;
}
---
<nav class="sidebar">
  <div class="sidebar-logo"><a href={`/${lang}/`}>hakaru</a></div>
  {apps.map((app) => {
    const isCurrent = currentApp === app.data.id;
    return (
      <div class={`sidebar-app ${isCurrent ? 'expanded' : ''}`} style={`--app-accent: ${app.data.accentColor}`}>
        <a class={`sidebar-app-header ${isCurrent ? 'active' : ''}`} href={`/${lang}/${app.data.id}/`}>
          <img src={app.data.icon} alt={app.data.name} width="24" height="24">
          <span>{app.data.name}</span>
          <span class="arrow">&#9654;</span>
        </a>
        {isCurrent && (
          <div class="sidebar-app-links">
            {app.data.sections.map((section) => (
              <a
                href={`/${lang}/${app.data.id}/${section === 'support' ? '' : section + '/'}`}
                class={currentSection === section ? 'active' : ''}
              >
                {sectionLabel(section, lang)}
              </a>
            ))}
          </div>
        )}
      </div>
    );
  })}
  <LangSwitcher currentLang={lang} pathWithoutLang={pathWithoutLang} />
</nav>

<style>
  .sidebar {
    width: var(--sidebar-width);
    flex-shrink: 0;
    background: var(--bg-subtle);
    border-right: 1px solid var(--border);
    padding: 28px 16px;
    position: fixed;
    top: 0; left: 0; bottom: 0;
    overflow-y: auto;
    z-index: 100;
  }
  .sidebar-logo { padding: 0 8px; margin-bottom: 28px; }
  .sidebar-logo a { color: var(--text); text-decoration: none; font-size: 1.2em; font-weight: 700; letter-spacing: -0.025em; }
  .sidebar-logo a:hover { color: var(--text-muted); }
  .sidebar-app { margin-bottom: 2px; }
  .sidebar-app-header {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 8px;
    color: var(--text-muted);
    font-size: 0.9em; font-weight: 500;
    text-decoration: none;
    border-radius: var(--radius-sm);
  }
  .sidebar-app-header:hover { color: var(--text); background: rgba(24,24,27,0.04); }
  .sidebar-app-header.active {
    color: var(--text); font-weight: 600; background: var(--bg-card);
    border-left: 3px solid var(--app-accent, var(--text)); padding-left: 5px;
  }
  .sidebar-app-header img { width: 24px; height: 24px; border-radius: 6px; }
  .sidebar-app-header .arrow { margin-left: auto; font-size: 0.7em; opacity: 0.5; transition: transform 0.2s; }
  .sidebar-app.expanded .arrow { transform: rotate(90deg); }
  .sidebar-app-links { padding: 4px 0 8px 12px; }
  .sidebar-app-links a {
    display: block; padding: 4px 8px;
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.85em;
    border-radius: var(--radius-sm);
  }
  .sidebar-app-links a:hover { color: var(--text); }
  .sidebar-app-links a.active { color: var(--text); font-weight: 500; }
  @media (max-width: 768px) {
    .sidebar { transform: translateX(-100%); transition: transform 0.3s; }
    .sidebar.open { transform: translateX(0); }
  }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add apps/web/src/components/Sidebar.astro
git commit -m "feat(redesign): Sidebar component (auto from apps collection)"
```

### Task 6: Create LangSwitcher component

**Files:**
- Create: `apps/web/src/components/LangSwitcher.astro`

- [ ] **Step 1: Write `apps/web/src/components/LangSwitcher.astro`**

```astro
---
interface Props {
  currentLang: string;
  pathWithoutLang: string;
}
const { currentLang, pathWithoutLang } = Astro.props;
const LANGS = [
  { code: 'en', label: 'EN' },
  { code: 'ja', label: 'JA' },
  { code: 'de', label: 'DE' },
  { code: 'es', label: 'ES' },
  { code: 'fr', label: 'FR' },
  { code: 'it', label: 'IT' },
  { code: 'ko', label: 'KO' },
  { code: 'nl', label: 'NL' },
  { code: 'pt-BR', label: 'PT-BR' },
  { code: 'sv', label: 'SV' },
  { code: 'zh-Hant', label: '繁體' },
];
---
<div class="lang-switcher">
  <div class="lang-label">Language</div>
  <div class="lang-row">
    {LANGS.map((l) => (
      l.code === currentLang
        ? <span class="lang-btn active" data-lang={l.code}>{l.label}</span>
        : <a class="lang-btn" data-lang={l.code} href={`/${l.code}${pathWithoutLang}`}>{l.label}</a>
    ))}
  </div>
</div>
<script>
  document.querySelectorAll('.lang-btn[data-lang]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const lang = (btn as HTMLElement).dataset.lang;
      if (lang) localStorage.setItem('hakaru-lang', lang);
    });
  });
</script>
<style>
  .lang-switcher { margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border); }
  .lang-label { font-size: 0.7em; color: var(--text-subtle); text-transform: uppercase; letter-spacing: 0.08em; padding: 0 8px; margin-bottom: 8px; font-weight: 600; }
  .lang-row { display: flex; flex-wrap: wrap; gap: 2px; padding: 0 6px; }
  .lang-btn { font-size: 0.72em; padding: 2px 6px; color: var(--text-subtle); text-decoration: none; border-radius: 3px; cursor: pointer; }
  .lang-btn:hover { color: var(--text); }
  .lang-btn.active { color: var(--text); font-weight: 600; background: var(--bg-card); }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add apps/web/src/components/LangSwitcher.astro
git commit -m "feat(redesign): LangSwitcher component (11 locales)"
```

### Task 7: Create card components (AppCard, FeatureCard, StatusCard, CTAs)

**Files:**
- Create: `apps/web/src/components/AppCard.astro`
- Create: `apps/web/src/components/FeatureCard.astro`
- Create: `apps/web/src/components/StatusCard.astro`
- Create: `apps/web/src/components/TestFlightCTA.astro`
- Create: `apps/web/src/components/AppStoreCTA.astro`

- [ ] **Step 1: Write `apps/web/src/components/AppCard.astro`**

```astro
---
interface Props {
  app: {
    id: string;
    name: string;
    icon: string;
    badge?: 'NEW' | 'COMING' | 'TESTFLIGHT';
    accentColor: string;
    category: string;
    description: string;
    links: { appStore?: string; testFlight?: string; github?: string };
  };
  lang: string;
  supportLabel: string;
}
const { app, lang, supportLabel } = Astro.props;
const primaryHref = app.links.appStore ?? app.links.testFlight ?? app.links.github;
const primaryLabel = app.links.appStore ? 'App Store' : app.links.testFlight ? 'TestFlight' : 'GitHub';
---
<article class="app-card" style={`--app-accent: ${app.accentColor}`}>
  <header class="app-card-header">
    <img src={app.icon} alt={app.name} class="app-card-icon" width="48" height="48">
    <div class="app-card-headings">
      <h2>
        {app.name}
        {app.badge && <span class={`badge badge-${app.badge.toLowerCase()}`}>{app.badge}</span>}
      </h2>
      <p class="app-card-category">{app.category}</p>
    </div>
  </header>
  <p class="app-card-desc">{app.description}</p>
  <div class="app-card-actions">
    {primaryHref && <a class="cta cta-primary" href={primaryHref}>{primaryLabel}</a>}
    <a class="cta cta-secondary" href={`/${lang}/${app.id}/`}>{supportLabel}</a>
  </div>
</article>

<style>
  .app-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s, transform 0.2s;
  }
  .app-card:hover { box-shadow: var(--shadow-md); transform: translateY(-1px); }
  .app-card-header { display: flex; gap: 14px; align-items: center; margin-bottom: 14px; }
  .app-card-icon { border-radius: var(--radius-md); }
  .app-card-headings h2 { font-size: 1.15em; margin: 0; display: flex; align-items: center; gap: 10px; }
  .app-card-category { font-size: 0.8em; color: var(--text-subtle); margin: 2px 0 0; }
  .app-card-desc { font-size: 0.95em; color: var(--text-muted); line-height: 1.6; margin-bottom: 18px; }
  .app-card-actions { display: flex; gap: 8px; }
  .cta { padding: 8px 14px; font-size: 0.85em; font-weight: 600; border-radius: var(--radius-sm); text-decoration: none; }
  .cta-primary { background: var(--app-accent, var(--text)); color: white; }
  .cta-secondary { background: var(--bg-card); color: var(--text); border: 1px solid var(--border-strong); }
  .badge { font-size: 0.6em; font-weight: 700; padding: 3px 8px; border-radius: 999px; letter-spacing: 0.04em; }
  .badge-new { background: #ecfdf5; color: #065f46; }
  .badge-coming { background: var(--bg-subtle); color: var(--text-muted); }
  .badge-testflight { background: var(--app-accent, var(--text)); color: white; }
</style>
```

- [ ] **Step 2: Write `apps/web/src/components/FeatureCard.astro`**

```astro
---
interface Props {
  label: string;
  title: string;
  description: string;
  accentColor?: string;
}
const { label, title, description, accentColor } = Astro.props;
---
<div class="feature-card" style={accentColor ? `--app-accent: ${accentColor}` : ''}>
  <div class="feature-label">{label}</div>
  <h4>{title}</h4>
  <p>{description}</p>
</div>

<style>
  .feature-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px;
  }
  .feature-label {
    font-size: 0.7em;
    color: var(--app-accent, var(--text-muted));
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-bottom: 6px;
  }
  .feature-card h4 { font-size: 1em; margin: 0 0 6px; }
  .feature-card p { font-size: 0.9em; color: var(--text-muted); line-height: 1.5; margin: 0; }
</style>
```

- [ ] **Step 3: Write `apps/web/src/components/StatusCard.astro`**

```astro
---
interface Props {
  label: string;
  title: string;
  accentColor?: string;
}
const { label, title, accentColor } = Astro.props;
---
<section class="status-card" style={accentColor ? `--app-accent: ${accentColor}` : ''}>
  <div class="status-card-meta">
    <span class="status-dot" />
    <h3>{label}</h3>
  </div>
  <h2>{title}</h2>
  <div class="status-card-body"><slot /></div>
</section>

<style>
  .status-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 28px;
    margin: 32px 0;
  }
  .status-card-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 14px; }
  .status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--app-accent, var(--text)); }
  .status-card-meta h3 { font-size: 0.85em; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; margin: 0; }
  .status-card h2 { font-size: 1.4em; margin: 0 0 12px; }
  .status-card-body :global(p) { color: var(--text-muted); line-height: 1.7; font-size: 0.95em; }
  .status-card-body :global(a) { color: var(--text); text-decoration-color: var(--app-accent, var(--text)); }
</style>
```

- [ ] **Step 4: Write `apps/web/src/components/TestFlightCTA.astro`**

```astro
---
interface Props { href: string; label: string; accentColor?: string; }
const { href, label, accentColor } = Astro.props;
---
<a class="testflight-cta" href={href} style={accentColor ? `background: ${accentColor}` : ''}>
  <span>{label}</span>
  <span class="arrow">→</span>
</a>

<style>
  .testflight-cta {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--text);
    color: white;
    font-weight: 600; font-size: 0.95em;
    padding: 10px 18px;
    border-radius: var(--radius-sm);
    text-decoration: none;
  }
  .testflight-cta:hover .arrow { transform: translateX(2px); }
  .arrow { transition: transform 0.15s; }
</style>
```

- [ ] **Step 5: Write `apps/web/src/components/AppStoreCTA.astro`**

```astro
---
interface Props { href: string; label: string; }
const { href, label } = Astro.props;
---
<a class="appstore-cta" href={href}>
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
  </svg>
  <span>{label}</span>
</a>

<style>
  .appstore-cta {
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--bg-card);
    color: var(--text);
    font-weight: 500; font-size: 0.9em;
    padding: 10px 16px;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    text-decoration: none;
  }
  .appstore-cta:hover { border-color: var(--text); }
</style>
```

- [ ] **Step 6: Commit**

```bash
git add apps/web/src/components/AppCard.astro apps/web/src/components/FeatureCard.astro apps/web/src/components/StatusCard.astro apps/web/src/components/TestFlightCTA.astro apps/web/src/components/AppStoreCTA.astro
git commit -m "feat(redesign): AppCard, FeatureCard, StatusCard, TestFlight/AppStore CTAs"
```

### Task 8: Create AppPageLayout

**Files:**
- Create: `apps/web/src/layouts/AppPageLayout.astro`

- [ ] **Step 1: Write `apps/web/src/layouts/AppPageLayout.astro`**

```astro
---
import RootLayout from './RootLayout.astro';

interface Props {
  title: string;
  description?: string;
  lang: string;
  appId: string;
  appName: string;
  appAccent: string;
  appBadgeLabel?: string;
  pageKind: 'support' | 'privacy' | 'blog' | 'manual';
  tagline?: string;
  pathWithoutLang: string;
}
const { title, description, lang, appId, appName, appAccent, appBadgeLabel, pageKind, tagline, pathWithoutLang } = Astro.props;
---
<RootLayout
  title={title}
  description={description}
  lang={lang}
  currentApp={appId}
  currentSection={pageKind}
  pathWithoutLang={pathWithoutLang}
>
  <div class="container">
    <header class="page-hero">
      <div class="page-eyebrow" style={`color: ${appAccent}`}>
        {appName}
        {appBadgeLabel && <span> · {appBadgeLabel}</span>}
      </div>
      <h1>{title}</h1>
      {tagline && <p class="page-tagline">{tagline}</p>}
      <slot name="hero-actions" />
    </header>
    <slot />
  </div>
  <style>
    .page-hero { margin-bottom: 40px; }
    .page-eyebrow { font-size: 0.75em; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 600; margin-bottom: 12px; }
    .page-hero h1 { margin-bottom: 12px; }
    .page-tagline { font-size: 1.05em; color: var(--text-muted); line-height: 1.6; margin-bottom: 24px; }
  </style>
</RootLayout>
```

- [ ] **Step 2: Commit**

```bash
git add apps/web/src/layouts/AppPageLayout.astro
git commit -m "feat(redesign): AppPageLayout with hero/eyebrow/tagline and sidebar wiring"
```

### Task 9: Author M2DX app metadata + hand-built support content

**Files:**
- Create: `apps/web/src/content/apps/m2dx.json`
- Create: `apps/web/src/content/support/m2dx/index.ja.md`
- Create: `apps/web/src/content/support/m2dx/index.en.md`
- Create: `apps/web/public/assets/midi2kit-icon.svg` (copy)

- [ ] **Step 1: Write `apps/web/src/content/apps/m2dx.json`**

```json
{
  "id": "m2dx",
  "name": "M2DX",
  "icon": "/assets/midi2kit-icon.svg",
  "badge": "TESTFLIGHT",
  "accentColor": "#e94560",
  "order": 70,
  "sections": ["support", "privacy"],
  "category": {
    "en": "Music · Synthesizer",
    "ja": "音楽 · シンセサイザー",
    "de": "Musik · Synthesizer",
    "es": "Música · Sintetizador",
    "fr": "Musique · Synthétiseur",
    "it": "Musica · Sintetizzatore",
    "ko": "음악 · 신디사이저",
    "nl": "Muziek · Synthesizer",
    "pt-BR": "Música · Sintetizador",
    "sv": "Musik · Synthesizer",
    "zh-Hant": "音樂 · 合成器"
  },
  "description": {
    "en": "MIDI 2.0 + DX7-compatible FM synthesizer for iOS. Public TestFlight beta.",
    "ja": "iOS 向けの MIDI 2.0 対応 DX7 互換 FM シンセサイザー。TestFlight ベータ公開中。",
    "de": "MIDI 2.0 + DX7-kompatibler FM-Synthesizer für iOS. Öffentliche TestFlight-Beta.",
    "es": "Sintetizador FM compatible con MIDI 2.0 + DX7 para iOS. Beta pública de TestFlight.",
    "fr": "Synthétiseur FM compatible MIDI 2.0 + DX7 pour iOS. Bêta publique TestFlight.",
    "it": "Sintetizzatore FM compatibile MIDI 2.0 + DX7 per iOS. Beta pubblica TestFlight.",
    "ko": "iOS용 MIDI 2.0 + DX7 호환 FM 신디사이저. TestFlight 공개 베타.",
    "nl": "MIDI 2.0 + DX7-compatibele FM-synthesizer voor iOS. Publieke TestFlight-bèta.",
    "pt-BR": "Sintetizador FM compatível com MIDI 2.0 + DX7 para iOS. Beta pública TestFlight.",
    "sv": "MIDI 2.0 + DX7-kompatibel FM-synthesizer för iOS. Publik TestFlight-beta.",
    "zh-Hant": "iOS 平台的 MIDI 2.0 + DX7 相容 FM 合成器。TestFlight 公開測試版。"
  },
  "links": {
    "testFlight": "https://testflight.apple.com/join/BAtGszPw",
    "github": "https://github.com/hakaru/M2DX"
  }
}
```

- [ ] **Step 2: Copy icon assets**

```bash
mkdir -p apps/web/public/assets
cp assets/midi2kit-icon.svg apps/web/public/assets/midi2kit-icon.svg
```

- [ ] **Step 3: Write `apps/web/src/content/support/m2dx/index.ja.md` (hand-built sample)**

```markdown
---
title: M2DX サポート
description: MIDI 2.0 対応 DX7 互換 FM シンセサイザーの iOS アプリ。TestFlight ベータ配信中。
lang: ja
app: m2dx
section: support
---

M2DX は、MIDI 2.0 に対応した iOS 向けの DX7 互換 FM シンセサイザーアプリです。シンセシスエンジンには [M2DX-Core](/ja/m2dx-core/) ライブラリを使用しています。

(Hand-built sample — full content will land via migration script in Phase 1.)
```

- [ ] **Step 4: Write `apps/web/src/content/support/m2dx/index.en.md`**

```markdown
---
title: M2DX Support
description: MIDI 2.0 + DX7-compatible FM synthesizer for iOS. Public TestFlight beta.
lang: en
app: m2dx
section: support
---

M2DX is a MIDI 2.0-compatible DX7 FM synthesizer for iOS. The synthesis engine is provided by the [M2DX-Core](/en/m2dx-core/) library.

(Hand-built sample — full content lands via migration in Phase 1.)
```

- [ ] **Step 5: Commit**

```bash
git add apps/web/src/content/apps/m2dx.json apps/web/src/content/support/m2dx/ apps/web/public/assets/midi2kit-icon.svg
git commit -m "feat(redesign): M2DX app metadata + sample support content (ja, en)"
```

### Task 10: Wire up `[lang]/[app]/index.astro` route

**Files:**
- Create: `apps/web/src/pages/[lang]/[app]/index.astro`

- [ ] **Step 1: Write `apps/web/src/pages/[lang]/[app]/index.astro`**

```astro
---
import { getCollection, getEntry, render } from 'astro:content';
import AppPageLayout from '../../../layouts/AppPageLayout.astro';
import TestFlightCTA from '../../../components/TestFlightCTA.astro';
import AppStoreCTA from '../../../components/AppStoreCTA.astro';

export async function getStaticPaths() {
  const apps = await getCollection('apps');
  const support = await getCollection('support', (e) => e.data.section === 'support');
  return support.map((entry) => ({
    params: { lang: entry.data.lang, app: entry.data.app },
    props: { entry, app: apps.find((a) => a.data.id === entry.data.app)! },
  }));
}

const { entry, app } = Astro.props;
const { Content } = await render(entry);

const tflLabels: Record<string, string> = {
  en: 'Join TestFlight Beta', ja: 'TestFlight ベータに参加', de: 'TestFlight-Beta beitreten',
  es: 'Unirse a la beta de TestFlight', fr: 'Rejoindre la bêta TestFlight',
  it: 'Unisciti alla beta TestFlight', ko: 'TestFlight 베타 참가',
  nl: 'Doe mee aan TestFlight-bèta', 'pt-BR': 'Entrar na beta do TestFlight',
  sv: 'Gå med i TestFlight-betan', 'zh-Hant': '加入 TestFlight 測試',
};
const tflLabel = tflLabels[entry.data.lang] ?? tflLabels.en;
---
<AppPageLayout
  title={entry.data.title}
  description={entry.data.description}
  lang={entry.data.lang}
  appId={app.data.id}
  appName={app.data.name}
  appAccent={app.data.accentColor}
  appBadgeLabel={app.data.badge ? `${app.data.badge}` : undefined}
  pageKind="support"
  tagline={app.data.description[entry.data.lang as keyof typeof app.data.description]}
  pathWithoutLang={`/${app.data.id}/`}
>
  <Fragment slot="hero-actions">
    {app.data.links.testFlight && <TestFlightCTA href={app.data.links.testFlight} label={tflLabel} accentColor={app.data.accentColor} />}
    {app.data.links.github && <AppStoreCTA href={app.data.links.github} label="GitHub" />}
  </Fragment>
  <article class="prose">
    <Content />
  </article>
</AppPageLayout>

<style>
  .prose :global(h2) { margin-top: 32px; margin-bottom: 14px; }
  .prose :global(h3) { margin-top: 24px; margin-bottom: 10px; }
  .prose :global(p), .prose :global(ul), .prose :global(ol) { margin-bottom: 14px; }
  .prose :global(ul), .prose :global(ol) { margin-left: 20px; }
  .prose :global(li) { margin-bottom: 6px; color: var(--text-muted); }
</style>
```

- [ ] **Step 2: Build and check the M2DX page renders**

```bash
cd apps/web && npm run build && cd ../..
```
Expected: build succeeds. Output should include `apps/web/dist/ja/m2dx/index.html` and `apps/web/dist/en/m2dx/index.html`.

- [ ] **Step 3: Local preview to eyeball**

```bash
cd apps/web && npm run preview &
sleep 2
open http://localhost:4321/ja/m2dx/
```
Expected: M2DX support page loads with sidebar, hero, "join TestFlight" button. Eyeball typography/spacing.

- [ ] **Step 4: Commit**

```bash
git add apps/web/src/pages/
git commit -m "feat(redesign): [lang]/[app]/index route renders support content"
```

### Task 11: Wire up `[lang]/[app]/privacy.astro` and verify Phase 0 deploys

**Files:**
- Create: `apps/web/src/pages/[lang]/[app]/privacy.astro`
- Create: `apps/web/src/content/support/m2dx/privacy.ja.md` (sample)
- Create: `apps/web/src/content/support/m2dx/privacy.en.md` (sample)

- [ ] **Step 1: Write privacy route at `apps/web/src/pages/[lang]/[app]/privacy.astro`**

```astro
---
import { getCollection, render } from 'astro:content';
import AppPageLayout from '../../../layouts/AppPageLayout.astro';

export async function getStaticPaths() {
  const apps = await getCollection('apps');
  const privacy = await getCollection('support', (e) => e.data.section === 'privacy');
  return privacy.map((entry) => ({
    params: { lang: entry.data.lang, app: entry.data.app },
    props: { entry, app: apps.find((a) => a.data.id === entry.data.app)! },
  }));
}

const { entry, app } = Astro.props;
const { Content } = await render(entry);
---
<AppPageLayout
  title={entry.data.title}
  description={entry.data.description}
  lang={entry.data.lang}
  appId={app.data.id}
  appName={app.data.name}
  appAccent={app.data.accentColor}
  pageKind="privacy"
  pathWithoutLang={`/${app.data.id}/privacy/`}
>
  <article class="prose">
    <Content />
  </article>
</AppPageLayout>
```

- [ ] **Step 2: Add minimal privacy sample content**

`apps/web/src/content/support/m2dx/privacy.ja.md`:
```markdown
---
title: M2DX プライバシーポリシー
lang: ja
app: m2dx
section: privacy
---
最終更新日: 2026 年 4 月 26 日。本ページの完全版は Phase 1 の移行スクリプトで生成されます。
```

`apps/web/src/content/support/m2dx/privacy.en.md`:
```markdown
---
title: M2DX Privacy Policy
lang: en
app: m2dx
section: privacy
---
Last updated: April 26, 2026. Full content lands via Phase 1 migration script.
```

- [ ] **Step 3: Push to `redesign` and verify Cloudflare preview**

```bash
git add apps/web/src/pages/[lang]/[app]/privacy.astro apps/web/src/content/support/m2dx/privacy.ja.md apps/web/src/content/support/m2dx/privacy.en.md
git commit -m "feat(redesign): privacy route + M2DX privacy samples; close P0"
git push
```
Expected: `redesign` branch updates on origin. Open Cloudflare Pages dashboard, verify the preview deployment for `redesign` succeeds and `redesign.hakaru-net.pages.dev/ja/m2dx/` renders.

**P0 acceptance:** M2DX (ja, en) support and privacy pages render in the new design on the Cloudflare preview URL with sidebar, hero, CTA, and a working language switcher.

---

## Phase 1: Migration Script + 3 Priority Apps

### Task 12: Build the HTML→Markdown migration script skeleton

**Files:**
- Create: `scripts/migrate-to-md.py`
- Create: `scripts/migration_link_map.json`

- [ ] **Step 1: Add Anthropic SDK to local Python env**

```bash
pip install anthropic beautifulsoup4
```
Expected: both installed. `python3 -c "import anthropic, bs4; print('ok')"` prints `ok`.

- [ ] **Step 2: Create `scripts/migration_link_map.json` with the URL rewrite rules**

```json
{
  "_comment": "Maps legacy URL prefixes to new Astro URLs. Used by migrate-to-md.py.",
  "rules": [
    { "from": "/M2DX-support/index-",       "to": "/{lang}/m2dx/" },
    { "from": "/M2DX-support/privacy-",     "to": "/{lang}/m2dx/privacy" },
    { "from": "/M2DX-support/",             "to": "/en/m2dx/" },
    { "from": "/M2DX-Core-support/index-",  "to": "/{lang}/m2dx-core/" },
    { "from": "/M2DX-Core-support/privacy-","to": "/{lang}/m2dx-core/privacy" },
    { "from": "/M2DX-Core-support/blog/",   "to": "/{lang}/m2dx-core/blog/" },
    { "from": "/M2DX-Core-support/",        "to": "/en/m2dx-core/" },
    { "from": "/PeerClockMetronome-support/index-",   "to": "/{lang}/peerclock-metronome/" },
    { "from": "/PeerClockMetronome-support/privacy-", "to": "/{lang}/peerclock-metronome/privacy" },
    { "from": "/PeerClockMetronome-support/blog/",    "to": "/{lang}/peerclock-metronome/blog/" },
    { "from": "/PeerClockMetronome-support/",         "to": "/en/peerclock-metronome/" },
    { "from": "/1Take-support/index-",      "to": "/{lang}/1take/" },
    { "from": "/1Take-support/privacy-",    "to": "/{lang}/1take/privacy" },
    { "from": "/1Take-support/changelog-",  "to": "/{lang}/1take/changelog" },
    { "from": "/1Take-support/manual/",     "to": "/{lang}/1take/manual/" },
    { "from": "/1Take-support/blog/",       "to": "/{lang}/1take/blog/" },
    { "from": "/1Take-support/",            "to": "/en/1take/" },
    { "from": "/GitInflow-support/",        "to": "/en/gitinflow/" },
    { "from": "/SonicDNACollector-support/","to": "/en/sonicdna-collector/" },
    { "from": "/SonicDNAEngine-support/",   "to": "/en/sonicdna-engine/" },
    { "from": "/simpleMIDIController-support/","to": "/en/simplemidi-controller/" },
    { "from": "/TineModeler-support/",      "to": "/en/tinemodeler/" },
    { "from": "/ChatArchive-support/",      "to": "/en/chatarchive/" }
  ]
}
```

- [ ] **Step 3: Write `scripts/migrate-to-md.py` skeleton**

```python
#!/usr/bin/env python3
"""HTML → Markdown migrator using Anthropic Claude.

Usage: python3 scripts/migrate-to-md.py <app-dir> --section index|privacy|... [--limit N] [--dry-run]
"""
import argparse, json, os, re, sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import anthropic

ROOT = Path(__file__).resolve().parent.parent
LINK_MAP = json.loads((ROOT / "scripts" / "migration_link_map.json").read_text(encoding="utf-8"))
OUT_ROOT = ROOT / "apps" / "web" / "src" / "content" / "support"
LANGS = ["en","ja","de","es","fr","it","ko","nl","pt-BR","sv","zh-Hant"]

# App dir name -> content dir name (must match apps/<id>.json id)
APP_ID_FROM_DIR = {
    "1Take-support": "1take",
    "GitInflow-support": "gitinflow",
    "SonicDNACollector-support": "sonicdna-collector",
    "SonicDNAEngine-support": "sonicdna-engine",
    "simpleMIDIController-support": "simplemidi-controller",
    "TineModeler-support": "tinemodeler",
    "M2DX-Core-support": "m2dx-core",
    "M2DX-support": "m2dx",
    "PeerClockMetronome-support": "peerclock-metronome",
    "ChatArchive-support": "chatarchive",
}

PROMPT = """Convert the following HTML content section to clean GitHub-flavored Markdown.

Rules (strict):
- Preserve meaning exactly. Do not add or remove information.
- Convert <strong>/<b> to **bold**, <em>/<i> to *italic*, <hr> to ---.
- Lists: <ul>/<li> to '-', <ol>/<li> to '1.'.
- Tables: GFM table syntax.
- Links: [text](href). Preserve external URLs as-is. The href substitution is handled later, leave them as written.
- Code: inline `code`, blocks ```lang.
- Drop classes, ids, inline styles, and stray <div> wrappers.
- Output ONLY the Markdown body. No frontmatter. No explanations.

HTML:
{html}
"""

def extract_body(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one(".content") or soup.select_one("main") or soup.body
    if not container:
        raise RuntimeError("no content container")
    # remove any leftover hero block if it's in the same parent — we'll keep the text but discard the wrapper noise
    return str(container)

def extract_meta(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""
    return {"title": title, "description": description}

def lang_from_filename(fname: str) -> str:
    m = re.match(r"(?:index|privacy|terms|changelog)(?:-([a-zA-Z-]+))?\.html$", fname)
    if not m:
        return "en"
    return m.group(1) or "en"

def section_from_filename(fname: str) -> str:
    if fname.startswith("index"): return "support"
    if fname.startswith("privacy"): return "privacy"
    if fname.startswith("terms"): return "terms"
    if fname.startswith("changelog"): return "changelog"
    return "support"

def rewrite_links(md: str, lang: str) -> str:
    out = md
    for rule in LINK_MAP["rules"]:
        # exact-prefix substitutions
        if rule["from"].endswith("-"):
            # /M2DX-support/index- → /{lang}/m2dx/
            pattern = re.compile(re.escape(rule["from"]) + r"([a-zA-Z-]+)")
            def replace(m):
                page_lang = m.group(1)
                return rule["to"].replace("{lang}", page_lang)
            out = pattern.sub(replace, out)
        else:
            out = out.replace(rule["from"], rule["to"].replace("{lang}", lang))
    return out

def call_claude(html_body: str, client: anthropic.Anthropic) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": PROMPT.format(html=html_body)}],
    )
    return response.content[0].text.strip()

def migrate_one(html_path: Path, app_id: str, client: anthropic.Anthropic, dry_run: bool=False) -> dict:
    html = html_path.read_text(encoding="utf-8")
    body = extract_body(html)
    meta = extract_meta(html)
    lang = lang_from_filename(html_path.name)
    section = section_from_filename(html_path.name)
    md_body = call_claude(body, client) if not dry_run else "(dry-run placeholder)"
    md_body = rewrite_links(md_body, lang)
    fm = [
        "---",
        f"title: {json.dumps(meta['title'], ensure_ascii=False)}",
    ]
    if meta["description"]:
        fm.append(f"description: {json.dumps(meta['description'], ensure_ascii=False)}")
    fm.extend([f"lang: {lang}", f"app: {app_id}", f"section: {section}", "---", ""])
    out_path = OUT_ROOT / app_id / f"{section if section != 'support' else 'index'}.{lang}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(fm) + md_body + "\n", encoding="utf-8")
    return {"in": str(html_path.relative_to(ROOT)), "out": str(out_path.relative_to(ROOT)), "lang": lang, "section": section}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("app_dir", help="legacy support dir name (e.g., M2DX-support)")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=10)
    args = ap.parse_args()

    src_dir = ROOT / args.app_dir
    if not src_dir.is_dir():
        sys.exit(f"not a dir: {src_dir}")
    app_id = APP_ID_FROM_DIR.get(args.app_dir)
    if not app_id:
        sys.exit(f"unknown app: {args.app_dir}")
    files = sorted([p for p in src_dir.glob("*.html") if not p.name.startswith("blog")])
    if args.limit:
        files = files[: args.limit]
    print(f"Migrating {len(files)} files from {args.app_dir} (app id: {app_id})")
    client = anthropic.Anthropic()
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(migrate_one, f, app_id, client, args.dry_run): f for f in files}
        for fut in as_completed(futures):
            try:
                r = fut.result()
                print(f"  [OK] {r['in']} → {r['out']}")
                results.append(r)
            except Exception as e:
                print(f"  [ERR] {futures[fut]}: {e}", file=sys.stderr)
    print(f"\n{len(results)}/{len(files)} migrated")

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Smoke-test the script in dry-run on M2DX**

```bash
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY python3 scripts/migrate-to-md.py M2DX-support --dry-run --limit 2
```
Expected: writes 2 placeholder MD files under `apps/web/src/content/support/m2dx/`. Inspect them — frontmatter correct, body says `(dry-run placeholder)`.

- [ ] **Step 5: Reset dry-run output and commit script**

```bash
git checkout -- apps/web/src/content/support/m2dx/
git add scripts/migrate-to-md.py scripts/migration_link_map.json
git commit -m "tools: HTML→Markdown migration script (Claude API)"
```

### Task 13: Real migration of M2DX (11 langs × index + privacy)

**Files:** populates `apps/web/src/content/support/m2dx/*.md`

- [ ] **Step 1: Run real migration**

```bash
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY python3 scripts/migrate-to-md.py M2DX-support
```
Expected: 22 files produced (11 langs × 2 sections). Each has proper frontmatter and Markdown body.

- [ ] **Step 2: Spot-check ja and en files**

```bash
head -20 apps/web/src/content/support/m2dx/index.ja.md
head -20 apps/web/src/content/support/m2dx/privacy.en.md
```
Expected: frontmatter correctly populated; body is Markdown with headings, lists, links rewritten to `/ja/m2dx/...` form. No leftover HTML tags.

- [ ] **Step 3: Build and preview**

```bash
cd apps/web && npm run build && cd ../..
```
Expected: build succeeds with 22 M2DX content pages.

- [ ] **Step 4: Commit**

```bash
git add apps/web/src/content/support/m2dx/
git commit -m "feat(redesign): migrate M2DX support content (11 languages)"
```

### Task 14: Migrate M2DX-Core (11 langs × index + privacy)

**Files:** populates `apps/web/src/content/support/m2dx-core/*.md`

- [ ] **Step 1: Author M2DX-Core app metadata**

`apps/web/src/content/apps/m2dx-core.json`:
```json
{
  "id": "m2dx-core",
  "name": "M2DX-Core",
  "icon": "/assets/midi2kit-icon.svg",
  "accentColor": "#4a90d9",
  "order": 71,
  "sections": ["support", "privacy", "blog"],
  "category": {
    "en": "Developer · Open Source", "ja": "開発者 · オープンソース", "de": "Entwickler · Open Source",
    "es": "Desarrollador · Código Abierto", "fr": "Développeur · Open Source", "it": "Sviluppatore · Open Source",
    "ko": "개발자 · 오픈소스", "nl": "Developer · Open source", "pt-BR": "Desenvolvedor · Código Aberto",
    "sv": "Utvecklare · Öppen källkod", "zh-Hant": "開發者 · 開源"
  },
  "description": {
    "en": "Pure Swift DX7 FM synthesis engine. Bit-accurate hardware emulation, MIDI 2.0 native.",
    "ja": "Pure Swift による DX7 FM シンセシスエンジン。ビット精度のハードウェアエミュレーション、MIDI 2.0 ネイティブ。",
    "de": "Pure-Swift DX7-FM-Synthesizer-Engine. Bit-genaue Hardware-Emulation, MIDI 2.0 nativ.",
    "es": "Motor de síntesis FM DX7 en Swift puro. Emulación de hardware bit a bit, MIDI 2.0 nativo.",
    "fr": "Moteur de synthèse FM DX7 en Swift pur. Émulation matérielle bit à bit, MIDI 2.0 natif.",
    "it": "Motore di sintesi FM DX7 in puro Swift. Emulazione hardware bit-accurata, MIDI 2.0 nativo.",
    "ko": "Pure Swift DX7 FM 합성 엔진. 비트 정확한 하드웨어 에뮬레이션, MIDI 2.0 네이티브.",
    "nl": "DX7 FM-synthese-engine in pure Swift. Bit-accurate hardware-emulatie, MIDI 2.0 native.",
    "pt-BR": "Motor de síntese FM DX7 em Swift puro. Emulação de hardware bit a bit, MIDI 2.0 nativo.",
    "sv": "DX7 FM-synthesmotor i ren Swift. Bit-exakt hårdvaruemulering, MIDI 2.0 inbyggt.",
    "zh-Hant": "純 Swift 實作的 DX7 FM 合成引擎。位元精確的硬體模擬、MIDI 2.0 原生支援。"
  },
  "links": {
    "github": "https://github.com/hakaru/M2DX-Core"
  }
}
```

- [ ] **Step 2: Run migration for M2DX-Core support pages**

```bash
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY python3 scripts/migrate-to-md.py M2DX-Core-support
```
Expected: 22 MD files in `apps/web/src/content/support/m2dx-core/`.

- [ ] **Step 3: Spot-check and build**

```bash
head -20 apps/web/src/content/support/m2dx-core/index.ja.md
cd apps/web && npm run build && cd ../..
```
Expected: ja file has correct frontmatter + Markdown body. Build succeeds.

- [ ] **Step 4: Commit**

```bash
git add apps/web/src/content/apps/m2dx-core.json apps/web/src/content/support/m2dx-core/
git commit -m "feat(redesign): migrate M2DX-Core support + metadata"
```

### Task 15: Migrate PeerClock Metronome

**Files:** populates `apps/web/src/content/support/peerclock-metronome/*.md`

- [ ] **Step 1: Author PeerClock metadata**

`apps/web/src/content/apps/peerclock-metronome.json`:
```json
{
  "id": "peerclock-metronome",
  "name": "PeerClock Metronome",
  "icon": "/apps/peerclock-metronome/app-icon.svg",
  "badge": "NEW",
  "accentColor": "#00bcd4",
  "order": 20,
  "sections": ["support", "privacy", "blog"],
  "category": {
    "en": "Music · Metronome", "ja": "音楽 · メトロノーム", "de": "Musik · Metronom",
    "es": "Música · Metrónomo", "fr": "Musique · Métronome", "it": "Musica · Metronomo",
    "ko": "음악 · 메트로놈", "nl": "Muziek · Metronoom", "pt-BR": "Música · Metrônomo",
    "sv": "Musik · Metronom", "zh-Hant": "音樂 · 節拍器"
  },
  "description": {
    "en": "P2P-synced metronome for Apple devices. ±2ms over local Wi-Fi.",
    "ja": "Apple デバイス向け P2P 同期メトロノーム。ローカル Wi-Fi で ±2ms。",
    "de": "P2P-synchronisiertes Metronom für Apple-Geräte. ±2 ms im lokalen Wi-Fi.",
    "es": "Metrónomo P2P sincronizado para dispositivos Apple. ±2 ms en Wi-Fi local.",
    "fr": "Métronome synchronisé P2P pour appareils Apple. ±2 ms sur Wi-Fi local.",
    "it": "Metronomo sincronizzato P2P per dispositivi Apple. ±2 ms su Wi-Fi locale.",
    "ko": "Apple 기기용 P2P 동기화 메트로놈. 로컬 Wi-Fi에서 ±2ms.",
    "nl": "P2P-gesynchroniseerde metronoom voor Apple-apparaten. ±2 ms via lokale Wi-Fi.",
    "pt-BR": "Metrônomo P2P sincronizado para dispositivos Apple. ±2 ms em Wi-Fi local.",
    "sv": "P2P-synkad metronom för Apple-enheter. ±2 ms över lokalt Wi-Fi.",
    "zh-Hant": "Apple 裝置用 P2P 同步節拍器，本地 Wi-Fi 上 ±2 毫秒。"
  },
  "links": {
    "appStore": "https://apps.apple.com/us/app/peerclock-metronome/id6762972307"
  }
}
```

- [ ] **Step 2: Copy PeerClock app icon**

```bash
mkdir -p apps/web/public/apps/peerclock-metronome
cp PeerClockMetronome-support/assets/app-icon.svg apps/web/public/apps/peerclock-metronome/app-icon.svg
```

- [ ] **Step 3: Run migration**

```bash
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY python3 scripts/migrate-to-md.py PeerClockMetronome-support
```
Expected: 22 MD files in `apps/web/src/content/support/peerclock-metronome/`.

- [ ] **Step 4: Build and commit**

```bash
cd apps/web && npm run build && cd ../..
git add apps/web/src/content/apps/peerclock-metronome.json apps/web/src/content/support/peerclock-metronome/ apps/web/public/apps/peerclock-metronome/
git commit -m "feat(redesign): migrate PeerClock Metronome support + metadata + icon"
```

### Task 16: Push Phase 1 and verify preview deploy

- [ ] **Step 1: Push to redesign**

```bash
git push
```
Expected: Cloudflare Pages preview rebuilds.

- [ ] **Step 2: Verify priority pages on preview URL**

Open in browser:
- `https://redesign.hakaru-net.pages.dev/ja/m2dx/`
- `https://redesign.hakaru-net.pages.dev/en/m2dx/privacy/`
- `https://redesign.hakaru-net.pages.dev/de/m2dx-core/`
- `https://redesign.hakaru-net.pages.dev/zh-Hant/peerclock-metronome/`

Expected: All render correctly with the new design. Sidebar shows current app expanded. Lang switcher works to swap pages keeping the same `app/section`.

**P1 acceptance:** 3 priority apps × 11 languages × support+privacy fully render on preview URL.

---

## Phase 2: Remaining Apps + Blogs + Manuals

### Task 17: Author metadata for the remaining 8 apps

**Files:**
- Create: `apps/web/src/content/apps/1take.json`
- Create: `apps/web/src/content/apps/gitinflow.json`
- Create: `apps/web/src/content/apps/sonicdna-collector.json`
- Create: `apps/web/src/content/apps/sonicdna-engine.json`
- Create: `apps/web/src/content/apps/simplemidi-controller.json`
- Create: `apps/web/src/content/apps/tinemodeler.json`
- Create: `apps/web/src/content/apps/tensync.json`
- Create: `apps/web/src/content/apps/chatarchive.json`

- [ ] **Step 1: Pull existing values**

For each app, read the existing metadata from the legacy root `index.html` app card and from `scripts/sidebar-config.json`:

```bash
grep -A 20 '<!-- 1Take' index.html
grep -A 30 '"id": "1Take"' scripts/sidebar-config.json
```

- [ ] **Step 2: Create one JSON per app**

Pattern (use the M2DX/M2DX-Core/PeerClock files as templates). Required fields:
- `id` (kebab-case, must match the migration script `APP_ID_FROM_DIR` value)
- `name` (display name with original casing — e.g., "1Take", "GitInflow", "SonicDNA Engine")
- `icon` (path under `/assets/` or `/apps/<id>/`)
- `accentColor` (pick from existing site CSS or use `#18181b` default)
- `order` (integer; lower = higher in sidebar; recommend: TenSync 10, PeerClock 20, 1Take 30, GitInflow 40, SonicDNACollector 50, SonicDNAEngine 51, simpleMIDI 60, TineModeler 65, M2DX 70, M2DX-Core 71, ChatArchive 80)
- `sections` (`["support","privacy"]` plus `"blog"` / `"manual"` / `"changelog"` / `"terms"` if the legacy site has those dirs)
- `category` (full 11-language record — copy from legacy `index-*.html` app cards' `<p class="app-category">`)
- `description` (full 11-language record — copy from `<p class="app-description">`)
- `links.appStore` / `links.github` / `links.testFlight` (from legacy `<a class="app-link primary">`)

- [ ] **Step 3: Copy any per-app icons not yet in `public/apps/<app>/`**

```bash
for app in 1Take SonicDNACollector SonicDNAEngine simpleMIDIController TineModeler ChatArchive; do
  src_dir="${app}-support/assets"
  if [ -d "$src_dir" ]; then
    dest_id=$(echo "$app" | tr '[:upper:]' '[:lower:]' | sed 's/midicontroller/midi-controller/;s/sonicdnacollector/sonicdna-collector/;s/sonicdnaengine/sonicdna-engine/')
    mkdir -p "apps/web/public/apps/${dest_id}"
    cp -R "$src_dir/." "apps/web/public/apps/${dest_id}/"
  fi
done
cp assets/tensync-icon.png apps/web/public/assets/ 2>/dev/null || true
cp assets/tinemodeler-icon.png apps/web/public/assets/ 2>/dev/null || true
cp assets/sonicdna-icon.png apps/web/public/assets/ 2>/dev/null || true
cp assets/1take-icon.png apps/web/public/assets/ 2>/dev/null || true
cp assets/gitinflow-icon.png apps/web/public/assets/ 2>/dev/null || true
cp assets/chatarchive-icon.png apps/web/public/assets/ 2>/dev/null || true
cp assets/simplemidi-icon.png apps/web/public/assets/ 2>/dev/null || true
```

- [ ] **Step 4: Build to verify schemas pass**

```bash
cd apps/web && npm run build && cd ../..
```
Expected: build succeeds. Failures usually mean a metadata field is missing — fix and retry.

- [ ] **Step 5: Commit**

```bash
git add apps/web/src/content/apps/ apps/web/public/
git commit -m "feat(redesign): app metadata + icons for remaining 8 apps"
```

### Task 18: Migrate remaining 8 apps' support content

**Files:** populates `apps/web/src/content/support/<app>/*.md`

- [ ] **Step 1: Migrate each legacy directory**

```bash
for dir in 1Take-support GitInflow-support SonicDNACollector-support SonicDNAEngine-support simpleMIDIController-support TineModeler-support ChatArchive-support; do
  ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY python3 scripts/migrate-to-md.py "$dir"
done
```
Expected: each app produces support / privacy / changelog / terms files matching its existing legacy file count.

- [ ] **Step 2: Handle `tensync/` (path differs — top-level dir, not `*-support`)**

Add `tensync` to `APP_ID_FROM_DIR` in `scripts/migrate-to-md.py`:
```python
"tensync": "tensync",
```
Then:
```bash
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY python3 scripts/migrate-to-md.py tensync
```

- [ ] **Step 3: Build**

```bash
cd apps/web && npm run build && cd ../..
```
Expected: build succeeds with all migrated content.

- [ ] **Step 4: Commit**

```bash
git add apps/web/src/content/support/ scripts/migrate-to-md.py
git commit -m "feat(redesign): migrate support content for remaining 8 apps"
```

### Task 19: Extend migration script to handle blog posts

**Files:**
- Modify: `scripts/migrate-to-md.py`

- [ ] **Step 1: Add a `--mode blog` mode**

In `scripts/migrate-to-md.py`, replace the `main()` body's file collection with:
```python
if args.mode == "support":
    files = sorted([p for p in src_dir.glob("*.html") if not p.name.startswith("blog")])
elif args.mode == "blog":
    # Blog posts live under <app-dir>/blog/<lang>/<slug>/index.html
    files = sorted(src_dir.glob("blog/*/*/index.html"))
elif args.mode == "manual":
    files = sorted(src_dir.glob("manual/*/*/index.html")) + sorted(src_dir.glob("manual/*/index.html"))
```
Add `--mode` arg (default `support`). Update output target:
```python
if args.mode == "blog":
    out_root = ROOT / "apps" / "web" / "src" / "content" / "blog"
elif args.mode == "manual":
    out_root = ROOT / "apps" / "web" / "src" / "content" / "manual"
else:
    out_root = ROOT / "apps" / "web" / "src" / "content" / "support"
```
For blog, the lang and slug come from the path: `<dir>/blog/<lang>/<slug>/index.html` → `lang=<lang>`, `slug=<slug>`. Adjust frontmatter (date pulled from `<time>` tag or filename pattern `YYYY-MM-DD-...`).

- [ ] **Step 2: Test on a single blog post**

```bash
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY python3 scripts/migrate-to-md.py M2DX-Core-support --mode blog --limit 1
```
Expected: one file lands at `apps/web/src/content/blog/m2dx-core/<slug>.<lang>.md` with `date:` frontmatter.

- [ ] **Step 3: Commit**

```bash
git add scripts/migrate-to-md.py
git commit -m "tools: extend migration script with blog/manual modes"
```

### Task 20: Migrate all blogs

**Files:** populates `apps/web/src/content/blog/<app>/`

- [ ] **Step 1: Find blog-bearing apps**

```bash
find . -path './apps' -prune -o -type d -name 'blog' -print | grep -v node_modules
```
Expected: directories like `1Take-support/blog`, `M2DX-Core-support/blog`, `PeerClockMetronome-support/blog`, `SonicDNACollector-support/blog`, `SonicDNAEngine-support/blog`, `simpleMIDIController-support/blog`, `ChatArchive-support/blog`.

- [ ] **Step 2: Run blog migration per app**

```bash
for dir in 1Take-support M2DX-Core-support PeerClockMetronome-support SonicDNACollector-support SonicDNAEngine-support simpleMIDIController-support ChatArchive-support; do
  ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY python3 scripts/migrate-to-md.py "$dir" --mode blog
done
```
Expected: hundreds of blog MD files produced.

- [ ] **Step 3: Build**

```bash
cd apps/web && npm run build && cd ../..
```
Expected: build succeeds. Failures usually due to invalid date frontmatter — fix in the script and re-run for the affected app.

- [ ] **Step 4: Commit**

```bash
git add apps/web/src/content/blog/
git commit -m "feat(redesign): migrate all blog posts (11 languages)"
```

### Task 21: Add blog index and post pages

**Files:**
- Create: `apps/web/src/pages/[lang]/[app]/blog/index.astro`
- Create: `apps/web/src/pages/[lang]/[app]/blog/[...slug].astro`
- Create: `apps/web/src/components/PostList.astro`
- Create: `apps/web/src/components/PostMeta.astro`
- Create: `apps/web/src/layouts/BlogLayout.astro`

- [ ] **Step 1: Write `apps/web/src/components/PostMeta.astro`**

```astro
---
interface Props { date: Date; lang: string; }
const { date, lang } = Astro.props;
const formatted = new Intl.DateTimeFormat(lang === 'zh-Hant' ? 'zh-TW' : lang, { year: 'numeric', month: 'short', day: 'numeric' }).format(date);
---
<time class="post-meta" datetime={date.toISOString()}>{formatted}</time>
<style>
  .post-meta { color: var(--text-subtle); font-size: 0.85em; }
</style>
```

- [ ] **Step 2: Write `apps/web/src/components/PostList.astro`**

```astro
---
import PostMeta from './PostMeta.astro';
interface Props {
  posts: Array<{ slug: string; data: { title: string; description?: string; date: Date; lang: string; app: string } }>;
  lang: string;
  appId: string;
}
const { posts, lang, appId } = Astro.props;
const sorted = posts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
---
<ul class="post-list">
  {sorted.map((p) => (
    <li>
      <a href={`/${lang}/${appId}/blog/${p.slug.replace(`.${lang}`,'')}/`}>
        <h3>{p.data.title}</h3>
        {p.data.description && <p>{p.data.description}</p>}
        <PostMeta date={p.data.date} lang={lang} />
      </a>
    </li>
  ))}
</ul>
<style>
  .post-list { list-style: none; padding: 0; }
  .post-list li { margin-bottom: 24px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }
  .post-list a { display: block; text-decoration: none; color: var(--text); }
  .post-list h3 { margin-bottom: 6px; }
  .post-list p { color: var(--text-muted); font-size: 0.95em; margin-bottom: 8px; }
</style>
```

- [ ] **Step 3: Write `apps/web/src/layouts/BlogLayout.astro`**

```astro
---
import RootLayout from './RootLayout.astro';
import PostMeta from '../components/PostMeta.astro';
interface Props {
  title: string;
  description?: string;
  date: Date;
  lang: string;
  appId: string;
  appName: string;
  appAccent: string;
  pathWithoutLang: string;
}
const { title, description, date, lang, appId, appName, appAccent, pathWithoutLang } = Astro.props;
---
<RootLayout title={title} description={description} lang={lang} currentApp={appId} currentSection="blog" pathWithoutLang={pathWithoutLang}>
  <div class="container">
    <header class="post-hero">
      <a class="post-app-back" href={`/${lang}/${appId}/blog/`} style={`color: ${appAccent}`}>← {appName}</a>
      <h1>{title}</h1>
      <PostMeta date={date} lang={lang} />
    </header>
    <article class="prose"><slot /></article>
  </div>
  <style>
    .post-hero { margin-bottom: 36px; }
    .post-app-back { font-size: 0.85em; font-weight: 600; text-decoration: none; }
    .post-hero h1 { margin: 12px 0 8px; }
    .prose :global(h2) { margin: 28px 0 12px; }
    .prose :global(h3) { margin: 22px 0 10px; }
    .prose :global(p), .prose :global(ul), .prose :global(ol) { margin-bottom: 14px; }
    .prose :global(ul), .prose :global(ol) { margin-left: 20px; }
    .prose :global(img) { max-width: 100%; border-radius: var(--radius-md); margin: 16px 0; }
  </style>
</RootLayout>
```

- [ ] **Step 4: Write `apps/web/src/pages/[lang]/[app]/blog/index.astro`**

```astro
---
import { getCollection } from 'astro:content';
import AppPageLayout from '../../../../layouts/AppPageLayout.astro';
import PostList from '../../../../components/PostList.astro';

export async function getStaticPaths() {
  const apps = await getCollection('apps');
  const blog = await getCollection('blog');
  // group by (lang, app)
  const groups = new Map<string, typeof blog>();
  for (const post of blog) {
    const key = `${post.data.lang}|${post.data.app}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key)!.push(post);
  }
  return Array.from(groups.entries()).map(([key, posts]) => {
    const [lang, app] = key.split('|');
    return {
      params: { lang, app },
      props: { posts, app: apps.find((a) => a.data.id === app)!, lang },
    };
  });
}
const { posts, app, lang } = Astro.props;
const titles: Record<string, string> = { en: 'Blog', ja: 'ブログ', de: 'Blog', es: 'Blog', fr: 'Blog', it: 'Blog', ko: '블로그', nl: 'Blog', 'pt-BR': 'Blog', sv: 'Blogg', 'zh-Hant': '部落格' };
---
<AppPageLayout
  title={`${app.data.name} ${titles[lang] ?? 'Blog'}`}
  lang={lang}
  appId={app.data.id}
  appName={app.data.name}
  appAccent={app.data.accentColor}
  pageKind="blog"
  pathWithoutLang={`/${app.data.id}/blog/`}
>
  <PostList posts={posts as any} lang={lang} appId={app.data.id} />
</AppPageLayout>
```

- [ ] **Step 5: Write `apps/web/src/pages/[lang]/[app]/blog/[...slug].astro`**

```astro
---
import { getCollection, render } from 'astro:content';
import BlogLayout from '../../../../layouts/BlogLayout.astro';

export async function getStaticPaths() {
  const apps = await getCollection('apps');
  const blog = await getCollection('blog');
  return blog.map((entry) => {
    const slug = entry.id.replace(/\.[^/.]+$/, '').replace(`.${entry.data.lang}`, '');
    return {
      params: { lang: entry.data.lang, app: entry.data.app, slug },
      props: { entry, app: apps.find((a) => a.data.id === entry.data.app)! },
    };
  });
}
const { entry, app } = Astro.props;
const { Content } = await render(entry);
const slug = entry.id.replace(/\.[^/.]+$/, '').replace(`.${entry.data.lang}`, '');
---
<BlogLayout
  title={entry.data.title}
  description={entry.data.description}
  date={entry.data.date}
  lang={entry.data.lang}
  appId={app.data.id}
  appName={app.data.name}
  appAccent={app.data.accentColor}
  pathWithoutLang={`/${app.data.id}/blog/${slug}/`}
>
  <Content />
</BlogLayout>
```

- [ ] **Step 6: Build**

```bash
cd apps/web && npm run build && cd ../..
```
Expected: build succeeds with blog index pages and individual post pages for all (lang, app, slug) triples.

- [ ] **Step 7: Commit**

```bash
git add apps/web/src/components/PostList.astro apps/web/src/components/PostMeta.astro apps/web/src/layouts/BlogLayout.astro apps/web/src/pages/[lang]/[app]/blog/
git commit -m "feat(redesign): blog index + post routes with PostList/BlogLayout"
```

### Task 22: Migrate manual content and add manual routes

**Files:**
- Create: `apps/web/src/pages/[lang]/[app]/manual/index.astro`
- Create: `apps/web/src/pages/[lang]/[app]/manual/[...slug].astro`
- Run migration in `--mode manual` for apps with manuals

- [ ] **Step 1: Run manual migration for relevant apps**

```bash
for dir in 1Take-support GitInflow-support SonicDNACollector-support simpleMIDIController-support; do
  ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY python3 scripts/migrate-to-md.py "$dir" --mode manual
done
```
Expected: manual pages migrated to `apps/web/src/content/manual/<app>/`.

- [ ] **Step 2: Write manual index route**

`apps/web/src/pages/[lang]/[app]/manual/index.astro`:
```astro
---
import { getCollection } from 'astro:content';
import AppPageLayout from '../../../../layouts/AppPageLayout.astro';
export async function getStaticPaths() {
  const apps = await getCollection('apps');
  const manual = await getCollection('manual');
  const groups = new Map<string, typeof manual>();
  for (const m of manual) {
    const key = `${m.data.lang}|${m.data.app}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key)!.push(m);
  }
  return Array.from(groups.entries()).map(([key, items]) => {
    const [lang, app] = key.split('|');
    return { params: { lang, app }, props: { items, app: apps.find((a) => a.data.id === app)!, lang } };
  });
}
const { items, app, lang } = Astro.props;
const titles: Record<string,string> = { en: 'Manual', ja: 'マニュアル', de: 'Handbuch', es: 'Manual', fr: 'Manuel', it: 'Manuale', ko: '매뉴얼', nl: 'Handleiding', 'pt-BR': 'Manual', sv: 'Manual', 'zh-Hant': '手冊' };
const sorted = items.sort((a, b) => a.data.order - b.data.order);
---
<AppPageLayout
  title={`${app.data.name} ${titles[lang] ?? 'Manual'}`}
  lang={lang}
  appId={app.data.id}
  appName={app.data.name}
  appAccent={app.data.accentColor}
  pageKind="manual"
  pathWithoutLang={`/${app.data.id}/manual/`}
>
  <ul class="manual-toc">
    {sorted.map((m) => {
      const slug = m.id.replace(/\.[^/.]+$/, '').replace(`.${lang}`, '');
      return <li><a href={`/${lang}/${app.data.id}/manual/${slug}/`}>{m.data.title}</a></li>;
    })}
  </ul>
</AppPageLayout>
<style>
  .manual-toc { list-style: none; padding: 0; }
  .manual-toc li { padding: 12px 0; border-bottom: 1px solid var(--border); }
  .manual-toc a { font-size: 1em; font-weight: 500; text-decoration: none; color: var(--text); }
  .manual-toc a:hover { text-decoration: underline; }
</style>
```

- [ ] **Step 3: Write manual post route**

`apps/web/src/pages/[lang]/[app]/manual/[...slug].astro`:
```astro
---
import { getCollection, render } from 'astro:content';
import AppPageLayout from '../../../../layouts/AppPageLayout.astro';

export async function getStaticPaths() {
  const apps = await getCollection('apps');
  const manual = await getCollection('manual');
  return manual.map((entry) => {
    const slug = entry.id.replace(/\.[^/.]+$/, '').replace(`.${entry.data.lang}`, '');
    return { params: { lang: entry.data.lang, app: entry.data.app, slug }, props: { entry, app: apps.find((a) => a.data.id === entry.data.app)! } };
  });
}
const { entry, app } = Astro.props;
const { Content } = await render(entry);
const slug = entry.id.replace(/\.[^/.]+$/, '').replace(`.${entry.data.lang}`, '');
---
<AppPageLayout
  title={entry.data.title}
  description={entry.data.description}
  lang={entry.data.lang}
  appId={app.data.id}
  appName={app.data.name}
  appAccent={app.data.accentColor}
  pageKind="manual"
  pathWithoutLang={`/${app.data.id}/manual/${slug}/`}
>
  <article class="prose"><Content /></article>
</AppPageLayout>
<style>
  .prose :global(h2) { margin-top: 28px; }
  .prose :global(p), .prose :global(ul) { margin-bottom: 14px; }
</style>
```

- [ ] **Step 4: Build, commit, push**

```bash
cd apps/web && npm run build && cd ../..
git add apps/web/src/content/manual/ apps/web/src/pages/[lang]/[app]/manual/
git commit -m "feat(redesign): migrate manual content + add manual routes"
git push
```
Expected: preview deploy succeeds with manual pages.

### Task 23: Build top page (`/[lang]/index.astro`)

**Files:**
- Create: `apps/web/src/pages/[lang]/index.astro`
- Create: `apps/web/src/pages/index.astro` (root redirect)

- [ ] **Step 1: Write `apps/web/src/pages/[lang]/index.astro`**

```astro
---
import { getCollection } from 'astro:content';
import RootLayout from '../../layouts/RootLayout.astro';
import AppCard from '../../components/AppCard.astro';

export async function getStaticPaths() {
  const LANGS = ['en','ja','de','es','fr','it','ko','nl','pt-BR','sv','zh-Hant'];
  return LANGS.map((lang) => ({ params: { lang }, props: { lang } }));
}
const { lang } = Astro.props;
const apps = (await getCollection('apps')).sort((a, b) => a.data.order - b.data.order);

const titles: Record<string, string> = {
  en: 'hakaru — Apps for Musicians & Creators',
  ja: 'hakaru — 音楽家・クリエイター向けアプリ',
  de: 'hakaru — Apps für Musiker & Kreative',
  es: 'hakaru — Apps para músicos y creadores',
  fr: 'hakaru — Applications pour musiciens et créateurs',
  it: 'hakaru — App per musicisti e creator',
  ko: 'hakaru — 음악가와 크리에이터를 위한 앱',
  nl: 'hakaru — Apps voor muzikanten en creators',
  'pt-BR': 'hakaru — Apps para músicos e criadores',
  sv: 'hakaru — Appar för musiker och kreatörer',
  'zh-Hant': 'hakaru — 給音樂人與創作者的應用程式',
};
const supportLabels: Record<string,string> = { en: 'Support', ja: 'サポート', de: 'Support', es: 'Soporte', fr: 'Support', it: 'Supporto', ko: '지원', nl: 'Support', 'pt-BR': 'Suporte', sv: 'Support', 'zh-Hant': '支援' };
---
<RootLayout title={titles[lang]} lang={lang} currentSection="home" pathWithoutLang="/">
  <div class="container">
    <header class="hero">
      <h1>hakaru</h1>
      <p class="subtitle">{titles[lang].replace('hakaru — ', '')}</p>
    </header>
    <div class="apps-grid">
      {apps.map((app) => (
        <AppCard
          app={{
            id: app.data.id,
            name: app.data.name,
            icon: app.data.icon,
            badge: app.data.badge,
            accentColor: app.data.accentColor,
            category: app.data.category[lang as keyof typeof app.data.category] ?? app.data.category.en,
            description: app.data.description[lang as keyof typeof app.data.description] ?? app.data.description.en,
            links: app.data.links,
          }}
          lang={lang}
          supportLabel={supportLabels[lang] ?? 'Support'}
        />
      ))}
    </div>
  </div>
</RootLayout>
<style>
  .hero { margin-bottom: 40px; }
  .hero h1 { font-size: 2.8em; margin-bottom: 10px; }
  .subtitle { color: var(--text-muted); font-size: 1.1em; }
  .apps-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  @media (max-width: 768px) { .apps-grid { grid-template-columns: 1fr; } }
</style>
```

- [ ] **Step 2: Write `apps/web/src/pages/index.astro` (root → default lang)**

```astro
---
return Astro.redirect('/en/');
---
```

- [ ] **Step 3: Build & commit**

```bash
cd apps/web && npm run build && cd ../..
git add apps/web/src/pages/[lang]/index.astro apps/web/src/pages/index.astro
git commit -m "feat(redesign): top page (per-lang index) with AppCard grid"
```

**P2 acceptance:** All 11 apps × 11 languages × {support, privacy, blog index, blog posts, manual where applicable} render on preview. Top page lists all apps with cards. No 404s on internal nav.

---

## Phase 3: Redirects, Sitemap, Link Check

### Task 24: Generate `_redirects` from legacy URLs

**Files:**
- Create: `scripts/build-redirects.py`
- Output: `apps/web/public/_redirects`

- [ ] **Step 1: Write `scripts/build-redirects.py`**

```python
#!/usr/bin/env python3
"""Generate _redirects mapping legacy URLs -> new Astro URLs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "apps" / "web" / "public" / "_redirects"
LANGS = ["en","ja","de","es","fr","it","ko","nl","pt-BR","sv","zh-Hant"]
APP_MAP = {
    "1Take-support":      "1take",
    "GitInflow-support":  "gitinflow",
    "SonicDNACollector-support": "sonicdna-collector",
    "SonicDNAEngine-support":    "sonicdna-engine",
    "simpleMIDIController-support": "simplemidi-controller",
    "TineModeler-support":      "tinemodeler",
    "M2DX-Core-support":        "m2dx-core",
    "M2DX-support":             "m2dx",
    "PeerClockMetronome-support":"peerclock-metronome",
    "ChatArchive-support":      "chatarchive",
    "tensync":                  "tensync",
}

EXISTING_HEADER = """# Case-sensitive URL redirects (lowercase -> correct case)
/1take-support/*              /1Take-support/:splat              301
/1take-support                /1Take-support/                    301
/chatarchive-support/*        /ChatArchive-support/:splat        301
/chatarchive-support          /ChatArchive-support/              301
/gitinflow-support/*          /GitInflow-support/:splat          301
/gitinflow-support            /GitInflow-support/                301
/m2dx-core-support/*          /M2DX-Core-support/:splat          301
/m2dx-core-support            /M2DX-Core-support/                301
/simplemidicontroller-support/*  /simpleMIDIController-support/:splat  301
/simplemidicontroller-support    /simpleMIDIController-support/        301
/sonicdnacollector-support/*  /SonicDNACollector-support/:splat  301
/sonicdnacollector-support    /SonicDNACollector-support/        301
/sonicdnaengine-support/*     /SonicDNAEngine-support/:splat     301
/sonicdnaengine-support       /SonicDNAEngine-support/           301
/tinemodeler-support/*        /TineModeler-support/:splat        301
/tinemodeler-support          /TineModeler-support/              301
"""

def main():
    lines = [EXISTING_HEADER, "", "# --- Redesign migration redirects ---"]
    for legacy_dir, app_id in APP_MAP.items():
        # support index
        lines.append(f"/{legacy_dir}/                 /en/{app_id}/                       301")
        for lang in LANGS:
            if lang == "en": continue
            lines.append(f"/{legacy_dir}/index-{lang}     /{lang}/{app_id}/                301")
        # privacy
        lines.append(f"/{legacy_dir}/privacy           /en/{app_id}/privacy/               301")
        for lang in LANGS:
            if lang == "en": continue
            lines.append(f"/{legacy_dir}/privacy-{lang}   /{lang}/{app_id}/privacy/        301")
        # blog (wildcard)
        lines.append(f"/{legacy_dir}/blog/en/*         /en/{app_id}/blog/:splat            301")
        for lang in LANGS:
            if lang == "en": continue
            lines.append(f"/{legacy_dir}/blog/{lang}/*    /{lang}/{app_id}/blog/:splat     301")
        # manual (wildcard)
        lines.append(f"/{legacy_dir}/manual/en/*       /en/{app_id}/manual/:splat          301")
        for lang in LANGS:
            if lang == "en": continue
            lines.append(f"/{legacy_dir}/manual/{lang}/*  /{lang}/{app_id}/manual/:splat   301")
        # changelog
        lines.append(f"/{legacy_dir}/changelog         /en/{app_id}/changelog/             301")
        for lang in LANGS:
            if lang == "en": continue
            lines.append(f"/{legacy_dir}/changelog-{lang} /{lang}/{app_id}/changelog/      301")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(lines)} lines)")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it and inspect**

```bash
python3 scripts/build-redirects.py
head -40 apps/web/public/_redirects
wc -l apps/web/public/_redirects
```
Expected: file generated with hundreds of redirect lines.

- [ ] **Step 3: Copy CNAME and robots into Astro `public/`**

```bash
cp CNAME apps/web/public/CNAME
cp robots.txt apps/web/public/robots.txt 2>/dev/null || true
```

- [ ] **Step 4: Build & commit**

```bash
cd apps/web && npm run build && cd ../..
git add scripts/build-redirects.py apps/web/public/_redirects apps/web/public/CNAME apps/web/public/robots.txt
git commit -m "feat(redesign): generate _redirects from legacy URLs + bring CNAME/robots.txt"
```

### Task 25: Verify sitemap output

**Files:** consumed: `@astrojs/sitemap` (already in config)

- [ ] **Step 1: Build and inspect generated sitemap**

```bash
cd apps/web && npm run build && cd ../..
ls apps/web/dist/sitemap-*.xml
head -30 apps/web/dist/sitemap-index.xml
```
Expected: `sitemap-index.xml` and one or more `sitemap-*.xml` exist with all generated URLs.

- [ ] **Step 2: Spot-check a few URLs**

```bash
grep "ja/m2dx" apps/web/dist/sitemap-0.xml
grep "zh-Hant/peerclock" apps/web/dist/sitemap-0.xml
```
Expected: present.

### Task 26: Run link checker

- [ ] **Step 1: Install lychee (one-time)**

```bash
brew install lychee 2>/dev/null || cargo install lychee
```
Expected: `lychee --version` works.

- [ ] **Step 2: Build site and check internal links**

```bash
cd apps/web && npm run build && cd ../..
lychee --offline apps/web/dist
```
Expected: 0 broken internal links. External links are not validated in `--offline` mode.

- [ ] **Step 3: Fix any reported broken links**

For each reported broken link, find the source MD file and fix or update the link map. Common causes:
- Slug mismatch between legacy and new
- Lang suffix in markdown link not stripped
- Manual content referring to relative `../` paths

- [ ] **Step 4: Commit fixes**

```bash
git add apps/web/src/content/
git commit -m "fix(redesign): broken internal link cleanup after lychee scan"
```

### Task 27: Run migration QA diff

**Files:**
- Create: `scripts/check-migration.py`

- [ ] **Step 1: Write `scripts/check-migration.py`**

```python
#!/usr/bin/env python3
"""Compare word/link counts between legacy HTML and migrated Markdown.

Usage: python3 scripts/check-migration.py
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
APP_MAP = {
    "1Take-support": "1take", "GitInflow-support": "gitinflow",
    "SonicDNACollector-support": "sonicdna-collector", "SonicDNAEngine-support": "sonicdna-engine",
    "simpleMIDIController-support": "simplemidi-controller", "TineModeler-support": "tinemodeler",
    "M2DX-Core-support": "m2dx-core", "M2DX-support": "m2dx",
    "PeerClockMetronome-support": "peerclock-metronome",
}
SUPPORT_DIR = ROOT / "apps" / "web" / "src" / "content" / "support"

def words(text):
    return len(re.findall(r"\w+", text))

def links(text):
    return len(re.findall(r"\]\([^)]+\)|<a [^>]*href=", text))

print(f"{'app':22} {'lang':6} {'sec':8} {'old_w':>6} {'new_w':>6} {'Δw':>5} {'old_l':>5} {'new_l':>5}")
print("-" * 70)

for legacy, app_id in APP_MAP.items():
    src_dir = ROOT / legacy
    if not src_dir.is_dir(): continue
    for html in sorted(src_dir.glob("*.html")):
        if html.name.startswith("blog"): continue
        section = "support" if html.name.startswith("index") else html.name.split("-")[0].split(".")[0]
        m = re.match(r"(?:index|privacy|terms|changelog)(?:-([a-zA-Z-]+))?\.html$", html.name)
        lang = (m.group(1) if m and m.group(1) else "en")
        soup = BeautifulSoup(html.read_text(encoding="utf-8"), "html.parser")
        body = soup.select_one(".content") or soup.body
        old_text = body.get_text(" ", strip=True) if body else ""
        old_w, old_l = words(old_text), len(body.find_all("a")) if body else 0
        md_path = SUPPORT_DIR / app_id / f"{'index' if section == 'support' else section}.{lang}.md"
        if not md_path.exists():
            print(f"{app_id:22} {lang:6} {section:8}    --     --   --     --     --   MISSING")
            continue
        new_text = md_path.read_text(encoding="utf-8")
        new_w, new_l = words(new_text), links(new_text)
        delta = new_w - old_w
        warn = "  ⚠" if abs(delta) > old_w * 0.2 and old_w > 50 else ""
        print(f"{app_id:22} {lang:6} {section:8} {old_w:6d} {new_w:6d} {delta:+5d} {old_l:5d} {new_l:5d}{warn}")
```

- [ ] **Step 2: Run and review**

```bash
python3 scripts/check-migration.py
```
Expected: word counts within ±20% (Markdown is denser; small reductions are normal). Investigate any rows flagged with ⚠ or "MISSING".

- [ ] **Step 3: Commit script**

```bash
git add scripts/check-migration.py
git commit -m "tools: migration QA diff (word/link count old vs new)"
```

**P3 acceptance:** `_redirects` generated, sitemap output looks correct, lychee reports 0 broken internal links, migration QA diff shows no surprises.

---

## Phase 4: Cutover to `main`

### Task 28: Update Cloudflare Pages build config for the new layout

**Files:** Cloudflare Pages dashboard (no repo file change here, but document it)

- [ ] **Step 1: Document the dashboard change**

Create `apps/web/CLOUDFLARE.md` (a runbook):
````markdown
# Cloudflare Pages Settings

After merging `redesign` to `main`, update these in the Cloudflare Pages project:

- Build command: `cd apps/web && npm ci && npm run build`
- Build output directory: `apps/web/dist`
- Production branch: `main`
- Node.js version env: `NODE_VERSION=20`

The `_redirects` file is at `apps/web/public/_redirects` and gets copied into the build output automatically.
````

- [ ] **Step 2: Commit the runbook**

```bash
git add apps/web/CLOUDFLARE.md
git commit -m "docs(redesign): Cloudflare Pages cutover runbook"
git push
```

### Task 29: Final preview QA

- [ ] **Step 1: Smoke-test priority pages on preview**

Manually open in browser (`https://redesign.hakaru-net.pages.dev/...`):

- `/ja/`, `/en/`, `/de/`, `/zh-Hant/` (top page)
- `/ja/m2dx/`, `/en/m2dx/privacy/`
- `/ja/m2dx-core/`, `/en/m2dx-core/blog/`, `/ja/m2dx-core/blog/2026-04-23-dx7-swift-reimplementation/`
- `/de/peerclock-metronome/`, `/zh-Hant/peerclock-metronome/`
- `/ja/1take/manual/`
- A couple of legacy URLs to confirm 301: `/M2DX-support/index-ja` → `/ja/m2dx/`

Eyeball: typography, spacing, sidebar highlight, lang switcher swaps page correctly, mobile drawer works at <768px.

- [ ] **Step 2: Note any visible regressions in `apps/web/CLOUDFLARE.md` "Known issues" and/or fix inline**

If the issue is a content bug (link, missing translation), fix and re-push. If it's a stylistic tweak, fix in the relevant component or `tokens.css`.

- [ ] **Step 3: Final commit**

```bash
git add -A apps/web/
git commit -m "fix(redesign): final QA pass adjustments" --allow-empty
git push
```

### Task 30: Cutover — merge to main

- [ ] **Step 1: Open PR**

```bash
gh pr create --title "Redesign hakaru.net (Astro + Warm Editorial Light)" \
  --body "$(cat <<'EOF'
## Summary
- Migrates 800+ HTML files to Astro with single source of truth
- Warm Editorial Light visual direction (#faf9f7 + per-app accents)
- 11-language i18n via astro:i18n
- Content collections (support / privacy / blog / manual)
- Generated _redirects (legacy URLs → new) for 301 coverage
- Cloudflare Pages: build cmd `cd apps/web && npm ci && npm run build`, output `apps/web/dist`

## Test plan
- [x] Cloudflare preview deploy (`redesign.hakaru-net.pages.dev`) renders all pages
- [x] Top page (11 langs) shows all apps
- [x] Sidebar nav + lang switcher work
- [x] Legacy URLs return 301 to new URLs
- [x] Sitemap generated; lychee reports 0 broken internal links

## Cutover steps (after merge)
1. Update Cloudflare Pages: build command + output dir + production branch (see apps/web/CLOUDFLARE.md)
2. Verify production URL renders new design
3. Spot-check 5 high-traffic legacy URLs return 301

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 2: Review the PR diff in your browser, then merge**

After your own approval, merge via `gh pr merge --squash` or via the GitHub UI.

- [ ] **Step 3: Update Cloudflare Pages production settings**

In the Cloudflare dashboard:
- Build command: `cd apps/web && npm ci && npm run build`
- Build output directory: `apps/web/dist`
- Production branch: `main`
- Trigger a fresh production deploy

- [ ] **Step 4: Smoke-test production**

Open https://hakaru.net/ja/m2dx/ and confirm new design serves. Check 3 legacy URLs (`/M2DX-support/index-ja`, `/PeerClockMetronome-support/`, `/1Take-support/blog/en/`) all 301 to the right new URL.

- [ ] **Step 5: Delete old top-level directories from `main`**

After production confirmation, remove the legacy directories that have been fully replaced:

```bash
git rm -r 1Take-support GitInflow-support SonicDNACollector-support SonicDNAEngine-support \
         simpleMIDIController-support TineModeler-support M2DX-Core-support M2DX-support \
         PeerClockMetronome-support ChatArchive-support tensync \
         index.html index-*.html assets sitemap.xml _redirects scripts/sidebar-*.json \
         scripts/sidebar-script.js scripts/transform.py scripts/update-sidebar.py
git commit -m "chore(redesign): remove legacy HTML files now served from apps/web"
git push
```
**Note:** `M2DX/privacy-policy.html` (App Store legal redirect) is **kept** — leave that file in place.
**Note:** `tasks/`, `oauth/`, `docs/`, `tokushoho.html` are kept (out of scope per spec).

- [ ] **Step 6: Final production smoke test**

```bash
curl -sI https://hakaru.net/M2DX-support/index-ja | head -3
curl -sI https://hakaru.net/ja/m2dx/ | head -3
```
Expected: first returns `301`, second returns `200`.

**P4 acceptance:** Production serves new design at `hakaru.net`. All legacy URLs 301 to their new equivalents. No 5xx errors. Cloudflare Pages dashboard shows the new build settings.

---

## Out of scope reminder

- `tasks/`, `oauth/`, `docs/`, `tokushoho.html`, `M2DX/privacy-policy.html` are preserved untouched
- Existing GA tracking ID (`G-N0830V28FD`) is reused
- Pre-existing case-insensitive `_redirects` rules carried forward in `build-redirects.py`

## Rollback

If production breaks after Task 30:
1. Cloudflare Pages dashboard → Deployments → Previous deployment → "Promote to production" (1 click).
2. Investigate offline. Don't revert the merge until the root cause is understood.
