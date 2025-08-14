# -*- coding: utf-8 -*-
# 이미지에 블러(흐림) 효과를 추가하는 스크립트
import os
import cv2
from tkinter import Tk, filedialog, messagebox

def blur_images(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg','.jpeg','.png'))]

    for fname in files:
        img_path = os.path.join(input_dir, fname)
        img = cv2.imread(img_path)
        if img is None:
            print(f"이미지 로드 실패: {fname}")
            continue

        blurred = cv2.GaussianBlur(img, (5,5), 0)

        save_path = os.path.join(output_dir, f"blur_{fname}")
        cv2.imwrite(save_path, blurred)
        print(f"저장: {save_path}")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    input_dir = filedialog.askdirectory(title="원본 이미지 폴더 선택")
    if not input_dir:
        messagebox.showerror("오류", "입력 이미지 폴더를 선택하지 않았습니다.")
        exit()
        
    output_dir = filedialog.askdirectory(title="결과 저장 폴더 선택")
    if not output_dir:
        messagebox.showerror("오류", "저장 이미지 폴더를 선택하지 않았습니다.")
        exit()
        
    blur_images(input_dir, output_dir)
