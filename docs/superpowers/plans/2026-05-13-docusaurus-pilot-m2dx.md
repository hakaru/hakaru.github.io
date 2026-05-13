# Docusaurus パイロット (M2DX-support) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** M2DX-support の 22 ファイル (11 言語 × {index, privacy}) を Docusaurus 化して `/M2DX-docs/` にマウントし、既存 `/M2DX-support/` と並存運用する。

**Architecture:** `M2DX-docs-src/` に Docusaurus プロジェクトを作り、Cloudflare Pages 上で `scripts/assemble-dist.sh` が「既存静的ファイル全部 + Docusaurus build」を `dist/` に集約して配信する。既存ファイル・既存スクリプトには触れない。

**Tech Stack:** Docusaurus (latest) + TypeScript、Node 20+、Python 3 (BeautifulSoup4 + markdownify) for HTML→MD 変換、rsync ベースの bash assemble script、Cloudflare Pages。

**Reference spec:** `docs/superpowers/specs/2026-05-13-docusaurus-pilot-m2dx-design.md`

---

## File Structure

| File / Directory | Responsibility |
|---|---|
| `M2DX-docs-src/package.json` | Docusaurus deps & scripts |
| `M2DX-docs-src/docusaurus.config.ts` | サイト設定（baseUrl, i18n, navbar, gtag） |
| `M2DX-docs-src/sidebars.ts` | 2 項目のシンプルサイドバー |
| `M2DX-docs-src/tsconfig.json` | TS config（scaffold 既定） |
| `M2DX-docs-src/docs/index.md` | EN ホーム（`/M2DX-docs/`） |
| `M2DX-docs-src/docs/privacy.md` | EN プライバシー（`/M2DX-docs/privacy/`） |
| `M2DX-docs-src/i18n/<locale>/docusaurus-plugin-content-docs/current/index.md` | 各言語のホーム翻訳（10 ファイル） |
| `M2DX-docs-src/i18n/<locale>/docusaurus-plugin-content-docs/current/privacy.md` | 各言語のプライバシー翻訳（10 ファイル） |
| `M2DX-docs-src/src/css/custom.css` | primary color 上書きのみ |
| `M2DX-docs-src/static/img/m2dx-icon.png` | ヒーローアイコン |
| `M2DX-docs-src/.gitignore` | `build/`, `node_modules/` を除外 |
| `scripts/migrate-m2dx-to-md.py` | M2DX-support/*.html → Markdown 変換スクリプト |
| `scripts/assemble-dist.sh` | リポジトリ全体 + Docusaurus build → `dist/` に集約 |
| `.gitignore`（root） | `dist/`, `M2DX-docs-src/build/`, `M2DX-docs-src/node_modules/` を追記 |

**触らない**: `M2DX-support/`, `scripts/update-sidebar.py`, `scripts/transform.py`, `_redirects`, `CNAME`, `sitemap.xml`, 各 `index*.html`, 他アプリディレクトリ。

---

## Pre-flight: 環境確認とブランチ作成

### Task 0: 前提環境確認と `docusaurus-pilot` ブランチ作成

**Files:** なし

- [ ] **Step 1: 現在のブランチが clean か確認**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git status
```
Expected: 既に直前のスペックコミット `af346ac` が main にあり、untracked / modified ファイルなし。

- [ ] **Step 2: Node バージョン確認**

```bash
node --version
```
Expected: `v20.x.x` 以上（既に `v22.22.2` であることを確認済み）。

- [ ] **Step 3: rsync の存在確認**

```bash
which rsync
```
Expected: `/usr/bin/rsync` など何らかのパス。

- [ ] **Step 4: M2DX-support の 22 ファイル存在確認**

```bash
ls M2DX-support/index*.html M2DX-support/privacy*.html | wc -l
```
Expected: `22`

- [ ] **Step 5: `docusaurus-pilot` ブランチ作成**

```bash
git checkout -b docusaurus-pilot
git push -u origin docusaurus-pilot
```
Expected: ブランチ作成・push 完了。Cloudflare Pages のプレビュービルドがトリガされるが、初回は build 設定未変更なので既存静的サイトと同じ内容のプレビューが出るのが想定挙動。

---

## Phase 1: Docusaurus Scaffold

### Task 1: Docusaurus プロジェクトを `M2DX-docs-src/` に初期化

**Files:**
- Create: `M2DX-docs-src/` 配下のscaffold 一式（npm が自動生成）

- [ ] **Step 1: scaffold 実行**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
npx create-docusaurus@latest M2DX-docs-src classic --typescript
```
Expected: `M2DX-docs-src/` が作成され、`package.json`, `docusaurus.config.ts`, `sidebars.ts`, `docs/`, `blog/`, `src/`, `static/`, `tsconfig.json` などが入る。npm install まで自動で走る（数十秒〜数分）。

- [ ] **Step 2: scaffold 動作確認（オプション・後で消す）**

```bash
cd M2DX-docs-src
npm run start -- --no-open
```
Expected: localhost:3000 で Docusaurus デフォルトページが立ち上がる（"My Site" のホーム + tutorial-basics docs + blog）。Ctrl-C で停止。

- [ ] **Step 3: 不要な scaffold コンテンツを削除**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io/M2DX-docs-src
rm -rf blog
rm -rf docs/*
rm -rf src/pages/index.tsx
rm -rf src/components/HomepageFeatures
rm -f static/img/docusaurus.png static/img/docusaurus-social-card.jpg static/img/logo.svg
rm -f static/img/undraw_*.svg
```
Expected: blog/, docs 配下、デフォルトホームページ、HomepageFeatures コンポーネント、Docusaurus ロゴ画像が消える。

- [ ] **Step 4: `M2DX-docs-src/.gitignore` 確認**

scaffold が以下のような `.gitignore` を作っているはず:

```
# Dependencies
/node_modules

# Production
/build

# Generated files
.docusaurus
.cache-loader

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
```
Read で確認。なければ上記内容で作成。

- [ ] **Step 5: ルート `.gitignore` を追記**

ルート `.gitignore` を Read してから、以下を append:

```
# Docusaurus build artifacts
/dist/
/M2DX-docs-src/build/
/M2DX-docs-src/node_modules/
/M2DX-docs-src/.docusaurus/
```

- [ ] **Step 6: ベースラインコミット**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git add M2DX-docs-src/ .gitignore
git commit -m "$(cat <<'EOF'
chore(docusaurus): Docusaurus scaffold を M2DX-docs-src/ に追加

create-docusaurus@latest classic + typescript で生成。
デフォルト blog/, デフォルト docs, HomepageFeatures, デフォルトロゴ画像
は削除済み。ルート .gitignore に dist/, build/, node_modules/ 追記。

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```
Expected: scaffold 一式と .gitignore 更新がコミットされる。

---

### Task 2: `docusaurus.config.ts` を本番設定に書き換える

**Files:**
- Modify: `M2DX-docs-src/docusaurus.config.ts`

- [ ] **Step 1: 既存設定を確認**

```bash
cat M2DX-docs-src/docusaurus.config.ts
```
（scaffold が生成した内容を把握）

- [ ] **Step 2: 設定ファイルを以下の内容で完全に置き換える**

```typescript
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'M2DX',
  tagline: 'MIDI 2.0 + DX7-compatible FM synthesizer for iOS',
  favicon: 'img/favicon.ico',
  url: 'https://hakaru.net',
  baseUrl: '/M2DX-docs/',
  trailingSlash: true,
  organizationName: 'hakaru',
  projectName: 'hakaru.github.io',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'de', 'es', 'fr', 'it', 'ja', 'ko', 'nl', 'pt-BR', 'sv', 'zh-Hant'],
  },
  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          editUrl: undefined,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
        gtag: {
          trackingID: 'G-N0830V28FD',
          anonymizeIP: false,
        },
      } satisfies Preset.Options,
    ],
  ],
  themeConfig: {
    image: 'img/m2dx-icon.png',
    navbar: {
      title: 'M2DX',
      logo: {
        alt: 'M2DX',
        src: 'img/m2dx-icon.png',
      },
      items: [
        {
          href: '/M2DX-support/',
          label: 'Main site',
          position: 'right',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
      ],
    },
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
```
（Write でファイルを丸ごと置換）

- [ ] **Step 3: 型エラーがないか tsc で確認**

```bash
cd M2DX-docs-src
npx tsc --noEmit
```
Expected: エラーなし。もし型エラーが出る場合は import か satisfies 句のミスなので確認。

- [ ] **Step 4: コミット**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git add M2DX-docs-src/docusaurus.config.ts
git commit -m "$(cat <<'EOF'
chore(docusaurus): config に baseUrl=/M2DX-docs/, 11 言語 i18n, gtag を設定

- baseUrl: /M2DX-docs/
- i18n locales: en, de, es, fr, it, ja, ko, nl, pt-BR, sv, zh-Hant
- navbar に "Main site" -> /M2DX-support/ と localeDropdown
- gtag: G-N0830V28FD (既存と同じ ID)
- routeBasePath: '/' で docs ルートを baseUrl に直結

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: `sidebars.ts` を 2 項目に簡略化

**Files:**
- Modify: `M2DX-docs-src/sidebars.ts`

- [ ] **Step 1: ファイル内容を以下で置き換え**

```typescript
import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    {type: 'doc', id: 'index', label: 'Overview'},
    {type: 'doc', id: 'privacy', label: 'Privacy Policy'},
  ],
};

export default sidebars;
```
（Write で丸ごと置換）

- [ ] **Step 2: 型エラーがないか確認**

```bash
cd M2DX-docs-src && npx tsc --noEmit
```
Expected: エラーなし（このタスク時点では `docs/index.md` `docs/privacy.md` がまだ存在しないので Docusaurus 起動時はエラーになるが、tsc レベルでは型は通る）。

- [ ] **Step 3: コミット**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git add M2DX-docs-src/sidebars.ts
git commit -m "chore(docusaurus): sidebars.ts を index/privacy の 2 項目に簡略化

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: 仮 `docs/index.md` `docs/privacy.md` を作成して Docusaurus を起動できる状態にする

**Files:**
- Create: `M2DX-docs-src/docs/index.md`（仮）
- Create: `M2DX-docs-src/docs/privacy.md`（仮）

> このタスクの目的は「Docusaurus が起動するかをチェックする」ためのプレースホルダ作成。Task 8 の移行スクリプトで本物の内容に上書きする。

- [ ] **Step 1: 仮 `docs/index.md` 作成**

```markdown
---
title: M2DX
description: M2DX placeholder — to be replaced by migration script.
slug: /
---

# M2DX (placeholder)

This page will be generated by `scripts/migrate-m2dx-to-md.py`.
```

- [ ] **Step 2: 仮 `docs/privacy.md` 作成**

```markdown
---
title: Privacy Policy
description: Privacy placeholder — to be replaced by migration script.
slug: /privacy
---

# Privacy Policy (placeholder)

This page will be generated by `scripts/migrate-m2dx-to-md.py`.
```

- [ ] **Step 3: Docusaurus を起動できることを確認**

```bash
cd M2DX-docs-src
npm run start -- --no-open
```
Expected: localhost:3000/M2DX-docs/ がブラウザで見られる（手動で開く）。Overview / Privacy Policy がサイドバーに出る。エラーなし。Ctrl-C で停止。

- [ ] **Step 4: コミット**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git add M2DX-docs-src/docs/index.md M2DX-docs-src/docs/privacy.md
git commit -m "chore(docusaurus): 仮 index.md / privacy.md（移行スクリプトで上書きされる）

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Phase 2: コンテンツ移行

### Task 5: 移行スクリプト `scripts/migrate-m2dx-to-md.py` を作成

**Files:**
- Create: `scripts/migrate-m2dx-to-md.py`

- [ ] **Step 1: 必要な Python パッケージを確認**

```bash
python3 -c "import bs4, markdownify" 2>&1
```
Expected: エラーなし、または `ModuleNotFoundError`。後者の場合:

```bash
pip3 install beautifulsoup4 markdownify
# または pyproject.toml/requirements.txt 管理派なら別途
```

- [ ] **Step 2: `scripts/migrate-m2dx-to-md.py` を Write で以下の内容で作成**

```python
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
        # hero icon
        icon = hero.select_one("img")
        if icon:
            alt = icon.get("alt", "M2DX")
            parts.append(f"![{alt}](/M2DX-docs/img/m2dx-icon.png)\n")
        # hero h1 は skip（front matter title と重複）
        # hero <p> tagline は本文先頭に出す
        tagline = hero.find("p")
        if tagline:
            parts.append(tagline.get_text(strip=True) + "\n")
        # TestFlight CTA
        cta = hero.select_one("a.testflight-cta")
        if cta:
            label = cta.get_text(strip=True)
            href = cta.get("href", "#")
            parts.append(f"\n[{label}]({href})\n")

    if content:
        # markdownify with heading_style=ATX
        parts.append(md(str(content), heading_style="ATX", strip=["script", "style"]))

    return "\n".join(parts)


def convert_admonitions(markdown: str) -> str:
    """Current Status section を `:::info ... :::` に変換。

    M2DX-support の各言語版は概ね以下の見出し構造を持つ:
      ## Current Status — Why TestFlight
      ## Aktueller Stand — Warum TestFlight
      ## Estado actual — Por qué TestFlight
      ...

    マーカーは "— Why TestFlight" / "— Warum TestFlight" 等の言語別表現で揺れるので、
    シンプルに「ヘッダー直後のセクションを admonition で括る」ではなく、
    ファイル内に対応する見出しが見つかったら、その見出しから次の同レベル見出しまでを
    admonition でラップする。
    """
    # 該当する見出しのキーワード（言語別、見出し本文に含まれるユニークな語）
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
        # ## を除いて見出し本文だけ抜き、admonition タイトルとして使う
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
```

- [ ] **Step 3: 実行権限を付与**

```bash
chmod +x scripts/migrate-m2dx-to-md.py
```

- [ ] **Step 4: EN/index だけで動作確認**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
python3 scripts/migrate-m2dx-to-md.py --lang en --page index
```
Expected:
```
  en       index    -> M2DX-docs-src/docs/index.md
Converted 1 file(s).
```

- [ ] **Step 5: 生成された MD を読んで内容確認**

```bash
cat M2DX-docs-src/docs/index.md
```
Expected:
- 先頭が `---` で title / description / slug が入っている
- `![M2DX](/M2DX-docs/img/m2dx-icon.png)` がある
- `[Join TestFlight](https://testflight.apple.com/...)` リンクがある
- `:::info ... :::` ブロックがある（"Current Status — Why TestFlight" セクションが admonition 化）
- `<style>` `<script>` が含まれていない
- `<` `>` の HTML タグが本文中に残っていない（言語例外的に `<br>` などが残るなら個別判断）

- [ ] **Step 6: コミット**

```bash
git add scripts/migrate-m2dx-to-md.py
git commit -m "$(cat <<'EOF'
feat(scripts): M2DX-support HTML を Docusaurus Markdown に変換するスクリプト

BeautifulSoup で .container > .hero と .content を抽出、markdownify で MD 化。
「Current Status — Why TestFlight」相当の見出し（11 言語別表現対応）は
::: info admonition でラップする。

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: 全 22 ファイルを一括変換し、ベースラインを作る

**Files:**
- Overwrite: `M2DX-docs-src/docs/index.md`, `M2DX-docs-src/docs/privacy.md`（Task 4 のプレースホルダ）
- Create: `M2DX-docs-src/i18n/<10 locales>/docusaurus-plugin-content-docs/current/{index,privacy}.md`

- [ ] **Step 1: 全 22 ファイルを変換**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
python3 scripts/migrate-m2dx-to-md.py
```
Expected:
```
  en       index    -> M2DX-docs-src/docs/index.md
  en       privacy  -> M2DX-docs-src/docs/privacy.md
  de       index    -> M2DX-docs-src/i18n/de/.../index.md
  ...
  zh-Hant  privacy  -> M2DX-docs-src/i18n/zh-Hant/.../privacy.md

Converted 22 file(s).
```

- [ ] **Step 2: ファイル数の検証**

```bash
find M2DX-docs-src/docs -name '*.md' | wc -l
find M2DX-docs-src/i18n -name '*.md' | wc -l
```
Expected: docs 配下 `2`、i18n 配下 `20`、合計 `22`。

- [ ] **Step 3: front matter が全ファイルにあるか確認**

```bash
for f in $(find M2DX-docs-src/docs M2DX-docs-src/i18n -name '*.md'); do
  head -1 "$f" | grep -q '^---$' || echo "MISSING FRONT MATTER: $f"
done
```
Expected: 出力なし（全ファイルに front matter がある）。

- [ ] **Step 4: `<style>` `<script>` が残っていないことを確認**

```bash
grep -rE '<(style|script)\b' M2DX-docs-src/docs M2DX-docs-src/i18n && echo "FOUND LEFTOVERS" || echo "OK"
```
Expected: `OK`

- [ ] **Step 5: コミット**

```bash
git add M2DX-docs-src/docs/ M2DX-docs-src/i18n/
git commit -m "$(cat <<'EOF'
feat(docusaurus): M2DX-support の 22 HTML から MD 22 本を初期生成

11 言語 × {index, privacy} = 22 ファイル。
scripts/migrate-m2dx-to-md.py の出力をそのままコミット（後段で手直し）。

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: EN 版を全文目視確認・必要に応じて手直し

**Files:**
- Edit: `M2DX-docs-src/docs/index.md`（必要なら）
- Edit: `M2DX-docs-src/docs/privacy.md`（必要なら）

- [ ] **Step 1: Docusaurus を起動**

```bash
cd M2DX-docs-src
npm run start -- --no-open
```

- [ ] **Step 2: ブラウザで開いて EN 全文確認**

http://localhost:3000/M2DX-docs/ と http://localhost:3000/M2DX-docs/privacy/ を開く。
チェック項目:
- ヒーローアイコンが表示される（404 ならパスを Task 9 のアイコン配置で対応する／Task 9 がまだ走っていなければ画像エラーは想定内）
- 「Join TestFlight」リンクが見える
- `:::info` admonition が青いボックスで表示される
- 見出し階層（h2/h3）が崩れていない
- 文字化けなし
- 内部リンク（既存 HTML 内で `#section-id` を使っていれば）が残骸として残ってないか

- [ ] **Step 3: 問題があれば該当 MD を Edit で直接修正**

例: admonition が壊れる、HTML タグが残る、リンクが壊れる、画像が出ない。

- [ ] **Step 4: Docusaurus サーバを停止 (Ctrl-C) してコミット**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git status
# 何か直していたら:
git add M2DX-docs-src/docs/
git commit -m "fix(docusaurus): EN 版 index/privacy の目視レビュー反映

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```
Expected: 直しが無ければコミット不要、ある場合は記録に残す。

---

### Task 8: JA / DE をブラウザ目視、他 8 言語は構造 diff で検証

**Files:**
- Edit: `M2DX-docs-src/i18n/*/docusaurus-plugin-content-docs/current/*.md`（必要に応じて）

- [ ] **Step 1: JA を起動して確認**

```bash
cd M2DX-docs-src
npm run start -- --locale ja --no-open
```
http://localhost:3000/M2DX-docs/ja/ と http://localhost:3000/M2DX-docs/ja/privacy/ を開く。
EN と同じチェック項目で確認。Ctrl-C で停止。

- [ ] **Step 2: DE を起動して確認**

```bash
npm run start -- --locale de --no-open
```
同様に確認。Ctrl-C で停止。

- [ ] **Step 3: 残り 8 言語の構造 diff**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
for lang in es fr it ko nl pt-BR sv zh-Hant; do
  for page in index privacy; do
    en_file="M2DX-docs-src/docs/${page}.md"
    lang_file="M2DX-docs-src/i18n/${lang}/docusaurus-plugin-content-docs/current/${page}.md"
    en_h=$(grep -c '^##' "$en_file")
    en_links=$(grep -oE '\[.+?\]\(http' "$en_file" | wc -l | tr -d ' ')
    lang_h=$(grep -c '^##' "$lang_file")
    lang_links=$(grep -oE '\[.+?\]\(http' "$lang_file" | wc -l | tr -d ' ')
    printf "%-8s %-8s  h2:%d/%d  links:%d/%d\n" "$lang" "$page" "$lang_h" "$en_h" "$lang_links" "$en_links"
  done
done
```
Expected: h2 数とリンク数が EN とほぼ同じ（±1 程度）。大幅にズレる言語があれば Task 8 Step 4 へ。

- [ ] **Step 4: 怪しい言語があればブラウザ確認 + 手直し**

該当言語の MD を Edit で修正。

- [ ] **Step 5: コミット**

```bash
git status
# 修正があれば:
git add M2DX-docs-src/i18n/
git commit -m "fix(docusaurus): 多言語版 MD の目視レビュー反映

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Phase 3: Assets & Theme

### Task 9: M2DX アイコン画像を Docusaurus static に配置 + favicon

**Files:**
- Create: `M2DX-docs-src/static/img/m2dx-icon.png`
- Create: `M2DX-docs-src/static/img/favicon.ico`（既存 assets から）

- [ ] **Step 1: 既存サイト内の M2DX アイコン候補を探す**

```bash
find /Users/hakaru/DEVELOP/hakaru.github.io/assets /Users/hakaru/DEVELOP/hakaru.github.io/M2DX-support -name '*.png' -o -name '*.jpg' -o -name '*.svg' | xargs ls -la 2>/dev/null
```
Expected: M2DX のアイコンファイル名と場所が出る。

- [ ] **Step 2: HTML 内で参照されているアイコンパスを確認**

```bash
grep -h 'hero-icon\|src=' M2DX-support/index.html | grep -i 'm2dx\|icon' | head -5
```
Expected: `<img src="...">` の src が出る。アイコンファイルが既存リポジトリ内のどこにあるか把握。

- [ ] **Step 3: アイコンを Docusaurus static にコピー**

```bash
# ファイルパスは Step 1-2 で判明したものを使う。例:
cp assets/M2DX/icon.png M2DX-docs-src/static/img/m2dx-icon.png
```
Expected: `M2DX-docs-src/static/img/m2dx-icon.png` が存在する。

- [ ] **Step 4: favicon もコピー（または scaffold デフォルトを差し替え）**

scaffold が用意した `static/img/favicon.ico` が `Docusaurus` のもの。M2DX アイコンを favicon に流用するか、既存 `assets/` 内に favicon があればそれを使う。

```bash
ls assets/*.ico 2>/dev/null
# あれば: cp assets/favicon.ico M2DX-docs-src/static/img/favicon.ico
# なければ: docusaurus デフォルトの favicon.ico は放置（後で差し替え）
```

- [ ] **Step 5: ローカル確認**

```bash
cd M2DX-docs-src
npm run start -- --no-open
```
ブラウザで `/M2DX-docs/` を開き、ヒーローアイコンとブラウザタブのファビコンを確認。Ctrl-C で停止。

- [ ] **Step 6: コミット**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git add M2DX-docs-src/static/img/
git commit -m "chore(docusaurus): M2DX アイコンと favicon を static/img/ に配置

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 10: `custom.css` で primary color のみ M2DX 赤 (#e94560) に上書き

**Files:**
- Modify: `M2DX-docs-src/src/css/custom.css`

- [ ] **Step 1: 既存 custom.css の中身を確認**

```bash
cat M2DX-docs-src/src/css/custom.css
```
scaffold が `--ifm-color-primary` 系の CSS 変数を定義している。

- [ ] **Step 2: primary color を `#e94560` 系に置き換え**

ファイル先頭の `:root` ブロックを以下に書き換える（Edit で `--ifm-color-primary` 関連の行を差し替え）:

```css
:root {
  --ifm-color-primary: #e94560;
  --ifm-color-primary-dark: #e63357;
  --ifm-color-primary-darker: #d92a4d;
  --ifm-color-primary-darkest: #b62240;
  --ifm-color-primary-light: #ec5871;
  --ifm-color-primary-lighter: #ed617a;
  --ifm-color-primary-lightest: #f1849a;
  --ifm-code-font-size: 95%;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.1);
}

[data-theme='dark'] {
  --ifm-color-primary: #ec5871;
  --ifm-color-primary-dark: #e94560;
  --ifm-color-primary-darker: #e63357;
  --ifm-color-primary-darkest: #d92a4d;
  --ifm-color-primary-light: #ed617a;
  --ifm-color-primary-lighter: #f0708a;
  --ifm-color-primary-lightest: #f48fa3;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.3);
}
```

- [ ] **Step 3: ローカル確認**

```bash
cd M2DX-docs-src && npm run start -- --no-open
```
ブラウザでリンク色・ボタン色・サイドバーアクティブ色が赤系になっていることを確認。Ctrl-C で停止。

- [ ] **Step 4: コミット**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git add M2DX-docs-src/src/css/custom.css
git commit -m "style(docusaurus): primary color を M2DX 赤 (#e94560) に変更

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Phase 4: Assembly Pipeline

### Task 11: `scripts/assemble-dist.sh` を作成

**Files:**
- Create: `scripts/assemble-dist.sh`

- [ ] **Step 1: Write でスクリプトを作成**

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# 1. Docusaurus ビルド
echo "==> Building Docusaurus"
cd M2DX-docs-src
npm ci
npm run build
cd "$REPO_ROOT"

# 2. dist/ に既存静的ファイルを集約
echo "==> Assembling dist/"
rm -rf dist
mkdir -p dist
rsync -a \
  --exclude='dist/'                 \
  --exclude='M2DX-docs-src/'        \
  --exclude='node_modules/'         \
  --exclude='.git/'                 \
  --exclude='.github/'              \
  --exclude='.claude/'              \
  --exclude='.superpowers/'         \
  --exclude='docs/superpowers/'     \
  --exclude='tasks/'                \
  --exclude='__pycache__/'          \
  --exclude='*.pyc'                 \
  --exclude='AGENTS.md'             \
  ./ dist/

# 3. Docusaurus 成果物を /M2DX-docs/ に重ねる
echo "==> Overlaying M2DX-docs/"
mkdir -p dist/M2DX-docs
rsync -a M2DX-docs-src/build/ dist/M2DX-docs/

echo "==> Done"
ls dist/ | head -20
```

- [ ] **Step 2: 実行権限**

```bash
chmod +x scripts/assemble-dist.sh
```

- [ ] **Step 3: コミット**

```bash
git add scripts/assemble-dist.sh
git commit -m "$(cat <<'EOF'
feat(scripts): assemble-dist.sh — 既存サイト + Docusaurus build を dist/ に集約

Cloudflare Pages の build command として使う。npm ci → npm run build →
rsync で既存ファイルを dist/ にコピー → M2DX-docs-src/build/ を
dist/M2DX-docs/ に重ねる。

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 12: ローカルで end-to-end ビルド + 静的サーバ検証

**Files:** なし（検証のみ）

- [ ] **Step 1: ビルド実行**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
bash scripts/assemble-dist.sh
```
Expected:
- `==> Building Docusaurus` ログ出力
- `==> Assembling dist/` ログ出力
- `==> Overlaying M2DX-docs/` ログ出力
- 最後に `dist/` のディレクトリ一覧（index.html, M2DX-support/, M2DX-docs/, 他アプリディレクトリ等）

- [ ] **Step 2: dist/ の中身を検証**

```bash
test -f dist/index.html && echo "OK root index"
test -f dist/M2DX-support/index.html && echo "OK M2DX-support"
test -f dist/M2DX-docs/index.html && echo "OK M2DX-docs EN"
test -d dist/M2DX-docs/ja && echo "OK M2DX-docs JA"
test -f dist/_redirects && echo "OK _redirects"
test -f dist/CNAME && echo "OK CNAME"
! test -d dist/M2DX-docs-src && echo "OK src not leaked"
! test -d dist/docs/superpowers && echo "OK spec/plan not leaked"
```
Expected: すべて `OK` 行が出る。

- [ ] **Step 3: 静的サーバで動作確認**

```bash
npx serve dist -p 8080 &
SERVE_PID=$!
sleep 2
```

別ターミナルまたは別コマンドで:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/                    # 既存トップ
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/M2DX-support/       # 既存
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/M2DX-docs/          # 新規 EN
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/M2DX-docs/ja/       # 新規 JA
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/M2DX-docs/privacy/  # 新規 privacy
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/1Take-support/      # 他アプリ無傷
```
Expected: すべて `200` （`serve` は trailing slash 周りで挙動が違う場合あるので、必要に応じて `/M2DX-docs/index.html` で再確認）。

- [ ] **Step 4: serve を停止**

```bash
kill $SERVE_PID
```

- [ ] **Step 5: ブラウザで /M2DX-docs/ を実際に開いて確認**

```bash
npx serve dist -p 8080
# ブラウザで http://localhost:8080/M2DX-docs/ を開く
# locale dropdown で言語切替テスト
# 「Main site」リンクが /M2DX-support/ に飛ぶことを確認（serve でも動く）
# Ctrl-C で停止
```

- [ ] **Step 6: コミット不要（dist/ は git ignored）**

このタスクの成果物はビルド検証のみ。

---

## Phase 5: Preview Deploy

### Task 13: ブランチを push して Cloudflare Pages プレビュー確認

**Files:** なし

- [ ] **Step 1: 現在のブランチが docusaurus-pilot であることを確認**

```bash
git branch --show-current
```
Expected: `docusaurus-pilot`

- [ ] **Step 2: push**

```bash
git push origin docusaurus-pilot
```
Expected: push 成功。Cloudflare Pages のプレビュービルドが自動トリガ。

- [ ] **Step 3: Cloudflare Pages ダッシュボードでビルド状況を確認**

ブラウザで Cloudflare Dashboard → Pages → プロジェクト → Deployments を開く。
`docusaurus-pilot` ブランチのデプロイが進行中 or 完了していることを確認。

**注意**: この時点では本番ビルド設定（Task 14）が未適用なので、プレビューは**現行設定**（コマンド空欄 / output `/`）で走る。つまりプレビュー URL を開いても `/M2DX-docs/` は出ない（既存静的サイトと同じ内容になる）。

これは想定挙動。Task 14 で設定変更してから再 push して初めて、プレビューに Docusaurus 成果物が出る。

- [ ] **Step 4: 現状の挙動を記録**

ダッシュボードでプレビュー URL を取得（`<sha>.hakaru-github-io.pages.dev` の形）。
ブラウザでそのプレビュー URL を開き、以下を確認:
- 既存トップが出る → OK（既存と同じ挙動）
- `/M2DX-docs/` を開く → 404 が出る → 想定挙動（次のタスクで解消）

---

### Task 14: Cloudflare Pages の本番ビルド設定を変更

**Files:** なし（Cloudflare Dashboard 操作）

> このタスクは Cloudflare Dashboard へのログイン操作。実装者（Hakaru さん）が手動実施。代わりに subagent が実施することはできない。

- [ ] **Step 1: Cloudflare Dashboard にログイン**

ブラウザで https://dash.cloudflare.com → 該当アカウント。

- [ ] **Step 2: Pages プロジェクト → Settings → Builds & deployments**

- [ ] **Step 3: Build configurations を変更**

| 項目 | 変更前 | 変更後 |
|---|---|---|
| Framework preset | None | None |
| Build command | （空欄） | `bash scripts/assemble-dist.sh` |
| Build output directory | `/` | `dist` |
| Root directory | `/` | `/`（変更なし） |
| Environment variables (Production) | — | `NODE_VERSION=20` を追加 |
| Environment variables (Preview) | — | `NODE_VERSION=20` を追加 |

- [ ] **Step 4: Save**

- [ ] **Step 5: docusaurus-pilot ブランチで再ビルドをトリガ**

Cloudflare Dashboard で「Retry deployment」または、ローカルで空コミットを push:

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git commit --allow-empty -m "chore(ci): retrigger CF Pages build after config change"
git push origin docusaurus-pilot
```

- [ ] **Step 6: ビルドログを Dashboard で確認**

`npm ci` → `npm run build` → rsync 各工程のログを確認。所要時間 2-5 分程度。
失敗した場合はログを Read してエラーを特定（典型例: rsync が無い、Node バージョン、npm install タイムアウト）。

- [ ] **Step 7: プレビュー URL で動作確認**

ダッシュボードで新しいプレビュー URL を取得し、ブラウザで以下を全部確認:

- [ ] `/` 既存トップが従来通り
- [ ] `/M2DX-support/` 既存サポートページが従来通り
- [ ] `/1Take-support/` `/ChatArchive-support/` `/MacSlowCooker-support/` など他アプリが従来通り
- [ ] `/m2dx-core-support/`（小文字）→ `/M2DX-Core-support/` への 301 リダイレクトが効く
- [ ] `/M2DX-docs/` で Docusaurus EN ホームが表示
- [ ] `/M2DX-docs/privacy/` で privacy 表示
- [ ] navbar の locale dropdown で 11 言語が切り替わる
- [ ] `/M2DX-docs/ja/` `/M2DX-docs/de/` `/M2DX-docs/zh-Hant/` が翻訳済みで表示
- [ ] navbar の「Main site」リンクが `/M2DX-support/` へ戻る
- [ ] DevTools の Network タブで `gtag` のリクエストが両側で発火

---

## Phase 6: Production Cutover

### Task 15: `main` にマージして本番反映

**Files:** なし

- [ ] **Step 1: main を最新化**

```bash
cd /Users/hakaru/DEVELOP/hakaru.github.io
git checkout main
git pull origin main
```
Expected: ロカル main が origin と同期。

- [ ] **Step 2: docusaurus-pilot を main にマージ**

```bash
git merge --no-ff docusaurus-pilot -m "$(cat <<'EOF'
Merge branch 'docusaurus-pilot'

M2DX-support の Docusaurus パイロット（/M2DX-docs/ にマウント、11 言語）を
本番に反映。既存 /M2DX-support/ は並存・無改変。

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```
Expected: マージコミット作成。

- [ ] **Step 3: push**

```bash
git push origin main
```
Expected: push 成功。Cloudflare Pages の**本番**ビルドが自動トリガ。

- [ ] **Step 4: ビルド完了を待つ**

Cloudflare Dashboard で本番デプロイの進行を確認。完了まで 2-5 分。

- [ ] **Step 5: 本番 URL で確認**

Task 14 Step 7 のチェックリストを `https://hakaru.net` で全項目再実施。
**全項目が通ったらパイロット完了**。

- [ ] **Step 6: ローカルブランチを残しておく**

```bash
# docusaurus-pilot ブランチは消さない（参照用に残す）
git branch | grep docusaurus-pilot
```

---

### Task 16: パイロット完了後の整理

**Files:** なし

- [ ] **Step 1: 既存 spec / plan の参照を確認**

```bash
ls docs/superpowers/specs/2026-05-13-docusaurus-pilot-m2dx-design.md
ls docs/superpowers/plans/2026-05-13-docusaurus-pilot-m2dx.md
```
両方存在することを確認。

- [ ] **Step 2: 観察したことを Hakaru さんに共有**

実装中・本番デプロイ後に気づいた以下の点をテキストで報告:
- 想定外だった事象（あれば）
- 翻訳の質で気になった言語（あれば）
- 次フェーズ（他アプリ横展開、blog 移行）に向けて引き継ぐべき注意点
- TestFlight CTA をプレーンリンクから装飾ボタンに昇格する必要性の判断材料

- [ ] **Step 3: 次フェーズの議論を別セッションで開始（出来事として記録のみ、本プランでは実装しない）**

横展開・カットオーバー方針・App Store URL 差し替え等は別 spec/plan で議論する。

---

## Self-Review Notes

- Spec カバレッジ: §1 (アーキテクチャ) → Task 11/12, §2 (リポジトリ構造) → Task 1, §3 (Docusaurus 設定) → Task 2/3, §4 (HTML→MD 移行) → Task 5/6/7/8, §5 (CF Pages 構成) → Task 11/14, §6 (テスト・カットオーバー) → Task 12/13/14/15 すべて対応。
- Out of scope はスペックの「スコープ外」セクションのまま、Task 16 Step 3 で次フェーズへの引き継ぎを明示。
- TDD は移行スクリプトに対して厳密適用していない（一回限りの ETL 的処理で、出力は Docusaurus レンダリングで検証する方が高効率なため）。代わりに Task 6 のステップ 3-4 で構造検証（front matter / leftover タグ）を実施。
- 型整合: `docusaurus.config.ts` の `i18n.locales` と `migrate-m2dx-to-md.py` の `LOCALES` リストが両方とも `['en', 'de', 'es', 'fr', 'it', 'ja', 'ko', 'nl', 'pt-BR', 'sv', 'zh-Hant']` で揃っていることを確認済み。
- プレースホルダなし。
