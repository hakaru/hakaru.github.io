# サポートページ統合 実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 6つの独立したサポート用リポジトリのコンテンツをメインリポジトリに統合し、デザインをダークテーマに統一する

**Architecture:** 各サポートリポジトリはJekyll（Markdown + Liquid）で構築されている。メインサイトは純粋な静的HTMLのため、Markdownコンテンツを静的HTMLに変換し、メインサイトと統一されたインラインCSSで配置する。共通のHTMLテンプレート構造を定義し、全サポートページに適用する。

**Tech Stack:** HTML, CSS (inline), GitHub Pages, Google Analytics (GA4)

---

## ファイル構造

### 新規作成ファイル

**SonicDNA Engine（パイロット）:**
```
SonicDNAEngine-support/
├── index.html              ← サポートトップ（英語）
├── index-ja.html           ← サポートトップ（日本語）
├── privacy.html            ← プライバシーポリシー（英語）
├── privacy-ja.html         ← プライバシーポリシー（日本語）
├── changelog.html          ← 更新履歴
├── assets/
│   └── app-icon.png        ← アプリアイコン
├── blog/
│   ├── en/
│   │   ├── index.html      ← ブログ一覧（英語）
│   │   └── 2026-03-10-introducing-sonicdna-engine/
│   │       └── index.html  ← ブログ記事
│   └── ja/
│       ├── index.html      ← ブログ一覧（日本語）
│       └── 2026-03-10-introducing-sonicdna-engine/
│           └── index.html  ← ブログ記事
```

以降のアプリも同様の構造で配置。各アプリの具体的なファイルはそれぞれのTaskで定義。

### 変更ファイル

```
index.html                  ← サポートリンクを相対パスに更新
```

---

## Task 1: 共通HTMLテンプレート構造の定義とSonicDNA Engine サポートトップページ作成

このタスクで共通テンプレートのパターンを確立し、以降の全ページに適用する。

**Files:**
- Create: `SonicDNAEngine-support/index.html`
- Create: `SonicDNAEngine-support/assets/app-icon.png`（ソースリポジトリからコピー）

### 共通テンプレート構造（全サポートページで使用）

全ページは以下のHTML構造に従う。ページごとに変わる部分はコメントで示す。

