# import cv2
# import os
#
#
# save_folder = 'captured_images'
# if not os.path.exists(save_folder):
#     os.makedirs(save_folder)
#
#
# cap = cv2.VideoCapture(0)
#
# image_count = 0
#
# while image_count < 20:
#     ret, frame = cap.read()
#
#
#     cv2.imshow('Chụp ảnh', frame)
#
#     # Lưu ảnh mỗi khi nhấn phím 's'
#     if cv2.waitKey(1) & 0xFF == ord('s'):
#         image_path = os.path.join(save_folder, f'image_{image_count + 1}.jpg')
#         cv2.imwrite(image_path, frame)
#         print(f'Đã lưu {image_path}')
#         image_count += 1
#
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
#
# cap.release()
# cv2.destroyAllWindows()
import cv2
import numpy as np
import os

def calculate_brightness(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Tính toán độ sáng trung bình
    return np.mean(gray)


image_folder = 'captured_images'
images = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

for img_name in images:
    img_path = os.path.join(image_folder, img_name)
    img = cv2.imread(img_path)


    brightness = calculate_brightness(img)


    if brightness > 127:  # Ngưỡng sáng
        print(f'{img_name}: Ảnh sáng (Brightness = {brightness:.2f})')
    else:
        print(f'{img_name}: Ảnh tối (Brightness = {brightness:.2f})')
