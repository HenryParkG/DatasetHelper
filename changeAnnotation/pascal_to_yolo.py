import os
import xml.etree.ElementTree as ET

# 클래스 목록 정의 (VOC에 나오는 클래스 순서 중요)
classes = ['Defect']  # 여기에 실제 클래스명 추가

# 경로 설정
xml_folder = r"D:\1_Yagai\3_Yagai_sausage_dataset\image\YOLO-OD\0730\labels"  # Pascal VOC XML 라벨 폴더
output_folder = r"D:\1_Yagai\3_Yagai_sausage_dataset\image\YOLO-OD\0730\images\labels_d"  # YOLO txt 저장할 폴더
os.makedirs(output_folder, exist_ok=True)

def convert_bbox(size, box):
    # size: (width, height)
    # box: (xmin, xmax, ymin, ymax)
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
