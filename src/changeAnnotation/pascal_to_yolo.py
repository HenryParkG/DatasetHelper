# -*- coding: utf-8 -*-
# Pascal VOC 형식의 XML 라벨을 YOLO 형식의 텍스트 파일로 변환하는 스크립트
import os
import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog, messagebox

# Tkinter 초기화 (창 숨김)
root = Tk()
root.withdraw()

# 폴더 선택
print("VOC XML 라벨 폴더를 선택하세요.")
xml_folder = filedialog.askdirectory(title="VOC XML 라벨 폴더 선택")
if not xml_folder:
    messagebox.showerror("오류", "라벨 폴더를 선택하지 않았습니다.")
    exit()

print("YOLO 라벨(.txt) 저장 폴더를 선택하세요.")
output_folder = filedialog.askdirectory(title="YOLO 라벨 저장 폴더 선택")
if not output_folder:
    messagebox.showerror("오류", "저장 폴더를 선택하지 않았습니다.")
    exit()

# 클래스 목록 정의 (VOC에 나오는 클래스 순서 중요)
classes = ['A']  # 필요 시 여러 클래스 추가

def convert_bbox(size, box):
    """Pascal VOC bbox → YOLO bbox 변환"""
    dw = 1. / size[0]
    dh = 1. / size[1]
    x_center = (box[0] + box[1]) / 2.0 * dw
    y_center = (box[2] + box[3]) / 2.0 * dh
    w = (box[1] - box[0]) * dw
    h = (box[3] - box[2]) * dh
    return x_center, y_center, w, h

# 모든 XML 파일 변환
for filename in os.listdir(xml_folder):
    if not filename.endswith(".xml"):
        continue

    tree = ET.parse(os.path.join(xml_folder, filename))
    root = tree.getroot()

    size = root.find('size')
    img_w = int(size.find('width').text)
    img_h = int(size.find('height').text)

    yolo_lines = []
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue  # 정의되지 않은 클래스는 스킵

        cls_id = classes.index(cls)

        xml_box = obj.find('bndbox')
        xmin = float(xml_box.find('xmin').text)
        xmax = float(xml_box.find('xmax').text)
        ymin = float(xml_box.find('ymin').text)
        ymax = float(xml_box.find('ymax').text)

        x, y, w, h = convert_bbox((img_w, img_h), (xmin, xmax, ymin, ymax))
        yolo_lines.append(f"{cls_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")

    # YOLO txt 저장
    output_name = os.path.splitext(filename)[0] + ".txt"
    with open(os.path.join(output_folder, output_name), "w") as out_file:
        out_file.write("\n".join(yolo_lines))

print("✅ 변환 완료: Pascal VOC → YOLO")
