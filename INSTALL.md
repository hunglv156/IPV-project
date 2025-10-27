# Hướng Dẫn Cài Đặt VisionSpeak

## Yêu Cầu Hệ Thống

- **Python**: 3.7 trở lên
- **Hệ điều hành**: Windows 10+, Linux (Ubuntu 18.04+), macOS 10.14+
- **RAM**: Tối thiểu 4GB (khuyến nghị 8GB)
- **Dung lượng**: Tối thiểu 1GB trống

## Bước 1: Cài Đặt Python

### Windows

1. Tải Python từ [python.org](https://www.python.org/downloads/)
2. Chọn phiên bản Python 3.7+ và tải installer
3. Chạy installer và **NHỚ TÍCH CHỌN** "Add Python to PATH"
4. Kiểm tra cài đặt: mở Command Prompt và gõ `python --version`

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### macOS

```bash
# Sử dụng Homebrew
brew install python3
```

## Bước 2: Cài Đặt Tesseract OCR

### Windows

1. Tải Tesseract từ: https://github.com/UB-Mannheim/tesseract/wiki
2. Chọn phiên bản phù hợp với hệ thống (32-bit hoặc 64-bit)
3. Chạy installer và ghi nhớ đường dẫn cài đặt (thường là `C:\Program Files\Tesseract-OCR\tesseract.exe`)
4. Thêm đường dẫn vào PATH hoặc ghi nhớ để thiết lập trong ứng dụng

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-vie tesseract-ocr-eng
```

### macOS

```bash
brew install tesseract
```

## Bước 3: Cài Đặt Dependencies

1. Mở terminal/command prompt
2. Di chuyển đến thư mục dự án:
   ```bash
   cd path/to/IPV-project
   ```
3. Cài đặt các thư viện Python:
   ```bash
   pip install -r requirements.txt
   ```

## Bước 4: Kiểm Tra Cài Đặt

Chạy file test để kiểm tra:

```bash
python test_vision_speak.py
```

## Bước 5: Chạy Ứng Dụng

```bash
python main.py
```

## Xử Lý Lỗi Thường Gặp

### Lỗi "ModuleNotFoundError"

```bash
# Cài đặt lại dependencies
pip install --upgrade -r requirements.txt
```

### Lỗi "Tesseract not found"

- **Windows**: Thiết lập đường dẫn Tesseract trong tab Cài Đặt của ứng dụng
- **Linux/macOS**: Kiểm tra Tesseract đã được cài đặt:
  ```bash
  tesseract --version
  ```

### Lỗi Camera

- Kiểm tra camera có hoạt động không
- Đảm bảo ứng dụng có quyền truy cập camera
- Thử với ứng dụng camera khác trước

### Lỗi TTS

- **Windows**: Kiểm tra Windows Speech Platform
- **Linux**: Cài đặt espeak hoặc festival:
  ```bash
  sudo apt install espeak
  ```
- **macOS**: Sử dụng giọng nói hệ thống

## Cấu Hình Nâng Cao

### Thiết Lập Đường Dẫn Tesseract (Windows)

Nếu Tesseract không được tìm thấy tự động:

1. Mở ứng dụng VisionSpeak
2. Vào tab "Cài Đặt"
3. Thiết lập đường dẫn đến `tesseract.exe`

### Cài Đặt Ngôn Ngữ OCR Bổ Sung

```bash
# Linux - cài đặt thêm ngôn ngữ
sudo apt install tesseract-ocr-fra tesseract-ocr-deu tesseract-ocr-jpn

# Windows - tải language packs từ GitHub
```

### Tối Ưu Hiệu Suất

- Sử dụng ảnh có độ phân giải vừa phải (không quá lớn)
- Bật debug mode để xem các bước xử lý
- Điều chỉnh cài đặt OCR theo loại văn bản

## Hỗ Trợ

Nếu gặp vấn đề:

1. Kiểm tra log lỗi trong terminal
2. Chạy test suite: `python test_vision_speak.py`
3. Kiểm tra phiên bản Python và các thư viện
4. Đảm bảo đã cài đặt đầy đủ dependencies

## Phiên Bản Được Hỗ Trợ

- **Python**: 3.7, 3.8, 3.9, 3.10, 3.11
- **OpenCV**: 4.5+
- **Tesseract**: 4.0+
- **pyttsx3**: 2.90+
