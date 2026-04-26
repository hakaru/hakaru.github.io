# hakaru.net Redesign — Design Spec

**Date:** 2026-04-26
**Author:** hakaru (with Claude Opus 4.7)
**Status:** Draft → Ready for review

## Goal

Modernize hakaru.net visually and structurally. Replace 800+ hand-maintained HTML files with a single Astro project, unify the visual language to a "Warm Editorial Light" direction, and eliminate the per-page CSS duplication and the Python-based sidebar regeneration step.

## Visual direction (approved)

**Warm Editorial Light** — off-white background (#faf9f7), neutral grays, per-app brand color used as accent. Inspirations: Anthropic, Substack, Notion, Apple Developer docs.

### Design tokens (`src/styles/tokens.css`)

```css
--bg            : #faf9f7;
--bg-subtle     : #f5f4f1;
--bg-card       : #ffffff;
--border        : #e7e5e4;
--border-strong : #d6d3d1;
--text          : #18181b;
--text-muted    : #57534e;
--text-subtle   : #78716c;
--accent        : #18181b;   /* default CTA */
/* per-app accent injected via app metadata: M2DX #e94560, PeerClock #00bcd4, etc. */
```

### Typography

- Base: `-apple-system, BlinkMacSystemFont, "Inter", system-ui, sans-serif`
- Japanese fallback: `"Hiragino Sans", "Noto Sans JP"`
- Headings: `letter-spacing: -0.025em`, `font-weight: 700`

## Architecture

### Tech stack

- **SSG:** Astro (latest)
- **i18n:** `astro:i18n` with locales `['en','ja','de','es','fr','it','ko','nl','pt-BR','sv','zh-Hant']`, default `'en'`
- **Content:** Astro Content Collections (typed Markdown)
- **Hosting:** Cloudflare Pages (current)
- **Build:** Node 20+, `npm run build` → static `dist/`

### Project layout

```
hakaru.github.io/
├── apps/web/                            ← Astro project
│   ├── src/
│   │   ├── content/
│   │   │   ├── apps/                    ← app metadata (icon, badge, links)
│   │   │   │   ├── m2dx.json
│   │   │   │   ├── m2dx-core.json
│   │   │   │   └── ...
│   │   │   ├── support/
│   │   │   │   └── m2dx/
│   │   │   │       ├── index.ja.md
│   │   │   │       ├── index.en.md
│   │   │   │       ├── privacy.ja.md
│   │   │   │       └── ...
│   │   │   ├── blog/
│   │   │   │   └── m2dx-core/
│   │   │   │       └── 2026-04-23-dx7-swift-reimplementation.ja.md
│   │   │   └── manual/
│   │   │       └── 1take/...
│   │   ├── components/
│   │   │   ├── Sidebar.astro
│   │   │   ├── LangSwitcher.astro
│   │   │   ├── AppCard.astro
│   │   │   ├── FeatureCard.astro
│   │   │   ├── StatusCard.astro
│   │   │   ├── TestFlightCTA.astro
│   │   │   ├── AppStoreCTA.astro
│   │   │   ├── PostList.astro
│   │   │   └── PostMeta.astro
│   │   ├── layouts/
│   │   │   ├── RootLayout.astro
│   │   │   ├── AppPageLayout.astro
│   │   │   └── BlogLayout.astro
│   │   ├── pages/
│   │   │   └── [lang]/
│   │   │       ├── index.astro          ← /[lang]/  (top page)
│   │   │       ├── m2dx/
│   │   │       │   ├── index.astro      ← /[lang]/m2dx/
│   │   │       │   ├── privacy.astro
│   │   │       │   └── blog/[...slug].astro
│   │   │       └── ...
│   │   ├── styles/
│   │   │   ├── tokens.css
│   │   │   └── global.css
│   │   └── content.config.ts            ← Content Collection schemas
│   ├── public/
│   │   ├── _redirects                   ← Cloudflare Pages redirects
│   │   ├── CNAME
│   │   ├── robots.txt
│   │   ├── assets/                      ← icons, logos (current /assets/ moved here)
│   │   └── apps/<app>/                  ← per-app icons reorganized
│   ├── astro.config.mjs
│   └── package.json
└── (existing top-level files preserved during transition;
   removed once redesign is on main and verified)
```

### URL scheme

- Top: `/` redirects to `/[detected-lang]/` (or `/en/`)
- App support: `/{lang}/{app}/` (e.g., `/ja/m2dx/`)
- Privacy: `/{lang}/{app}/privacy`
- Blog: `/{lang}/{app}/blog/{slug}`
- Manual: `/{lang}/{app}/manual/{slug}`
- `astro:i18n` emits `<link rel="alternate" hreflang="...">` for all 11 locales automatically

### Content collection schemas (`content.config.ts`)

```ts
const apps = defineCollection({
  type: 'data',
  schema: z.object({
    id: z.string(),
    name: z.string(),
    icon: z.string(),                    // path under /assets/
    badge: z.enum(['NEW', 'COMING', 'TESTFLIGHT']).optional(),
    accentColor: z.string(),             // e.g. '#e94560'
    category: z.record(z.string()),      // {en: 'Music · Synth', ja: '音楽 · シンセ', ...}
    description: z.record(z.string()),
    links: z.object({
      appStore: z.string().optional(),
      testFlight: z.string().optional(),
      github: z.string().optional(),
    }),
  }),
});

const support = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    lang: z.string(),
    app: z.string(),
    section: z.enum(['support', 'privacy', 'terms', 'changelog']),
    date: z.date().optional(),
  }),
});

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    lang: z.string(),
    app: z.string(),
    date: z.date(),
    tags: z.array(z.string()).optional(),
  }),
});
```

## Components

### `<Sidebar>`

- Width: 220px desktop, drawer on mobile (<768px)
- Auto-built from `apps` content collection — no manual JSON list
- Current app expanded showing sub-links (`Support` / `Privacy` / `Blog` / `Manual` per its config)
- Active app highlighted with 3px left border in app's accent color
- `<LangSwitcher>` at bottom: 11 language buttons keeping the current path in the new locale
- Replaces `scripts/update-sidebar.py` entirely

### `<AppCard>` (top page)

- White card on warm bg with 1px border
- App icon, name, optional badge (`NEW` / `COMING` / `TESTFLIGHT`)
- Category, description (per-locale)
- Primary CTA (App Store / TestFlight / GitHub) styled with app's accent color
- Secondary CTA (Support) styled with mono outline

### `<StatusCard>`

- Used by M2DX support page for the "Current Status — Why TestFlight" section
- Colored dot (per-app accent), small caps label, headline, body, optional CTA link
- Reusable for any "status / disclosure" need on other apps

### `<FeatureCard>`

- Small caps label (accent color), title, body in 2-col grid
- Replaces inline divs in current pages

## Migration pipeline

### `scripts/migrate-to-md.py`

Auto-converts existing HTML support pages to Markdown using Claude API (`claude-sonnet-4-6`).

**Steps per page:**
1. Read existing HTML
2. Extract `<div class="content">` body
3. Send to Claude with a precise prompt: "Convert this section to Markdown without changing meaning. Preserve code blocks, lists, tables, links, `<strong>` → `**`. Output only Markdown."
4. Build frontmatter from existing `<title>`, `og:description`, file path
5. Rewrite internal links via mapping table:
   - `/M2DX-support/index-ja` → `/ja/m2dx/`
   - `/M2DX-support/privacy-ja` → `/ja/m2dx/privacy`
   - (similar for all apps × 11 locales)
6. Write to `apps/web/src/content/support/<app>/<section>.<lang>.md`

**Parallelism:** ~10 concurrent API calls with rate limiting.

**Scope:**
| Type | Approx count | Output |
|---|---|---|
| Support index | 11 apps × 11 langs ≈ 120 | `support/<app>/index.<lang>.md` |
| Privacy / terms / changelog | varies | `support/<app>/<section>.<lang>.md` |
| Blog posts | several apps × 11 langs ≈ several hundred | `blog/<app>/<slug>.<lang>.md` |
| Manual pages | varies | `manual/<app>/<slug>.<lang>.md` |
| App metadata | 11 × 1 (manual authoring) | `apps/<app>.json` |

### Asset migration

- `assets/*` → `apps/web/public/assets/*` (paths preserved)
- Per-app icons in `1Take-support/assets/`, `PeerClockMetronome-support/assets/` → consolidated into `apps/web/public/apps/<app>/`

### Validation

- Word count / link count diff between old HTML and new MD per file (regression detection)
- Build all 11 locales × all pages
- Link checker (lychee) for dead links
- Manual eyeballing of M2DX, M2DX-Core, PeerClock pages first

## Redirects

`apps/web/public/_redirects` — generated by `scripts/build-redirects.py`:

```
# New: keep existing case-insensitive rules at the top

# Migration redirects (generated)
/M2DX-support/index-ja           /ja/m2dx/                         301
/M2DX-support/index-en           /en/m2dx/                         301
... (all 11 locales × all apps × {index, privacy, blog, manual})
```

Generator iterates all (app, locale, section) combinations and emits a 301 to the new URL. Existing case-insensitive rules at top of `_redirects` are preserved.

## Build & deploy

### Cloudflare Pages settings

- Build command: `cd apps/web && npm ci && npm run build`
- Output directory: `apps/web/dist`
- Production branch (initially): `redesign`
- Production branch (post-cutover): `main`
- Node.js version: 20

### Branch strategy

1. Work on `redesign` branch
2. Cloudflare Pages preview deploys per push (`redesign.hakaru-net.pages.dev`)
3. Validate full preview
4. Merge `redesign` → `main` (single PR)
5. Cloudflare auto-deploys `main` to production

### Rollback

- Pre-merge: discard `redesign` branch
- Post-merge: Cloudflare Pages "redeploy previous" (1-click rollback)

## Phase plan

| Phase | Scope | Estimate | Done when |
|---|---|---|---|
| **P0** | Astro scaffold, design tokens, core components, M2DX page hand-built | 1 day | Single M2DX support page renders in new design on preview |
| **P1** | Migration script + M2DX, M2DX-Core, PeerClock auto-migrated (3 apps × 11 langs × index/privacy) | 1–2 days | 3 priority apps fully on new site in preview |
| **P2** | Remaining 8 apps + all blogs + all manuals migrated | 2 days | All pages render in preview |
| **P3** | Redirects generator + sitemap regen + link check | 0.5 day | 0 dead links, all old URLs return 301 |
| **P4** | Merge to main + production cutover + smoke test | 0.5 day | Production live, no regressions |

**Total: 5–6 days.**

## Out of scope

- `tensync/`, `tasks/`, `oauth/`, `docs/`, `M2DX/privacy-policy.html` (App Store legal redirect target — keep static)
- Existing GA tracking ID is reused
- Existing `_redirects` case-insensitive rules preserved
- ChatArchive's separate locale path style (`/zh-Hant/...` instead of suffix) — we will normalize to the new `/[lang]/chatarchive/...` pattern with redirects

## Open questions

None remaining at spec time. Implementation plan (created via writing-plans skill) will break the phases above into concrete tasks.

## Decisions log

- **Visual direction:** Warm Editorial Light (`#faf9f7` base, per-app accent colors)
- **SSG:** Astro
- **Migration strategy:** Parallel construction on `redesign` branch, single cutover merge to `main`
- **Content conversion:** Auto via Claude API, structure-only (do not touch human translation quality)
- **Blog scope:** All existing 11-language posts migrated
- **URL form:** Astro standard `/[lang]/[app]/...`
- **Redirects:** Full 301 via Cloudflare Pages `_redirects`
