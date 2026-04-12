# hakaru.net 多言語化計画

作成日: 2026-04-12
対象言語: en, ja, fr, de, es, it, ko, nl, pt-BR, sv, zh-Hant（11言語）
参照実装: /1Take-support/（完了済み）

---

## 多言語化パターン（1Take-support に準拠）

### パターン A: ファイル名サフィックス方式（メインページ・プライバシー・チェンジログ）
- en: `index.html`（デフォルト）
- 他言語: `index-{lang}.html`（例: `index-fr.html`, `index-zh-Hant.html`）
- プライバシー: `privacy.html`（en）、`privacy-{lang}.html`（他）
- チェンジログ: `changelog.html`（en）、`changelog-{lang}.html`（他）

### パターン B: ディレクトリ方式（blog・manual）
- en: `blog/en/`、`manual/en/`（既存）
- 他言語: `blog/{lang}/`、`manual/{lang}/`（新規作成）
- 各言語ディレクトリに `index.html` + 記事ディレクトリ（記事ディレクトリ内に `index.html`）

### パターン C: サブディレクトリ方式（ChatArchive のみ）
- ja: `ChatArchive-support/`（ルート、既存）
- en: `ChatArchive-support/en/`（既存）
- 新規: `ChatArchive-support/{lang}/`（9言語追加）

### 言語スイッチャー（サイドバー）
- `.sidebar-lang` div 内に各言語へのリンク
- 現在のページ言語を `<span class="sidebar-lang-btn active">` で表示
- 他言語は `<a href="..." class="sidebar-lang-btn" data-lang="{lang}">` リンク
- 1Take-support の11言語完全スイッチャーをすべての新規ページに適用

### 自動リダイレクト（各ページ末尾 `<script>`）
- `localStorage.getItem('hakaru-lang')` で保存済み設定を確認
- なければ `navigator.language` でブラウザ言語を検出
- 11言語にマッピング（`/1Take-support/index.html` の `detectLang()` を参照実装とする）
- 初回訪問かつ現在ページ言語と異なる場合にリダイレクト

---

## 除外対象（多言語化しない）

- `tokushoho.html` — 日本の法的義務ページ（日本語のみ）
- `oauth/google/` — 技術的コールバックページ
- `blog/appstore-review-monitor.html` — 英語専用記事（現状維持）
- `blog/peerclock-p2p-sync.html` — 英語専用記事（現状維持）

---

## 翻訳言語コード対応表

| コード   | 言語名（英語）          | サイドバー表示  |
|----------|------------------------|----------------|
| en       | English                | English        |
| ja       | Japanese               | 日本語          |
| fr       | French                 | Français       |
| de       | German                 | Deutsch        |
| es       | Spanish                | Español        |
| it       | Italian                | Italiano       |
| ko       | Korean                 | 한국어          |
| nl       | Dutch                  | Nederlands     |
| pt-BR    | Portuguese (Brazil)    | Português      |
| sv       | Swedish                | Svenska        |
| zh-Hant  | Traditional Chinese    | 繁體中文        |

---

## フェーズ別作業一覧

---

### Phase 1: TineModeler-support（最小規模・足慣らし）

対象ページ: index.html、index-ja.html、privacy.html、privacy-ja.html
新規作成: 9言語 × 2ページ = **18ファイル**

- [ ] 1-1. `index-{lang}.html` を9言語分作成（fr/de/es/it/ko/nl/pt-BR/sv/zh-Hant）
- [ ] 1-2. `privacy-{lang}.html` を9言語分作成
- [ ] 1-3. 既存4ファイルの言語スイッチャーを11言語に更新
  - `index.html`、`index-ja.html`、`privacy.html`、`privacy-ja.html`

**コミット**: `feat: localize TineModeler-support to 11 languages`
**見積もり**: 新規 18 ファイル + 既存 4 ファイル更新

---

### Phase 2: M2DX-Core-support（最小規模）

対象ページ: index.html、index-ja.html、privacy.html、privacy-ja.html
新規作成: 9言語 × 2ページ = **18ファイル**

