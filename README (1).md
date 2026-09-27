# KhetRakshak AI

Offline crop disease diagnosis and treatment advisor for Snapdragon-powered HP PCs, built for the Snapdragon® AI Lab Build & Present Challenge.

## What it does

1. **Capture** — a webcam photo or an imported image of a diseased crop leaf/plant.
2. **Diagnose** — an on-device vision model classifies the disease, running fully offline on the Snapdragon NPU via Qualcomm AI Hub.
3. **Prescribe** — a local rules engine returns organic/chemical treatment options with dosage scaled to the farmer's actual field size.
4. **Explain** — results are shown in the farmer's regional language as text and audio (on-device TTS), for low-literacy users.
5. **Connect** — matching government subsidy/crop-insurance schemes are surfaced from a locally cached database.
6. **Sync (opportunistic)** — when the device briefly gets Wi-Fi (e.g. at a Common Service Centre), anonymized reports sync to build a block-level outbreak heatmap.

## Why this is different

Most on-device agri-AI demos stop at "photo in, disease name out." KhetRakshak closes the loop: diagnosis → correctly-dosed treatment → scheme eligibility → outbreak visibility — entirely offline.

## Tech stack

- **Vision model:** EfficientNet-Lite / MobileNetV3, fine-tuned on plant-disease imagery, optimized and compiled through [Qualcomm AI Hub](https://aihub.qualcomm.com).
- **On-device inference:** ONNX Runtime with the QNN execution provider, targeting the Snapdragon NPU.
- **Dosage + scheme engine:** deterministic, rules-based (not LLM-driven) for auditable recommendations.
- **Regional language output:** on-device TTS, no cloud translation calls.
- **Platform:** Windows desktop app for Snapdragon-powered HP Omnibook devices.

## Status

Prototype submission for the Build & Present Challenge — see the pitch deck (`/docs`) for the full architecture and roadmap.

## Roadmap

- [ ] Phase 1: capture → diagnosis → treatment + dosage, one regional language (this submission)
- [ ] Phase 2: additional regional languages, audio playback, opportunistic sync + heatmap module
- [ ] Phase 3: pilot with a Krishi Vigyan Kendra to validate dosage engine and scheme database

## License

TBD
