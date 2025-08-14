# -*- coding: utf-8 -*-
# 이미지 수평 뒤집기 스크립트
import os
import cv2
from tkinter import Tk, filedialog, messagebox

def flip_images(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg','.jpeg','.png'))]

    for img_name in image_files:
        img_path = os.path.join(input_dir, img_name)
        img = cv2.imread(img_path)

        if img is None:
            print(f"이미지 로드 실패: {img_name}")
            continue

        # 수평 뒤집기
        flipped = cv2.flip(img, 1)

        save_path = os.path.join(output_dir, f"flip_{img_name}")
        cv2.imwrite(save_path, flipped)
        print(f"저장: {save_path}")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    input_folder = filedialog.askdirectory(title="원본 이미지 폴더 선택")
    if input_folder is None:
        messagebox.showerror("오류", "입력 이미지 폴더를 선택하지 않았습니다.")
        exit()
    output_folder = filedialog.askdirectory(title="결과 저장 폴더 선택")
    if output_folder is None:
        messagebox.showerror("오류", "저장 이미지 폴더를 선택하지 않았습니다.")
        exit()
    flip_images(input_folder, output_folder)
