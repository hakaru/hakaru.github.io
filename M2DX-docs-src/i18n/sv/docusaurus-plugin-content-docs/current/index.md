---
title: "M2DX Support"
description: "Supportsida för M2DX. En DX7-kompatibel FM-synthesizer för iOS med stöd för MIDI 2.0. Just nu i öppen beta via TestFlight."
slug: /
---

DX7-kompatibel FM-synth med MIDI 2.0


[Gå med i TestFlight-betan](https://testflight.apple.com/join/BAtGszPw)

Välkommen till supportsidan för M2DX.

M2DX är en DX7-kompatibel FM-synth för iOS med fullt stöd för MIDI 2.0. Sex operatorer och samtliga 32 algoritmer ger dig den klassiska FM-klangen, helt nyimplementerad i Pure Swift 6. Själva synthesmotorn bygger på biblioteket [M2DX-Core](/M2DX-Core-support/index-sv).

---

## Öppen beta via TestFlight

Provkör den öppna betan på **iOS eller iPadOS 18 och senare**:

1. Installera Apples **TestFlight**-app från App Store (bara första gången).
2. Öppna [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw) på din iPhone eller iPad.
3. Tryck på ”Acceptera” och därefter ”Installera”.

Obs: direkt efter att en ny build har godkänts i Beta App Review kan det dröja ett par minuter (i enstaka fall upp till 24 timmar) innan den dyker upp i TestFlight.

---

## Aktuell status — därför kör vi via TestFlight

M2DX håller **ännu inte instrumentkvalitet**. Vi släpper ändå en öppen beta via TestFlight, med begränsningarna och de otestade punkterna nedan, för att kunna samla in återkoppling och förbättra appen steg för steg.

### Begränsad täckning för MIDI 2.0

* Vi har inte lyckats få tag på tillräckligt med MIDI 2.0-kompatibel hårdvara, så UMP-beteendet är bara verifierat för ett fåtal kombinationer av enheter.
* Skillnader i hur MIDI 2.0 stöds mellan olika macOS-versioner (till exempel hur CoreMIDI uppför sig) är inte fullt kartlagda.
* Tillverkarspecifika tillägg och egna profiler ovanpå MIDI 2.0 är bara delvis analyserade (närmare bestämt delar av KORG:s implementation); andra tillverkares egna lösningar har vi ännu inte tittat på.

### DX7-presetkompatibilitet

* 32 inledande presets följer med, men klangkaraktären jämfört med klassisk FM-syntes är inte fullt verifierad för samtliga presets.
* Inläsning av hela banker och import av SysEx-patcher förbättras gradvis i kommande TestFlight-builds.

### FX-kedjan

* Den sexstegs FX-kedjan (EQ → Drive → Chorus → Reverb → Stereo → Maximizer) är **på "fungerande implementation"-nivå**. Musikalisk finjustering av parameterintervall och ändpunkter, CPU-effektivitet och optimering av samspelet mellan stegen återstår.

### Om du hittar buggar eller något som känns konstigt

Krascher rapporteras automatiskt via Firebase Crashlytics (se [integritetspolicyn](/M2DX-support/privacy-sv) för mer information). Buggar som går att återskapa är lättare att åtgärda — om du har möjlighet, skicka gärna en rapport till [support@hakaru.net](mailto:support@hakaru.net).

---

## Funktioner i korthet

### Fullt stöd för MIDI 2.0 UMP

Universal MIDI Packet (UMP) hanteras nativt. Du får 16-bitars velocity (65 536 nivåer), 32-bitars CC och 32-bitars pitch bend för ett mjukt och uttrycksfullt spel. Vid behov går synthen automatiskt tillbaka till MIDI 1.0.

### DX7-kompatibel FM-motor

En FM-syntesmotor i DX7-stil med 6 operatorer och 32 algoritmer, implementerad i ren Swift. Int32 Q24-fixpunktsaritmetiken siktar på klangkaraktären hos klassisk FM-syntes. 32 inledande presets ingår.

### 16-stämmig polyfoni

Spela upp till 16 toner samtidigt med stöd för sustainpedal (CC64) och pitch bend (±2 halvtoner). En mjuk klippning baserad på Padé-approximerad tanh håller den digitala distorsionen borta.

### Effektkedja i sex steg

Signalvägen EQ → Drive → Chorus → Reverb → Stereo → Maximizer ger dig effekter av hög kvalitet. Alla parametrar kan kopplas till valfri CC via MIDI Learn.

### MIDI-CI Property Exchange

Över 155 parametrar exponeras i en hierarkisk struktur. Stödjande DAW:ar och styrenheter kan upptäcka parametrarna automatiskt, och presethanteringen sker via JSON utan något behov av SysEx — ett självbeskrivande instrument helt enkelt.

### Låg latens

FM-motorn körs direkt från CoreAudios renderingscallback via AVAudioSourceNode. Den extra fördröjningen från buffertköer försvinner helt, och det är iOS IOBufferDuration (ungefär 5 ms) som sätter den faktiska latensen.

---

## Systemkrav

* **iOS eller iPadOS 18 och senare** (distribueras via TestFlight).
* En macOS-version planeras längre fram.

---

## Vanliga frågor

### Knappen ”Installera” är gråmarkerad

Direkt efter att en build har godkänts i Beta App Review kan det ta en stund innan TestFlight uppdateras. Försök igen efter ungefär 24 timmar.

### Vad gör jag om appen kraschar?

Från och med v1.3.1 (build 5) skickar appen automatiska kraschrapporter via Firebase Crashlytics. Om du kan reproducera kraschen hjälper loggarna oss att hitta orsaken och åtgärda problemet snabbt. Vad som samlas in beskrivs i vår [integritetspolicy](/M2DX-support/privacy-sv).

### Kan jag läsa in SysEx-presets från DX7?

Just nu följer 32 inledande presets med appen. Hur import av egna SysEx-banker fungerar berättar vi mer om i kommande TestFlight-builds.

### Behöver jag en DAW med MIDI 2.0?

Nej. Eftersom M2DX även hanterar MIDI 1.0 fungerar appen utmärkt med traditionella MIDI-styrenheter och DAW:ar. I en MIDI 2.0-miljö får du dock tillgång till uttrycksmedel med högre upplösning.

### Kan jag använda M2DX som AUv3-plugin?

I dagsläget är M2DX en fristående app för iOS och iPadOS. AUv3-stöd är något vi tittar närmare på.

---

## Länkar

* GitHub: [github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* Synthesmotor: [M2DX-Core](/M2DX-Core-support/index-sv) (DX7 FM-bibliotek i Pure Swift)
* [Integritetspolicy](/M2DX-support/privacy-sv)

---

## Kontakt

Hör gärna av dig med frågor, buggrapporter eller önskemål om nya funktioner till adressen nedan:  
[**support@hakaru.net**](mailto:support@hakaru.net)