```html
<!DOCTYPE html>
<html lang="en"><!-- ページの言語に応じて "en" or "ja" -->
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><!-- ページタイトル --> | hakaru</title>
    <meta name="description" content="<!-- ページ説明文 -->">

    <!-- OGP -->
    <meta property="og:title" content="<!-- ページタイトル -->">
    <meta property="og:description" content="<!-- ページ説明文 -->">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://hakaru.net/<!-- パス -->">

    <!-- Google Analytics (統一ID) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-N0830V28FD"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-N0830V28FD');
    </script>

    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #e0e0e0;
            line-height: 1.7;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 60px 20px;
        }

        /* Back link */
        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #a0a0a0;
            text-decoration: none;
            font-size: 0.9em;
            margin-bottom: 30px;
            transition: color 0.3s;
        }
        .back-link:hover { color: #e94560; }

        /* Hero section */
        .hero {
            text-align: center;
            margin-bottom: 40px;
        }
        .hero-icon {
            width: 100px;
            height: 100px;
            border-radius: 22px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-bottom: 20px;
        }
        .hero h1 {
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #e94560, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hero p {
            color: #a0a0a0;
            font-size: 1.1em;
        }

        /* App Store link */
        .app-store-link {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 12px 20px;
            margin: 16px 0;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            text-decoration: none;
            color: #fff;
            transition: all 0.3s;
        }
        .app-store-link:hover {
            background: rgba(255,255,255,0.1);
            transform: translateY(-2px);
        }
        .app-store-link .app-icon-small {
            width: 50px;
            height: 50px;
            border-radius: 11px;
        }
        .app-store-text { font-size: 12px; line-height: 1.3; }
        .app-store-text .download { font-size: 16px; font-weight: 600; }

        /* Navigation */
        .support-nav {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            margin: 30px 0;
            padding: 20px 0;
            border-top: 1px solid rgba(255,255,255,0.1);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .support-nav a {
            color: #a0a0a0;
            text-decoration: none;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 0.9em;
            transition: all 0.3s;
        }
        .support-nav a:hover,
        .support-nav a.active {
            color: #fff;
            background: rgba(255,255,255,0.1);
        }

        /* Content sections */
        .content h2 {
            font-size: 1.4em;
            color: #fff;
            margin: 40px 0 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .content h3 {
            font-size: 1.1em;
            color: #e0e0e0;
            margin: 24px 0 12px;
        }
        .content p { margin-bottom: 16px; }
        .content ul, .content ol {
            margin: 0 0 16px 24px;
            color: #b0b0b0;
        }
        .content li { margin-bottom: 8px; }
        .content a {
            color: #e94560;
            text-decoration: none;
        }
        .content a:hover { text-decoration: underline; }
        .content code {
            background: rgba(255,255,255,0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }
        .content pre {
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 16px;
            overflow-x: auto;
            margin-bottom: 16px;
        }
        .content pre code {
            background: none;
            padding: 0;
        }
        .content table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 16px;
        }
        .content th, .content td {
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .content th {
            color: #fff;
            font-weight: 600;
        }
        .content td { color: #b0b0b0; }
        .content hr {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin: 30px 0;
        }

        /* Blog list */
        .blog-list { list-style: none; padding: 0; margin: 0; }
        .blog-list li {
            padding: 20px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .blog-list a {
            color: #fff;
            text-decoration: none;
            font-size: 1.1em;
            font-weight: 500;
        }
        .blog-list a:hover { color: #e94560; }
        .blog-date {
            color: #666;
            font-size: 0.85em;
            margin-top: 4px;
        }

        /* Footer */
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 0;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: #666;
            font-size: 0.9em;
        }
        footer a { color: #888; text-decoration: none; }
        footer a:hover { color: #e94560; }

        /* Responsive */
        @media (max-width: 600px) {
            .hero h1 { font-size: 1.5em; }
            .support-nav { gap: 4px; }
            .support-nav a { padding: 4px 10px; font-size: 0.8em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link">← hakaru Apps</a>

        <div class="hero">
            <img src="/SonicDNAEngine-support/assets/app-icon.png" alt="SonicDNA Engine" class="hero-icon">
            <h1>SonicDNA Engine</h1>
            <p><!-- アプリの説明文 --></p>
            <!-- App Store リンク（あれば） -->
        </div>

        <nav class="support-nav">
            <!-- 各アプリのナビゲーションリンク -->
        </nav>

        <div class="content">
            <!-- ページ固有コンテンツ -->
        </div>

        <footer>
            <p>© 2026 hakaru. All rights reserved.</p>
            <p style="margin-top: 10px;">
                <a href="/tokushoho.html">特定商取引法に基づく表記</a>
                <span style="margin: 0 10px;">|</span>
                <a href="mailto:hakaruapps-contact@hakaru.net">Contact</a>
            </p>
        </footer>
    </div>
</body>
</html>
```

- [ ] **Step 1: アプリアイコンを取得**

WebFetchでソースリポジトリの `app-icon.png` を取得するか、ローカルのソースリポジトリ `/Volumes/Dev/DEVELOP/hakaruapps/SonicDNAEngine-support/` からコピーする。

```bash
mkdir -p SonicDNAEngine-support/assets
cp /Volumes/Dev/DEVELOP/hakaruapps/SonicDNAEngine-support/assets/app-icon.png SonicDNAEngine-support/assets/
```

もしローカルにソースリポジトリがない場合は、別途クローンする:
```bash
cd /tmp && git clone https://github.com/hakaru/SonicDNAEngine-support.git
cp /tmp/SonicDNAEngine-support/assets/app-icon.png /Volumes/Dev/DEVELOP/hakaru.github.io/SonicDNAEngine-support/assets/
```

- [ ] **Step 2: SonicDNA Engine サポートトップ（英語）を作成**

