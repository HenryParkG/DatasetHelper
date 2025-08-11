# YOLO 형식의 라벨을 Pascal VOC XML 형식으로 변환하는 스크립트
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

# 클래스 목록
classes = ['A']  # YOLO 라벨에 사용된 클래스 순서와 동일하게

# 경로 설정
yolo_folder = r"D:\new\labels"      # YOLO txt가 있는 폴더
image_folder = r"D:\images"         # 이미지가 있는 폴더 (size 정보 필요)
output_folder = r"D:\new\xmls"      # Pascal VOC XML 저장 폴더
os.makedirs(output_folder, exist_ok=True)

def convert_bbox(size, box):
    # size: (width, height)
    # box: (x_center, y_center, width, height)
    w_img, h_img = size
    x_center, y_center, w, h = box
    xmin = int((x_center - w / 2) * w_img)
    xmax = int((x_center + w / 2) * w_img)
    ymin = int((y_center - h / 2) * h_img)
    ymax = int((y_center + h / 2) * h_img)
    return xmin, ymin, xmax, ymax

def prettify(elem):
    rough = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ")

# YOLO txt 파일 하나씩 처리
for filename in os.listdir(yolo_folder):
    if not filename.endswith(".txt"):
        continue

    txt_path = os.path.join(yolo_folder, filename)
    image_name = os.path.splitext(filename)[0] + ".jpg"  # 이미지 확장자 맞게 수정
    image_path = os.path.join(image_folder, image_name)

    # 이미지 크기 구하기
    import cv2
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

    # txt 파일 읽기
    with open(txt_path, "r") as f:
        for line in f.readlines():
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

    # 저장
    output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".xml")
    with open(output_path, "w") as xml_file:
        xml_file.write(prettify(annotation))

print("✅ 변환 완료: YOLO → Pascal VOC")
