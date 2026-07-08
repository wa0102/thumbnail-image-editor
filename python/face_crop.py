# face_crop.py
import sys
import os
import numpy as np
from PIL import Image
import mediapipe as mp


def main():
    # -----------------------
    # 1. 引数
    # -----------------------
    if len(sys.argv) < 3:
        print("usage: python face_crop.py input_image output_image")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print("input image not found")
        sys.exit(1)

    # -----------------------
    # 2. 画像読み込み
    # -----------------------
    image = Image.open(input_path).convert("RGB")
    img_w, img_h = image.size

    # -----------------------
    # 3. 顔検出
    # -----------------------
    mp_face = mp.solutions.face_detection
    face_detection = mp_face.FaceDetection(
        model_selection=0,          # 近距離向け（小さい顔に強い）
        min_detection_confidence=0.3
    )

    image_np = np.array(image)
    results = face_detection.process(image_np)

    # -----------------------
    # 4. クロップ領域決定
    # -----------------------
    if results.detections:
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box

        x = int(bbox.xmin * img_w)
        y = int(bbox.ymin * img_h)
        w = int(bbox.width * img_w)
        h = int(bbox.height * img_h)

        cx = x + w // 2
        cy = y + h // 2

        crop_w = int(w * 1.8)
        crop_h = int(h * 2.5)

        left = max(cx - crop_w // 2, 0)
        top = max(cy - int(crop_h * 0.4), 0)
    else:
        print("face not detected -> center crop")

        crop_w = int(img_w * 0.6)
        crop_h = int(img_h * 0.8)

        left = img_w // 2 - crop_w // 2
        top = img_h // 2 - crop_h // 2

    right = min(left + crop_w, img_w)
    bottom = min(top + crop_h, img_h)

    cropped = image.crop((left, top, right, bottom))

    # -----------------------
    # 5. 保存
    # -----------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cropped.save(output_path)

    print(f"saved: {output_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