`SonicDNAEngine-support/index.html` を作成する。上記の共通テンプレート構造を使用し、ソースリポジトリの `index.md` のMarkdownコンテンツをHTMLに変換して埋め込む。

**ページ固有の設定:**
- `lang="en"`
- `<title>SonicDNA Engine Support | hakaru</title>`
- `<meta name="description" content="Support page for SonicDNA Engine - IR/NAM Audio Processor & AUv3 Plugin for iOS">`
- ヒーロー説明文: `IR/NAM Audio Processor & AUv3 Plugin for iOS`
- App Store リンク: `#`（Coming Soon）
- ナビゲーション: Support(active) / サポート / Privacy / プライバシー / Blog / ブログ / Changelog

**コンテンツ:** ソースの `index.md` から以下のセクションをHTMLに変換:
- Overview, Key Features (NAM, IR, Effects, AUv3, Standalone, Preset), Use Cases, Setup Guide, Using the App, FAQ, Contact, Links

ソースのMarkdownコンテンツを読み取り、HTMLタグに変換する。見出し `##` → `<h2>`、`###` → `<h3>`、リスト → `<ul><li>`、テーブル → `<table>`、コードブロック → `<pre><code>` 等。

- [ ] **Step 3: ブラウザで表示確認**

```bash
open /Volumes/Dev/DEVELOP/hakaru.github.io/SonicDNAEngine-support/index.html
```

ダークテーマが正しく適用されていること、レイアウトが崩れていないこと、ナビリンクが正しいことを確認する。

- [ ] **Step 4: コミット**

```bash
git add SonicDNAEngine-support/
git commit -m "feat: add SonicDNA Engine support top page (EN) with unified dark theme"
```

---

## Task 2: SonicDNA Engine 残りのページを作成

**Files:**
- Create: `SonicDNAEngine-support/index-ja.html`
- Create: `SonicDNAEngine-support/privacy.html`
- Create: `SonicDNAEngine-support/privacy-ja.html`
- Create: `SonicDNAEngine-support/changelog.html`
- Create: `SonicDNAEngine-support/blog/en/index.html`
- Create: `SonicDNAEngine-support/blog/ja/index.html`
- Create: `SonicDNAEngine-support/blog/en/2026-03-10-introducing-sonicdna-engine/index.html`
- Create: `SonicDNAEngine-support/blog/ja/2026-03-10-introducing-sonicdna-engine/index.html`

全ページ共通: Task 1で定義した共通テンプレート構造を使用。GA IDは `G-N0830V28FD`。

- [ ] **Step 1: 日本語サポートトップ作成**

`SonicDNAEngine-support/index-ja.html` を作成。`lang="ja"`。`index.html` と同構造で、ソースの `index-ja.md` の日本語コンテンツをHTMLに変換。ナビゲーションの「サポート」リンクに `active` クラスを付与。

- [ ] **Step 2: プライバシーポリシー（英語・日本語）作成**

`SonicDNAEngine-support/privacy.html` と `SonicDNAEngine-support/privacy-ja.html` を作成。

ソースの `privacy.md` / `privacy-ja.md` の全セクション（Introduction, Summary, Audio Processing, IR and NAM Files, Firebase Analytics & Crashlytics, Tone3000 API, iCloud Drive, Microphone Access, AUv3 Plugin, Third-Party Services, Data Storage, Data Deletion, Tracking and Advertising, Children's Privacy, Changes, Contact）をHTMLに変換。

外部リンク（Google Privacy, Tone3000 Privacy, Apple Privacy）はそのまま維持。ナビゲーションの「Privacy」/「プライバシー」リンクに `active` クラスを付与。

- [ ] **Step 3: 更新履歴ページ作成**

`SonicDNAEngine-support/changelog.html` を作成。ソースの `changelog/index.md` のコンテンツをHTMLに変換。バージョン `[1.0.0] - 2026-03-10` の全項目と `[Unreleased]` セクションを含む。ナビゲーションの「Changelog」リンクに `active` クラスを付与。

