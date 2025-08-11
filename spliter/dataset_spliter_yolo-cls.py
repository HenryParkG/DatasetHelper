# YOLO 이미지 데이터를 분할하여 train/val/test 폴더로 나누는 스크립트
import os
import shutil
import random

def split_classification_dataset(source_dir, output_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6

    class_names = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]

    for class_name in class_names:
        class_dir = os.path.join(source_dir, class_name)
        images = [f for f in os.listdir(class_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
        random.shuffle(images)

        n = len(images)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)
        n_test = n - n_train - n_val

        split_map = {
            "train": images[:n_train],
            "val": images[n_train:n_train + n_val],
            "test": images[n_train + n_val:]
        }

        for split_name, files in split_map.items():
            dest_dir = os.path.join(output_dir, split_name, class_name)
            os.makedirs(dest_dir, exist_ok=True)
            for file in files:
                src = os.path.join(class_dir, file)
                dst = os.path.join(dest_dir, file)
                shutil.copy2(src, dst)

    print("✅ 데이터셋 분할 완료.")

# 예시 사용
split_classification_dataset(
    source_dir=r"D:\original",       # A/B/C 폴더가 있는 원본
    output_dir=r"D:\modified",          # train/val/test 생성될 폴더
    train_ratio=0.8,
    val_ratio=0.1,
    test_ratio=0.1
)
