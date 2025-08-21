import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys
import os
import importlib.util

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

def get_script_path(relative_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)

def run_script(script_path):
    python_exe = sys.executable
    try:
        subprocess.run([python_exe, script_path], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"스크립트 실행 실패:\n{e}")

def create_button(frame, text, script_relative_path, tooltip_text=None):
    script_path = get_script_path(script_relative_path)
    btn = tk.Button(frame, text=text, width=40, command=lambda: run_script(script_path))
    btn.pack(pady=3)
    if tooltip_text:
        ToolTip(btn, tooltip_text)
    return btn

def create_scrollable_tab(notebook, tab_name):
    frame_container = ttk.Frame(notebook)
    canvas = tk.Canvas(frame_container)
    scrollbar = ttk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    notebook.add(frame_container, text=tab_name)
    return scroll_frame  # 여기다 버튼이나 라벨 넣기

def check_ffmpeg(canvas, circle_id):
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
        version_line = result.stdout.splitlines()[0]
        canvas.itemconfig(circle_id, fill="green")
        messagebox.showinfo("FFmpeg 확인", f"FFmpeg 설치됨!\n{version_line}")
    except FileNotFoundError:
        canvas.itemconfig(circle_id, fill="red")
        messagebox.showerror("FFmpeg 확인", "FFmpeg이 설치되어 있지 않습니다.")
    except subprocess.CalledProcessError:
        canvas.itemconfig(circle_id, fill="red")
        messagebox.showerror("FFmpeg 확인", "FFmpeg 실행 중 오류가 발생했습니다.")
        
def check_ultralytics(status_canvas, status_circle):
    """
    ultralytics 설치 여부 확인 후 상태 원 색상 변경
    """
    try:
        if importlib.util.find_spec("ultralytics") is not None:
            # 설치됨 → 초록색
            status_canvas.itemconfig(status_circle, fill="green")
            messagebox.showinfo("확인", "ultralytics가 설치되어 있습니다.")
        else:
            # 설치 안됨 → 빨간색
            status_canvas.itemconfig(status_circle, fill="red")
            messagebox.showwarning("확인", "ultralytics가 설치되어 있지 않습니다.")
    except Exception as e:
        status_canvas.itemconfig(status_circle, fill="red")
        messagebox.showerror("오류", f"확인 중 오류 발생:\n{e}")

        
