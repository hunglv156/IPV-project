"""
VisionSpeak - Hệ Thống Nhận Dạng Ký Tự Quang Học (OCR) và Phát Âm Thanh (TTS) Thích Ứng

File chính để chạy ứng dụng VisionSpeak
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Thêm thư mục hiện tại vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui import VisionSpeakGUI
except ImportError as e:
    print(f"Lỗi import: {e}")
    print("Vui lòng cài đặt các thư viện cần thiết bằng lệnh: pip install -r requirements.txt")
    sys.exit(1)


def check_dependencies():
    """
    Kiểm tra các thư viện cần thiết
    """
    required_modules = [
        'cv2',
        'pytesseract', 
        'PIL',
        'pyttsx3',
        'numpy'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"Các thư viện sau chưa được cài đặt: {', '.join(missing_modules)}\n\n"
        error_msg += "Vui lòng chạy lệnh: pip install -r requirements.txt"
        
        root = tk.Tk()
        root.withdraw()  # Ẩn cửa sổ chính
        messagebox.showerror("Lỗi Dependencies", error_msg)
        root.destroy()
        return False
    
    return True


def check_tesseract():
    """
    Kiểm tra Tesseract OCR
    """
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        return True
    except Exception as e:
        error_msg = "Không thể tìm thấy Tesseract OCR!\n\n"
        error_msg += "Vui lòng cài đặt Tesseract OCR:\n"
        error_msg += "- Windows: Tải từ https://github.com/UB-Mannheim/tesseract/wiki\n"
        error_msg += "- Linux: sudo apt-get install tesseract-ocr\n"
        error_msg += "- macOS: brew install tesseract\n\n"
        error_msg += "Sau đó thiết lập đường dẫn trong cài đặt ứng dụng."
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Lỗi Tesseract", error_msg)
        root.destroy()
        return False


def main():
    """
    Hàm main để chạy ứng dụng VisionSpeak
    """
    print("=== VisionSpeak - Hệ Thống OCR và TTS Thích Ứng ===")
    print("Đang khởi động ứng dụng...")
    
    # Kiểm tra dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Kiểm tra Tesseract
    if not check_tesseract():
        sys.exit(1)
    
    try:
        # Tạo cửa sổ chính
        root = tk.Tk()
        
        # Thiết lập icon (nếu có)
        try:
            # root.iconbitmap('icon.ico')  # Uncomment nếu có file icon
            pass
        except:
            pass
        
        # Tạo ứng dụng
        app = VisionSpeakGUI(root)
        
        print("Ứng dụng đã sẵn sàng!")
        print("Hướng dẫn:")
        print("1. Tải ảnh hoặc chụp ảnh từ camera")
        print("2. Xử lý ảnh để tối ưu hóa OCR")
        print("3. Nhận dạng văn bản")
        print("4. Phát âm văn bản hoặc lưu ra file")
        
        # Chạy ứng dụng
        root.mainloop()
        
    except Exception as e:
        error_msg = f"Lỗi khi khởi động ứng dụng: {e}"
        print(error_msg)
        
        # Hiển thị lỗi trong GUI nếu có thể
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Lỗi Khởi Động", error_msg)
            root.destroy()
        except:
            pass
        
        sys.exit(1)
    
    finally:
        # Dọn dẹp tài nguyên
        try:
            if 'app' in locals():
                app.tts_engine.cleanup()
        except:
            pass
        
        print("Ứng dụng đã thoát.")


if __name__ == "__main__":
    main()
