# -*- coding: utf-8 -*-
# 이미지 폴더를 선택하여 동영상으로 만드는 스크립트
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def create_ffmpeg_input_file(image_files, txt_path, duration=0.5):
    """
    FFmpeg concat용 입력 파일 생성
    """
    with open(txt_path, 'w', encoding='utf-8') as f:
        for img in image_files:
            f.write(f"file '{img}'\n")
            f.write(f"duration {duration}\n")
        f.write(f"file '{image_files[-1]}'\n")  # 마지막 이미지 반복

def run_ffmpeg_create_video(concat_txt_path, output_video_path):
    """
    FFmpeg 실행
    """
    command = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_txt_path,
               '-vsync', 'vfr', '-pix_fmt', 'yuv420p', output_video_path]
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        messagebox.showinfo("완료", f"동영상 생성 완료!\n출력파일: {output_video_path}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"FFmpeg 실행 실패:\n{e.stderr}")

def main():
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우 숨기기

    # 1. 이미지 폴더 선택
    folder_path = filedialog.askdirectory(title="이미지 폴더 선택")
    if not folder_path:
        messagebox.showwarning("경고", "폴더를 선택하지 않았습니다.")
        return

    # 이미지 파일 목록
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        messagebox.showerror("오류", "폴더 내에 이미지 파일이 없습니다.")
        return
    image_files.sort()

    # 2. concat 텍스트 파일 저장 위치 선택
    concat_txt_path = filedialog.asksaveasfilename(
        title="concat 텍스트 파일 저장",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if not concat_txt_path:
        messagebox.showwarning("경고", "concat 텍스트 파일 저장 위치를 선택하지 않았습니다.")
        return

    # 3. 출력 동영상 파일명 선택
    output_video_path = filedialog.asksaveasfilename(
        title="출력 동영상 파일 저장",
        defaultextension=".mp4",
        filetypes=[("MP4 video", "*.mp4"), ("WebM video", "*.webm"), ("All files", "*.*")]
    )
    if not output_video_path:
        messagebox
if __name__ == "__main__":
    main()