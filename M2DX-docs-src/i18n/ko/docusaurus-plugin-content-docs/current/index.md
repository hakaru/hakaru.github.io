---
title: "M2DX 지원"
description: "M2DX 지원 페이지. MIDI 2.0 지원 DX7 호환 FM 신디사이저 iOS 앱. TestFlight 베타 배포 중."
slug: /
---

MIDI 2.0 지원 DX7 호환 FM 신디사이저


[TestFlight 베타에 참여하기](https://testflight.apple.com/join/BAtGszPw)

M2DX 지원 페이지에 오신 것을 환영합니다.

M2DX는 MIDI 2.0을 지원하는 iOS용 DX7 호환 FM 신디사이저 앱입니다. 6 오퍼레이터 × 32 알고리즘이 만들어내는 클래식 FM 사운드를 Pure Swift 6로 완전히 재구현했습니다. 신디시스 엔진은 [M2DX-Core](/M2DX-Core-support/index-ko) 라이브러리를 사용합니다.

---

## TestFlight 베타 배포 중

**iOS / iPadOS 18 이상**에서 퍼블릭 베타를 사용해 보실 수 있습니다.

1. App Store에서 Apple **TestFlight** 앱 설치 (최초 1회)
2. iPhone / iPad에서 [testflight.apple.com/join/BAtGszPw](https://testflight.apple.com/join/BAtGszPw) 열기
3. '승인' → '설치' 탭

※ 베타 앱 심사 승인 직후 처음 설치하는 경우, 반영까지 1~2분 (경우에 따라 24시간 정도) 걸릴 수 있습니다.

---

## 현재 상태 — TestFlight로 공개하는 이유

M2DX는 아직 **악기로서 실용 수준에 도달하지 못했습니다**. 아래의 제약 사항과 미검증 항목을 안고 있는 상태이지만, 피드백을 수집하고 개선해 나가기 위해 TestFlight에서 퍼블릭 베타로 공개하고 있습니다.

### MIDI 2.0 검증 범위가 제한적입니다

* MIDI 2.0 지원 하드웨어를 충분히 확보하지 못해, UMP 동작 확인은 한정된 기기 조합에서만 진행한 상태입니다
* macOS 버전별 MIDI 2.0 지원 차이(CoreMIDI 동작 차이 등)는 완전히 파악하지 못했습니다
* 각 제조사가 MIDI 2.0 사양 위에 얹은 독자 확장 및 독자 프로파일에 대한 분석은 일부(구체적으로는 KORG의 일부)만 대응되어 있으며, 타사의 독자 구현은 아직 손대지 못한 상태입니다

### DX7 프리셋 호환성 검증

* 32종의 초기 프리셋을 내장하고 있지만, 빈티지 FM 사운드와 비교한 음색 검증은 모든 프리셋에 대해 마치지 못했습니다
* 뱅크 전체 및 SysEx 패치 로딩 호환성은 향후 TestFlight 빌드를 통해 단계적으로 정비해 나갈 예정입니다

### 이펙트 체인

* 6단 FX 체인(EQ → Drive → Chorus → Reverb → Stereo → Maximizer)은 **일단 동작하는 형태로 구현한 단계**입니다. 파라미터 가청 범위 및 엔드포인트 값의 음악적 조정, CPU 효율, 상호작용 최적화는 앞으로 진행할 예정입니다

### 버그나 이상 동작을 발견하신 분께

크래시는 Firebase Crashlytics를 통해 자동으로 수집됩니다(자세한 내용은 [개인정보 처리방침](/M2DX-support/privacy-ko)을 참조해 주십시오). 재현 조건이 명확한 버그는 원인 파악이 빨라지므로, 가능하시다면 [support@hakaru.net](mailto:support@hakaru.net)으로 보고해 주시면 감사하겠습니다.

---

## 주요 특징

### MIDI 2.0 UMP 완전 지원

Universal MIDI Packet (UMP)을 네이티브로 지원합니다. 16비트 벨로시티 (65,536단계), 32비트 CC, 32비트 피치 벤드를 통해 부드럽고 표현력 풍부한 연주가 가능합니다. MIDI 1.0으로 자동 폴백도 지원합니다.

### DX7 호환 FM 엔진

DX7 계열의 6 오퍼레이터 × 32 알고리즘 FM 신디시스 엔진을 Pure Swift로 구현했습니다. Int32 Q24 고정 소수점 연산으로 빈티지 FM 신디사이저의 캐릭터를 지향합니다. 32종의 초기 프리셋이 내장되어 있습니다.

### 16 보이스 폴리포니

16 보이스 동시 발음, 서스테인 페달 (CC64), 피치 벤드 (±2 반음)를 지원합니다. Padé 근사 tanh 기반의 소프트 클리핑으로 디지털 왜곡을 방지합니다.

### 6단 이펙트 체인

EQ → Drive → Chorus → Reverb → Stereo → Maximizer 순서로 연결된 고품질 이펙트를 제공합니다. 모든 파라미터는 MIDI Learn으로 원하는 CC에 매핑할 수 있습니다.

### MIDI-CI Property Exchange

155개 이상의 파라미터를 계층 구조로 공개합니다. 호환되는 DAW나 컨트롤러에서 파라미터를 자동으로 검색할 수 있으며, JSON 기반 프리셋 관리 (SysEx 불필요)가 가능한 자기 기술형 인스트루먼트입니다.

### 저지연

AVAudioSourceNode로 직접 렌더링하여 CoreAudio 렌더 콜백 위에서 FM 엔진을 구동합니다. 버퍼 큐잉 오버헤드를 제거하여 iOS의 IOBufferDuration (약 5ms)이 실질적인 지연 시간이 됩니다.

---

## 동작 환경

* **iOS / iPadOS 18 이상** (TestFlight 배포 중)
* macOS 버전은 향후 지원 예정

---

## 자주 묻는 질문

### '설치' 버튼이 비활성화되어 있어요

베타 앱 심사 승인 직후에는 TestFlight에 반영되기까지 시간이 걸릴 수 있습니다. 약 24시간 후에 다시 시도해 주세요.

### 크래시가 발생했을 때는 어떻게 하나요?

v1.3.1 (build 5)부터 Firebase Crashlytics를 통한 자동 크래시 리포트가 활성화되어 있습니다. 크래시를 재현해 주시면 로그를 통해 원인을 파악하여 신속하게 수정할 수 있습니다. 수집되는 데이터에 대한 자세한 내용은 [개인정보 처리방침](/M2DX-support/privacy-ko)을 참고해 주세요.

### DX7 SysEx 프리셋을 불러올 수 있나요?

32종의 초기 프리셋이 내장되어 있습니다. 사용자가 직접 가진 뱅크의 SysEx 가져오기에 대해서는 향후 TestFlight 빌드를 통해 안내드리겠습니다.

### MIDI 2.0 지원 DAW가 필요한가요?

아니요. MIDI 1.0 폴백도 지원하므로 기존 MIDI 컨트롤러나 DAW에서도 사용하실 수 있습니다. MIDI 2.0 지원 환경에서는 더 높은 해상도의 표현이 가능해집니다.

### AUv3 플러그인으로 사용할 수 있나요?

현재는 스탠드얼론 iOS / iPadOS 앱입니다. AUv3 지원은 검토 중입니다.

---

## 링크

* GitHub: [github.com/hakaru/M2DX](https://github.com/hakaru/M2DX)
* 신디시스 엔진: [M2DX-Core](/M2DX-Core-support/index-ko) (Pure Swift DX7 FM 라이브러리)
* [개인정보 처리방침](/M2DX-support/privacy-ko)

---

## 문의

질문, 버그 신고, 기능 요청은 아래 이메일로 편하게 연락해 주세요.  
[**support@hakaru.net**](mailto:support@hakaru.net)
