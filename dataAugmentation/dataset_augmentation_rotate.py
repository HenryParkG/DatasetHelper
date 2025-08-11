import os
import cv2
from tkinter import Tk, filedialog

def rotate_images_180_in_place(input_dir):
    image_files = [f for f in os.listdir(input_dir)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

    for img_name in image_files:
        img_path = os.path.join(input_dir, img_name)
        img = cv2.imread(img_path)

        if img is None:
            print(f"이미지 로드 실패: {img_name}")
            continue

        rotated = cv2.rotate(img, cv2.ROTATE_180)

        base, ext = os.path.splitext(img_name)
        save_name = f"Rotate_{base}{ext}"
        save_path = os.path.join(input_dir, save_name)

        cv2.imwrite(save_path, rotated)

    print(f"{len(image_files)}장의 이미지가 180도 회전되어 저장되었습니다.")

# Tkinter 초기화 (창 숨김)
root = Tk()
root.withdraw()

print("이미지가 있는 폴더를 선택하세요.")
input_folder = filedialog.askdirectory(title="이미지 폴더 선택")

if input_folder:
    rotate_images_180_in_place(input_folder)
else:
    print("폴더가 선택되지 않았습니다.")
