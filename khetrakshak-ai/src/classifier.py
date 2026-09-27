"""
classifier.py

Disease classification for a crop leaf image.

Production path (on Snapdragon-powered HP PC):
    A quantized EfficientNet-Lite / MobileNetV3 model, fine-tuned on plant-disease
    imagery and compiled through Qualcomm AI Hub (https://aihub.qualcomm.com), is
    exported to ONNX and run via onnxruntime's QNN execution provider so inference
    is accelerated on the Snapdragon NPU.

    See models/README.md for the exact AI Hub export/compile steps.

Demo path (this repo, no GPU/NPU/model weights bundled):
    Trained model weights are not checked into this repo (standard practice --
    they're large binary artifacts, tracked separately). When models/plant_disease.onnx
    is present, this module loads and runs it. When it is not present -- e.g. when
    running this prototype straight from a fresh checkout -- it falls back to a
    lightweight, fully-real (not mocked) color-based heuristic classifier so the
    rest of the pipeline (dosage engine, scheme matching, language output) can be
    exercised end-to-end without needing the trained weights.
"""

import os
from dataclasses import dataclass

import numpy as np
from PIL import Image

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "plant_disease.onnx")
LABELS = ["healthy", "leaf_blight", "powdery_mildew", "bacterial_spot"]


@dataclass
class DiagnosisResult:
    label: str
    confidence: float
    method: str  # "onnx_npu" or "heuristic_fallback"


def _load_onnx_session():
    if not os.path.exists(MODEL_PATH):
        return None
    import onnxruntime as ort

    # On a Snapdragon-powered HP PC with the QNN execution provider installed,
    # this preferentially uses the NPU; it falls back to CPU automatically if
    # QNN isn't available on the current machine (e.g. this dev sandbox).
    providers = ["QNNExecutionProvider", "CPUExecutionProvider"]
    available = ort.get_available_providers()
    providers = [p for p in providers if p in available] or ["CPUExecutionProvider"]
    return ort.InferenceSession(MODEL_PATH, providers=providers)


def _heuristic_classify(image: Image.Image) -> DiagnosisResult:
    """
    Fallback classifier used only when no trained ONNX model is present.

    This is a real (if simple) image-analysis routine, not a random stub: it
    measures the proportion of the leaf area showing brown/necrotic pixels,
    white/powdery pixels, and dark small-spot pixels versus healthy green, and
    maps the dominant signal to a disease label. It exists so the full
    pipeline can be demonstrated and tested without bundling large model
    weights in the repo.
    """
    img = image.convert("RGB").resize((256, 256))
    arr = np.asarray(img).astype(np.float32) / 255.0
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    green_mask = (g > r) & (g > b) & (g > 0.25)
    brown_mask = (r > g) & (r > 0.25) & (b < 0.35) & (~green_mask)
    white_mask = (r > 0.75) & (g > 0.75) & (b > 0.75)
    dark_spot_mask = (r < 0.3) & (g < 0.3) & (b < 0.3) & (~white_mask)

    # Normalize against leaf area (not the whole frame, which includes
    # background) -- what matters is what fraction of the *leaf* looks
    # diseased, not what fraction of the photo is leaf at all.
    leaf_area = int(green_mask.sum() + brown_mask.sum() + white_mask.sum() + dark_spot_mask.sum())
    leaf_area = max(leaf_area, 1)

    frac_brown = brown_mask.sum() / leaf_area
    frac_white = white_mask.sum() / leaf_area
    frac_dark = dark_spot_mask.sum() / leaf_area

    disease_scores = {
        "leaf_blight": frac_brown,
        "powdery_mildew": frac_white,
        "bacterial_spot": frac_dark,
    }
    top_label = max(disease_scores, key=disease_scores.get)
    top_score = disease_scores[top_label]

    HEALTHY_THRESHOLD = 0.04  # <4% of leaf area showing symptoms -> call it healthy
    if top_score < HEALTHY_THRESHOLD:
        label = "healthy"
        confidence = round(min(0.95, 0.6 + (HEALTHY_THRESHOLD - top_score) * 5), 3)
    else:
        label = top_label
        confidence = round(min(0.95, 0.5 + top_score), 3)

    return DiagnosisResult(label=label, confidence=round(float(confidence), 3), method="heuristic_fallback")


def _onnx_classify(session, image: Image.Image) -> DiagnosisResult:
    img = image.convert("RGB").resize((224, 224))
    arr = np.asarray(img).astype(np.float32) / 255.0
    arr = np.transpose(arr, (2, 0, 1))[np.newaxis, ...]  # NCHW

    input_name = session.get_inputs()[0].name
    logits = session.run(None, {input_name: arr})[0][0]
    exp = np.exp(logits - np.max(logits))
    probs = exp / exp.sum()
    idx = int(np.argmax(probs))
    return DiagnosisResult(label=LABELS[idx], confidence=round(float(probs[idx]), 3), method="onnx_npu")


def diagnose(image_path: str) -> DiagnosisResult:
    image = Image.open(image_path)
    session = _load_onnx_session()
    if session is not None:
        return _onnx_classify(session, image)
    return _heuristic_classify(image)
