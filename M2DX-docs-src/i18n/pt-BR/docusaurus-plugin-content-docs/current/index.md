---
title: "M2DX Suporte"
description: "Página de suporte do M2DX. Sintetizador FM compatível com DX7 e MIDI 2.0 para iOS. Beta disponível pelo TestFlight."
slug: /
---

Sintetizador FM compatível com DX7 e MIDI 2.0


[Entrar na beta do TestFlight](https://testflight.apple.com/join/BAtGszPw)

Bem-vindo à página de suporte do M2DX.

O M2DX é um sintetizador FM compatível com DX7 para iOS, com suporte a MIDI 2.0. Ele recria o som FM clássico de 6 operadores e 32 algoritmos, totalmente reimplementado em Pure Swift 6. O motor de síntese usa a biblioteca [M2DX-Core](https://hakaru.net/M2DX-Core-support/index-pt-BR).

---

## Beta disponível pelo TestFlight

A beta pública roda em **iOS / iPadOS 18 ou superior**:

1. Instale o app **TestFlight** da Apple pela App Store (apenas na primeira vez)
2. No iPhone ou iPad, abra [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw)
3. Toque em "Aceitar" e depois em "Instalar"

Observação: logo após a aprovação da revisão da beta, a primeira instalação pode levar de 1 a 2 minutos para ficar disponível (em alguns casos, até 24 horas).

---

:::info Status atual — Por que TestFlight

O M2DX **ainda não atingiu a qualidade de um instrumento pronto para uso profissional**. Estamos publicando a beta pública no TestFlight com as limitações e pontos não verificados listados abaixo, com o objetivo de reunir feedback e evoluir o app.

### A cobertura de MIDI 2.0 é limitada

* Não conseguimos obter hardware compatível com MIDI 2.0 em quantidade suficiente, por isso o comportamento do UMP só foi testado em um conjunto restrito de combinações de dispositivos
* As diferenças no suporte a MIDI 2.0 entre versões do macOS (variações de comportamento do CoreMIDI etc.) ainda não foram totalmente mapeadas
* Extensões específicas de fabricantes e perfis proprietários construídos sobre o MIDI 2.0 só foram analisados parcialmente (especificamente, partes da implementação da KORG); as implementações proprietárias de outros fabricantes ainda não foram abordadas

### Compatibilidade com presets do DX7

* 32 presets iniciais estão incluídos, mas o caráter sonoro em relação à síntese FM clássica ainda não foi totalmente verificado em todos os presets
* A compatibilidade com o carregamento de bancos e a importação de patches via SysEx será aprimorada de forma gradual nas próximas builds do TestFlight

### Cadeia de FX

* A cadeia de FX de 6 estágios (EQ → Drive → Chorus → Reverb → Stereo → Maximizer) está **no estágio de "implementação funcional"**. O ajuste musical das faixas de parâmetros e dos valores de extremidade, a eficiência de CPU e a otimização das interações entre os módulos ainda estão por vir

### Se você encontrar bugs ou comportamentos estranhos

Os crashes são reportados automaticamente pelo Firebase Crashlytics (consulte a [Política de Privacidade](https://hakaru.net/M2DX-support/privacy-pt-BR) para mais detalhes). Problemas com passos de reprodução são mais fáceis de corrigir — se possível, envie um relato para [support@hakaru.net](mailto:support@hakaru.net).

---

:::
## Principais recursos

### Suporte completo a MIDI 2.0 UMP

Suporte nativo a Universal MIDI Packet (UMP). Velocidade de 16 bits (65.536 níveis), CC de 32 bits e pitch bend de 32 bits permitem uma execução fluida e cheia de expressão. Faz fallback automático para MIDI 1.0 quando necessário.

### Motor FM compatível com DX7

Motor de síntese FM no estilo DX7 com 6 operadores e 32 algoritmos, implementado em Swift puro. A aritmética em ponto fixo Int32 Q24 busca o caráter da síntese FM clássica. Inclui 32 presets iniciais.

### Polifonia de 16 vozes

Até 16 vozes simultâneas, com suporte a pedal de sustain (CC64) e pitch bend (±2 semitons). Soft clipping baseado em tanh por aproximação de Padé evita a distorção digital.

### Cadeia de efeitos em 6 estágios

Efeitos de alta qualidade na ordem EQ → Drive → Chorus → Reverb → Stereo → Maximizer. Todos os parâmetros podem ser mapeados para qualquer CC via MIDI Learn.

### MIDI-CI Property Exchange

Mais de 155 parâmetros expostos em estrutura hierárquica. Um instrumento autodescritivo: DAWs e controladores compatíveis descobrem os parâmetros automaticamente, e o gerenciamento de presets em JSON dispensa o uso de SysEx.

### Baixa latência

Renderização direta via AVAudioSourceNode: o motor FM é executado dentro do callback de render do CoreAudio. Sem overhead de fila de buffers, a latência efetiva é o IOBufferDuration do iOS (cerca de 5 ms).

---

## Requisitos

* **iOS / iPadOS 18 ou superior** (em distribuição via TestFlight)
* Versão para macOS prevista para o futuro

---

## Perguntas frequentes

### O botão "Instalar" está esmaecido

Logo após a aprovação da revisão da beta, a propagação no TestFlight pode demorar um pouco. Tente novamente em cerca de 24 horas.

### O que fazer se o app travar?

A partir da versão 1.3.1 (build 5), os relatórios automáticos de falha pelo Firebase Crashlytics estão ativados. Se você conseguir reproduzir a falha, os logs nos ajudam a identificar a causa e corrigi-la rapidamente. Para detalhes sobre os dados coletados, consulte a [Política de Privacidade](https://hakaru.net/M2DX-support/privacy-pt-BR).

### Posso carregar presets SysEx do DX7?

O app já vem com 32 presets iniciais. Informações sobre a importação de bancos SysEx do usuário serão divulgadas em builds futuras do TestFlight.

### Preciso de uma DAW compatível com MIDI 2.0?

Não. Como o app faz fallback para MIDI 1.0, ele funciona normalmente com controladores e DAWs convencionais. Em ambientes com MIDI 2.0, você ganha uma expressividade de resolução ainda maior.

### Funciona como plug-in AUv3?

Por enquanto, é um app standalone para iOS / iPadOS. O suporte a AUv3 está em estudo.

---

## Links

* GitHub: [github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* Motor de síntese: [M2DX-Core](https://hakaru.net/M2DX-Core-support/index-pt-BR) (biblioteca FM DX7 em Pure Swift)
* [Política de Privacidade](https://hakaru.net/M2DX-support/privacy-pt-BR)

---

## Contato

Para dúvidas, relatos de bugs ou sugestões de recursos, escreva para:  
[**support@hakaru.net**](mailto:support@hakaru.net)
