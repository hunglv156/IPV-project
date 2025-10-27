# VisionSpeak - Hệ Thống Nhận Dạng Ký Tự Quang Học (OCR) và Phát Âm Thanh (TTS) Thích Ứng

## Mô tả dự án

VisionSpeak là một ứng dụng desktop được phát triển bằng Python, tích hợp công nghệ OCR (Optical Character Recognition) và TTS (Text-to-Speech) để nhận dạng văn bản từ hình ảnh và chuyển đổi thành giọng nói.

## Tính năng chính

- **Xử lý ảnh nâng cao**: Giảm nhiễu, adaptive thresholding, phát hiện và xử lý ảnh đảo ngược màu
- **OCR chính xác**: Sử dụng Tesseract với các cấu hình tối ưu
- **Text-to-Speech**: Chuyển đổi văn bản thành giọng nói với khả năng điều chỉnh tốc độ
- **Giao diện thân thiện**: GUI trực quan với Tkinter

## Cài đặt

1. Cài đặt Python 3.x
2. Cài đặt Tesseract OCR:

   - Windows: Tải từ https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`

3. Cài đặt các thư viện Python:

```bash
pip install -r requirements.txt
```

## Sử dụng

### Chạy ứng dụng chính:

```bash
python main.py
```

### Chạy test suite:

```bash
python test_vision_speak.py
```

### Chạy demo:

```bash
python demo.py
```

### Các tính năng chính:

1. **Tải ảnh**: Chọn file ảnh từ máy tính
2. **Chụp ảnh**: Sử dụng camera để chụp ảnh trực tiếp
3. **Xử lý ảnh**: Tối ưu hóa ảnh cho OCR (giảm nhiễu, adaptive thresholding, phát hiện đảo ngược màu)
4. **OCR**: Nhận dạng văn bản với nhiều cấu hình tối ưu
5. **TTS**: Phát âm văn bản đã nhận dạng
6. **Lưu file**: Xuất văn bản hoặc audio ra file

## Cấu trúc dự án

```
IPV-project/
├── main.py                 # File chính của ứng dụng
├── gui.py                  # Module giao diện người dùng
├── image_processor.py      # Module xử lý ảnh với OpenCV
├── ocr_engine.py          # Module OCR với Pytesseract
├── tts_engine.py          # Module Text-to-Speech
├── test_vision_speak.py   # File test các module
├── demo.py               # File demo minh họa
├── requirements.txt        # Danh sách thư viện cần thiết
├── INSTALL.md             # Hướng dẫn cài đặt chi tiết
└── README.md              # Tài liệu dự án
```

## Yêu cầu hệ thống

- Python 3.7+
- Tesseract OCR Engine
- Camera hoặc khả năng upload ảnh
- Hệ điều hành: Windows, Linux, macOS
