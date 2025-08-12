import os
from tkinter import Tk, filedialog
from PIL import Image

def select_folder(prompt):
    """파일 탐색기를 열어 폴더를 선택하도록 함."""
    root = Tk()
    root.withdraw()  # Tkinter 기본창 숨김
    return filedialog.askdirectory(title=prompt)

def split_image_into_columns(image_path, output_folder, columns=4):
    """이미지를 지정된 열 수로 분할하여 저장."""
    img = Image.open(image_path)
    img_width, img_height = img.size

    # 각 열의 너비 계산
    col_width = img_width // columns

    for col in range(columns):
        left = col * col_width
        right = (col + 1) * col_width if col < columns - 1 else img_width
        cropped = img.crop((left, 0, right, img_height))
        
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_folder, f"{base_name}_part{col+1}.png")
        cropped.save(output_path)
        print(f"저장 완료 → {output_path}")

def main():
    # 입력 폴더 선택
    input_folder = select_folder("분할할 이미지들이 있는 폴더를 선택하세요")
    if not input_folder:
        print("입력 폴더를 선택하지 않았습니다. 종료합니다.")
        return

    # 저장 폴더 선택
    output_folder = select_folder("결과 이미지를 저장할 폴더를 선택하세요")
    if not output_folder:
        print("저장 폴더를 선택하지 않았습니다. 종료합니다.")
        return

    # 이미지 파일 목록 가져오기
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(image_extensions)]

    if not image_files:
        print("이미지 파일이 없습니다.")
        return

    # 각 이미지에 대해 4열로 분할 저장
    for img_file in image_files:
        img_path = os.path.join(input_folder, img_file)
        split_image_into_columns(img_path, output_folder, columns=4)

if __name__ == "__main__":
    main()
