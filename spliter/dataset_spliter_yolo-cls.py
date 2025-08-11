import os
import shutil
import random
from tkinter import Tk, filedialog

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

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # GUI 숨기기

    print("원본 데이터셋이 있는 폴더를 선택하세요.")
    source_dir = filedialog.askdirectory(title="원본 데이터셋 폴더 선택")
    if not source_dir:
        print("❌ 원본 폴더를 선택하지 않았습니다. 종료합니다.")
        exit()

    print("분할된 데이터셋을 저장할 폴더를 선택하세요.")
    output_dir = filedialog.askdirectory(title="출력 폴더 선택")
    if not output_dir:
        print("❌ 출력 폴더를 선택하지 않았습니다. 종료합니다.")
        exit()

    # 비율 설정 필요하면 여기서 수정 가능
    train_ratio = 0.8
    val_ratio = 0.1
    test_ratio = 0.1

    split_classification_dataset(source_dir, output_dir, train_ratio, val_ratio, test_ratio)
