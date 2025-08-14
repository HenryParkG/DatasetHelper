# -*- coding: utf-8 -*-
# coco 어노테이션을 YOLO 형식으로 변환하는 스크립트
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict

# ----------------------------
# COCO → YOLO
# ----------------------------

coco_json_path = filedialog.askopenfilename(
    title="COCO JSON 파일 선택",
    filetypes=[("JSON files", "*.json")]
)
if not coco_json_path:
    messagebox.showerror("오류", "COCO JSON 파일을 선택하지 않았습니다.")
    exit()

img_dir = filedialog.askdirectory(title="이미지 폴더 선택")
if not img_dir:
    messagebox.showerror("오류", "이미지 폴더를 선택하지 않았습니다.")
    exit()

yolo_dir = filedialog.askdirectory(title="YOLO 저장 폴더 선택")
if not yolo_dir:
    messagebox.showerror("오류", "YOLO 저장 폴더를 선택하지 않았습니다.")
    exit()

with open(coco_json_path) as f:
    coco_data = json.load(f)

cat_id_to_class_id = {cat["id"]: idx for idx, cat in enumerate(coco_data["categories"])}
img_id_map = {img["id"]: (img["file_name"], img["width"], img["height"]) for img in coco_data["images"]}
ann_map = defaultdict(list)
for ann in coco_data["annotations"]:
    ann_map[ann["image_id"]].append(ann)

os.makedirs(yolo_dir, exist_ok=True)
for img_id, anns in ann_map.items():
    img_name, width, height = img_id_map[img_id]
    txt_path = os.path.join(yolo_dir, os.path.splitext(img_name)[0] + ".txt")
    with open(txt_path, "w") as f:
        for ann in anns:
            class_id = cat_id_to_class_id[ann["category_id"]]
            x, y, w, h = ann["bbox"]
            x_c = (x + w/2) / width
            y_c = (y + h/2) / height
            w_norm = w / width
            h_norm = h / height
            f.write(f"{class_id} {x_c:.6f} {y_c:.6f} {w_norm:.6f} {h_norm:.6f}\n")

messagebox.showinfo("완료", "COCO → YOLO 변환 완료!")