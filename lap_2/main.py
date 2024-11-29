import cv2



def hien_thi():
    img = cv2.imread('anh.jpg')
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def chuyen_Xam():

    img = cv2.imread('anh.jpg')


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('ảnh xám ', gray)
    cv2.waitKey(0)


    cv2.imshow('ảnh màu', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def crop_image():
    img = cv2.imread('anh.jpg')
    # cắt nửa
    height, width = img.shape[:2]
    cropped_img = img[int(height * 0.25):int(height * 0.75), int(width * 0.25):int(width * 0.75)]
    cv2.imshow('Cropped Image', cropped_img)
    cv2.imwrite('cropped_image.jpg', cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def resize_image(scale):
    img = cv2.imread('anh.jpg')
    #tinh lại chiều cao vào rộng
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    cv2.imshow('Resized Image', resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def flip_image():
    img = cv2.imread('anh.jpg')
    Lat_Ngang = cv2.flip(img, 1)  
    Lat_Doc = cv2.flip(img, 0)  
    cv2.imshow('Lật ngang', Lat_Ngang)
    cv2.imshow(' Lật dọc', Lat_Doc)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def xoay_Anh():
    img = cv2.imread('anh.jpg')
    # lay kich thươc
    height, width = img.shape[:2]

    #lấy tâm
    center = (width // 2, height // 2)

    #tạo ma trận xoay
    matrix = cv2.getRotationMatrix2D(center, 45, 1.0)

    #vẽ lại ảnh
    rotated_img = cv2.warpAffine(img, matrix, (width, height))
    cv2.imshow('anh da xoay', rotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def menu():
    while True:
        print("\nMenu Bài Tập:")
        print("1. Đọc và hiển thị ảnh")
        print("2. Chuyển màu")
        print("3. cắt anh")
        print("4. Thay đổi kích thước")
        print("5. Lật ảnh")
        print("6. Xoay ảnh")
        print("0. Thoát")

        choice = input("Chọn bài tập (0-6): ")

        if choice == '1':
            hien_thi()
        elif choice == '2':
            chuyen_Xam()
        elif choice == '3':
            crop_image()
        elif choice == '4':
            scale = float(input("Nhập tỷ lệ (ví dụ: 0.9 cho 90%): "))
            resize_image(scale)
        elif choice == '5':
            flip_image()
        elif choice == '6':
            xoay_Anh()
        elif choice == '0':
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")


if __name__ == "__main__":
    menu()
