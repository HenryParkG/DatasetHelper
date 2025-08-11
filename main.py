import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# 현재 파일 기준 상대경로 계산 함수
def get_script_path(relative_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)

# 버튼 누르면 해당 스크립트를 별도 프로세스로 실행
def run_script(script_path):
    # Python 실행파일 경로
    python_exe = sys.executable
    try:
        subprocess.run([python_exe, script_path], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"스크립트 실행 실패:\n{e}")

def create_button(frame, text, script_relative_path):
    script_path = get_script_path(script_relative_path)
    btn = tk.Button(frame, text=text, width=40, command=lambda: run_script(script_path))
    btn.pack(pady=3)

def main():
    root = tk.Tk()
    root.title("Project Script Launcher")
    root.geometry("500x700")

    # changeAnnotation 폴더
    frame1 = tk.LabelFrame(root, text="changeAnnotation", padx=10, pady=10)
    frame1.pack(fill="x", padx=10, pady=5)
    create_button(frame1, "Pascal VOC → YOLO 변환", "changeAnnotation/pascal_to_yolo.py")
    create_button(frame1, "YOLO → Pascal VOC 변환", "changeAnnotation/yolo_to_pascal.py")

    # dataAugmentation 폴더
    frame2 = tk.LabelFrame(root, text="dataAugmentation", padx=10, pady=10)
    frame2.pack(fill="x", padx=10, pady=5)
    create_button(frame2, "밝기 및 대비 조정", "dataAugmentation/dataset_augmentation_brightness.py")
    create_button(frame2, "이미지 180도 회전", "dataAugmentation/dataset_augmentation_rotate.py")
    create_button(frame2, "자르기", "dataAugmentation/dataset_augmentation_crop.py")
    create_button(frame2, "흐림 추가", "dataAugmentation/dataset_augmentation_blur.py")
    create_button(frame2, "뒤집기", "dataAugmentation/dataset_augmentation_flip.py")
    create_button(frame2, "노이즈 추가", "dataAugmentation/dataset_augmentation_noise.py")
    create_button(frame2, "이동", "dataAugmentation/dataset_augmentation_translate.py")

    # dataGenerator 폴더
    frame3 = tk.LabelFrame(root, text="dataGenerator", padx=10, pady=10)
    frame3.pack(fill="x", padx=10, pady=5)
    create_button(frame3, "컬럼별 데이터 생성 통합", "dataGenerator/dataset_generatior_column_integrate.py")
    create_button(frame3, "FFmpeg 프레임 분할", "dataGenerator/dataset_generator_ffmpeg_frame_splitter.py")
    create_button(frame3, "라벨 생성", "dataGenerator/dataset_generator_label_creation.py")

    # spliter 폴더
    frame4 = tk.LabelFrame(root, text="spliter", padx=10, pady=10)
    frame4.pack(fill="x", padx=10, pady=5)
    create_button(frame4, "YOLO 분류용 데이터 분할", "spliter/dataset_spliter_yolo-cls.py")
    create_button(frame4, "YOLO 객체검출용 데이터 분할", "spliter/dataset_spliter_yolo-od.py")

    name_label = tk.Label(root, text="HenryParkG | GitHub: https://github.com/HenryParkG/DatasetHelper", font=("Arial", 10, "italic"), fg="gray")
    name_label.pack(side="bottom", pady=10)


    root.mainloop()

if __name__ == "__main__":
    main()