- [ ] **Step 4: ブログ一覧ページ（英語・日本語）作成**

`SonicDNAEngine-support/blog/en/index.html` と `SonicDNAEngine-support/blog/ja/index.html` を作成。

ブログ一覧は `.blog-list` スタイルを使用:
```html
<ul class="blog-list">
    <li>
        <a href="/SonicDNAEngine-support/blog/en/2026-03-10-introducing-sonicdna-engine/">
            Introducing SonicDNA Engine — IR/NAM Audio Processor for iOS
        </a>
        <div class="blog-date">2026-03-10</div>
    </li>
</ul>
```

ナビゲーションの「Blog」/「ブログ」リンクに `active` クラスを付与。

- [ ] **Step 5: ブログ記事（英語・日本語）作成**

`SonicDNAEngine-support/blog/en/2026-03-10-introducing-sonicdna-engine/index.html` と日本語版を作成。

ソースの `_posts_en/2026-03-10-introducing-sonicdna-engine.md` のコンテンツをHTMLに変換。記事末尾に「← Back to Blog」リンクを配置。

JSON-LD構造化データをheadに含める:
```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "Introducing SonicDNA Engine — IR/NAM Audio Processor for iOS",
    "datePublished": "2026-03-10",
    "author": {"@type": "Person", "name": "hakaru"},
    "publisher": {"@type": "Organization", "name": "hakaru apps", "url": "https://hakaru.net/"},
    "mainEntityOfPage": {"@type": "WebPage", "@id": "https://hakaru.net/SonicDNAEngine-support/blog/en/2026-03-10-introducing-sonicdna-engine/"},
    "description": "..."
}
</script>
```

- [ ] **Step 6: 全リンクの整合性を確認**

全ページのナビゲーションリンク、ページ内リンク、外部リンクが正しいことを確認。特に:
- ナビゲーションのパスが `/SonicDNAEngine-support/` で始まること
- ブログ記事の「← Back to Blog」リンクが正しいこと
- 「← hakaru Apps」の戻るリンクが `/` であること

- [ ] **Step 7: コミット**

```bash
git add SonicDNAEngine-support/
git commit -m "feat: add remaining SonicDNA Engine support pages (JA, privacy, blog, changelog)"
```

---

## Task 3: GitInflow サポートページを作成

**Files:**
- Create: `GitInflow-support/index.html`
- Create: `GitInflow-support/privacy.html`
- Create: `GitInflow-support/changelog.html`
- Create: `GitInflow-support/assets/app-icon.png`
- Create: `GitInflow-support/manual/en/index.html`
- Create: `GitInflow-support/blog/en/index.html`
- Create: `GitInflow-support/blog/en/2026-03-22-building-gitinflow/index.html`
- Create: `GitInflow-support/blog/en/2026-03-22-introducing-gitinflow/index.html`
- Create: `GitInflow-support/blog/en/2026-03-22-kanban-workflow-with-github-issues/index.html`

GitInflowは英語のみ（日本語版なし）。ソースリポジトリはPico CSSを使用しているが、ダークテーマに変換する。

- [ ] **Step 1: ソースリポジトリからコンテンツとアセットを取得**

ソースリポジトリ `hakaru/GitInflow-support` をクローンまたはWebFetchでコンテンツを取得。アプリアイコンをコピー。

```bash
mkdir -p GitInflow-support/assets GitInflow-support/manual/en GitInflow-support/blog/en/2026-03-22-building-gitinflow GitInflow-support/blog/en/2026-03-22-introducing-gitinflow GitInflow-support/blog/en/2026-03-22-kanban-workflow-with-github-issues
```

- [ ] **Step 2: サポートトップページを作成**

`GitInflow-support/index.html` を Task 1の共通テンプレート構造で作成。ソースのコンテンツをHTMLに変換。

**ページ固有の設定:**
- `lang="en"`
- `<title>GitInflow Support | hakaru</title>`
- ヒーロー: GitInflowアイコン + 説明文
- ナビゲーション: Support(active) / Manual / Privacy / Blog / Changelog
- App Store リンク: 実際のApp Store URL

