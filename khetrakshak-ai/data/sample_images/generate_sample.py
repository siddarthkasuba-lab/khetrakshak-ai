"""
Generates simple synthetic leaf-shaped test images (not real photos -- avoids
any copyright concern) so the pipeline has something to run against out of
the box. Swap in real (your own) crop photos for actual testing.
"""
import os
from PIL import Image, ImageDraw

OUT_DIR = os.path.dirname(__file__)


def leaf_base(w=256, h=256, green=(60, 140, 60)):
    # Background must not read as near-white/near-green/near-dark under the
    # classifier's simple color heuristic, or it skews the disease signal.
    img = Image.new("RGB", (w, h), (150, 150, 140))
    draw = ImageDraw.Draw(img)
    draw.ellipse([40, 20, 216, 236], fill=green)
    draw.line([128, 20, 128, 236], fill=(40, 100, 40), width=3)
    return img, draw


def make_healthy():
    img, _ = leaf_base()
    img.save(os.path.join(OUT_DIR, "sample_leaf_healthy.png"))


def make_blight():
    img, draw = leaf_base()
    import random
    random.seed(1)
    for _ in range(40):
        x, y = random.randint(50, 210), random.randint(30, 230)
        r = random.randint(4, 10)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(120, 70, 30))
    img.save(os.path.join(OUT_DIR, "sample_leaf.png"))


def make_mildew():
    img, draw = leaf_base()
    import random
    random.seed(2)
    for _ in range(60):
        x, y = random.randint(50, 210), random.randint(30, 230)
        r = random.randint(3, 7)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(235, 235, 235))
    img.save(os.path.join(OUT_DIR, "sample_leaf_mildew.png"))


if __name__ == "__main__":
    make_healthy()
    make_blight()
    make_mildew()
    print("Generated sample images in", OUT_DIR)