- [ ] 2-1. `index-{lang}.html` を9言語分作成
- [ ] 2-2. `privacy-{lang}.html` を9言語分作成
- [ ] 2-3. 既存4ファイルの言語スイッチャーを11言語に更新

**コミット**: `feat: localize M2DX-Core-support to 11 languages`
**見積もり**: 新規 18 ファイル + 既存 4 ファイル更新

---

### Phase 3: SonicDNAEngine-support（小規模）

対象ページ: index.html、index-ja.html、changelog.html、privacy.html、privacy-ja.html
blog: `blog/en/` に1記事（`2026-03-10-introducing-sonicdna-engine/`）、`blog/ja/` に1記事

- [ ] 3-1. `index-{lang}.html` を9言語分作成（9ファイル）
- [ ] 3-2. `privacy-{lang}.html` を9言語分作成（9ファイル）
- [ ] 3-3. `changelog-{lang}.html` を9言語分作成（9ファイル）
- [ ] 3-4. `blog/{lang}/` を9言語分作成
  - 各言語 `index.html`（ブログ一覧）：9ファイル
  - 記事 `2026-03-10-introducing-sonicdna-engine/index.html` を9言語分：9ファイル
- [ ] 3-5. 既存5ファイルの言語スイッチャーを11言語に更新
  - `index.html`、`index-ja.html`、`changelog.html`、`privacy.html`、`privacy-ja.html`

**コミット**: `feat: localize SonicDNAEngine-support to 11 languages`
**見積もり**: 新規 45 ファイル + 既存 5 ファイル更新

---

### Phase 4: GitInflow-support（小〜中規模）

対象ページ: index.html、index-ja.html、changelog.html、changelog-ja.html、privacy.html、privacy-ja.html
blog: `blog/en/` に3記事、`blog/ja/` に3記事
manual: `manual/en/index.html`、`manual/ja/index.html`

- [ ] 4-1. `index-{lang}.html` を9言語分作成（9ファイル）
- [ ] 4-2. `privacy-{lang}.html` を9言語分作成（9ファイル）
- [ ] 4-3. `changelog-{lang}.html` を9言語分作成（9ファイル）
- [ ] 4-4. `blog/{lang}/` を9言語分作成
  - 各言語 `index.html`（一覧）：9ファイル
  - 記事3本 × 9言語 = 27ファイル
    - `2026-03-22-building-gitinflow/index.html`
    - `2026-03-22-introducing-gitinflow/index.html`
    - `2026-03-22-kanban-workflow-with-github-issues/index.html`
- [ ] 4-5. `manual/{lang}/index.html` を9言語分作成（9ファイル）
- [ ] 4-6. 既存6ファイルの言語スイッチャーを11言語に更新
  - `index.html`、`index-ja.html`、`changelog.html`、`changelog-ja.html`、`privacy.html`、`privacy-ja.html`

**コミット**: `feat: localize GitInflow-support to 11 languages`
**見積もり**: 新規 63 ファイル + 既存 6 ファイル更新

---

### Phase 5: SonicDNACollector-support（中規模）

対象ページ: index.html、index-ja.html、privacy.html、privacy-ja.html
changelog: `changelog/index.html`（ディレクトリ形式）
blog: `blog/en/` に4記事、`blog/ja/` に4記事
manual: `manual/en/index.html`、`manual/ja/index.html`

- [ ] 5-1. `index-{lang}.html` を9言語分作成（9ファイル）
- [ ] 5-2. `privacy-{lang}.html` を9言語分作成（9ファイル）
- [ ] 5-3. `changelog/{lang}/index.html` を9言語分作成（9ファイル）
  - 注意: changelog がディレクトリ形式のため `changelog/{lang}/` サブディレクトリを作成
- [ ] 5-4. `blog/{lang}/` を9言語分作成
  - 各言語 `index.html`（一覧）：9ファイル
  - 記事4本 × 9言語 = 36ファイル
    - `2026-01-25-welcome/index.html`
    - `2026-03-08-analog-gear-frequency-analysis/index.html`
    - `2026-03-08-analog-synth-market-growth-2026/index.html`
    - `2026-03-08-feature-deep-dive/index.html`
