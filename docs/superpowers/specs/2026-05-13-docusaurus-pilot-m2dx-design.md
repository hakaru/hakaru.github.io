# Docusaurus パイロット — M2DX-support 移行設計

**作成日:** 2026-05-13
**対象:** hakaru.net サイト管理を Docusaurus へ段階移行する第一歩（M2DX-support のみ）
**動機:** Markdown 中心でドキュメントを書きたい。手書き HTML + Python サイドバー注入の運用から脱却したい
**前段:** 2026-04-26 の Astro 全面リデザイン計画は未実行のまま方針転換

---

## サマリ

M2DX-support の 22 ファイル（11 言語 × {index, privacy}）を Docusaurus 化して `/M2DX-docs/` にマウントする。既存 `/M2DX-support/` 配下と既存スクリプトには触らず、並存運用する。リスク最小のパイロットとして「Docusaurus の i18n・デプロイ・Markdown 編集ループ」を実機検証する。

成功条件:

1. 既存サイト全 URL の挙動が変わらない
2. `/M2DX-docs/` で 11 言語が動き、ロケール切替と内部リンクが正常
3. Markdown 1 ファイル編集 → push → 反映が**手動 HTML 編集なし**で回る
4. ロールバックが実機で確認済み

---

## アーキテクチャ全体像

```
[git push main]
      ↓
[Cloudflare Pages build]
   1. リポジトリ全体を checkout
   2. Node 20 セットアップ
   3. cd M2DX-docs-src && npm ci && npm run build
      → M2DX-docs-src/build/  (Docusaurus 成果物)
   4. ./scripts/assemble-dist.sh を実行
      → dist/ に既存静的ファイル + Docusaurus build を集約
   5. Cloudflare Pages が dist/ を配信
      ↓
hakaru.net
  ├── /                       既存 index.html（変更なし）
  ├── /M2DX-support/          既存 HTML（変更なし）
  ├── /M2DX-docs/             新規 Docusaurus（EN）
  ├── /M2DX-docs/ja/          新規 Docusaurus（JA）
  ├── /M2DX-docs/de/          新規 Docusaurus（DE）
  ├── /M2DX-docs/{es,fr,it,ko,nl,pt-BR,sv,zh-Hant}/
  └── /_redirects             既存（変更なし）
```

### 設計の柱

- 既存静的ファイル・既存スクリプト (`update-sidebar.py` / `transform.py`) は**読み取り専用**
- `M2DX-docs-src/` を追加するだけ、既存ディレクトリは無改変
- Cloudflare Pages の build command と output directory のみ変更
- `assemble-dist.sh` がリポジトリ全体を `dist/` に rsync しつつ、`M2DX-docs-src/build/` を `dist/M2DX-docs/` に重ねる
- Docusaurus の `baseUrl: '/M2DX-docs/'` でアセットパスが整合

---

## リポジトリ構造

```
hakaru.github.io/
├── M2DX-docs-src/                     ★ 新規（Docusaurus ソース）
│   ├── package.json
│   ├── docusaurus.config.ts           baseUrl: '/M2DX-docs/'
│   ├── sidebars.ts                    Sidebar 構造（2 項目）
│   ├── tsconfig.json
│   ├── docs/                          英語（defaultLocale）
│   │   ├── index.md                   → /M2DX-docs/
│   │   └── privacy.md                 → /M2DX-docs/privacy/
│   ├── i18n/                          10 言語の翻訳
│   │   ├── ja/docusaurus-plugin-content-docs/current/
│   │   │   ├── index.md
│   │   │   └── privacy.md
│   │   ├── de/docusaurus-plugin-content-docs/current/...
│   │   ├── es/...
│   │   ├── fr/...
│   │   ├── it/...
│   │   ├── ko/...
│   │   ├── nl/...
│   │   ├── pt-BR/...
│   │   ├── sv/...
│   │   └── zh-Hant/...
│   ├── src/css/custom.css             テーマカラー（M2DX 赤 #e94560）
│   ├── static/img/                    M2DX アイコン等
│   ├── .gitignore                     build/, node_modules/
│   └── build/                         npm run build 出力（git ignored）
│
├── scripts/
│   ├── assemble-dist.sh               ★ 新規（rsync で dist/ 集約）
│   ├── migrate-m2dx-to-md.py          ★ 新規（HTML → MD 変換）
│   ├── update-sidebar.py              既存・触らない
│   ├── transform.py                   既存・触らない
│   └── sidebar-*.{json,js,css}        既存・触らない
│
├── .gitignore                         追記（M2DX-docs-src/build, node_modules, dist）
│
└── (既存ファイル全部そのまま)
    ├── index*.html                    変更なし
    ├── M2DX-support/                  並存・変更なし
    ├── 1Take-support/                 他アプリ・変更なし
    ├── ...
    ├── _redirects
    └── CNAME
```

