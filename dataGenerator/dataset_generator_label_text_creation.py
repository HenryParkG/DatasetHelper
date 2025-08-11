import os
import cv2
from pathlib import Path
from ultralytics import YOLO
from tkinter import Tk, filedialog

# Tkinter 초기화 (창 숨김)
root = Tk()
root.withdraw()

# 폴더 / 파일 선택
print("이미지 폴더를 선택하세요.")
image_dir = filedialog.askdirectory(title="이미지 폴더 선택")

print("라벨 저장 폴더를 선택하세요.")
output_dir = filedialog.askdirectory(title="라벨 저장 폴더 선택")

print("YOLO 모델 파일(.pt)을 선택하세요.")
model_path = filedialog.askopenfilename(title="YOLO 모델 파일 선택", filetypes=[("PyTorch Model", "*.pt")])

# 파라미터 설정
img_size = 640
conf_thres = 0.68

# 라벨 저장 폴더 생성
os.makedirs(output_dir, exist_ok=True)

# YOLO 모델 로드
model = YOLO(model_path)

# 이미지 파일 목록 불러오기
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

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
