---
title: "M2DX Support"
description: "Page de support de M2DX. Synthétiseur FM compatible DX7 avec MIDI 2.0 pour iOS. Bêta TestFlight en cours."
slug: /
---

Synthétiseur FM compatible DX7 avec MIDI 2.0


[Rejoindre la bêta TestFlight](https://testflight.apple.com/join/BAtGszPw)

Bienvenue sur la page de support de M2DX.

M2DX est une application de synthétiseur FM pour iOS, compatible DX7 et compatible MIDI 2.0. Le son FM classique signé 6 opérateurs et 32 algorithmes y est entièrement réimplémenté en pur Swift 6. Le moteur de synthèse repose sur la bibliothèque [M2DX-Core](/M2DX-Core-support/index-fr).

---

## Bêta TestFlight en cours

La bêta publique est ouverte sur **iOS / iPadOS 18 ou ultérieur** :

1. Installez l'application **TestFlight** d'Apple depuis l'App Store (uniquement la première fois)
2. Sur votre iPhone ou iPad, ouvrez [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw)
3. Touchez « Accepter », puis « Installer »

Note : juste après la validation par Beta App Review, la première installation peut mettre 1 à 2 minutes (parfois jusqu'à 24 heures) avant d'être disponible.

---

:::info État actuel — Pourquoi TestFlight

M2DX **n'a pas encore atteint un niveau de qualité digne d'un véritable instrument**. Nous publions cette bêta publique sur TestFlight avec les limites et les points non vérifiés énumérés ci-dessous, afin de recueillir vos retours et de progresser à partir de là.

### Couverture MIDI 2.0 limitée

* Faute d'avoir pu réunir suffisamment de matériel compatible MIDI 2.0, le comportement UMP n'a été vérifié que sur un éventail restreint de combinaisons d'appareils
* Les différences de prise en charge de MIDI 2.0 selon les versions de macOS (variations du comportement de CoreMIDI, etc.) ne sont pas encore entièrement caractérisées
* Les extensions et profils propriétaires que chaque fabricant ajoute par-dessus la spécification MIDI 2.0 ne sont analysés que partiellement (en l'occurrence une partie de l'implémentation KORG) ; les implémentations propriétaires des autres fabricants n'ont pas encore été abordées

### Compatibilité des presets DX7

* 32 presets initiaux sont fournis, mais le caractère sonore par rapport à la synthèse FM classique n'a pas été entièrement vérifié pour l'ensemble des presets
* Le chargement de banques complètes et la compatibilité d'import de patches SysEx seront améliorés progressivement au fil des prochaines builds TestFlight

### Chaîne FX

* La chaîne FX à 6 étages (EQ → Drive → Chorus → Reverb → Stereo → Maximizer) **n'en est qu'au stade « implémentation fonctionnelle »**. Le réglage musical des plages de paramètres et de leurs valeurs limites, l'efficacité CPU et l'optimisation des interactions restent à faire

### Si vous repérez des bugs ou des comportements étranges

Les crashes sont remontés automatiquement via Firebase Crashlytics (voir la [politique de confidentialité](/M2DX-support/privacy-fr) pour plus de détails). Les anomalies reproductibles sont nettement plus rapides à corriger : si possible, merci d'envoyer un rapport à [support@hakaru.net](mailto:support@hakaru.net).

---

:::
## Caractéristiques principales

### Prise en charge complète de MIDI 2.0 UMP

Universal MIDI Packet (UMP) pris en charge nativement. La vélocité 16 bits (65 536 niveaux), les CC 32 bits et le pitch bend 32 bits permettent un jeu fluide et hautement expressif. Repli automatique vers MIDI 1.0 lorsque nécessaire.

### Moteur FM compatible DX7

Moteur de synthèse FM de style DX7 à 6 opérateurs et 32 algorithmes, implémenté en pur Swift. L'arithmétique en virgule fixe Int32 Q24 vise le caractère de la synthèse FM classique. 32 presets initiaux sont inclus.

### Polyphonie 16 voix

16 voix simultanées, pédale de sustain (CC64) et pitch bend (±2 demi-tons). Un soft clipping basé sur une approximation de Padé de tanh évite la distorsion numérique.

### Chaîne d'effets à 6 étages

Effets haut de gamme dans l'ordre EQ → Drive → Chorus → Reverb → Stereo → Maximizer. Tous les paramètres peuvent être assignés à n'importe quel CC via MIDI Learn.

### MIDI-CI Property Exchange

Plus de 155 paramètres exposés dans une structure hiérarchique. Un instrument auto-descriptif : les DAW et contrôleurs compatibles découvrent automatiquement les paramètres, et la gestion des presets en JSON (sans SysEx) est possible.

### Faible latence

Rendu direct via AVAudioSourceNode : le moteur FM tourne dans le callback de rendu CoreAudio. La surcharge de la file d'attente de buffers est éliminée, et l'IOBufferDuration d'iOS (environ 5 ms) constitue la latence effective.

---

## Configuration requise

* **iOS / iPadOS 18 ou ultérieur** (en distribution TestFlight)
* Une version macOS est prévue ultérieurement

---

## Foire aux questions

### Le bouton « Installer » est grisé

Juste après la validation par Beta App Review, la propagation vers TestFlight peut prendre un certain temps. Réessayez environ 24 heures plus tard.

### Que faire en cas de plantage ?

Depuis la version 1.3.1 (build 5), la remontée automatique des plantages via Firebase Crashlytics est activée. Si vous parvenez à reproduire le plantage, les journaux nous permettent d'identifier la cause et de corriger rapidement. Pour le détail des données collectées, consultez notre [politique de confidentialité](/M2DX-support/privacy-fr).

### Peut-on charger des presets SysEx du DX7 ?

32 presets initiaux sont fournis. Des informations sur l'importation de banques SysEx personnelles seront communiquées dans une prochaine build TestFlight.

### Faut-il un DAW compatible MIDI 2.0 ?

Non. Le repli MIDI 1.0 étant assuré, les contrôleurs MIDI et les DAW classiques fonctionnent parfaitement. Sur un environnement compatible MIDI 2.0, vous bénéficierez en plus d'une expressivité à plus haute résolution.

### L'app fonctionne-t-elle en plug-in AUv3 ?

Pour le moment, c'est une app standalone iOS / iPadOS. Une version AUv3 est à l'étude.

---

## Liens

* GitHub : [github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* Moteur de synthèse : [M2DX-Core](/M2DX-Core-support/index-fr) (bibliothèque FM DX7 en pur Swift)
* [Politique de confidentialité](/M2DX-support/privacy-fr)

---

## Contact

Pour toute question, signalement de bug ou demande de fonctionnalité, écrivez-nous sans hésiter à l'adresse suivante :  
[**support@hakaru.net**](mailto:support@hakaru.net)
