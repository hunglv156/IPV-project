# VisionSpeak - OCR & TTS Application

**Ứng dụng nhận dạng chữ (OCR) và đọc văn bản (TTS) cho ảnh chất lượng thấp**

## ✨ Tính năng chính

- 🖼️ **Xử lý ảnh nâng cao**: Giảm nhiễu, tăng độ tương phản, tự động đảo ngược
- 🔍 **OCR chính xác**: Tesseract OCR với cấu hình tối ưu
- 🔊 **Text-to-Speech**: Đọc văn bản bằng giọng nói
- 📊 **Giao diện trực quan**: Xem ảnh trước/sau xử lý
- 🌐 **Hỗ trợ đa ngôn ngữ**: Tiếng Anh, Tiếng Việt, v.v.

## 🚀 Cài đặt

### 1. Cài đặt Tesseract OCR

**macOS:**

```bash
brew install tesseract
```

**Ubuntu/Debian:**

```bash
sudo apt-get install tesseract-ocr
```

### 2. Cài đặt thư viện Python

```bash
pip install -r requirements.txt
```

## 📖 Sử dụng

### Chạy ứng dụng GUI

```bash
python gui.py
```

### Test với ảnh mẫu

**Bước 1: Tạo ảnh test**

```bash
python create_test_images.py
```

**Bước 2: Chạy demo test**

```bash
# Test 1 ảnh cụ thể
python demo_test.py test_images/01_en_normal.png

# Hoặc chạy interactive
python demo_test.py
```

### Sử dụng trong code

```python
from image_processor import ImageProcessor
from ocr_engine import OCREngine
from tts_engine import TTSEngine

# Xử lý ảnh
processor = ImageProcessor()
processed = processor.process_image('image.png')

# OCR
ocr = OCREngine()
text = ocr.recognize_text(processed)

# TTS
tts = TTSEngine()
tts.speak(text)
```

## 📁 Cấu trúc project

```
IPV-project/
├── gui.py                    # Ứng dụng GUI chính
├── image_processor.py        # Xử lý ảnh
├── ocr_engine.py            # OCR engine
├── tts_engine.py            # Text-to-Speech
├── demo.py                  # Demo command-line
├── demo_test.py             # Demo test script
├── create_test_images.py    # Tạo ảnh test
├── test_images/             # Thư mục ảnh test (16 ảnh)
├── requirements.txt         # Dependencies
├── README.md               # File này
└── INSTALL.md              # Hướng dẫn cài đặt chi tiết
```

## 🎯 Test Cases

Script `create_test_images.py` tạo 16 ảnh test:

**Tiếng Anh (8 ảnh):**

- Normal, Noisy, Blurry, Dark
- Inverted, Skewed, Low contrast, Multiline

**Tiếng Việt (8 ảnh):**

- Normal, Noisy, Blurry, Dark
- Inverted, Skewed, Low contrast, Multiline

## ⌨️ Phím tắt GUI

| Phím           | Chức năng   |
| -------------- | ----------- |
| `Ctrl+O`       | Mở ảnh      |
| `Ctrl+P`       | Xử lý ảnh   |
| `Ctrl+R`       | Chạy OCR    |
| `Ctrl+Shift+P` | Xử lý & OCR |
| `Ctrl+Space`   | Đọc văn bản |
| `Ctrl+S`       | Lưu văn bản |

## 🔧 Xử lý các loại ảnh khó

VisionSpeak xử lý được:

- ✅ Ảnh nhiễu, mờ
- ✅ Ảnh tối, độ sáng thấp
- ✅ Text trắng trên nền đen
- ✅ Ảnh bị nghiêng
- ✅ Độ tương phản thấp
- ✅ Font chữ không đều

## 📚 Tài liệu

- **README.md** (file này) - Hướng dẫn nhanh
- **INSTALL.md** - Hướng dẫn cài đặt chi tiết
- **demo.py** - Demo command-line
- **demo_test.py** - Test tất cả tính năng

## ⚙️ Yêu cầu hệ thống

- Python 3.8+
- Tesseract OCR 5.0+
- OpenCV, Pillow, NumPy
- pytesseract, pyttsx3

## 🐛 Khắc phục sự cố

**Tesseract không tìm thấy:**

```bash
# Kiểm tra Tesseract
tesseract --version

# Thêm vào PATH hoặc cài đặt lại
```

**Không nhận dạng được text:**

- Xử lý ảnh trước khi OCR
- Bật "Apply Deskew" nếu ảnh bị nghiêng
- Kiểm tra chất lượng ảnh

**TTS không hoạt động:**

```bash
pip install --upgrade pyttsx3
```

## 👨‍💻 Tác giả

VisionSpeak - Dự án IPV

---

**Bắt đầu ngay:** `python gui.py` 🚀