- [ ] **Step 3: プライバシーポリシー、マニュアル、更新履歴を作成**

各ページをソースのコンテンツからHTMLに変換し、共通テンプレートで作成。

- [ ] **Step 4: ブログ一覧とブログ記事3件を作成**

ブログ一覧 `GitInflow-support/blog/en/index.html` と3記事を作成。JSON-LD構造化データを含む。

- [ ] **Step 5: リンク整合性確認**

全ページのナビゲーション・内部リンクが正しいことを確認。

- [ ] **Step 6: コミット**

```bash
git add GitInflow-support/
git commit -m "feat: add GitInflow support pages with unified dark theme"
```

---

## Task 4: SonicDNA Collector サポートページを作成

**Files:**
- Create: `SonicDNACollector-support/` 以下のファイル群

ソースリポジトリ `hakaru/SonicDNACollector-support` から取得。日英対応。

ページ構成:
- `index.html` / `index-ja.html` （サポートトップ）
- `privacy/en/index.html` / `privacy/ja/index.html` （プライバシーポリシー）
  ※ URL構造がSonicDNA Engineと異なる（`/privacy/en/`形式）
- `manual/en/index.html` / `manual/ja/index.html` （マニュアル）
- `changelog/index.html` （更新履歴）
- `blog/en/index.html` / `blog/ja/index.html` （ブログ一覧）
- `blog/en/2026-03-08-feature-deep-dive/index.html` 等ブログ記事4件（英語）
- `blog/ja/` 日本語ブログ記事

- [ ] **Step 1: ソースリポジトリからコンテンツとアセットを取得**

- [ ] **Step 2: 全ページを共通テンプレートで作成**

SonicDNA Engine と同じパターンで全ページを作成。ナビゲーションにはManualリンクも含む。

- [ ] **Step 3: リンク整合性確認**

特に `/SonicDNACollector-support/privacy/en/` のようなサブディレクトリ形式のURLが正しく動作することを確認。

- [ ] **Step 4: コミット**

```bash
git add SonicDNACollector-support/
git commit -m "feat: add SonicDNA Collector support pages with unified dark theme"
```

---

## Task 5: ChatArchive サポートページを作成

**Files:**
- Create: `ChatArchive-support/` 以下のファイル群

ChatArchiveの特殊な点:
- macOSアプリ（他はiOS）
- 利用規約ページ (`terms.html`) がある
- Lemon Squeezy決済リンクがある
- ブログは日本語メイン
- プライバシーポリシーは `privacy.html` （サブディレクトリなし）

ページ構成:
- `index.html` （メインページ、ランディングページ型）
- `privacy.html` （プライバシーポリシー）
- `terms.html` （利用規約）
- `blog/index.html` （ブログ一覧）
- `blog/line-backup-complete-guide.html` 等ブログ記事4件

- [ ] **Step 1: ソースリポジトリからコンテンツとアセットを取得**

- [ ] **Step 2: 全ページを共通テンプレートで作成**

ChatArchiveはシングルページ型（`#features`, `#howto`, `#faq` アンカー）。この構造を維持しつつダークテーマを適用。Lemon Squeezy決済リンクはそのまま維持。

ナビゲーション: Home(active) / Privacy / Terms / Blog

- [ ] **Step 3: リンク整合性確認**

- [ ] **Step 4: コミット**

```bash
git add ChatArchive-support/
git commit -m "feat: add ChatArchive support pages with unified dark theme"
```

---

## Task 6: simpleMIDIController サポートページを作成

**Files:**
- Create: `simpleMIDIController-support/` 以下のファイル群

ページ構成:
- `index.html` （サポートトップ、英語）
- `manual/en/index.html` / `manual/ja/index.html` （マニュアル）
- `support/index.html` （サポート詳細）
- `privacy/index.html` （プライバシーポリシー）
- `blog/en/index.html` / `blog/ja/index.html` （ブログ一覧）
- ブログ記事8件（英語）+ 日本語版

