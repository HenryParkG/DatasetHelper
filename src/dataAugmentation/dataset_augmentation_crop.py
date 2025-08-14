# -*- coding: utf-8 -*-
# 이미지 크롭 및 저장 스크립트
import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def crop_image(image_path, output_dir, crop_size=(256, 256), overlap=0):
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(image_path)
    img_width, img_height = img.size
    crop_w, crop_h = crop_size

    count = 0
    step_x = crop_w - overlap
    step_y = crop_h - overlap

    for top in range(0, img_height - crop_h + 1, step_y):
        for left in range(0, img_width - crop_w + 1, step_x):
            box = (left, top, left + crop_w, top + crop_h)
            cropped_img = img.crop(box)
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            cropped_img.save(os.path.join(output_dir, f"{base_name}_crop_{count:03d}.png"))
            count += 1

    print(f"{image_path} → {count}개의 크롭 이미지 저장 완료")

def process_folder(input_folder, output_folder, crop_size=(256,256), overlap=0):
    image_exts = (".jpg", ".jpeg", ".png", ".bmp")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(image_exts):
            img_path = os.path.join(input_folder, filename)
            crop_image(img_path, output_folder, crop_size, overlap)

def main():
    root = tk.Tk()
    root.withdraw()

    input_dir = filedialog.askdirectory(title="크롭할 이미지 폴더 선택")
    if not input_dir:
        messagebox.showerror("오류", "입력 폴더가 선택되지 않았습니다.")
        exit()

    output_dir = filedialog.askdirectory(title="크롭 결과 저장 폴더 선택")
    if not output_dir:
        messagebox.showerror("오류", "출력 폴더가 선택되지 않았습니다.")
        exit()

    crop_w = simpledialog.askinteger("크롭 너비", "크롭 너비 입력 (예: 256):", minvalue=1)
    if crop_w is None:
        messagebox.showerror("오류", "크롭 너비를 입력해야 합니다.")
        exit()

    crop_h = simpledialog.askinteger("크롭 높이", "크롭 높이 입력 (예: 256):", minvalue=1)
    if crop_h is None:
        messagebox.showerror("오류", "크롭 높이를 입력해야 합니다.")
        exit()

    overlap_px = simpledialog.askinteger("겹침 영역", "겹치는 영역 픽셀 수 입력 (기본 0):", minvalue=0)
    if overlap_px is None:
        overlap_px = 0

    process_folder(input_dir, output_dir, crop_size=(crop_w, crop_h), overlap=overlap_px)

    messagebox.showinfo("완료", "✅ 크롭 작업 완료")

if __name__ == "__main__":
    main()
