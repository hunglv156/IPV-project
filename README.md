# VisionSpeak - OCR & TTS Application

**Ứng dụng nhận dạng chữ (OCR) và đọc văn bản (TTS) cho ảnh chất lượng thấp**

## ⚡ Quick Fixes

### 1. OCR tiếng Việt không có dấu?

> **Vấn đề:** OCR trả về "Xin chao" thay vì "Xin chào"  
> **Giải pháp:** ✅ **ĐÃ SỬA** - GUI mặc định dùng `vie` (tốt nhất cho tiếng Việt)

📖 **Lưu ý:** Dùng `vie` cho tiếng Việt (không phải `eng+vie`) để có dấu chính xác nhất!

### 2. App không đọc được chữ viết tay?

> **Vấn đề:** Tesseract OCR không được thiết kế cho chữ viết tay (handwriting)  
> **Độ chính xác:** 20-40% (rất thấp) ❌  
> **Giải pháp:** Sử dụng EasyOCR hoặc Google Cloud Vision

📖 **Chi tiết:** Xem [HANDWRITING_SUPPORT.md](HANDWRITING_SUPPORT.md)  
⚠️ **Lưu ý:** VisionSpeak hiện tại **chỉ tốt cho văn bản in**, không phải chữ viết tay

---

## ✨ Tính năng chính

- 🖼️ **Xử lý ảnh nâng cao (v1.2 - ĐÃ TỐI ƯU)**:
  - Upscaling tự động cho ảnh độ phân giải thấp (+20-30% độ chính xác)
  - Sharpening và morphological cleaning
  - Adaptive thresholding với dynamic block size
  - Giảm nhiễu, tăng độ tương phản, tự động đảo ngược
- 🔍 **OCR chính xác (v1.2 - ĐÃ TỐI ƯU)**:
  - Tesseract OCR với OEM mode optimized (LSTM engine)
  - Auto multiple PSM modes cho ảnh khó
  - Cải thiện 10-30% độ chính xác tùy loại ảnh
- 🔊 **Text-to-Speech đa ngôn ngữ (v1.2.1 - ĐÃ CẢI TIẾN)**:
  - Tự động nhận diện ngôn ngữ
  - Ngắt nghỉ tự động theo dấu câu (. ! ? ;) và xuống dòng
  - Pause 300ms giữa các câu cho speech tự nhiên
  - Google TTS cho tiếng Việt (chất lượng cao)
  - pyttsx3 cho tiếng Anh (hoặc fallback)
- 📊 **Giao diện trực quan**: Xem ảnh trước/sau xử lý
- 🌐 **Hỗ trợ đa ngôn ngữ**: Tiếng Anh, Tiếng Việt, v.v.

## 🚀 Cài đặt

### 1. Cài đặt Tesseract OCR

**macOS:**

```bash
brew install tesseract
# Cài đặt ngôn ngữ tiếng Việt
brew install tesseract-lang
```

**Ubuntu/Debian:**

```bash
sudo apt-get install tesseract-ocr
# Cài đặt ngôn ngữ tiếng Việt
sudo apt-get install tesseract-ocr-vie
```

**Windows:**

Tải Tesseract installer từ [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
và chọn cài thêm Vietnamese language pack trong quá trình cài đặt.

### 2. Cài đặt thư viện Python

```bash
pip install -r requirements.txt
```

**Lưu ý:** Ứng dụng sử dụng Google TTS cho tiếng Việt, cần kết nối Internet khi đọc văn bản tiếng Việt lần đầu.

## 📖 Sử dụng

### Kiểm tra hệ thống (Quick Test)

```bash
python test_quick.py
```

Kết quả phải: **✅ TẤT CẢ TEST PASSED!**

### Chạy ứng dụng GUI

```bash
python gui.py
```

### Sử dụng trong code

```python
from image_processor import ImageProcessor
from ocr_engine import OCREngine
from tts_engine import TTSEngine

# Xử lý ảnh
processor = ImageProcessor()
processed = processor.process_image('image.png')

# OCR với tiếng Việt
ocr = OCREngine()
text = ocr.recognize_text(processed, lang='vie')  # 'eng' cho tiếng Anh, 'eng+vie' cho cả hai

# TTS với tự động nhận diện ngôn ngữ
tts = TTSEngine()
tts.speak(text)  # Tự động phát hiện ngôn ngữ và chọn TTS engine phù hợp

# Hoặc chỉ định ngôn ngữ cụ thể
tts.speak(text, lang='vi')  # Tiếng Việt
tts.speak(text, lang='en')  # Tiếng Anh
```

## 📁 Cấu trúc project

```
IPV-project/
├── gui.py                    # Ứng dụng GUI chính
├── main.py                   # Entry point
├── image_processor.py        # Xử lý ảnh
├── ocr_engine.py            # OCR engine
├── tts_engine.py            # Text-to-Speech
├── test_images/             # Thư mục ảnh test mẫu
├── requirements.txt         # Dependencies
├── README.md               # File này
├── INSTALL.md              # Hướng dẫn cài đặt
├── FIX_VIETNAMESE_OCR.md   # Fix tiếng Việt không dấu
├── HANDWRITING_SUPPORT.md  # Hướng dẫn OCR chữ viết tay
└── VIETNAMESE_SUPPORT.md   # Hỗ trợ tiếng Việt đầy đủ
```

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
- **GIAI_THICH_XU_LY_ANH.md** - Giải thích chi tiết 13 bước xử lý ảnh (MỚI) ⭐⭐⭐
- **FINAL_SUMMARY.md** - Tổng kết hoàn chỉnh v1.2.1 ⭐
- **TTS_IMPROVEMENTS.md** - Cải tiến TTS ngắt nghỉ theo dấu câu ⭐
- **VIETNAMESE_SUPPORT.md** - Hỗ trợ đầy đủ tiếng Việt
- **HANDWRITING_LIMITATION.md** - Giới hạn chữ viết tay

## ⚙️ Yêu cầu hệ thống

- Python 3.8+
- Tesseract OCR 5.0+ (với Vietnamese language pack)
- OpenCV, Pillow, NumPy
- pytesseract, pyttsx3, gTTS, pygame
- langdetect (tự động nhận diện ngôn ngữ)
- Kết nối Internet (cho Google TTS tiếng Việt)

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
pip install --upgrade pyttsx3 gTTS pygame
```

**TTS tiếng Việt không hoạt động:**

- Kiểm tra kết nối Internet (Google TTS cần Internet)
- Bật "Use Google TTS for Vietnamese" trong Speech > TTS Settings
- Kiểm tra các thư viện đã cài đặt:
  ```bash
  pip install gTTS pygame langdetect
  ```

**OCR không nhận tiếng Việt:**

```bash
# Kiểm tra ngôn ngữ đã cài
tesseract --list-langs

# Nếu không có 'vie', cài thêm:
# macOS:
brew install tesseract-lang

# Ubuntu:
sudo apt-get install tesseract-ocr-vie
```

## 👨‍💻 Tác giả

VisionSpeak - Dự án IPV

---

**Bắt đầu ngay:** `python gui.py` 🚀
