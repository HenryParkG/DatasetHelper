# -*- coding: utf-8 -*-
# 이미지 밝기 및 대비 조정 스크립트
import cv2
import os
from glob import glob
from tkinter import Tk, filedialog

def adjust_brightness_contrast(image, alpha=1.0, beta=0):
    """
    alpha: 대비 (contrast), 1.0 유지
    beta: 밝기 (brightness), -100~100 권장
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def process_images_in_folder(folder_path, prefix='bright_', alpha=1.0, beta=30):
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    image_paths = []

    for ext in image_extensions:
        image_paths.extend(glob(os.path.join(folder_path, ext)))

    for image_path in image_paths:
        filename = os.path.basename(image_path)
        new_filename = prefix + filename
        new_path = os.path.join(folder_path, new_filename)

        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load: {image_path}")
            continue

        adjusted = adjust_brightness_contrast(image, alpha, beta)
        cv2.imwrite(new_path, adjusted)
        print(f"Saved: {new_path}")

# Tkinter 초기화 (창 숨김)
root = Tk()
root.withdraw()

print("이미지 폴더를 선택하세요.")
folder = filedialog.askdirectory(title="이미지 폴더 선택")

if folder:
    # 필요에 따라 alpha, beta 값 변경
    process_images_in_folder(folder, prefix='bright_', alpha=1.0, beta=50)
else:
    print("폴더가 선택되지 않았습니다.")
