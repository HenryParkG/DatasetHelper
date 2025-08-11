import os
import cv2
import numpy as np
from tkinter import Tk, filedialog

def translate_images(input_dir, output_dir, x_shift=50, y_shift=50):
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg','.jpeg','.png'))]

    for fname in files:
        img_path = os.path.join(input_dir, fname)
        img = cv2.imread(img_path)
        if img is None:
            print(f"이미지 로드 실패: {fname}")
            continue

        rows, cols = img.shape[:2]
        M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
        shifted = cv2.warpAffine(img, M, (cols, rows))

        save_path = os.path.join(output_dir, f"translate_{fname}")
        cv2.imwrite(save_path, shifted)
        print(f"저장: {save_path}")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    input_dir = filedialog.askdirectory(title="원본 이미지 폴더 선택")
    output_dir = filedialog.askdirectory(title="결과 저장 폴더 선택")

    translate_images(input_dir, output_dir)
