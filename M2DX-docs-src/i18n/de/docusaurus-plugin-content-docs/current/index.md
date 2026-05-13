---
title: "M2DX Support"
description: "M2DX Support-Seite. MIDI 2.0-fähiger, DX7-kompatibler FM-Synthesizer für iOS. Jetzt als TestFlight-Beta verfügbar."
slug: /
---

MIDI 2.0-fähiger, DX7-kompatibler FM-Synthesizer


[An TestFlight-Beta teilnehmen](https://testflight.apple.com/join/BAtGszPw)

Willkommen auf der M2DX Support-Seite.

M2DX ist ein DX7-kompatibler FM-Synthesizer für iOS mit voller MIDI 2.0-Unterstützung. Der klassische FM-Sound aus 6 Operatoren und 32 Algorithmen wurde komplett in Pure Swift 6 neu implementiert. Als Synthese-Engine kommt die Bibliothek [M2DX-Core](/M2DX-Core-support/index-de) zum Einsatz.

---

## TestFlight-Beta jetzt verfügbar

Die öffentliche Beta läuft auf **iOS / iPadOS 18 oder neuer**:

1. Apples **TestFlight**-App aus dem App Store installieren (nur beim ersten Mal nötig)
2. Auf dem iPhone oder iPad [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw) öffnen
3. Auf „Akzeptieren“ und anschließend „Installieren“ tippen

Hinweis: Direkt nach der Beta-App-Review kann die erste Installation 1–2 Minuten dauern, in Einzelfällen bis zu 24 Stunden.

---

:::info Aktueller Stand — Warum TestFlight

M2DX hat **noch nicht das Niveau eines vollwertigen Instruments erreicht**. Wir veröffentlichen die öffentliche TestFlight-Beta trotz der unten aufgeführten Einschränkungen und offenen Punkte, um Rückmeldungen zu sammeln und das Programm Schritt für Schritt zu verbessern.

### MIDI 2.0 nur eingeschränkt verifiziert

* Wir konnten bisher nicht genug MIDI 2.0-fähige Hardware beschaffen, sodass das UMP-Verhalten nur mit einer begrenzten Auswahl an Geräte-Kombinationen geprüft werden konnte
* Unterschiede in der MIDI 2.0-Unterstützung zwischen den macOS-Versionen (etwa abweichendes CoreMIDI-Verhalten) sind nicht vollständig erfasst
* Herstellerspezifische Erweiterungen und proprietäre Profile, die auf MIDI 2.0 aufsetzen, sind nur teilweise analysiert (konkret Teile von KORG); eigene Implementierungen anderer Hersteller sind bisher unberücksichtigt

### Kompatibilität der DX7-Presets

* 32 Anfangs-Presets sind enthalten; der klangliche Charakter im Vergleich zu klassischer FM-Synthese ist jedoch noch nicht für alle Presets vollständig überprüft
* Das Laden ganzer Bänke und der Import von SysEx-Patches werden in den kommenden TestFlight-Builds Schritt für Schritt ausgebaut

### Effekt-Kette

* Die sechsstufige FX-Kette (EQ → Drive → Chorus → Reverb → Stereo → Maximizer) befindet sich **auf dem Stand einer ersten lauffähigen Implementierung**. Die musikalische Feinabstimmung der Parameterbereiche und Endpunkte, CPU-Effizienz und das Optimieren des Zusammenspiels stehen noch aus

### Wenn dir Bugs oder Auffälligkeiten begegnen

Abstürze werden über Firebase Crashlytics automatisch erfasst (Details in der [Datenschutzerklärung](/M2DX-support/privacy-de)). Reproduzierbare Fehler lassen sich deutlich schneller eingrenzen – wenn möglich, schick uns gerne eine Meldung an [support@hakaru.net](mailto:support@hakaru.net).

---

:::
## Hauptfunktionen

### Volle Unterstützung für MIDI 2.0 UMP

Universal MIDI Packet (UMP) wird nativ unterstützt. Mit 16-Bit-Velocity (65.536 Stufen), 32-Bit-CCs und 32-Bit-Pitchbend lässt sich extrem geschmeidig und ausdrucksstark spielen. Bei Bedarf wird automatisch auf MIDI 1.0 zurückgeschaltet.

### DX7-kompatible FM-Engine

Eine FM-Synthese-Engine im DX7-Stil mit 6 Operatoren und 32 Algorithmen, in reinem Swift implementiert. Die Int32-Q24-Festkomma-Arithmetik strebt den Charakter klassischer FM-Klangerzeugung an. 32 Anfangs-Presets sind enthalten.

### 16-stimmige Polyphonie

16 Stimmen gleichzeitig, mit Sustain-Pedal (CC64) und Pitchbend (±2 Halbtöne). Soft-Clipping per Padé-genähertem tanh verhindert digitale Verzerrungen.

### Sechsstufige Effekt-Kette

Hochwertige Effekte in fester Signalfolge: EQ → Drive → Chorus → Reverb → Stereo → Maximizer. Jeder Parameter lässt sich per MIDI Learn auf einen beliebigen CC legen.

### MIDI-CI Property Exchange

Über 155 Parameter werden in einer hierarchischen Struktur veröffentlicht. Kompatible DAWs und Controller erkennen die Parameter automatisch, und das Preset-Handling läuft komplett über JSON – ganz ohne SysEx. Ein wirklich selbstbeschreibendes Instrument.

### Niedrige Latenz

Dank direkter Wiedergabe über AVAudioSourceNode läuft die FM-Engine direkt im CoreAudio-Render-Callback. Buffer-Queueing-Overhead entfällt vollständig, sodass die effektive Latenz im Wesentlichen der iOS-IOBufferDuration (rund 5 ms) entspricht.

---

## Systemvoraussetzungen

* **iOS / iPadOS 18 oder neuer** (TestFlight-Beta)
* Eine macOS-Version ist für die Zukunft geplant

---

## Häufige Fragen

### „Installieren“ ist ausgegraut

Direkt nach der Beta-App-Review kann es einen Moment dauern, bis die Build in TestFlight sichtbar wird. Bitte nach etwa 24 Stunden noch einmal versuchen.

### Was tun bei einem Absturz?

Ab Version 1.3.1 (Build 5) ist automatisches Crash-Reporting per Firebase Crashlytics aktiv. Wenn du den Absturz reproduzieren kannst, lässt sich die Ursache anhand der Logs schnell finden und beheben. Details zu den erfassten Daten findest du in der [Datenschutzerklärung](/M2DX-support/privacy-de).

### Lassen sich DX7-SysEx-Presets laden?

32 Anfangs-Presets sind bereits enthalten. Den Import eigener SysEx-Banks kündigen wir in einem der kommenden TestFlight-Builds an.

### Brauche ich eine MIDI 2.0-fähige DAW?

Nein. Da M2DX automatisch auf MIDI 1.0 zurückfällt, funktioniert er problemlos mit klassischen MIDI-Controllern und DAWs. Mit MIDI 2.0-fähiger Hardware oder Software gewinnst du zusätzlich an Auflösung und Ausdruck.

### Lässt sich M2DX als AUv3-Plug-in nutzen?

Aktuell läuft M2DX als eigenständige App für iOS und iPadOS. Eine AUv3-Version ist in Überlegung.

---

## Links

* GitHub: [github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* Synthese-Engine: [M2DX-Core](/M2DX-Core-support/index-de) (Pure-Swift-DX7-FM-Bibliothek)
* [Datenschutzerklärung](/M2DX-support/privacy-de)

---

## Kontakt

Fragen, Fehlerberichte oder Feature-Wünsche schickst du am besten an:  
[**support@hakaru.net**](mailto:support@hakaru.net)
