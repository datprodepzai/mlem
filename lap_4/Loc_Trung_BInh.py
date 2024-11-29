import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

img = None
img_display = None
img_original = None



def open_image():
    global img, img_display, img_original

    # Mở hộp thoại để chọn tệp hình ảnh
    file_path = filedialog.askopenfilename()

    if file_path:

        img = cv2.imread(file_path)


        img_original = img.copy()


        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_display = ImageTk.PhotoImage(Image.fromarray(img_rgb))


        panel.config(image=img_display)
        panel.image = img_display



def apply_filters():
    global img_display

    if img is not None:

        mean_ksize = mean_scale.get()
        median_ksize = median_scale.get()
        gaussian_ksize = gaussian_scale.get()


        if mean_ksize % 2 == 0:
            mean_ksize += 1
        if median_ksize % 2 == 0:
            median_ksize += 1
        if gaussian_ksize % 2 == 0:
            gaussian_ksize += 1


        filtered_img = cv2.blur(img, (mean_ksize, mean_ksize))


        filtered_img = cv2.medianBlur(filtered_img, median_ksize)


        filtered_img = cv2.GaussianBlur(filtered_img, (gaussian_ksize, gaussian_ksize), 0)


        img_rgb = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
        img_display = ImageTk.PhotoImage(Image.fromarray(img_rgb))


        panel.config(image=img_display)
        panel.image = img_display



def reset_to_original():
    global img_display

    if img_original is not None:
        img_rgb = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)
        img_display = ImageTk.PhotoImage(Image.fromarray(img_rgb))


        panel.config(image=img_display)
        panel.image = img_display  # Giữ tham chiếu để không bị xóa bộ nhớ

        mean_scale.set(1)  # Đặt lại giá trị kernel mặc định là 1
    median_scale.set(1)  # Đặt lại giá trị kernel mặc định là 1
    gaussian_scale.set(1)  # Đặt lại giá trị kernel mặc định là 1



def on_scale_change(val):
    apply_filters()



root = tk.Tk()
root.title("Chỉnh sửa hình ảnh với các bộ lọc")


btn_open = tk.Button(root, text="Mở ảnh", command=open_image)
btn_open.pack(side="top", pady=5)


btn_reset = tk.Button(root, text="Chuyển về ảnh gốc", command=reset_to_original)
btn_reset.pack(side="top", pady=5)


mean_scale = tk.Scale(root, from_=1, to=31, orient="horizontal", label="Mean Filter Kernel Size",
                      command=on_scale_change)
mean_scale.pack(side="top", pady=5)
mean_scale.set(3)


median_scale = tk.Scale(root, from_=1, to=31, orient="horizontal", label="Median Filter Kernel Size",
                        command=on_scale_change)
median_scale.pack(side="top", pady=5)
median_scale.set(3)


gaussian_scale = tk.Scale(root, from_=1, to=31, orient="horizontal", label="Gaussian Filter Kernel Size",
                          command=on_scale_change)
gaussian_scale.pack(side="top", pady=5)
gaussian_scale.set(3)  # Đặt giá trị mặc định


panel = tk.Label(root)
panel.pack(padx=5, pady=5)


root.mainloop()