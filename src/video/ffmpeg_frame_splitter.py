# -*- coding: utf-8 -*-
# 비디오 파일에서 프레임을 추출하여 저장하는 스크립트
import os
import cv2
import tkinter as tk
from tkinter import filedialog

# Tkinter 기본창 숨김
root = tk.Tk()
root.withdraw()

# 1. 원본 비디오 폴더 선택
print("원본 영상이 있는 폴더를 선택하세요.")
input_dir = filedialog.askdirectory(title="원본 영상 폴더 선택")
if not input_dir:
    print("원본 영상 폴더를 선택하지 않았습니다. 종료합니다.")
    exit()

# 2. 저장 경로 선택
print("프레임을 저장할 폴더를 선택하세요.")
save_dir = filedialog.askdirectory(title="프레임 저장할 폴더 선택")
if not save_dir:
    print("저장 경로를 선택하지 않았습니다. 종료합니다.")
    exit()

# 3. FPS 설정
target_fps = 10

# 4. .webm 파일 순회
for file_name in os.listdir(input_dir):
    if file_name.lower().endswith(".webm"):
        video_path = os.path.join(input_dir, file_name)
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"비디오 열기 실패: {video_path}")
            continue

        # 원본 영상 FPS
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(round(original_fps / target_fps))

        frame_count = 0
        saved_count = 0
        base_name = os.path.splitext(file_name)[0]

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                output_filename = f"{base_name}_frame_{saved_count:04d}.png"
                output_path = os.path.join(save_dir, output_filename)
                cv2.imwrite(output_path, frame)
                saved_count += 1

            frame_count += 1

        cap.release()
        print(f"{file_name} → {saved_count} 프레임 저장 완료")

print("모든 영상 처리 완료!")
