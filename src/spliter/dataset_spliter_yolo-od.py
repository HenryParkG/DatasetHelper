# -*- coding: utf-8 -*-
# YOLO 형식의 데이터셋을 train/test로 분할하는 스크립트
import os
import shutil
import random
from tkinter import Tk, filedialog

def select_folder(title):
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title=title)
    if not folder:
        print(f"❌ {title} 폴더를 선택하지 않았습니다. 종료합니다.")
        exit()
    return folder

def main():
    src_image_dir = select_folder("원본 이미지 폴더 선택")
    src_label_dir = select_folder("원본 라벨 폴더 선택")
    dst_base = select_folder("출력 데이터셋 저장 폴더 선택")

    train_ratio = 0.8

    for split in ['train', 'test']:
        os.makedirs(os.path.join(dst_base, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(dst_base, split, 'labels'), exist_ok=True)

    image_files = [f for f in os.listdir(src_image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    image_files.sort()
    random.shuffle(image_files)

    split_idx = int(len(image_files) * train_ratio)
    train_files = image_files[:split_idx]
    test_files = image_files[split_idx:]

    def copy_files(file_list, split):
        for img_name in file_list:
            label_name = os.path.splitext(img_name)[0] + ".txt"

            src_img = os.path.join(src_image_dir, img_name)
            src_lbl = os.path.join(src_label_dir, label_name)

            dst_img = os.path.join(dst_base, split, "images", img_name)
            dst_lbl = os.path.join(dst_base, split, "labels", label_name)

            if os.path.exists(src_img) and os.path.exists(src_lbl):
                shutil.copy2(src_img, dst_img)
                shutil.copy2(src_lbl, dst_lbl)
            else:
                print(f"[경고] 파일 없음: {img_name} / {label_name}")

    copy_files(train_files, "train")
    copy_files(test_files, "test")

    print(f"완료: {len(train_files)} train / {len(test_files)} test 파일 분할됨.")

if __name__ == "__main__":
    main()