- [ ] 5-5. `manual/{lang}/index.html` を9言語分作成（9ファイル）
- [ ] 5-6. 既存5ファイルの言語スイッチャーを11言語に更新
  - `index.html`、`index-ja.html`、`privacy.html`、`privacy-ja.html`、`changelog/index.html`

**コミット**: `feat: localize SonicDNACollector-support to 11 languages`
**見積もり**: 新規 72 ファイル + 既存 5 ファイル更新

---

### Phase 6: simpleMIDIController-support（最大規模）

対象ページ: index.html、index-ja.html
privacy: `privacy/index.html`（ディレクトリ形式）
support: `support/index.html`（ディレクトリ形式）
blog: `blog/en/` に8記事、`blog/ja/` に8記事
manual: `manual/en/index.html`、`manual/ja/index.html`

- [ ] 6-1. `index-{lang}.html` を9言語分作成（9ファイル）
- [ ] 6-2. `privacy/{lang}/index.html` を9言語分作成（9ファイル）
  - 注意: privacy がディレクトリ形式のため `privacy/{lang}/` サブディレクトリを作成
- [ ] 6-3. `support/{lang}/index.html` を9言語分作成（9ファイル）
  - 注意: support がディレクトリ形式のため `support/{lang}/` サブディレクトリを作成
- [ ] 6-4. `blog/{lang}/` を9言語分作成
  - 各言語 `index.html`（一覧）：9ファイル
  - 記事8本 × 9言語 = 72ファイル
    - `2026-03-03-performance-tips/index.html`
    - `2026-03-04-customization/index.html`
    - `2026-03-05-controller-interface/index.html`
    - `2026-03-06-virtual-midi/index.html`
    - `2026-03-07-usb-midi/index.html`
    - `2026-03-08-bluetooth-midi/index.html`
    - `2026-03-08-iphone-midi-controller-setup/index.html`
    - `2026-03-08-midi2-comes-to-windows/index.html`
- [ ] 6-5. `manual/{lang}/index.html` を9言語分作成（9ファイル）
- [ ] 6-6. 既存5ファイルの言語スイッチャーを11言語に更新
  - `index.html`、`index-ja.html`、`privacy/index.html`、`support/index.html`、`manual/en/index.html`

**コミット**: `feat: localize simpleMIDIController-support to 11 languages`
**見積もり**: 新規 117 ファイル + 既存 5 ファイル更新

---

### Phase 7: ChatArchive-support（中規模・構造移行含む）

現状: ja（ルート）+ en/th/zh-Hant（サブディレクトリ）の4言語
追加: fr/de/es/it/ko/nl/pt-BR/sv の8言語（th は対象外・現状維持）

- [ ] 7-1. 新規8言語のサブディレクトリを作成、各言語ごとに以下を作成
  - `{lang}/index.html`
  - `{lang}/privacy.html`
  - `{lang}/terms.html`
  - `{lang}/blog/index.html`（ブログ一覧）
  - `{lang}/blog/chatarchive-getting-started.html`
  - `{lang}/blog/line-backup-complete-guide.html`
  - `{lang}/blog/line-backup-news-2026.html`
  - `{lang}/blog/line-backup-notebooklm.html`
  - `{lang}/blog/line-export-all-chats.html`
  - 8言語 × 9ファイル = 72ファイル
- [ ] 7-2. 既存言語ページの言語スイッチャーを11言語に更新
  - `index.html`（ja ルート）
  - `en/index.html`、`en/privacy.html`、`en/terms.html`、`en/blog/index.html`
  - `en/blog/` 各記事 5ファイル
  - `th/index.html`、`th/privacy.html`、`th/terms.html`（th はスイッチャー追加のみ）
  - `zh-Hant/index.html`、`zh-Hant/privacy.html`、`zh-Hant/terms.html`
- [ ] 7-3. ルート `index.html` のリダイレクト検出ロジックを11言語対応に更新
  （現状 `ja/en` の2択 → 11言語 `detectLang()` に更新）

**コミット**: `feat: localize ChatArchive-support to 11 languages`
**見積もり**: 新規 72 ファイル + 既存 17 ファイル更新

---