- [ ] **Step 1: ソースリポジトリからコンテンツとアセットを取得**

- [ ] **Step 2: 全ページを共通テンプレートで作成**

ナビゲーション: Support(active) / Manual(EN/JA) / Privacy / Blog(EN/JA)

- [ ] **Step 3: リンク整合性確認**

- [ ] **Step 4: コミット**

```bash
git add simpleMIDIController-support/
git commit -m "feat: add simpleMIDIController support pages with unified dark theme"
```

---

## Task 7: 1Take サポートページを作成

**Files:**
- Create: `1Take-support/` 以下のファイル群

最大のサポートサイト（30+ページ）。

ページ構成:
- `index.html` / `index-ja.html` （サポートトップ）
- `manual/en/index.html` / `manual/ja/index.html` （マニュアル）
- `privacy.html` / `privacy-ja.html` （プライバシーポリシー）
- `changelog.html` （更新履歴）
- `blog/en/index.html` / `blog/ja/index.html` （ブログ一覧）
- ブログ記事13件（英語）+ 日本語版

- [ ] **Step 1: ソースリポジトリからコンテンツとアセットを取得**

- [ ] **Step 2: サポートトップ・プライバシーポリシー・更新履歴・マニュアルを作成**

ナビゲーション: Support(EN/JA) / Manual(EN/JA) / Privacy(EN/JA) / Blog(EN/JA) / Changelog

Product Huntバッジ、X(Twitter)/Indie Hackerソーシャルリンクは維持。

- [ ] **Step 3: ブログ一覧とブログ記事13件を作成**

各記事をHTMLに変換。JSON-LD構造化データを含む。

- [ ] **Step 4: リンク整合性確認**

- [ ] **Step 5: コミット**

```bash
git add 1Take-support/
git commit -m "feat: add 1Take support pages with unified dark theme"
```

---

## Task 8: メインサイト index.html のサポートリンクを更新

**Files:**
- Modify: `index.html`

- [ ] **Step 1: サポートリンクを相対パスに変更**

`index.html` 内の各アプリカードのサポートリンクを更新:

```
変更前: href="https://hakaru.github.io/1Take-support/"
変更後: href="/1Take-support/"

変更前: href="https://hakaru.github.io/GitInflow-support/"
変更後: href="/GitInflow-support/"

変更前: href="https://hakaru.github.io/SonicDNACollector-support/"
変更後: href="/SonicDNACollector-support/"

変更前: href="https://hakaru.github.io/SonicDNAEngine-support/"
変更後: href="/SonicDNAEngine-support/"

変更前: href="https://hakaru.github.io/simpleMIDIController-support/"
変更後: href="/simpleMIDIController-support/"

変更前: href="https://hakaru.github.io/ChatArchive-support/"
変更後: href="/ChatArchive-support/"
```

- [ ] **Step 2: コミット**

```bash
git add index.html
git commit -m "feat: update support links to relative paths after repo integration"
```

---

## Task 9: 最終検証

- [ ] **Step 1: 全ページのリンクチェック**

全てのHTMLファイルのリンクが有効であることを確認するスクリプトを実行:

```bash
# 全HTMLファイルのリスト
find . -name "*.html" -not -path "./.git/*" | sort

# 内部リンクの参照先ファイルが存在するか確認
grep -roh 'href="/[^"]*"' --include="*.html" | sort -u
```

- [ ] **Step 2: ローカルサーバーで表示確認**

```bash
cd /Volumes/Dev/DEVELOP/hakaru.github.io
python3 -m http.server 8000
```

ブラウザで以下を確認:
- `http://localhost:8000/` （メインサイト、サポートリンクが動作すること）
- `http://localhost:8000/SonicDNAEngine-support/` （パイロット、デザイン統一）
- 各アプリのサポートトップページ
- ナビゲーションの全リンク
- モバイル表示（レスポンシブ）

- [ ] **Step 3: 最終コミットとプッシュ**

問題がなければプッシュ:
```bash
git push origin main
```
