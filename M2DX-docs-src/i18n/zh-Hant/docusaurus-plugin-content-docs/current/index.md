---
title: "M2DX 支援"
description: "M2DX 支援頁面。支援 MIDI 2.0 的 DX7 相容 FM 合成器 iOS 應用程式。TestFlight Beta 測試中。"
slug: /
---

支援 MIDI 2.0 的 DX7 相容 FM 合成器


[加入 TestFlight Beta](https://testflight.apple.com/join/BAtGszPw)

歡迎來到 M2DX 支援頁面。

M2DX 是一款支援 MIDI 2.0 的 iOS 平台 DX7 相容 FM 合成器應用程式。透過 6 組運算器搭配 32 種演算法，重現經典的 FM 音色，並以 Pure Swift 6 完整重新實作。合成引擎採用 [M2DX-Core](https://hakaru.net/M2DX-Core-support/index-zh-Hant) 函式庫。

---

## TestFlight Beta 測試中

歡迎在 **iOS / iPadOS 18 以上**的環境中試用公開 Beta：

1. 從 App Store 安裝 Apple 的 **TestFlight** 應用程式（僅首次需要）
2. 在 iPhone / iPad 上開啟 [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw)
3. 依序點選「接受」→「安裝」

※ Beta App 審查通過後第一次安裝時，可能需要 1〜2 分鐘（部分情況下最多 24 小時）才會生效。

---

## 目前的狀態 — 為何採用 TestFlight 公開

M2DX 目前還**尚未達到可作為樂器實際使用的成熟度**。我們在仍存在以下限制與未驗證項目的情況下，於 TestFlight 公開 Beta 版本，目的是收集使用者回饋並持續改進。

### MIDI 2.0 的驗證範圍有限

* 由於尚未充分取得支援 MIDI 2.0 的硬體裝置，UMP 的實機驗證僅能在有限的器材組合上進行
* 各個 macOS 版本之間的 MIDI 2.0 支援差異（例如 CoreMIDI 的行為差異等）尚未完整掌握
* 各家廠商在 MIDI 2.0 規範之上加入的獨家擴充與專屬 Profile，目前僅部分（具體而言為 KORG 的部分內容）有解析支援，其他廠商的獨家實作尚未著手

### DX7 音色相容性驗證

* 雖然內建了 32 種初始音色，但與經典 FM 合成的音色比較目前尚未針對所有音色完成驗證
* 整個音色庫（Bank）以及 SysEx Patch 的載入相容性，將於後續 TestFlight 版本中分階段陸續完善

### 效果鏈

* 6 段 FX 鏈（EQ → Drive → Chorus → Reverb → Stereo → Maximizer）**目前僅停留在「能運作」的實作階段**。參數的可聽範圍、端點數值的音樂性調整、CPU 效率以及彼此之間的交互作用最佳化，都將於後續陸續處理

### 若您發現任何 Bug 或不對勁之處

當機資訊會由 Firebase Crashlytics 自動收集（詳情請參閱[隱私權政策](https://hakaru.net/M2DX-support/privacy-zh-Hant)）。具有可重現條件的問題能更快被定位，因此若可行的話，懇請您透過 [support@hakaru.net](mailto:support@hakaru.net) 回報，我們將不勝感激。

---

## 主要特色

### 完整支援 MIDI 2.0 UMP

原生支援 Universal MIDI Packet (UMP)。透過 16 位元力度（65,536 階）、32 位元 CC 與 32 位元 Pitch Bend，呈現流暢且富表現力的演奏。同時自動向下相容 MIDI 1.0。

### DX7 相容 FM 引擎

具備 6 組運算器 × 32 種演算法的 DX7 風格 FM 合成引擎，以 Pure Swift 實作。透過 Int32 Q24 定點運算，追求經典 FM 音色的特性。內建 32 種初始音色。

### 16 複音

支援 16 複音同時發聲、延音踏板（CC64）以及 Pitch Bend（±2 半音）。採用 Padé 近似 tanh 軟切削，避免數位破音。

### 6 段效果鏈

依 EQ → Drive → Chorus → Reverb → Stereo → Maximizer 的順序串接的高品質效果。所有參數皆可透過 MIDI Learn 對應到任意 CC。

### MIDI-CI Property Exchange

以階層式結構公開 155 個以上的參數，是一款自我描述型樂器。相容的 DAW 或控制器可自動探索參數，並支援以 JSON 為基礎的音色管理（無需 SysEx）。

### 低延遲

採用 AVAudioSourceNode 直接渲染，FM 引擎在 CoreAudio 渲染回呼上運作，省去緩衝佇列的額外開銷，實際延遲取決於 iOS 的 IOBufferDuration（約 5ms）。

---

## 系統需求

* **iOS / iPadOS 18 以上**（TestFlight 配發中）
* macOS 版本將於日後支援

---

## 常見問題

### 「安裝」按鈕呈現灰色無法點選

Beta App 審查剛通過時，可能需要一些時間才會反映到 TestFlight。請於約 24 小時後再試一次。

### 應用程式發生當機時該怎麼辦？

自 v1.3.1 (build 5) 起，已啟用 Firebase Crashlytics 自動回報當機。若您能重現該當機，我們便能從紀錄中找出原因並迅速修正。關於收集資料的詳細內容，請參閱[隱私權政策](https://hakaru.net/M2DX-support/privacy-zh-Hant)。

### 是否可以匯入 DX7 的 SysEx 音色？

內建 32 種初始音色。使用者自備 SysEx 音色檔的匯入功能將於後續 TestFlight 版本中提供更多資訊。

### 是否需要支援 MIDI 2.0 的 DAW？

不需要。由於可向下相容 MIDI 1.0，您仍可搭配傳統的 MIDI 控制器或 DAW 使用。在支援 MIDI 2.0 的環境下，則能享有更高解析度的演奏表現。

### 可以作為 AUv3 外掛使用嗎？

目前僅為獨立的 iOS / iPadOS 應用程式。AUv3 支援目前正在評估中。

---

## 相關連結

* GitHub：[github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* 合成引擎：[M2DX-Core](https://hakaru.net/M2DX-Core-support/index-zh-Hant)（Pure Swift DX7 FM 函式庫）
* [隱私權政策](https://hakaru.net/M2DX-support/privacy-zh-Hant)

---

## 聯絡我們

若有任何疑問、Bug 回報或功能需求，歡迎透過下列電子郵件與我們聯絡：  
[**support@hakaru.net**](mailto:support@hakaru.net)
