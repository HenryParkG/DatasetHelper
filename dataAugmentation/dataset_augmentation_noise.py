import os
import cv2
import numpy as np
from tkinter import Tk, filedialog

def add_gaussian_noise(img, mean=0, sigma=10):
    gauss = np.random.normal(mean, sigma, img.shape).astype('uint8')
    noisy = cv2.add(img, gauss)
    return noisy

def noise_images(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg','.jpeg','.png'))]

    for fname in files:
        img_path = os.path.join(input_dir, fname)
        img = cv2.imread(img_path)
        if img is None:
            print(f"이미지 로드 실패: {fname}")
            continue

        noisy_img = add_gaussian_noise(img)

        save_path = os.path.join(output_dir, f"noise_{fname}")
        cv2.imwrite(save_path, noisy_img)
        print(f"저장: {save_path}")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    input_dir = filedialog.askdirectory(title="원본 이미지 폴더 선택")
    output_dir = filedialog.askdirectory(title="결과 저장 폴더 선택")

    noise_images(input_dir, output_dir)
