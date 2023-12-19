import tkinter as tk
from PIL import Image, ImageTk
import cv2
import easyocr
from tkinter import filedialog

class LicensePlateRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng nhận diện biển số xe")

        # Tạo và đặt vị trí các thành phần trên giao diện
        self.label_image = tk.Label(root)
        self.label_image.pack(pady=10)

        self.btn_nhan_dien = tk.Button(root, text="Nhận diện", command=self.capture_and_recognize_license_plate)
        self.btn_nhan_dien.pack(pady=5)

        self.label_hien_thi = tk.Label(root, text="Biển số xe: ")
        self.label_hien_thi.pack(pady=10)

        # Khởi tạo mô hình nhận diện biển số xe
        self.reader = easyocr.Reader(['en'])

    def capture_and_recognize_license_plate(self):
        # Sử dụng hộp thoại tệp để lấy đường dẫn của tệp ảnh
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

        if file_path:
            # Đọc ảnh đã chọn
            self.captured_image = cv2.imread(file_path)

            # Hiển thị ảnh đã chọn trên cửa sổ Tkinter
            rgb_image = cv2.cvtColor(self.captured_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_image)
            image = ImageTk.PhotoImage(image)

            # Hiển thị ảnh đã chọn trên cửa sổ Tkinter
            self.label_image.config(image=image)
            self.label_image.image = image

            # Thực hiện nhận diện biển số trên ảnh đã chọn và hiển thị
            self.recognize_license_plate()

    def recognize_license_plate(self):
        if self.captured_image is not None:
            # Chuyển đổi ảnh sang đen trắng
            gray = cv2.cvtColor(self.captured_image, cv2.COLOR_BGR2GRAY)

            # Thực hiện OCR trên ảnh đen trắng để nhận diện biển số xe
            results = self.reader.readtext(gray)

            if results:
                # Kết hợp kết quả nhận diện trên hai hàng chữ
                license_plate_number = ' '.join([result[-2] for result in results])
                # Hiển thị biển số trên giao diện
                self.label_hien_thi.config(text=f"Biển số xe: {license_plate_number}")
            else:
                self.label_hien_thi.config(text="Không nhận diện được biển số xe")
        else:
            self.label_hien_thi.config(text="Vui lòng nhận diện biển số xe trước khi lưu")

if __name__ == "__main__":
    root = tk.Tk()
    app = LicensePlateRecognitionApp(root)
    root.mainloop()
