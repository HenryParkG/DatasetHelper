# -*- coding: utf-8 -*-
# YOLO 형식의 라벨을 COCO 형식으로 변환하는 스크립트
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict



yolo_dir = filedialog.askdirectory(title="YOLO 라벨 폴더 선택")
if not yolo_dir:
    messagebox.showerror("오류", "YOLO 라벨 폴더를 선택하지 않았습니다.")
    exit()

img_dir = filedialog.askdirectory(title="이미지 폴더 선택")
if not img_dir:
    messagebox.showerror("오류", "이미지 폴더를 선택하지 않았습니다.")
    exit()

coco_save_path = filedialog.asksaveasfilename(
    title="저장할 COCO JSON 파일 선택",
    defaultextension=".json",
    filetypes=[("JSON files", "*.json")]
)
if not coco_save_path:
    messagebox.showerror("오류", "저장할 COCO JSON 파일을 선택하지 않았습니다.")
    exit()

# YOLO 클래스 이름 예시
class_names = ["class0", "class1", "class2"]  # 필요시 수정
categories = [{"id": i, "name": name} for i, name in enumerate(class_names)]

images = []
annotations = []
ann_id = 1
for idx, img_file in enumerate(os.listdir(img_dir)):
    if not img_file.lower().endswith((".jpg", ".png", ".jpeg")):
        continue
    img_path = os.path.join(img_dir, img_file)
    width, height = 640, 480  # 실제 이미지 크기 필요시 PIL.Image로 불러오기 가능
    images.append({"id": idx+1, "file_name": img_file, "width": width, "height": height})

    txt_file = os.path.splitext(img_file)[0] + ".txt"
    yolo_path = os.path.join(yolo_dir, txt_file)
    if os.path.exists(yolo_path):
        with open(yolo_path) as f:
            for line in f:
                class_id, x_c, y_c, w, h = map(float, line.strip().split())
                x = (x_c - w/2) * width
                y = (y_c - h/2) * height
                w_pix = w * width
                h_pix = h * height
                annotations.append({
                    "id": ann_id,
                    "image_id": idx+1,
                    "category_id": int(class_id),
                    "bbox": [x, y, w_pix, h_pix],
                    "area": w_pix * h_pix,
                    "iscrowd": 0
                })
                ann_id += 1

coco_data = {"images": images, "annotations": annotations, "categories": categories}
with open(coco_save_path, "w") as f:
    json.dump(coco_data, f, indent=4)

messagebox.showinfo("완료", "YOLO → COCO 변환 완료!")

