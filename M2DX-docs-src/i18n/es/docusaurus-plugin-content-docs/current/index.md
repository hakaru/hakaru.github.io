---
title: "Soporte de M2DX"
description: "Página de soporte de M2DX. Sintetizador FM compatible con DX7 y MIDI 2.0 para iOS. Disponible en beta a través de TestFlight."
slug: /
---

Sintetizador FM compatible con DX7 y MIDI 2.0


[Únete a la beta de TestFlight](https://testflight.apple.com/join/BAtGszPw)

Te damos la bienvenida a la página de soporte de M2DX.

M2DX es un sintetizador FM para iOS compatible con DX7 y con MIDI 2.0. Reproduce el clásico sonido FM con sus 6 operadores y 32 algoritmos, totalmente reimplementado en Pure Swift 6. El motor de síntesis se apoya en la biblioteca [M2DX-Core](https://hakaru.net/M2DX-Core-support/index-es).

---

## Beta disponible en TestFlight

Puedes probar la beta pública en **iOS o iPadOS 18 o superior**:

1. Instala la app **TestFlight** de Apple desde la App Store (solo la primera vez).
2. Abre [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw) en tu iPhone o iPad.
3. Toca «Aceptar» y luego «Instalar».

Nota: justo después de que Apple aprueba una beta, la primera instalación puede tardar entre 1 y 2 minutos en aparecer (en algunos casos hasta 24 horas).

---

:::info Estado actual — Por qué TestFlight

M2DX **todavía no está al nivel necesario para usarse como instrumento en producción**. Lo publicamos como beta pública en TestFlight, con las limitaciones y áreas pendientes que se describen abajo, precisamente para recoger comentarios y poder mejorar la app.

### El alcance de la verificación de MIDI 2.0 es limitado

* No hemos podido conseguir suficiente hardware compatible con MIDI 2.0, así que las pruebas con UMP solo cubren un puñado de combinaciones de equipo.
* Las diferencias en el soporte de MIDI 2.0 entre versiones de macOS (variaciones de comportamiento de CoreMIDI, etc.) no están del todo caracterizadas.
* Solo hemos analizado parcialmente las extensiones y los perfiles propietarios que cada fabricante añade sobre la especificación de MIDI 2.0 (en concreto, una parte de los de KORG); las implementaciones propietarias de otras marcas siguen sin abordarse.

### Verificación de la compatibilidad con presets del DX7

* La app incluye 32 presets iniciales, pero todavía no hemos verificado el carácter sonoro frente a la síntesis FM clásica en todos ellos.
* La compatibilidad con la carga de bancos completos y de patches SysEx la iremos ampliando en próximas builds de TestFlight.

### Cadena de efectos

* La cadena de FX de 6 etapas (EQ → Drive → Chorus → Reverb → Stereo → Maximizer) **está implementada en una primera versión funcional**. El ajuste musical de los rangos audibles y de los valores de los puntos extremos de cada parámetro, la eficiencia de CPU y la optimización de las interacciones quedan como trabajo pendiente.

### Si encuentras un fallo o algo que no suena bien

Los crashes se recogen automáticamente con Firebase Crashlytics (consulta los detalles en la [política de privacidad](https://hakaru.net/M2DX-support/privacy-es)). Cuando un fallo es reproducible, encontrar la causa es mucho más rápido, así que, si te es posible, agradecemos que nos lo comuniques en [support@hakaru.net](mailto:support@hakaru.net).

---

:::
## Características principales

### Compatibilidad total con MIDI 2.0 UMP

Soporte nativo para Universal MIDI Packet (UMP). Velocidad de 16 bits (65 536 niveles), CC de 32 bits y pitch bend de 32 bits para una interpretación fluida y muy expresiva. Si el entorno solo admite MIDI 1.0, la app cambia automáticamente a ese modo.

### Motor FM compatible con DX7

Motor de síntesis FM al estilo DX7 con 6 operadores y 32 algoritmos, implementado en Swift puro. La aritmética en punto fijo Int32 Q24 busca el carácter de la síntesis FM clásica. Incluye 32 presets iniciales.

### Polifonía de 16 voces

16 voces simultáneas, pedal de sustain (CC64) y pitch bend (±2 semitonos). El soft clipping mediante la aproximación de tanh con Padé evita la distorsión digital.

### Cadena de efectos de 6 etapas

Efectos de alta calidad encadenados en el orden EQ → Drive → Chorus → Reverb → Stereo → Maximizer. Cualquier parámetro puede asignarse a cualquier CC mediante MIDI Learn.

### MIDI-CI Property Exchange

Más de 155 parámetros expuestos en una estructura jerárquica. Es un instrumento autodescriptivo: los DAW y controladores compatibles pueden detectar los parámetros automáticamente y gestionar presets en formato JSON, sin necesidad de SysEx.

### Latencia baja

Renderizado directo con AVAudioSourceNode, ejecutando el motor FM dentro del callback de render de CoreAudio. Al eliminar la sobrecarga del buffering en cola, la latencia efectiva queda determinada por el IOBufferDuration de iOS (unos 5 ms).

---

## Requisitos del sistema

* **iOS o iPadOS 18 o superior** (disponible vía TestFlight).
* La versión para macOS llegará más adelante.

---

## Preguntas frecuentes

### El botón «Instalar» aparece atenuado

Justo después de que Apple aprueba la beta, TestFlight tarda un poco en propagar la actualización. Vuelve a intentarlo después de unas 24 horas.

### ¿Qué hago si la app se cierra de forma inesperada?

Desde la versión 1.3.1 (build 5) están activos los informes automáticos de fallos mediante Firebase Crashlytics. Si puedes reproducir el problema, los registros nos permiten encontrar la causa y publicar una corrección rápidamente. Encontrarás el detalle de los datos recogidos en la [política de privacidad](https://hakaru.net/M2DX-support/privacy-es).

### ¿Se pueden cargar presets SysEx del DX7?

La app incluye 32 presets iniciales. Sobre la importación de SysEx propios, daremos más información en próximas versiones de TestFlight.

### ¿Hace falta un DAW compatible con MIDI 2.0?

No. Como existe fallback automático a MIDI 1.0, puedes usar M2DX con cualquier controlador o DAW MIDI tradicional. En entornos compatibles con MIDI 2.0 obtendrás una resolución y una expresividad mayores.

### ¿Funciona como plugin AUv3?

De momento es una app independiente para iOS y iPadOS. La compatibilidad con AUv3 está en estudio.

---

## Enlaces

* GitHub: [github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* Motor de síntesis: [M2DX-Core](https://hakaru.net/M2DX-Core-support/index-es) (biblioteca FM DX7 en Pure Swift)
* [Política de privacidad](https://hakaru.net/M2DX-support/privacy-es)

---

## Contacto

Si tienes preguntas, quieres reportar un fallo o proponer una nueva función, escríbenos sin dudarlo a:  
[**support@hakaru.net**](mailto:support@hakaru.net)
