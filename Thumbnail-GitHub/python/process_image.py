import sys
import os
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import mediapipe as mp

def main():
    if len(sys.argv) < 2:
        print("画像パスが渡されていません")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print("画像ファイルが存在しません")
        sys.exit(1)

    # -----------------------
    # 1. 画像読み込み
    # -----------------------
    image = Image.open(input_path).convert("RGB")
    img_w, img_h = image.size

    # -----------------------
    # 2. 顔検出
    # -----------------------
    mp_face = mp.solutions.face_detection
    face_detection = mp_face.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.3
    )

    image_np = np.array(image)
    results = face_detection.process(image_np)

    if not results.detections:
        print("顔未検出 → そのまま保存")
        image.save(input_path.replace(".", "_thumb."))
        return

    detection = results.detections[0]
    bbox = detection.location_data.relative_bounding_box

    x = int(bbox.xmin * img_w)
    y = int(bbox.ymin * img_h)
    w = int(bbox.width * img_w)
    h = int(bbox.height * img_h)

    cx = x + w // 2
    cy = y + h // 2

    # -----------------------
    # 3. 人物エリア拡張
    # -----------------------
    crop_w = int(w * 1.8)
    crop_h = int(h * 2.8)

    left = max(cx - crop_w // 2, 0)
    top = max(cy - int(crop_h * 0.4), 0)
    right = min(left + crop_w, img_w)
    bottom = min(top + crop_h, img_h)

    person = image.crop((left, top, right, bottom))

    # -----------------------
    # 4. 背景ぼかし
    # -----------------------
    background = image.filter(ImageFilter.GaussianBlur(radius=25))

    # -----------------------
    # 5. 人物の色調補正（A-8）
    # -----------------------
    enhancer = ImageEnhance.Brightness(person)
    person = enhancer.enhance(1.15)

    enhancer = ImageEnhance.Contrast(person)
    person = enhancer.enhance(1.1)

    enhancer = ImageEnhance.Color(person)
    person = enhancer.enhance(1.0)

    person = person.filter(ImageFilter.SHARPEN)

    # -----------------------
    # 6. 縁・光（A-9 核心）
    # -----------------------

    # 人物をコピーして「縁用」にする
    glow = person.copy()

    # 少し大きくする（縁の太さ）
    glow = glow.resize(
        (int(glow.width * 1.05), int(glow.height * 1.05)),
        Image.LANCZOS
    )

    # 強めにぼかす
    glow = glow.filter(ImageFilter.GaussianBlur(radius=20))

    # 貼り付け位置を中央に合わせる
    glow_x = left - (glow.width - person.width) // 2
    glow_y = top - (glow.height - person.height) // 2

    # 先に光を貼る
    background.paste(glow, (glow_x, glow_y))

    # 上に人物を貼る
    background.paste(person, (left, top))

    # -----------------------
    # 7. 保存
    # -----------------------
    base, ext = os.path.splitext(input_path)
    output_path = base + "_thumb" + ext
    background.save(output_path)

    print(f"saved: {output_path}")

if __name__ == "__main__":
    main()
