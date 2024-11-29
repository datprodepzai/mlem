import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from rembg import remove

def select_image():
    global image_path, img, display_img
    image_path = filedialog.askopenfilename()
    if image_path:
        img = cv2.imread(image_path)
        resized_img = resize_to_fit(img, 400, 300)  # Resize vừa khung hiển thị
        display_image(resized_img)

# Hàm hiển thị ảnh trên giao diện Tkinter
def display_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(image)
    img_tk = ImageTk.PhotoImage(img_pil)
    display_img.configure(image=img_tk)
    display_img.image = img_tk

# Hàm thu nhỏ ảnh vừa với khung hình
def resize_to_fit(image, frame_width, frame_height):
    h, w = image.shape[:2]
    scale = min(frame_width / w, frame_height / h)
    new_size = (int(w * scale), int(h * scale))
    resized_img = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    return resized_img

# Phát hiện cạnh với thuật toán Sobel
def edge_detection_sobel():
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobel_edges = cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=5)
    abs_sobel_edges = np.uint8(np.absolute(sobel_edges))
    resized_img = resize_to_fit(abs_sobel_edges, 400, 300)  # Resize vừa khung hiển thị
    display_image(resized_img)

# Phát hiện cạnh với thuật toán Canny
def edge_detection_canny():
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny_edges = cv2.Canny(gray, 100, 200)
    resized_img = resize_to_fit(canny_edges, 400, 300)  # Resize vừa khung hiển thị
    display_image(resized_img)

def background_subtraction():
    # Chuyển đổi mảng numpy img thành ảnh PIL để dùng rembg
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_no_bg = remove(img_pil)  # Tách nền

    # Chuyển kết quả từ PIL thành numpy array để hiển thị
    img_no_bg = np.array(img_no_bg)
    img_no_bg = cv2.cvtColor(img_no_bg, cv2.COLOR_RGB2BGR)  # Chuyển sang định dạng BGR cho OpenCV
    resized_img = resize_to_fit(img_no_bg, 400, 300)  # Resize vừa khung hiển thị
    display_image(resized_img)

# Thay đổi kích thước ảnh
def resize_image():
    resized_img = cv2.resize(img, (200, 200), interpolation=cv2.INTER_LINEAR)
    display_image(resized_img)

# Tạo giao diện Tkinter
window = tk.Tk()
window.title("Image Processing Application")
window.geometry("600x500")

btn_select_image = ttk.Button(window, text="Chọn Ảnh", command=select_image)
btn_select_image.pack(pady=5)

btn_sobel = ttk.Button(window, text="Phát hiện cạnh (Sobel)", command=edge_detection_sobel)
btn_sobel.pack(pady=5)

btn_canny = ttk.Button(window, text="Phát hiện cạnh (Canny)", command=edge_detection_canny)
btn_canny.pack(pady=5)

btn_background_sub = ttk.Button(window, text="Tách nền", command=background_subtraction)
btn_background_sub.pack(pady=5)

btn_resize = ttk.Button(window, text="Thay đổi kích thước ảnh", command=resize_image)
btn_resize.pack(pady=5)

display_img = tk.Label(window)
display_img.pack(pady=10)

window.mainloop()
