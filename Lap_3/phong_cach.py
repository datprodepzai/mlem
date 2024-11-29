import cv2
import numpy as np
import os


def classify_sharpness(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()


    if laplacian_var > 100:
        return "Sắc nét"
    else:
        return "Mờ"


def classify_colorfulness(image):
    # Chuyển đổi ảnh từ không gian màu BGR sang LAB để đo mức độ màu sắc
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    colorfulness = np.std(a) + np.std(b)

    if colorfulness > 100:
        return "Màu sắc đậm"
    else:
        return "Màu sắc nhạt"

def classify_contrast(image):
    # Chuyển ảnh sang xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Đo độ tương phản bằng phương sai của cường độ ánh sáng
    contrast = np.std(gray)

    if contrast > 50:  # Ngưỡng có thể điều chỉnh
        return "Tương phản cao"
    else:
        return "Tương phản thấp"



image_folder = 'captured_images'
images = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

for img_name in images:
    img_path = os.path.join(image_folder, img_name)
    img = cv2.imread(img_path)

    # Phân loại ảnh dựa trên độ sắc nét, mức độ màu sắc và tương phản
    sharpness = classify_sharpness(img)
    colorfulness = classify_colorfulness(img)
    contrast = classify_contrast(img)

    print(f'{img_name}: {sharpness}, {colorfulness}, {contrast}')