def main():
    root = tk.Tk()
    root.title("DatasetHelper Script Launcher")
    root.geometry("500x800")
    root.resizable(False, False)

    # Notebook 생성
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # 각 탭 프레임
    tab_annotation = ttk.Frame(notebook)
    tab_augmentation = ttk.Frame(notebook)
    tab_generator = ttk.Frame(notebook)
    tab_spliter = ttk.Frame(notebook)
    tab_video = ttk.Frame(notebook)
    tab_test = ttk.Frame(notebook)


    # 탭 추가
    notebook.add(tab_annotation, text="라벨 변환")
    notebook.add(tab_augmentation, text="데이터 증강")
    notebook.add(tab_generator, text="데이터 생성")
    notebook.add(tab_spliter, text="데이터 분할")
    notebook.add(tab_video, text="비디오 처리")
    notebook.add(tab_test, text="모델 테스트")

    # ───── 라벨 변환 탭 ─────
    lf_format_conversion = ttk.LabelFrame(tab_annotation, text="포맷 변환", padding=10)
    lf_format_conversion.pack(fill="x", padx=10, pady=5)
    create_button(lf_format_conversion, "Pascal VOC → YOLO 변환", "changeAnnotation/pascal_to_yolo.py",
                  "Pascal VOC 형식 어노테이션을 YOLO 형식으로 변환")
    create_button(lf_format_conversion, "YOLO → Pascal VOC 변환", "changeAnnotation/yolo_to_pascal.py",
                  "YOLO 형식 어노테이션을 Pascal VOC 형식으로 변환")

    lf_other_conversion = ttk.LabelFrame(tab_annotation, text="기타 변환", padding=10)
    lf_other_conversion.pack(fill="x", padx=10, pady=5)
    create_button(lf_other_conversion, "COCO → YOLO 변환", "changeAnnotation/coco_to_yolo.py",
                  "COCO 형식 어노테이션을 YOLO 형식으로 변환")
    create_button(lf_other_conversion, "YOLO → COCO 변환", "changeAnnotation/yolo_to_coco.py",
                  "YOLO 형식 어노테이션을 COCO 형식으로 변환")

    # ───── 데이터 증강 탭 ─────
    lf_basic_aug = ttk.LabelFrame(tab_augmentation, text="기본 증강", padding=10)
    lf_basic_aug.pack(fill="x", padx=10, pady=5)
    create_button(lf_basic_aug, "밝기 및 대비 조정", "dataAugmentation/dataset_augmentation_brightness.py", "이미지 밝기와 대비를 조절")
    create_button(lf_basic_aug, "이미지 180도 회전", "dataAugmentation/dataset_augmentation_rotate.py", "이미지를 180도 회전")
    create_button(lf_basic_aug, "자르기", "dataAugmentation/dataset_augmentation_crop.py", "이미지 일부분을 잘라냄")

    lf_effects_aug = ttk.LabelFrame(tab_augmentation, text="효과 추가", padding=10)
    lf_effects_aug.pack(fill="x", padx=10, pady=5)
    create_button(lf_effects_aug, "흐림 추가", "dataAugmentation/dataset_augmentation_blur.py", "이미지에 블러(흐림) 효과 추가")
    create_button(lf_effects_aug, "뒤집기", "dataAugmentation/dataset_augmentation_flip.py", "이미지를 좌우 또는 상하 반전")
    create_button(lf_effects_aug, "노이즈 추가", "dataAugmentation/dataset_augmentation_noise.py", "이미지에 랜덤 노이즈 추가")
    create_button(lf_effects_aug, "이동", "dataAugmentation/dataset_augmentation_translate.py", "이미지를 좌표축 방향으로 이동")

    # ───── 데이터 생성 탭 ─────
    lf_column_ops = ttk.LabelFrame(tab_generator, text="데이터 쪼개기", padding=10)
    lf_column_ops.pack(fill="x", padx=10, pady=5)
    create_button(lf_column_ops, "4열 분할 데이터 생성", "dataGenerator/dataset_generator_column_splitter.py", "데이터를 컬럼별로 나누어 생성")
    create_button(lf_column_ops, "4열 데이터 1개의 이미지로 통합", "dataGenerator/dataset_generator_column_integrate.py", "컬럼별 데이터를 하나로 합침")

    lf_label_ops = ttk.LabelFrame(tab_generator, text="라벨 작업", padding=10)
    lf_label_ops.pack(fill="x", padx=10, pady=5)
    create_button(lf_label_ops, "라벨 생성", "dataGenerator/dataset_generator_label_text_creation.py", "데이터 라벨 텍스트 파일 생성")
    create_button(lf_label_ops, "라벨링(프로토)", "dataGenerator/dataset_labeler.py", "데이터 라벨링 웹 UI")

    # ───── 데이터 분할 탭 ─────
    lf_split_cls = ttk.LabelFrame(tab_spliter, text="분류용", padding=10)
    lf_split_cls.pack(fill="x", padx=10, pady=5)
    create_button(lf_split_cls, "YOLO 분류용 데이터 분할", "spliter/dataset_spliter_yolo-cls.py", "YOLO 분류용 데이터셋을 학습/검증용으로 분할")

    lf_split_od = ttk.LabelFrame(tab_spliter, text="객체검출용", padding=10)
    lf_split_od.pack(fill="x", padx=10, pady=5)
    create_button(lf_split_od, "YOLO 객체검출용 데이터 분할", "spliter/dataset_spliter_yolo-od.py", "YOLO 객체 검출용 데이터셋을 학습/검증용으로 분할")

    # ───── 비디오 처리 탭 ─────
    lf_video_merge = ttk.LabelFrame(tab_video, text="동영상+동영상 -> 동영상", padding=10)
    lf_video_merge.pack(fill="x", padx=10, pady=5)
    create_button(lf_video_merge, "FFmpeg 동영상 병합", "video/ffmpeg_merge_videos.py", "여러 동영상을 하나로 병합")

    lf_video_split = ttk.LabelFrame(tab_video, text="동영상 -> 이미지", padding=10)
    lf_video_split.pack(fill="x", padx=10, pady=5)
    create_button(lf_video_split, "FFmpeg 프레임 분할", "video/ffmpeg_frame_splitter.py", "동영상을 프레임 단위 이미지로 분할")
    
    lf_image_merge = ttk.LabelFrame(tab_video, text="이미지+이미지 -> 동영상", padding=10)
    lf_image_merge.pack(fill="x", padx=10, pady=5)
    create_button(lf_image_merge, "FFmpeg 프레임 병합", "video/ffmpeg_frame_merge.py", "이미지를 병합하여 하나의 동영상으로 생성")

    # video 탭 안에서 FFmpeg 확인 버튼 + 상태 원
    frame_ffmpeg = tk.Frame(tab_video)
    frame_ffmpeg.pack(pady=5, padx=5, anchor="w")  # 왼쪽 정렬

    btn_check = tk.Button(frame_ffmpeg, text="FFmpeg 설치 확인",
                        command=lambda: check_ffmpeg(status_canvas, status_circle))
    btn_check.pack(side="left", padx=10)

    # 상태 표시용 Canvas
    status_canvas = tk.Canvas(frame_ffmpeg, width=20, height=20, highlightthickness=0)
    status_canvas.pack(side="left")
    status_circle = status_canvas.create_oval(2, 2, 18, 18, fill="gray")  # 초기 상태: 회색
    
    # ───── 테스트 탭 ─────
    lf_yolo_test = ttk.LabelFrame(tab_test, text="YOLO 모델 테스트", padding=10)
    lf_yolo_test.pack(fill="x", padx=10, pady=5)
    create_button(lf_yolo_test, "모델 테스트", "test/yolo_model_test.py", "YOLO 모델 및 이미지 테스트")

    frame_ultralytics = tk.Frame(tab_test)
    frame_ultralytics.pack(pady=5, padx=5, anchor="w")

    btn_check_ultra = tk.Button(frame_ultralytics, text="Ultralytics 설치 확인",
                                command=lambda: check_ultralytics(ultra_canvas, ultra_circle))
    btn_check_ultra.pack(side="left", padx=10)
    
    ultra_canvas = tk.Canvas(frame_ultralytics, width=20, height=20, highlightthickness=0)
    ultra_canvas.pack(side="left")
    ultra_circle = ultra_canvas.create_oval(2, 2, 18, 18, fill="gray")  # ultralytics 상태 원

    # ──────────────────────────
    # 하단 정보
    version_lavel = tk.Label(root, text="Version 1.0.0",
                          font=("Arial", 10, "italic"), fg="gray")
    version_lavel.pack(side="bottom", pady=2)

    name_label = tk.Label(root, text="HenryParkG | GitHub: https://github.com/HenryParkG/DatasetHelper",
                          font=("Arial", 10, "italic"), fg="gray")
    name_label.pack(side="bottom", pady=2)

    root.mainloop()

if __name__ == "__main__":
    #main()
    import multiprocessing
    multiprocessing.freeze_support()  # pyinstaller exe 실행 시 필요
    app = main()  # tkinter 윈도우 실행
    app.mainloop()