### Phase 8: ルート index.html の多言語化

現状: 英語のみ（479行）、言語切替機能なし
対応: 10言語版（index-{lang}.html）を新規作成 + 言語スイッチャー・自動リダイレクト追加

- [ ] 8-1. `index-{lang}.html` を10言語分作成（10ファイル）
  - ja/fr/de/es/it/ko/nl/pt-BR/sv/zh-Hant
- [ ] 8-2. `index.html` に言語スイッチャーと自動リダイレクトを追加
  - ヘッダー右上などに軽量な言語切替 UI を追加

**コミット**: `feat: localize root index.html to 11 languages`
**見積もり**: 新規 10 ファイル + 既存 1 ファイル更新

---

### Phase 9: サイドバー横断リンク整合性確認・修正

全言語別ページのサイドバーに含まれる「他アプリへのリンク」が、正しく対応言語の URL を指しているか確認・修正。

- [ ] 9-1. 各新規ページのサイドバー内「他アプリリンク」が対応言語 URL を指しているか確認
  - 例: `index-fr.html` のサイドバー内 GitInflow リンクが `/GitInflow-support/index-fr` になっているか
- [ ] 9-2. 既存 en/ja ページのサイドバーに新規9言語のリンクを追加
- [ ] 9-3. `detectLang()` が現在 en/ja の2択になっている旧アプリ（GitInflow/SonicDNACollector/SonicDNAEngine/simpleMIDIController 等）を11言語版に更新済みか再確認

**コミット**: `fix: update cross-app sidebar links for all 11 languages`
**見積もり**: 横断的修正（全アプリの全言語別ページ）

---

## 作業量サマリー

| フェーズ | 対象 | 新規ファイル | 更新ファイル | コミット |
|---------|------|------------|------------|---------|
| Phase 1 | TineModeler-support | 18 | 4 | 1 |
| Phase 2 | M2DX-Core-support | 18 | 4 | 1 |
| Phase 3 | SonicDNAEngine-support | 45 | 5 | 1 |
| Phase 4 | GitInflow-support | 63 | 6 | 1 |
| Phase 5 | SonicDNACollector-support | 72 | 5 | 1 |
| Phase 6 | simpleMIDIController-support | 117 | 5 | 1 |
| Phase 7 | ChatArchive-support | 72 | 17 | 1 |
| Phase 8 | root index.html | 10 | 1 | 1 |
| Phase 9 | 横断的サイドバー整合性 | 0 | 多数 | 1 |
| **合計** | | **415** | **47+** | **9** |

---

## 実装メモ・注意事項

### ChatArchive の構造的特殊性
- ChatArchive はサブディレクトリ方式（`/en/`、`/th/`、`/zh-Hant/`）を採用済み
- 他アプリ（パターン A）と異なるため、サイドバーのリンクパターンも別扱い
- `th`（タイ語）は今回の対象11言語に含まれないが、既存ページは維持する

### SonicDNACollector の changelog 構造
- `changelog/` がディレクトリ形式（`changelog/index.html`）
- 多言語化は `changelog/{lang}/index.html` で対応（ファイル名サフィックス方式は使わない）

### simpleMIDIController の privacy・support 構造
- `privacy/` と `support/` がディレクトリ形式
- 多言語化は `privacy/{lang}/index.html`、`support/{lang}/index.html` で対応

### detectLang() の11言語版への統一
- 現在 GitInflow/SonicDNACollector/SonicDNAEngine 等は `ja` のみ検出する2択版
- `/1Take-support/index.html` の11言語版 `detectLang()` に統一すること
- pt-BR の検出: `navLang === 'pt-br' || navLang.startsWith('pt')`
- zh-Hant の検出: `navLang === 'zh-tw' || navLang === 'zh-hk' || navLang.startsWith('zh-hant')`

### サイドバーの他アプリリンクも言語対応が必要
- 各ページのサイドバーには全アプリへのリンクが含まれる
- 言語別ページでは、サイドバー内の他アプリリンクも対応言語に向ける
- 例: `index-fr.html` のサイドバー内 GitInflow リンクは `/GitInflow-support/index-fr` にする
