---
title: "M2DX Support"
description: "M2DX support page. MIDI 2.0 + DX7-compatible FM synthesizer for iOS. Public TestFlight beta available."
slug: /
---

MIDI 2.0 + DX7-compatible FM Synthesizer


[Join TestFlight Beta](https://testflight.apple.com/join/BAtGszPw)

Welcome to M2DX support.

M2DX is a MIDI 2.0-compatible DX7 FM synthesizer for iOS, delivering classic 6-operator / 32-algorithm FM tones reimplemented entirely in Swift 6. The synthesis engine is provided by the [M2DX-Core](https://hakaru.net/M2DX-Core-support/) library.

---

## TestFlight Beta

**iOS / iPadOS 18+** — install the public beta:

1. Install Apple's **TestFlight** app from the App Store (one-time)
2. On your iPhone / iPad, open [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw)
3. Tap "Accept" → "Install"

Note: the very first install after Beta App Review approval may take 1–2 minutes (occasionally up to 24 hours) to propagate.

---

:::info Current Status — Why TestFlight

M2DX is **not yet at instrument-grade quality**. We are publishing the public TestFlight beta with the constraints and untested items below, in order to gather feedback and iterate.

### MIDI 2.0 coverage is limited

* We have not been able to procure enough MIDI 2.0-capable hardware, so UMP behavior has only been verified across a limited set of device combinations
* Differences in MIDI 2.0 support across macOS versions (CoreMIDI behavior, etc.) are not fully characterized
* Vendor-specific extensions and proprietary profiles built on top of MIDI 2.0 have only been partially analyzed (specifically, parts of KORG's implementation); other vendors' proprietary implementations remain untouched

### DX7 preset compatibility

* 32 initial presets are bundled, but the tonal character compared to vintage FM has not been fully verified across all presets
* Bank loading and SysEx patch import compatibility will be improved progressively across upcoming TestFlight builds

### FX chain

* The 6-stage FX chain (EQ → Drive → Chorus → Reverb → Stereo → Maximizer) is **at the "working implementation" stage**. Musical tuning of parameter ranges and endpoints, CPU efficiency, and interaction optimization are still ahead

### If you spot bugs or oddities

Crashes are auto-reported via Firebase Crashlytics (see the [Privacy Policy](https://hakaru.net/M2DX-support/privacy) for details). Reproducible issues are easier to fix — if you can, please send a report to [support@hakaru.net](mailto:support@hakaru.net).

---

:::
## Features

### Full MIDI 2.0 UMP Support

Native Universal MIDI Packet (UMP) decoding with 16-bit velocity (65,536 levels), 32-bit CC values, and 32-bit pitch bend for smooth, expressive control. MIDI 1.0 fallback is automatic.

### DX7-Compatible FM Engine

A 6-operator / 32-algorithm DX7-style FM synthesis engine implemented in pure Swift. Int32 Q24 fixed-point arithmetic targets the character of vintage FM. 32 initial presets are bundled.

### 16-Voice Polyphony

16 simultaneous voices with sustain pedal (CC64) and pitch bend (±2 semitones) support. Padé-approximation tanh soft-clipping prevents digital distortion.

### 6-Stage FX Chain

EQ → Drive → Chorus → Reverb → Stereo → Maximizer signal chain. Every parameter can be MIDI Learn-mapped to any CC.

### MIDI-CI Property Exchange

Exposes 155+ parameters in a hierarchical namespace. Compatible DAWs and controllers auto-discover parameters, with JSON-based preset management (no SysEx required) — a self-describing instrument.

### Low Latency

AVAudioSourceNode direct rendering drives the FM engine inside the CoreAudio render callback, eliminating buffer-queueing overhead. The iOS IOBufferDuration (~5 ms) is the effective latency floor.

---

## System Requirements

* **iOS / iPadOS 18+** (TestFlight beta available now)
* macOS support is planned for the future

---

## FAQ

### "Install" is grayed out

Right after Beta App Review approval, propagation to TestFlight can take a while. Please try again after about 24 hours.

### What happens if the app crashes?

Starting with v1.3.1 (build 5), Firebase Crashlytics auto-reports crashes. Reproducing a crash helps us identify and fix it quickly. See the [Privacy Policy](https://hakaru.net/M2DX-support/privacy) for details on the data we collect.

### Can I load DX7 SysEx presets?

32 initial presets are built in. SysEx import for user-supplied banks will be announced in upcoming TestFlight builds.

### Do I need a MIDI 2.0-compatible DAW?

No. MIDI 1.0 fallback is automatic, so any traditional MIDI controller or DAW works. A MIDI 2.0 environment unlocks higher-resolution expression.

### Is M2DX available as an AUv3 plug-in?

Currently it ships as a standalone iOS / iPadOS app. AUv3 support is under consideration.

---

## Links

* GitHub: [github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* Synthesis engine: [M2DX-Core](https://hakaru.net/M2DX-Core-support/) (Pure Swift DX7 FM library)
* [Privacy Policy](https://hakaru.net/M2DX-support/privacy)

---

## Contact

For questions, bug reports, and feature requests, please reach out at:  
[**support@hakaru.net**](mailto:support@hakaru.net)
