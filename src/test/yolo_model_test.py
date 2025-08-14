import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO
import glob

def select_model_file():
    file_path = filedialog.askopenfilename(
        title="YOLO 모델 파일 선택",
        filetypes=[("YOLO 모델 파일", "*.pt")]
    )
    return file_path

def select_dataset_folder():
    folder_path = filedialog.askdirectory(title="테스트 데이터셋 폴더 선택")
    return folder_path

def run_detection():
    model_path = select_model_file()
    if not model_path:
        messagebox.showerror("에러", "모델 파일을 선택해주세요.")
        exit()

    dataset_path = select_dataset_folder()
    if not dataset_path:
        messagebox.showerror("에러", "테스트 데이터셋 폴더를 선택해주세요.")
        exit()

    # 이미지 파일 목록
    image_files = glob.glob(os.path.join(dataset_path, "*.jpg")) + \
                  glob.glob(os.path.join(dataset_path, "*.png")) + \
                  glob.glob(os.path.join(dataset_path, "*.jpeg"))

    if not image_files:
        messagebox.showerror("에러", "데이터셋 폴더에 이미지가 없습니다.")
        exit()

    result_folder = os.path.join(dataset_path, "result")
    os.makedirs(result_folder, exist_ok=True)

    # 모델 로드
    model = YOLO(model_path)

    # 진행 바 초기화
    progress_bar["maximum"] = len(image_files)
    progress_bar["value"] = 0
    root.update_idletasks()

    for idx, img_path in enumerate(image_files):
        results = model(img_path)
        res = results[0]

        # 원본 이미지 로드
        img = Image.open(img_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        # 폰트 설정 (없으면 기본)
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()

        # 바운딩박스 + confidence 표시
        for box in res.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = float(box.conf[0])
            label = f"{conf:.2f}"
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            draw.text((x1, y1 - 15), label, fill="yellow", font=font)

        # 저장
        save_path = os.path.join(result_folder, os.path.basename(img_path))
        img.save(save_path)

        # 진행바 업데이트
        progress_bar["value"] = idx + 1
        root.update_idletasks()

    messagebox.showinfo("완료", f"검출이 완료되었습니다.\n결과는 {result_folder}에 저장되었습니다.")

# GUI 세팅
root = tk.Tk()
root.title("YOLO 모델 테스트")
root.geometry("400x150")

label = tk.Label(root, text="YOLO 모델로 테스트 데이터셋 검출")
label.pack(pady=10)

start_button = tk.Button(root, text="모델 & 데이터셋 선택 후 실행", command=run_detection)
start_button.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
