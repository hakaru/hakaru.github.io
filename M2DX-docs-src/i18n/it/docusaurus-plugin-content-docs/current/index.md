---
title: "M2DX Supporto"
description: "Pagina di supporto di M2DX. Sintetizzatore FM compatibile DX7 con MIDI 2.0 per iOS. Beta disponibile su TestFlight."
slug: /
---

Sintetizzatore FM compatibile DX7 con MIDI 2.0


[Partecipa alla beta su TestFlight](https://testflight.apple.com/join/BAtGszPw)

Benvenuto nella pagina di supporto di M2DX.

M2DX è un'app per iOS che riproduce fedelmente il sintetizzatore FM DX7, con il supporto nativo per MIDI 2.0. Le sonorità FM classiche, ottenute da 6 operatori e 32 algoritmi, sono state riscritte completamente in Pure Swift 6. Il motore di sintesi si basa sulla libreria [M2DX-Core](https://hakaru.net/M2DX-Core-support/index-it).

---

## Beta su TestFlight

La beta pubblica è disponibile su **iOS / iPadOS 18 o successivi**:

1. Installa l'app **TestFlight** di Apple dall'App Store (solo la prima volta)
2. Apri [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw) da iPhone o iPad
3. Tocca "Accetta" e poi "Installa"

Nota: subito dopo l'approvazione della Beta App Review, la prima installazione potrebbe richiedere uno o due minuti per essere disponibile (in alcuni casi fino a 24 ore).

---

:::info Stato attuale — Perché TestFlight

M2DX **non ha ancora raggiunto una qualità da strumento professionale**. Pubblichiamo la beta pubblica su TestFlight con i limiti e i punti non ancora verificati elencati di seguito, per raccogliere feedback e migliorare progressivamente.

### Copertura MIDI 2.0 limitata

* Non siamo riusciti a procurarci hardware MIDI 2.0 in quantità sufficiente, perciò il comportamento dei UMP è stato verificato solo su un numero ristretto di combinazioni di dispositivi
* Le differenze nel supporto MIDI 2.0 tra le varie versioni di macOS (differenze di comportamento di CoreMIDI, ecc.) non sono state ancora caratterizzate del tutto
* Le estensioni proprietarie e i profili specifici dei produttori basati su MIDI 2.0 sono stati analizzati solo parzialmente (in particolare alcune parti dell'implementazione KORG); le implementazioni proprietarie degli altri produttori non sono ancora state affrontate

### Compatibilità con i preset DX7

* L'app include 32 preset iniziali, ma il carattere sonoro rispetto alla sintesi FM classica non è ancora stato verificato in modo completo per tutti i preset
* La compatibilità nel caricamento di intere bank e nell'importazione di patch SysEx verrà migliorata gradualmente nelle prossime build su TestFlight

### Catena FX

* La catena FX a 6 stadi (EQ → Drive → Chorus → Reverb → Stereo → Maximizer) è **per ora a livello di implementazione funzionante**. La taratura musicale dei range dei parametri e dei valori di estremo, l'efficienza CPU e l'ottimizzazione delle interazioni sono ancora da affrontare

### Se incontri bug o comportamenti strani

I crash vengono raccolti automaticamente tramite Firebase Crashlytics (per i dettagli consulta la [Privacy Policy](https://hakaru.net/M2DX-support/privacy-it)). I problemi riproducibili sono più facili da risolvere: se puoi, ti chiediamo di inviare una segnalazione a [support@hakaru.net](mailto:support@hakaru.net).

---

:::
## Caratteristiche principali

### Pieno supporto MIDI 2.0 UMP

Supporto nativo per Universal MIDI Packet (UMP). Velocity a 16 bit (65.536 livelli), CC a 32 bit e pitch bend a 32 bit garantiscono un'esecuzione fluida e ricca di sfumature espressive. Il fallback automatico al MIDI 1.0 è sempre garantito.

### Motore FM compatibile DX7

Un motore di sintesi FM in stile DX7 a 6 operatori e 32 algoritmi, implementato in puro Swift. L'aritmetica a virgola fissa Int32 Q24 punta al carattere della sintesi FM classica. Sono inclusi 32 preset iniziali.

### Polifonia a 16 voci

16 voci simultanee, supporto per il pedale sustain (CC64) e pitch bend (±2 semitoni). La saturazione morbida con tanh ad approssimazione di Padé previene la distorsione digitale.

### Catena di effetti a 6 stadi

Effetti di alta qualità nell'ordine EQ → Drive → Chorus → Reverb → Stereo → Maximizer. Ogni parametro è assegnabile a qualunque CC tramite il MIDI Learn.

### MIDI-CI Property Exchange

Strumento auto-descrittivo che espone oltre 155 parametri organizzati in modo gerarchico. I DAW e i controller compatibili possono individuare automaticamente i parametri e gestire i preset in formato JSON, senza ricorrere al SysEx.

### Bassa latenza

Rendering diretto tramite AVAudioSourceNode: il motore FM viene pilotato all'interno della render callback di CoreAudio, eliminando il sovraccarico del buffer queueing. La latenza effettiva coincide con l'IOBufferDuration di iOS (circa 5 ms).

---

## Requisiti di sistema

* **iOS / iPadOS 18 o successivi** (in distribuzione su TestFlight)
* La versione macOS è prevista in futuro

---

## Domande frequenti

### Il pulsante "Installa" è in grigio

Subito dopo l'approvazione della Beta App Review può servire un po' di tempo perché TestFlight si aggiorni. Ti consigliamo di riprovare entro 24 ore.

### Cosa fare in caso di crash?

A partire dalla versione 1.3.1 (build 5) i report automatici dei crash, gestiti tramite Firebase Crashlytics, sono attivi. Se riesci a riprodurre il problema, possiamo individuare la causa nei log e correggerla rapidamente. Per i dettagli sui dati raccolti consulta la [privacy policy](https://hakaru.net/M2DX-support/privacy-it).

### Posso caricare i preset SysEx del DX7?

L'app include 32 preset iniziali. Daremo informazioni sull'importazione di banchi SysEx personali in una delle prossime build su TestFlight.

### Serve un DAW compatibile MIDI 2.0?

No. Il fallback al MIDI 1.0 ti permette di usare M2DX con qualunque controller o DAW esistente. Naturalmente, in un ambiente MIDI 2.0 puoi sfruttare una risoluzione espressiva molto più alta.

### È disponibile come plug-in AUv3?

Per ora M2DX è un'app standalone per iOS / iPadOS. Stiamo valutando il supporto AUv3.

---

## Link

* GitHub: [github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* Motore di sintesi: [M2DX-Core](https://hakaru.net/M2DX-Core-support/index-it) (libreria FM DX7 in Pure Swift)
* [Privacy policy](https://hakaru.net/M2DX-support/privacy-it)

---

## Contatti

Per domande, segnalazioni di bug o richieste di nuove funzionalità, scrivici pure all'indirizzo:  
[**support@hakaru.net**](mailto:support@hakaru.net)
