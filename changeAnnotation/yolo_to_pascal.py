import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tkinter import Tk, filedialog
import cv2

# Tkinter 초기화 (창 숨김)
root = Tk()
root.withdraw()

# 경로 선택
print("YOLO 라벨(.txt) 폴더를 선택하세요.")
yolo_folder = filedialog.askdirectory(title="YOLO 라벨 폴더 선택")
if not yolo_folder:
    print("라벨 폴더를 선택하지 않았습니다. 종료합니다.")
    exit()

print("이미지 폴더를 선택하세요.")
image_folder = filedialog.askdirectory(title="이미지 폴더 선택")
if not image_folder:
    print("이미지 폴더를 선택하지 않았습니다. 종료합니다.")
    exit()

print("Pascal VOC XML 저장 폴더를 선택하세요.")
output_folder = filedialog.askdirectory(title="XML 저장 폴더 선택")
if not output_folder:
    print("저장 폴더를 선택하지 않았습니다. 종료합니다.")
    exit()

# 클래스 목록 (YOLO 라벨 순서와 동일해야 함)
classes = ['A']  

def convert_bbox(size, box):
    """YOLO bbox → Pascal VOC bbox 좌표 변환"""
    w_img, h_img = size
    x_center, y_center, w, h = box
    xmin = int((x_center - w / 2) * w_img)
    xmax = int((x_center + w / 2) * w_img)
    ymin = int((y_center - h / 2) * h_img)
    ymax = int((y_center + h / 2) * h_img)
    return xmin, ymin, xmax, ymax

def prettify(elem):
    """XML 예쁘게 출력"""
    rough = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ")

# 변환 실행
for filename in os.listdir(yolo_folder):
    if not filename.endswith(".txt"):
        continue

    txt_path = os.path.join(yolo_folder, filename)
    image_name = os.path.splitext(filename)[0] + ".jpg"  # 확장자 필요 시 수정
    image_path = os.path.join(image_folder, image_name)

    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ 이미지 없음: {image_path}")
        continue

    height, width, _ = img.shape

    # XML 구조 생성
    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = os.path.basename(image_folder)
    ET.SubElement(annotation, 'filename').text = image_name

    size_elem = ET.SubElement(annotation, 'size')
    ET.SubElement(size_elem, 'width').text = str(width)
    ET.SubElement(size_elem, 'height').text = str(height)
    ET.SubElement(size_elem, 'depth').text = "3"

    ET.SubElement(annotation, 'segmented').text = "0"

    with open(txt_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue

            class_id = int(parts[0])
            x, y, w, h = map(float, parts[1:])
            xmin, ymin, xmax, ymax = convert_bbox((width, height), (x, y, w, h))

            obj = ET.SubElement(annotation, 'object')
            ET.SubElement(obj, 'name').text = classes[class_id]
            ET.SubElement(obj, 'pose').text = "Unspecified"
            ET.SubElement(obj, 'truncated').text = "0"
            ET.SubElement(obj, 'difficult').text = "0"

            bbox = ET.SubElement(obj, 'bndbox')
            ET.SubElement(bbox, 'xmin').text = str(xmin)
            ET.SubElement(bbox, 'ymin').text = str(ymin)
            ET.SubElement(bbox, 'xmax').text = str(xmax)
            ET.SubElement(bbox, 'ymax').text = str(ymax)

    output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".xml")
    with open(output_path, "w") as xml_file:
        xml_file.write(prettify(annotation))

print("✅ 변환 완료: YOLO → Pascal VOC")
