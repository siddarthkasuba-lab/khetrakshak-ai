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

## Getting started

```bash
pip install -r requirements.txt
python data/sample_images/generate_sample.py   # creates 3 synthetic test leaf images
python src/main.py --image data/sample_images/sample_leaf.png --crop tomato --area 2 --language hi
```

Try the other sample images too:

```bash
python src/main.py --image data/sample_images/sample_leaf_healthy.png --crop tomato --area 1
python src/main.py --image data/sample_images/sample_leaf_mildew.png --crop tomato --area 1.5 --language hi
```

No trained model weights are bundled in this repo (see `models/README.md` for why, and how the real NPU model is produced via Qualcomm AI Hub). Without `models/plant_disease.onnx` present, the classifier automatically uses a lightweight color-based heuristic so the full pipeline — diagnosis, dosage calculation, scheme matching, regional-language output, local outbreak logging — is runnable and testable end-to-end right now.

## Project structure

```
src/
  classifier.py      on-device vision model (ONNX/QNN) + heuristic fallback
  dosage_engine.py   deterministic treatment + dosage calculator
  scheme_matcher.py  matches disease to cached government schemes
  language.py        regional-language text + on-device TTS hook
  sync_log.py        local-first diagnosis log + opportunistic sync stub
  main.py            CLI entrypoint tying the pipeline together
data/
  treatments.json    treatment/dosage database
  schemes.json       government scheme database
  sample_images/     synthetic test images + generator script
models/
  README.md          how the real NPU model is produced and where it goes
```

## Tech stack

- **Vision model:** EfficientNet-Lite / MobileNetV3, fine-tuned on plant-disease imagery, optimized and compiled through [Qualcomm AI Hub](https://aihub.qualcomm.com).
- **On-device inference:** ONNX Runtime with the QNN execution provider, targeting the Snapdragon NPU.
- **Dosage + scheme engine:** deterministic, rules-based (not LLM-driven) for auditable recommendations.
- **Regional language output:** on-device TTS, no cloud translation calls.
- **Platform:** Windows desktop app for Snapdragon-powered HP Omnibook devices.

## Status

Working prototype submission for the Build & Present Challenge — CLI pipeline is fully functional with the heuristic fallback classifier; see `models/README.md` for the path to swap in the trained NPU model. See the pitch deck (submitted separately) for the full architecture and roadmap.

## Roadmap

- [x] Phase 1: capture → diagnosis → treatment + dosage, one regional language (this submission)
- [ ] Phase 2: additional regional languages, audio playback, opportunistic sync + heatmap module
- [ ] Phase 3: pilot with a Krishi Vigyan Kendra to validate dosage engine and scheme database

## License

TBD
