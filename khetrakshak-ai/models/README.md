# Model

This folder is where the trained, NPU-ready classifier lives at runtime:
`plant_disease.onnx`. It is **not checked into this repo** — trained weights
are a large binary artifact that should be tracked separately (e.g. Git LFS,
or downloaded as a release asset), not committed directly.

When `plant_disease.onnx` is absent (e.g. a fresh clone of this repo), the
app automatically falls back to the color-heuristic classifier in
`src/classifier.py` so the rest of the pipeline can still be run and tested
end-to-end. See that file's docstring for details.

## How the real model is produced (Qualcomm AI Hub)

1. **Train / fine-tune** an EfficientNet-Lite or MobileNetV3 classifier on a
   plant-disease image dataset (e.g. PlantVillage, extended with regionally
   collected samples for Indian crop varieties).
2. **Upload to Qualcomm AI Hub** (https://aihub.qualcomm.com) using the
   Bring-Your-Own-Model (BYOM) flow to compile and optimize the model for
   Snapdragon X-series targets.
3. **Export to ONNX** and download the AI-Hub-optimized artifact.
4. **Place it at** `models/plant_disease.onnx` in this repo structure.
5. `src/classifier.py` will pick it up automatically and run it via
   `onnxruntime`'s `QNNExecutionProvider`, which targets the Snapdragon NPU
   (falling back to CPU automatically if QNN isn't available on the current
   machine, e.g. in local development).

## Expected model I/O contract

- **Input:** `float32` tensor, shape `(1, 3, 224, 224)`, RGB, normalized to `[0, 1]`.
- **Output:** logits over the label set in `src/classifier.py::LABELS`
  (`healthy`, `leaf_blight`, `powdery_mildew`, `bacterial_spot`).

Extending the label set only requires updating `LABELS` here and adding the
matching entries to `data/treatments.json` and `data/schemes.json`.