---

## Docusaurus 設定

### `docusaurus.config.ts` の要点

```ts
{
  title: 'M2DX',
  url: 'https://hakaru.net',
  baseUrl: '/M2DX-docs/',
  trailingSlash: true,
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'de', 'es', 'fr', 'it', 'ja', 'ko', 'nl', 'pt-BR', 'sv', 'zh-Hant'],
  },
  presets: [
    ['classic', {
      docs: {
        routeBasePath: '/',            // /M2DX-docs/ をドキュメントルートに
        sidebarPath: './sidebars.ts',
        editUrl: undefined,            // GitHub edit リンクは出さない
      },
      blog: false,                     // パイロットはブログ不要
      theme: { customCss: './src/css/custom.css' },
      gtag: { trackingID: 'G-N0830V28FD' },  // 既存と同じ計測 ID
    }],
  ],
  themeConfig: {
    navbar: {
      title: 'M2DX',
      logo: { src: 'img/m2dx-icon.png' },
      items: [
        { href: '/M2DX-support/', label: 'Main site', position: 'right' },
        { type: 'localeDropdown', position: 'right' },
      ],
    },
    colorMode: { defaultMode: 'dark', respectPrefersColorScheme: true },
  },
}
```

### URL マッピング

| ロケール | URL |
|---|---|
| EN (default) | `/M2DX-docs/`, `/M2DX-docs/privacy/` |
| JA | `/M2DX-docs/ja/`, `/M2DX-docs/ja/privacy/` |
| DE | `/M2DX-docs/de/`, `/M2DX-docs/de/privacy/` |
| ES, FR, IT, KO, NL, PT-BR, SV, ZH-Hant | 同パターン |

### `sidebars.ts`

```ts
export default {
  docs: [
    { type: 'doc', id: 'index', label: 'Overview' },
    { type: 'doc', id: 'privacy', label: 'Privacy Policy' },
  ],
};
```

### テーマ・配色

- Docusaurus 標準のライト/ダーク両モード（`colorMode.defaultMode: 'dark'`）
- `custom.css` で primary color のみ `#e94560`（M2DX 赤系）に上書き
- 既存 `/M2DX-support/` の濃紺グラデーション + 赤アクセントの**ピクセル一致は狙わない**
- フォント、レイアウト、サイドバーは Docusaurus デフォルト

---

## コンテンツ移行（HTML → Markdown）

### 戦略

1. **抽出は機械的に** — Python + BeautifulSoup
2. **整形は手作業の見直し** — 22 ファイル × 数分で完了する規模
3. **API キー不要**

### `scripts/migrate-m2dx-to-md.py` の概要

```
for lang in [en, de, es, fr, it, ja, ko, nl, pt-BR, sv, zh-Hant]:
  for page in [index, privacy]:
    1. 入力 HTML を読む
       - en:   M2DX-support/{page}.html
       - lang: M2DX-support/{page}-{lang}.html
    2. BeautifulSoup でパース
    3. インライン <style>, <script>, .sidebar*, gtag を全部捨てる
    4. .container > .hero と .content の中身だけ取り出す
    5. markdownify で MD 化
    6. 「Current Status — Why TestFlight」ブロックを ::: info admonition に変換
    7. TestFlight CTA <a class="testflight-cta"> を [テキスト](url) リンク化
    8. Front matter を生成して prepend
    9. 出力先:
       - en:   M2DX-docs-src/docs/{page}.md
       - lang: M2DX-docs-src/i18n/{lang}/docusaurus-plugin-content-docs/current/{page}.md
```

### Front matter ルール

**`docs/index.md` (EN)**
```yaml
---
title: M2DX
description: M2DX — MIDI 2.0 + DX7-compatible FM synthesizer for iOS.
slug: /
---
```

**`docs/privacy.md` (EN)**
```yaml
---
title: Privacy Policy
description: Privacy policy for M2DX.
slug: /privacy
---
```

各言語の翻訳ファイルも同じ構造で title だけ翻訳。

### CTA / 装飾の扱い（パイロット方針）

| 元 HTML | MD 化後 |
|---|---|
| 赤グラデの TestFlight ボタン | プレーン MD リンク `[Join TestFlight](url)`。Docusaurus の primary color が当たる |
| ヒーローのアイコン画像 | `static/img/m2dx-icon.png` に配置、ページ冒頭で `![](/M2DX-docs/img/m2dx-icon.png)` |
| 「Current Status」セクション | Docusaurus admonition `:::info ... :::` |
| `<hr>` 区切り | 標準 MD `---` |
| インラインスタイル / class | 全捨て |

### 検証粒度

