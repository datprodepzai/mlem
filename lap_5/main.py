import tkinter as tk
from tkinter import filedialog, Scale
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np

img = None


def open_image():
    global img, img_display
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        update_image()


def update_image():
    global img_display
    if img is None:
        return

    img_cv = np.array(img.convert("RGB"))


    if color_space.get() == "YUV":
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2YUV)
    elif color_space.get() == "CMYK":
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2LAB)  # CMYK không có sẵn trong OpenCV


    enhancer = ImageEnhance.Color(img)
    img_pil = enhancer.enhance(color_balance_scale.get())


    img_pil = ImageEnhance.Contrast(img_pil).enhance(contrast_scale.get())


    img_cv = np.array(img_pil.convert("RGB"))
    r, g, b = cv2.split(img_cv)
    r = cv2.multiply(r, red_scale.get())
    g = cv2.multiply(g, green_scale.get())
    b = cv2.multiply(b, blue_scale.get())
    img_cv = cv2.merge([r, g, b])

    img_pil = Image.fromarray(img_cv)
    img_pil = img_pil.resize((500, 500), Image.LANCZOS)  # Chỉnh kích thước ảnh cho vừa khung
    img_display = ImageTk.PhotoImage(img_pil)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_display)



root = tk.Tk()
root.title("Chỉnh sửa ảnh với tkinter")


canvas = tk.Canvas(root, width=500, height=500)
canvas.grid(row=0, column=0, rowspan=12)


btn_open = tk.Button(root, text="Chọn ảnh", command=open_image)
btn_open.grid(row=0, column=1, padx=10, pady=10)


tk.Label(root, text="Chọn không gian màu:").grid(row=1, column=1, padx=10, pady=5, sticky='w')
color_space = tk.StringVar(value="RGB")
color_menu = tk.OptionMenu(root, color_space, "RGB", "YUV", "CMYK", command=lambda _: update_image())
color_menu.grid(row=2, column=1, padx=10, pady=5)


tk.Label(root, text="Cân bằng màu:").grid(row=3, column=1, padx=10, pady=5, sticky='w')
color_balance_scale = Scale(root, from_=0.5, to=3, resolution=0.1, orient=tk.HORIZONTAL, command=lambda _: update_image())
color_balance_scale.set(1.0)
color_balance_scale.grid(row=4, column=1, padx=10, pady=5)


tk.Label(root, text="Tăng cường độ tương phản:").grid(row=5, column=1, padx=10, pady=5, sticky='w')
contrast_scale = Scale(root, from_=0.5, to=3, resolution=0.1, orient=tk.HORIZONTAL, command=lambda _: update_image())
contrast_scale.set(1.0)
contrast_scale.grid(row=6, column=1, padx=10, pady=5)


tk.Label(root, text="Lọc màu Đỏ:").grid(row=7, column=1, padx=10, pady=5, sticky='w')
red_scale = Scale(root, from_=0.5, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=lambda _: update_image())
red_scale.set(1.0)
red_scale.grid(row=8, column=1, padx=10, pady=5)


tk.Label(root, text="Lọc màu Xanh Lục:").grid(row=9, column=1, padx=10, pady=5, sticky='w')
green_scale = Scale(root, from_=0.5, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=lambda _: update_image())
green_scale.set(1.0)
green_scale.grid(row=10, column=1, padx=10, pady=5)


tk.Label(root, text="Lọc màu Xanh Lam:").grid(row=11, column=1, padx=10, pady=5, sticky='w')
blue_scale = Scale(root, from_=0.5, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=lambda _: update_image())
blue_scale.set(1.0)
blue_scale.grid(row=12, column=1, padx=10, pady=5)

root.mainloop()
