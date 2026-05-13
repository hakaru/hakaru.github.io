---
title: "M2DX Support"
description: "M2DX supportpagina. DX7-compatibele FM-synthesizer met MIDI 2.0 voor iOS. Nu beschikbaar als TestFlight-bèta."
slug: /
---

DX7-compatibele FM-synthesizer met MIDI 2.0


[Doe mee aan de TestFlight-bèta](https://testflight.apple.com/join/BAtGszPw)

Welkom op de supportpagina van M2DX.

M2DX is een DX7-compatibele FM-synthesizer voor iOS met ondersteuning voor MIDI 2.0. De klassieke FM-klank van 6 operators en 32 algoritmes is volledig opnieuw geïmplementeerd in pure Swift 6. De synthesemotor draait op de bibliotheek [M2DX-Core](/M2DX-Core-support/index-nl).

---

## Nu beschikbaar als TestFlight-bèta

Probeer de publieke bèta uit op **iOS / iPadOS 18 of hoger**:

1. Installeer Apple's **TestFlight**-app uit de App Store (alleen de eerste keer)
2. Open [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw) op je iPhone of iPad
3. Tik op "Accepteren" en daarna op "Installeer"

Let op: vlak na goedkeuring van een nieuwe bètabuild door de App Review kan het 1 à 2 minuten duren voordat de eerste installatie beschikbaar is — in uitzonderlijke gevallen tot zo'n 24 uur.

---

## Huidige status — waarom TestFlight

M2DX heeft **nog niet het kwaliteitsniveau van een volwaardig instrument** bereikt. We brengen de publieke TestFlight-bèta uit met de onderstaande beperkingen en onbeproefde onderdelen, om feedback te verzamelen en de app stap voor stap te verbeteren.

### MIDI 2.0-dekking is beperkt

* We hebben onvoldoende MIDI 2.0-hardware kunnen aanschaffen, waardoor het UMP-gedrag slechts met een beperkt aantal apparaatcombinaties is gecontroleerd
* De verschillen in MIDI 2.0-ondersteuning tussen macOS-versies (afwijkend gedrag van CoreMIDI en dergelijke) zijn nog niet volledig in kaart gebracht
* Fabrikantspecifieke uitbreidingen en eigen profielen bovenop MIDI 2.0 zijn slechts gedeeltelijk geanalyseerd (concreet: delen van de implementatie van KORG); eigen implementaties van andere fabrikanten zijn nog niet aangeraakt

### Compatibiliteit van DX7-presets

* Er zijn 32 initiële presets meegeleverd, maar het klankkarakter ten opzichte van klassieke FM-synthese is nog niet voor alle presets volledig geverifieerd
* De compatibiliteit van het laden van complete banks en het importeren van SysEx-patches wordt geleidelijk verbeterd in toekomstige TestFlight-builds

### FX-keten

* De zesdelige FX-keten (EQ → Drive → Chorus → Reverb → Stereo → Maximizer) bevindt zich **in de fase van een werkende implementatie**. Het muzikaal afstemmen van parameterbereiken en eindwaarden, de CPU-efficiëntie en het optimaliseren van de onderlinge wisselwerking moeten nog gebeuren

### Bugs of vreemd gedrag tegengekomen?

Crashes worden automatisch gemeld via Firebase Crashlytics (zie het [privacybeleid](/M2DX-support/privacy-nl) voor meer informatie). Reproduceerbare problemen zijn makkelijker op te lossen — als het lukt, stuur dan graag een melding naar [support@hakaru.net](mailto:support@hakaru.net).

---

## Belangrijkste functies

### Volledige ondersteuning voor MIDI 2.0 UMP

Native ondersteuning voor Universal MIDI Packet (UMP). Met 16-bits velocity (65.536 stappen), 32-bits CC en 32-bits pitchbend speel je vloeiend en bijzonder expressief. Bij MIDI 1.0-apparatuur valt M2DX automatisch terug.

### DX7-compatibele FM-engine

Een DX7-achtige FM-synthese-engine met 6 operators en 32 algoritmes, geïmplementeerd in puur Swift. De Int32 Q24-vastekommarekening streeft naar het karakter van klassieke FM-synthese. 32 initiële presets zijn meegeleverd.

### 16-stemmige polyfonie

Speel 16 noten tegelijk, met ondersteuning voor het sustainpedaal (CC64) en pitchbend (±2 halve tonen). Soft clipping op basis van een Padé-benadering van tanh houdt digitale vervorming buiten de deur.

### Effectketen met zes secties

Een hoogwaardige effectketen in de volgorde EQ → Drive → Chorus → Reverb → Stereo → Maximizer. Elke parameter is via MIDI Learn aan een willekeurige CC te koppelen.

### MIDI-CI Property Exchange

Meer dan 155 parameters worden hiërarchisch beschikbaar gemaakt. Ondersteunde DAW's en controllers ontdekken parameters automatisch, en presetbeheer verloopt via JSON — zonder SysEx. Een volledig zelfbeschrijvend instrument dus.

### Lage latency

De FM-engine wordt rechtstreeks aangedreven door AVAudioSourceNode binnen de render-callback van CoreAudio. Doordat er geen overhead is van bufferqueues, valt de feitelijke latency samen met IOBufferDuration van iOS (circa 5 ms).

---

## Systeemvereisten

* **iOS / iPadOS 18 of hoger** (beschikbaar via TestFlight)
* Een macOS-versie staat op de planning

---

## Veelgestelde vragen

### "Installeer" is grijs en niet aan te tikken

Vlak nadat de App Review een bètabuild heeft goedgekeurd, duurt het soms even voordat TestFlight de wijziging heeft verwerkt. Probeer het na ongeveer 24 uur opnieuw.

### Wat moet ik doen als de app crasht?

Vanaf v1.3.1 (build 5) staan automatische crashrapporten via Firebase Crashlytics aan. Als je de crash kunt reproduceren, kunnen we via de logs snel de oorzaak vinden en oplossen. Voor details over welke gegevens we verzamelen verwijzen we naar het [privacybeleid](/M2DX-support/privacy-nl).

### Kan ik DX7 SysEx-presets inladen?

Op dit moment zijn er 32 initiële presets meegeleverd. Over het importeren van eigen SysEx-banken volgt meer informatie in een toekomstige TestFlight-build.

### Heb ik een MIDI 2.0-DAW nodig?

Nee. Omdat M2DX automatisch terugvalt op MIDI 1.0, werkt het ook prima met je bestaande MIDI-controllers en DAW's. In een MIDI 2.0-omgeving krijg je daarbovenop een veel hogere expressieresolutie.

### Is M2DX als AUv3-plug-in te gebruiken?

Voorlopig is het een standalone iOS / iPadOS-app. Een AUv3-versie wordt overwogen.

---

## Links

* GitHub: [github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* Synthesemotor: [M2DX-Core](/M2DX-Core-support/index-nl) (pure-Swift DX7 FM-bibliotheek)
* [Privacybeleid](/M2DX-support/privacy-nl)

---

## Contact

Vragen, bugmeldingen of suggesties voor nieuwe functies zijn van harte welkom op:  
[**support@hakaru.net**](mailto:support@hakaru.net)
