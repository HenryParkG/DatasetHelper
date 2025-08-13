import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# ──────────────────────────────
# 툴팁 기능 클래스
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify="left",
            background="#ffffe0", relief="solid", borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
# ──────────────────────────────


# 현재 파일 기준 상대경로 계산 함수
def get_script_path(relative_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)

# 버튼 누르면 해당 스크립트를 별도 프로세스로 실행
def run_script(script_path):
    python_exe = sys.executable
    try:
        subprocess.run([python_exe, script_path], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"스크립트 실행 실패:\n{e}")

# 버튼 생성 함수 (툴팁 가능)
def create_button(frame, text, script_relative_path, tooltip_text=None):
    script_path = get_script_path(script_relative_path)
    btn = tk.Button(frame, text=text, width=40, command=lambda: run_script(script_path))
    btn.pack(pady=3)
    if tooltip_text:
        ToolTip(btn, tooltip_text)
    return btn


def main():
    root = tk.Tk()
    root.title("DatasetHelper Script Launcher")
    root.geometry("500x800")

    # changeAnnotation 폴더
    frame1 = tk.LabelFrame(root, text="라벨 텍스트 변환", padx=10, pady=10)
    frame1.pack(fill="x", padx=10, pady=5)
    create_button(frame1, "Pascal VOC → YOLO 변환", "changeAnnotation/pascal_to_yolo.py", "Pascal VOC 형식 어노테이션을 YOLO 형식으로 변환")
    create_button(frame1, "YOLO → Pascal VOC 변환", "changeAnnotation/yolo_to_pascal.py", "YOLO 형식 어노테이션을 Pascal VOC 형식으로 변환")

    # dataAugmentation 폴더
    frame2 = tk.LabelFrame(root, text="데이터 증강", padx=10, pady=10)
    frame2.pack(fill="x", padx=10, pady=5)
    create_button(frame2, "밝기 및 대비 조정", "dataAugmentation/dataset_augmentation_brightness.py", "이미지 밝기와 대비를 조절")
    create_button(frame2, "이미지 180도 회전", "dataAugmentation/dataset_augmentation_rotate.py", "이미지를 180도 회전")
    create_button(frame2, "자르기", "dataAugmentation/dataset_augmentation_crop.py", "이미지 일부분을 잘라냄")
    create_button(frame2, "흐림 추가", "dataAugmentation/dataset_augmentation_blur.py", "이미지에 블러(흐림) 효과 추가")
    create_button(frame2, "뒤집기", "dataAugmentation/dataset_augmentation_flip.py", "이미지를 좌우 또는 상하 반전")
    create_button(frame2, "노이즈 추가", "dataAugmentation/dataset_augmentation_noise.py", "이미지에 랜덤 노이즈 추가")
    create_button(frame2, "이동", "dataAugmentation/dataset_augmentation_translate.py", "이미지를 좌표축 방향으로 이동")

    # dataGenerator 폴더
    frame3 = tk.LabelFrame(root, text="데이터 생성", padx=10, pady=10)
    frame3.pack(fill="x", padx=10, pady=5)
    create_button(frame3, "4열 분할 데이터 생성", "dataGenerator/dataset_generator_column_splitter.py", "데이터를 컬럼별로 나누어 생성")
    create_button(frame3, "4열 데이터 1개의 이미지로 통합", "dataGenerator/dataset_generator_column_integrate.py", "컬럼별 데이터를 하나로 합침")
    create_button(frame3, "라벨 생성", "dataGenerator/dataset_generator_label_text_creation.py", "데이터 라벨 텍스트 파일 생성")

    # spliter 폴더
    frame4 = tk.LabelFrame(root, text="동영상 데이터 관리", padx=10, pady=10)
    frame4.pack(fill="x", padx=10, pady=5)
    create_button(frame4, "YOLO 분류용 데이터 분할", "spliter/dataset_spliter_yolo-cls.py", "YOLO 분류용 데이터셋을 학습/검증용으로 분할")
    create_button(frame4, "YOLO 객체검출용 데이터 분할", "spliter/dataset_spliter_yolo-od.py", "YOLO 객체 검출용 데이터셋을 학습/검증용으로 분할")

    # video 폴더
    frame5 = tk.LabelFrame(root, text="video", padx=10, pady=10)
    frame5.pack(fill="x", padx=10, pady=5)
    create_button(frame5, "FFmpeg 동영상 병합", "video/ffmpeg_merge_videos.py", "여러 동영상을 하나로 병합")
    create_button(frame5, "FFmpeg 프레임 분할", "video/ffmpeg_frame_splitter.py", "동영상을 프레임 단위 이미지로 분할")

    # 하단 정보
    name_label = tk.Label(root, text="HenryParkG | GitHub: https://github.com/HenryParkG/DatasetHelper",
                          font=("Arial", 10, "italic"), fg="gray")
    name_label.pack(side="bottom", pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
