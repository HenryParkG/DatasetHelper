# 이미 존재하는 모델 파일을 사용하여 이미지에 대한 라벨을 생성하는 스크립트입니다.
import os
import cv2
from pathlib import Path
from ultralytics import YOLO

# 설정
image_dir = r'D:\test\images' # 대상 이미지 경로
output_dir = r'D:\test\labels' # 라벨 저장 경로
model_path = r'D:\runs\detect\train\weights\best.pt' # 이미 존재하는 모델 파일 경로
img_size = 640
conf_thres = 0.68

# 라벨 저장 폴더 생성
os.makedirs(output_dir, exist_ok=True)

# YOLOv11 모델 로드
model = YOLO(model_path)

# 이미지 추론 및 라벨 생성
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))] # 이미지 파일 필터링

for img_name in image_files:
    img_path = os.path.join(image_dir, img_name)
    img = cv2.imread(img_path)
    h, w = img.shape[:2]

    # 추론
    results = model(img, imgsz=img_size, conf=conf_thres)
    boxes = results[0].boxes

    # 라벨 저장
    label_path = os.path.join(output_dir, Path(img_name).stem + '.txt')
    with open(label_path, 'w') as f:
        for box in boxes:
            cls_id = int(box.cls.cpu().item())
            x_center, y_center, box_w, box_h = box.xywh[0].cpu().numpy()

            # 정규화
            x_center /= w
            y_center /= h
            box_w /= w
            box_h /= h

            f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {box_w:.6f} {box_h:.6f}\n")

print("YOLO 라벨 생성 완료.")