1. スクリプト実行 → 22 ファイル生成
2. **EN 版だけ目視で全文確認**
3. 残り 10 言語は「行数・リンク数・見出し数」を EN と diff
4. `npm run start -- --locale ja` 等で 3 言語ぐらいブラウザ目視
5. 怪しい言語は個別に手直し

---

## Cloudflare Pages 構成変更

### 変更前後の比較

| 項目 | 現在（推定） | 新設定 |
|---|---|---|
| ビルドコマンド | なし（空欄） | `bash scripts/assemble-dist.sh` |
| 出力ディレクトリ | `/` | `dist` |
| 環境変数 | — | `NODE_VERSION=20` |
| ビルドブランチ | `main` | `main`（変更なし） |

### `scripts/assemble-dist.sh`

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
```

### 前提条件

- Cloudflare ダッシュボードへのアクセス権を確保していること
- GitHub Pages が当該リポジトリで二重に有効化されていないことを確認（Settings → Pages を要確認）

---

## テスト・カットオーバー戦略

### フェーズ分解

| Phase | 内容 | 失敗時の影響範囲 |
|---|---|---|
| **0** | `docusaurus-pilot` ブランチ作成、`M2DX-docs-src/` Scaffold、ローカル `npm run start` で「Hello Docusaurus」が表示 | ローカルのみ |
| **1** | 移行スクリプトで 22 ファイル生成、ローカルで全 11 言語ブラウザ確認 | ローカルのみ |
| **2** | `assemble-dist.sh` 作成、ローカルで `npx serve dist` 検証 | ローカルのみ |
| **3** | `docusaurus-pilot` を push → CF Pages **プレビューデプロイ**（`<sha>.hakaru-github-io.pages.dev`） | 本番無傷 |
| **4** | プレビュー URL の `/M2DX-docs/` + 既存ページ抜き取り確認 | 本番無傷 |
| **5** | CF Pages の**本番ビルド設定変更** | ★ 本番影響開始 |
| **6** | `main` へ merge → 本番反映、既存ページ抜き取り確認 | 失敗時は CF Pages のロールバックで即時復帰 |

**Phase 5 がリスク最大のポイント**。プレビューデプロイは現行ビルド設定でも動くが、本番で `/M2DX-docs/` を見せるには Phase 5 必須。

### Phase 4 動作確認チェックリスト

- [ ] `/` 既存トップが従来通り
- [ ] `/M2DX-support/` 既存サポートページが従来通り
- [ ] 他アプリ `/1Take-support/` `/ChatArchive-support/` などが従来通り
- [ ] `/_redirects` の 301 が効いている（例: `/m2dx-core-support/` → `/M2DX-Core-support/`）
- [ ] `/M2DX-docs/` で Docusaurus EN ホームが表示
- [ ] `/M2DX-docs/privacy/` で privacy 表示
- [ ] navbar の locale dropdown で 11 言語が切り替わる
- [ ] `/M2DX-docs/ja/` `/M2DX-docs/de/` などが翻訳済み
- [ ] navbar の「Main site」リンクが `/M2DX-support/` へ戻る
- [ ] gtag が両側で発火

### ロールバックシナリオ

| 失敗パターン | 影響 | 復旧 |
|---|---|---|
| `assemble-dist.sh` 失敗 | デプロイ失敗 → 前デプロイ維持 | コード修正して push（既存サイト無傷） |
| ビルド成功・`/M2DX-docs/` だけ崩れる | 既存無傷、新ページのみ 404/崩れ | fix-forward か commit revert |
| 全面的に壊れた | 全サイト影響 | CF Pages の「Previous deployment」で即時復帰 |
| 設計ごと撤回 | — | ビルド設定を「コマンド空欄 + Output `/`」に戻して再デプロイ |

### ローカル検証コマンド

```bash
cd M2DX-docs-src && npm run start                # http://localhost:3000/M2DX-docs/
npm run start -- --locale ja                     # 日本語版
```

本番ビルドの事前確認:

```bash
bash scripts/assemble-dist.sh
npx serve dist                                    # 全サイト動作確認
```

---

## スコープ外（次フェーズ）

- 他アプリ（1Take, ChatArchive, MacSlowCooker, SonicDNA, TineModeler, GitInflow, PeerClockMetronome, simpleMIDIController, M2DX-Core 等）への横展開
- App Store Connect の privacy URL 差し替え
- 既存 `/M2DX-support/` の段階的アーカイブ
- M2DX-Core blog の Docusaurus blog プラグインへの移行
- Algolia DocSearch の組み込み
- 既存 `sitemap.xml` への `/M2DX-docs/` URL 追加（Docusaurus は自前で `/M2DX-docs/sitemap.xml` を生成、本番カットオーバー時に統合判断）
- TestFlight ボタンの装飾 React コンポーネント化
- Anthropic API による翻訳の humanizer 再処理
