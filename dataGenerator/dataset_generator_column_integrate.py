import os
import random
from tkinter import Tk, filedialog
from PIL import Image

def select_folder(prompt):
    """파일 탐색기를 열어 폴더를 선택하도록 함."""
    root = Tk()
    root.withdraw()  # Tkinter GUI 숨김
    folder_path = filedialog.askdirectory(title=prompt)
    return folder_path

def stitch_images_horizontally(image_paths, output_path):
    """이미지들을 가로로 이어붙이고 저장."""
    images = [Image.open(img_path) for img_path in image_paths]
    
    # 모든 이미지의 높이를 동일하게 맞추기 위해 최소 높이 계산
    min_height = min(img.height for img in images)
    resized_images = [img.resize((int(img.width * min_height / img.height), min_height)) for img in images]
    
    # 이어붙일 전체 너비 계산
    total_width = sum(img.width for img in resized_images)
    
    # 새로운 이미지 캔버스 생성
    stitched_image = Image.new("RGB", (total_width, min_height))
    
    # 이미지를 이어붙임
    x_offset = 0
    for img in resized_images:
        stitched_image.paste(img, (x_offset, 0))
        x_offset += img.width
    
    # 결과 저장
    stitched_image.save(output_path)

def main():
    # 입력 폴더 선택
    input_folder = select_folder("이미지가 있는 폴더를 선택하세요")
    if not input_folder:
        print("입력 폴더를 선택하지 않았습니다. 프로그램을 종료합니다.")
        return
    
    # 저장 폴더 선택
    output_folder = select_folder("결과 이미지를 저장할 폴더를 선택하세요")
    if not output_folder:
        print("저장 폴더를 선택하지 않았습니다. 프로그램을 종료합니다.")
        return
    
    # 입력 폴더에서 이미지 파일 가져오기
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(image_extensions)]
    
    if len(image_files) < 4:
        print("이미지가 4개 이상 있어야 합니다. 프로그램을 종료합니다.")
        return
    
    for i in range(1, 21):  # 1부터 20까지 반복
        # 랜덤으로 4개의 이미지 선택
        selected_images = random.sample(image_files, 4)
        selected_image_paths = [os.path.join(input_folder, img) for img in selected_images]
        
        # 결과 저장 경로 설정 (파일명에 번호 추가)
        output_path = os.path.join(output_folder, f"stitched_image_{i:02d}.jpg")
        
        # 이미지 이어붙이기 및 저장
        stitch_images_horizontally(selected_image_paths, output_path)
        print(f"{i}번째 결과 이미지가 저장되었습니다: {output_path}")

if __name__ == "__main__":
    main()
