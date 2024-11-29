import cv2  # Thư viện xử lý ảnh và video
import mediapipe as mp  # Mediapipe dùng để phân đoạn (segmentation) ảnh
import numpy as np  # Thư viện xử lý mảng số học
from tkinter import Tk, filedialog, Button, Label, Scale, HORIZONTAL  # Tkinter dùng để tạo giao diện đồ họa
from PIL import Image, ImageTk  # PIL hỗ trợ xử lý ảnh để hiển thị trên giao diện Tkinter

# Khởi tạo mô hình Selfie Segmentation của Mediapipe (tách nền khỏi ảnh)
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)  # Chọn mô hình phiên bản 1

# Hàm thay đổi kích thước của ảnh nền sao cho khớp với kích thước ảnh chính
def resize_background(bg_img, anh_shape):
    return cv2.resize(bg_img, (anh_shape[1], anh_shape[0]))  # Thay đổi kích thước dựa trên chiều cao và rộng của ảnh chính

# Hàm tải ảnh chính từ máy tính
def load_image():
    global anh  # Khai báo biến toàn cục để lưu trữ ảnh chính
    # Mở hộp thoại để chọn file ảnh với các định dạng cho phép
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if file_path:  # Nếu người dùng đã chọn file
        anh = cv2.imread(file_path)  # Đọc file ảnh bằng OpenCV
        display_image(anh, "Original Image")  # Hiển thị ảnh chính lên giao diện

# Hàm tải ảnh nền từ máy tính
def load_background():
    global background_img  # Khai báo biến toàn cục để lưu trữ ảnh nền
    # Mở hộp thoại để chọn file ảnh nền
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if file_path:  # Nếu người dùng đã chọn file
        background_img = cv2.imread(file_path)  # Đọc file ảnh nền bằng OpenCV
        display_image(background_img, "Background Image")  # Hiển thị ảnh nền lên giao diện

# Hàm xử lý ảnh chính và ảnh nền để tạo ra kết quả
def process_image():
    # Kiểm tra xem cả ảnh chính và ảnh nền đã được tải chưa
    if anh is None or background_img is None:
        print("Please load both the image and the background!")  # Thông báo nếu thiếu ảnh
        return

    # Chuyển ảnh chính từ không gian màu BGR sang RGB (Mediapipe yêu cầu định dạng RGB)
    rgb_anh = cv2.cvtColor(anh, cv2.COLOR_BGR2RGB)

    # Sử dụng Mediapipe để tách nền bằng cách tạo mặt nạ phân đoạn (segmentation mask)
    result = selfie_segmentation.process(rgb_anh)

    # Tạo mặt nạ phân đoạn (giá trị True/False) dựa trên kết quả segmentation mask
    condition = np.stack((result.segmentation_mask,) * 3, axis=-1) > 0.5

    # Thay đổi kích thước ảnh nền sao cho khớp với kích thước của ảnh chính
    resized_background = resize_background(background_img, anh.shape)

    # Tạo ảnh kết quả: ghép ảnh chính và ảnh nền dựa trên mặt nạ
    output_image = np.where(condition, anh, resized_background)

    # Lấy tỷ lệ từ thanh trượt để thay đổi kích thước của ảnh kết quả
    scale_percent = scale_slider.get()  # Tỷ lệ phần trăm từ thanh trượt
    width = int(output_image.shape[1] * scale_percent / 100)  # Tính chiều rộng mới
    height = int(output_image.shape[0] * scale_percent / 100)  # Tính chiều cao mới
    dim = (width, height)  # Kích thước mới

    # Thay đổi kích thước ảnh kết quả theo kích thước mới
    resized_output = cv2.resize(output_image, dim)

    # Hiển thị ảnh kết quả lên giao diện
    display_image(resized_output, "Result Image")

# Hàm hiển thị ảnh lên giao diện Tkinter
def display_image(image, title):
    # Chuyển ảnh từ không gian màu BGR sang RGB (để hiển thị đúng màu sắc trên Tkinter)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Chuyển đổi ảnh từ định dạng OpenCV thành định dạng PIL
    img_pil = Image.fromarray(image_rgb)

    # Chuyển đổi ảnh từ định dạng PIL thành định dạng Tkinter
    img_tk = ImageTk.PhotoImage(image=img_pil)

    # Cập nhật hình ảnh và tiêu đề lên giao diện Tkinter
    label.config(image=img_tk)  # Gán ảnh mới cho label
    label.image = img_tk  # Lưu trữ ảnh trong label để tránh bị xóa
    label_text.set(title)  # Cập nhật tiêu đề hiển thị trên giao diện

# Tạo cửa sổ giao diện Tkinter
root = Tk()
root.title("Ghép ảnh cùng Đạt")  # Đặt tiêu đề cho cửa sổ
root.geometry("800x600")  # Thiết lập kích thước cửa sổ

# Khởi tạo biến toàn cục để lưu trữ ảnh chính và ảnh nền
anh = None
background_img = None

# Tạo các nút bấm trên giao diện
Button(root, text="Load Image", command=load_image).pack(pady=10)  # Nút tải ảnh chính
Button(root, text="Load Background", command=load_background).pack(pady=10)  # Nút tải ảnh nền
Button(root, text="Process Image", command=process_image).pack(pady=10)  # Nút xử lý ghép ảnh

# Tạo thanh trượt để thay đổi tỷ lệ của ảnh đầu ra
scale_slider = Scale(root, from_=10, to=100, orient=HORIZONTAL, label="Scale (%)")  # Thanh trượt từ 10% đến 100%
scale_slider.set(30)  # Mặc định là 30%
scale_slider.pack(pady=10)  # Thêm vào giao diện

# Tạo label hiển thị trạng thái và hình ảnh
label_text = Label(root, text="No image loaded")  # Nhãn hiển thị trạng thái (chưa tải ảnh)
label_text.pack(pady=5)  # Thêm vào giao diện
label = Label(root)  # Nhãn để hiển thị ảnh
label.pack()  # Thêm vào giao diện

# Chạy vòng lặp giao diện Tkinter
root.mainloop()
