import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def create_concat_file(file_paths, concat_txt_path):
    with open(concat_txt_path, 'w', encoding='utf-8') as f:
        for path in file_paths:
            # ffmpeg concat은 경로 앞에 file '...' 형식으로 작성해야 함
            f.write(f"file '{path}'\n")

def run_ffmpeg_concat(concat_txt_path, output_path):
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_txt_path, '-c', 'copy', output_path]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        messagebox.showinfo("완료", f"동영상 합치기 완료!\n출력파일: {output_path}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"ffmpeg 실행 실패:\n{e.stderr}")

def main():
    root = tk.Tk()
    root.withdraw()

    # 1. 여러 파일 선택 (동영상 파일)
    file_paths = filedialog.askopenfilenames(
        title="합칠 동영상 파일들을 선택하세요",
        filetypes=[("Video files", "*.mp4 *.avi *.webm *.mov *.mkv")]
    )
    if not file_paths:
        messagebox.showwarning("경고", "파일을 선택하지 않았습니다.")
        return

    # 2. input.txt 저장할 위치 및 이름 지정
    concat_txt_path = filedialog.asksaveasfilename(
        title="concat 텍스트 파일 저장",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if not concat_txt_path:
        messagebox.showwarning("경고", "concat 텍스트 파일 저장 위치를 선택하지 않았습니다.")
        return

    # 3. output 동영상 파일명 지정
    output_path = filedialog.asksaveasfilename(
        title="합친 동영상 파일 저장",
        defaultextension=".webm",
        filetypes=[("WebM video", "*.webm"), ("MP4 video", "*.mp4"), ("All files", "*.*")]
    )
    if not output_path:
        messagebox.showwarning("경고", "출력 동영상 파일명을 선택하지 않았습니다.")
        return

    # 4. concat 텍스트 파일 생성
    create_concat_file(file_paths, concat_txt_path)

    # 5. ffmpeg 명령어 실행
    run_ffmpeg_concat(concat_txt_path, output_path)

if __name__ == "__main__":
    main()
