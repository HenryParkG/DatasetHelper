import os
import shutil
import random

# 원본 경로
src_image_dir = r"D:\original\images"
src_label_dir = r"D:\original\labels"

# 저장 경로
dst_base = "dataset"
train_ratio = 0.8  # train: 80%, test: 20%

# 대상 폴더 생성
for split in ['train', 'test']:
    os.makedirs(os.path.join(dst_base, split, 'images'), exist_ok=True)
    os.makedirs(os.path.join(dst_base, split, 'labels'), exist_ok=True)

# 이미지 리스트 불러오기
image_files = [f for f in os.listdir(src_image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
image_files.sort()  # 순서 고정 (optional)
random.shuffle(image_files)  # 무작위 셔플

# train/test 분할
split_idx = int(len(image_files) * train_ratio)
train_files = image_files[:split_idx]
test_files = image_files[split_idx:]

def copy_files(file_list, split):
    for img_name in file_list:
        label_name = os.path.splitext(img_name)[0] + ".txt"
        
        src_img = os.path.join(src_image_dir, img_name)
        src_lbl = os.path.join(src_label_dir, label_name)

        dst_img = os.path.join(dst_base, split, "images", img_name)
        dst_lbl = os.path.join(dst_base, split, "labels", label_name)

        if os.path.exists(src_img) and os.path.exists(src_lbl):
            shutil.copy2(src_img, dst_img)
            shutil.copy2(src_lbl, dst_lbl)
        else:
            print(f"[경고] 파일 없음: {img_name} / {label_name}")

copy_files(train_files, "train")
copy_files(test_files, "test")

print(f"완료: {len(train_files)} train / {len(test_files)} test 파일 분할됨.")
