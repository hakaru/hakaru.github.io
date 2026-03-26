# サポートページ統合設計

## 概要

6つの独立したサポート用リポジトリを `hakaru.github.io` メインリポジトリに統合する。デザインをメインサイトのダークテーマに統一し、Google Analytics IDも一本化する。

## 対象リポジトリ

| リポジトリ | ページ数 | 特記事項 |
|-----------|---------|---------|
| SonicDNA Engine | ~10 | 日英対応、ブログ1記事 |
| GitInflow | ~8 | Pico CSS使用→ダークテーマに変更 |
| SonicDNA Collector | ~15 | 日英対応、ブログ4記事 |
| ChatArchive | ~10 | macOSアプリ、利用規約あり |
| simpleMIDIController | ~15 | ブログ8記事、日英対応 |
| 1Take | ~30+ | ブログ13記事、マニュアル、日英対応 |

## 設計方針

### URL構造

既存のURLパスを維持する。リダイレクト不要。

```
/[アプリ名]-support/              ← サポートトップ（英語）
/[アプリ名]-support/index-ja      ← サポートトップ（日本語）
/[アプリ名]-support/manual/en/    ← マニュアル（英語）
/[アプリ名]-support/manual/ja/    ← マニュアル（日本語）
/[アプリ名]-support/privacy       ← プライバシーポリシー（英語）
/[アプリ名]-support/privacy-ja    ← プライバシーポリシー（日本語）
/[アプリ名]-support/blog/en/      ← ブログ一覧（英語）
/[アプリ名]-support/blog/ja/      ← ブログ一覧（日本語）
/[アプリ名]-support/blog/en/YYYY-MM-DD-slug/  ← 個別記事
/[アプリ名]-support/changelog     ← 更新履歴
```

### ディレクトリ構造

```
hakaru.github.io/
├── index.html
├── tokushoho.html
├── assets/
├── blog/
├── 1Take-support/
│   ├── index.html
│   ├── index-ja.html
│   ├── privacy.html
│   ├── privacy-ja.html
│   ├── changelog.html
│   ├── manual/
│   │   ├── en/index.html
│   │   └── ja/index.html
│   └── blog/
│       ├── en/index.html
│       ├── en/YYYY-MM-DD-slug/index.html
│       ├── ja/index.html
│       └── ja/YYYY-MM-DD-slug/index.html
├── GitInflow-support/
│   └── (同様の構造)
├── SonicDNACollector-support/
├── SonicDNAEngine-support/
├── simpleMIDIController-support/
└── ChatArchive-support/
```

### 共通デザインシステム

メインサイト (`index.html`) のダークテーマに統一する。

**カラー：**
- 背景: `linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)`
- アクセント: `#e94560`
- テキスト本文: `#e0e0e0`
- テキスト補助: `#a0a0a0`

**フォント：**
- `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`

**共通レイアウト：**
```
┌─────────────────────────────────┐
│ ← hakaru Apps    [アプリ名]     │  戻るリンク + アプリ名
├─────────────────────────────────┤
│ [アイコン] アプリ名              │  ヒーローセクション
│ 説明文                          │
│ [App Store] [各種リンク]         │
├─────────────────────────────────┤
│ ナビゲーション                   │  サポート/マニュアル/ブログ/Privacy等
├─────────────────────────────────┤
│ コンテンツ                       │  max-width: 800px
├─────────────────────────────────┤
│ © 2026 hakaru | links           │  統一フッター
└─────────────────────────────────┘
```

### Google Analytics

全ページのGA IDをメインサイトの `G-N0830V28FD` に統一する。

### メインサイトの変更

`index.html` 内の各アプリカードのサポートリンクを外部URL (`https://hakaru.github.io/xxx-support/`) から相対パス (`/xxx-support/`) に更新する。

## 統合順序

小規模なアプリから着手し、リスクを最小化する。

1. **SonicDNA Engine** (~10ページ) ← パイロット
2. **GitInflow** (~8ページ)
3. **SonicDNA Collector** (~15ページ)
4. **ChatArchive** (~10ページ)
5. **simpleMIDIController** (~15ページ)
6. **1Take** (~30+ページ)

## 各アプリの統合ステップ

1. ソースリポジトリからHTMLコンテンツを取得
2. 共通デザインに変換（スタイル統一、GA ID統一）
3. ディレクトリに配置
4. リンクの整合性を確認
5. `index.html` のサポートリンクを相対パスに更新

## 元リポジトリの扱い

統合完了後に別途決定する。
