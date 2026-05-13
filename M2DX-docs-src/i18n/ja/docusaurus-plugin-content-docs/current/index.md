---
title: "M2DX サポート"
description: "M2DX サポートページ。MIDI 2.0 対応 DX7 互換 FM シンセサイザー iOS アプリ。TestFlight ベータ配信中。"
slug: /
---

MIDI 2.0 対応 DX7 互換 FM シンセサイザー


[TestFlight ベータに参加](https://testflight.apple.com/join/BAtGszPw)

M2DX サポートページへようこそ。

M2DX は、MIDI 2.0 に対応した iOS 向けの DX7 互換 FM シンセサイザーアプリです。6 オペレータ × 32 アルゴリズムによるクラシックな FM サウンドを、Pure Swift 6 で完全再実装しています。シンセシスエンジンには [M2DX-Core](/M2DX-Core-support/index-ja) ライブラリを使用しています。

---

## TestFlight ベータ配信中

**iOS / iPadOS 18 以上**でパブリックベータをお試しいただけます：

1. App Store から Apple の **TestFlight** アプリをインストール（初回のみ）
2. iPhone / iPad で [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw) を開く
3. 「承認」→「インストール」をタップ

※ ベータ App レビュー承認直後の最初のインストールは、反映までに 1〜2 分（場合により 24 時間程度）かかることがあります。

---

## 現在のステータス — TestFlight 公開の理由

M2DX はまだ**楽器として実用レベルには達していません**。以下の制約・未検証項目を抱えたまま、フィードバックを集めて改善するために TestFlight でパブリックベータとして公開しています。

### MIDI 2.0 の検証範囲は限定的

* MIDI 2.0 対応ハードウェアを十分に調達できておらず、UMP の動作確認は限られた機材の組み合わせでしか行えていません
* macOS のバージョンごとの MIDI 2.0 サポート差異（CoreMIDI の挙動違い等）は完全には把握できていません
* 各メーカーが MIDI 2.0 仕様の上に載せている独自拡張・独自プロファイルの解析は一部のみ（具体的には KORG の一部）対応しており、他社の独自実装は未着手です

### DX7 プリセットの互換性検証

* 32 種類の初期プリセットを内蔵していますが、ビンテージ FM 音源と比較したときの音作り検証は途上です
* バンク全体や SysEx パッチの読み込み互換性は今後の TestFlight ビルドで段階的に整備します

### エフェクトチェーン

* 6 段の FX チェーン（EQ → Drive → Chorus → Reverb → Stereo → Maximizer）は**ひとまず動く形で実装した段階**です。パラメータの可聴範囲・エンドポイント値の音楽的調整、CPU 効率、相互作用の最適化は今後行います

### 不具合・違和感を見つけた方へ

クラッシュは Firebase Crashlytics で自動収集されます（詳細は[プライバシーポリシー](/M2DX-support/privacy-ja)）。再現条件のある不具合は特定が早まりますので、可能であれば [support@hakaru.net](mailto:support@hakaru.net) までご報告いただけると助かります。

---

## 主な特徴

### MIDI 2.0 UMP 完全対応

Universal MIDI Packet (UMP) をネイティブにサポート。16 ビットベロシティ（65,536 段階）、32 ビット CC、32 ビットピッチベンドによる滑らかで表現力豊かな演奏が可能です。MIDI 1.0 にも自動フォールバックします。

### DX7 互換 FM エンジン

6 オペレータ × 32 アルゴリズムの DX7 系 FM 合成エンジンを Pure Swift で実装。Int32 Q24 固定小数点演算により、ビンテージ FM 音源らしいキャラクターを目指しています。32 種類の初期プリセットを内蔵しています。

### 16 ボイス ポリフォニー

16 ボイスの同時発音、サスティンペダル（CC64）、ピッチベンド（±2 半音）に対応。Padé 近似 tanh によるソフトクリッピングでデジタル歪みを防止します。

### 6 段エフェクトチェーン

EQ → Drive → Chorus → Reverb → Stereo → Maximizer の信号順で構成された高品質エフェクト。すべてのパラメータを MIDI Learn で任意の CC にマッピングできます。

### MIDI-CI Property Exchange

155 以上のパラメータを階層構造で公開。対応する DAW やコントローラーがパラメータを自動発見でき、JSON ベースのプリセット管理（SysEx 不要）が可能な、自己記述型インストゥルメントです。

### 低レイテンシ

AVAudioSourceNode による直接レンダリングで、CoreAudio レンダーコールバック上で FM エンジンを駆動。バッファキューイングのオーバーヘッドを排除し、iOS の IOBufferDuration（約 5ms）が実質的なレイテンシとなります。

---

## 動作環境

* **iOS / iPadOS 18 以上**（TestFlight 配信中）
* macOS 版は将来対応予定

---

## よくある質問

### 「インストール」がグレーアウトしている

ベータ App レビュー承認直後は、TestFlight への反映まで時間がかかる場合があります。約 24 時間後に再度お試しください。

### クラッシュした場合は？

v1.3.1 (build 5) から Firebase Crashlytics による自動クラッシュレポートが有効になっています。クラッシュを再現していただくと、ログから原因を特定して迅速に修正できます。収集データの詳細は[プライバシーポリシー](/M2DX-support/privacy-ja)をご覧ください。

### DX7 の SysEx プリセットは読み込めますか？

32 種類の初期プリセットを内蔵しています。ユーザーが手元のバンクを読み込む SysEx 取り込みについては、今後の TestFlight ビルドでご案内します。

### MIDI 2.0 対応の DAW が必要ですか？

いいえ。MIDI 1.0 にもフォールバック対応しているため、従来の MIDI コントローラーや DAW でもお使いいただけます。MIDI 2.0 対応環境ではより高解像度の表現が可能になります。

### AUv3 プラグインとして使えますか？

現時点ではスタンドアロン iOS / iPadOS アプリです。AUv3 対応については検討中です。

---

## リンク

* GitHub: [github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* シンセシスエンジン: [M2DX-Core](/M2DX-Core-support/index-ja)（Pure Swift DX7 FM ライブラリ）
* [プライバシーポリシー](/M2DX-support/privacy-ja)

---

## お問い合わせ

ご質問・不具合報告・機能リクエストは、以下のメールアドレスまでお気軽にどうぞ：  
[**support@hakaru.net**](mailto:support@hakaru.net)
