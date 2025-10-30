# 📖 HƯỚNG DẪN SỬ DỤNG VISIONSPEAK

## 🚀 Cài đặt nhanh

### 1. Cài đặt Tesseract

```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr
```

### 2. Cài đặt Python packages

```bash
pip install -r requirements.txt
```

## 💻 Chạy ứng dụng

### Giao diện GUI

```bash
python gui.py
```

### Tạo ảnh test mẫu

```bash
python create_test_images.py
```

### Chạy demo test

```bash
# Test 1 ảnh
python demo_test.py test_images/01_en_normal.png

# Interactive mode
python demo_test.py
```

## 📱 Sử dụng GUI

### Bước 1: Mở ảnh

- Click **"📁 Open Image"** hoặc nhấn `Ctrl+O`
- Chọn file ảnh cần xử lý

### Bước 2: Xử lý & OCR

- Click **"⚡ Process & OCR"** để xử lý và nhận dạng text trong 1 lần
- Hoặc:
  - Click **"🔧 Process Image"** để xử lý ảnh trước
  - Click **"🔍 Run OCR"** để nhận dạng text

### Bước 3: Xem kết quả

- Ảnh đã xử lý hiển thị bên phải
- Text nhận dạng hiển thị ở khung dưới

### Bước 4: Nghe text (tùy chọn)

- Click **"🔊 Speak"** để nghe text được đọc
- Click **"⏹ Stop"** để dừng

### Bước 5: Lưu kết quả

- Click **File > Save Text** hoặc nhấn `Ctrl+S`

## ⌨️ Phím tắt

| Phím           | Chức năng   |
| -------------- | ----------- |
| `Ctrl+O`       | Mở ảnh      |
| `Ctrl+P`       | Xử lý ảnh   |
| `Ctrl+R`       | Chạy OCR    |
| `Ctrl+Shift+P` | Xử lý & OCR |
| `Ctrl+Space`   | Đọc text    |
| `Ctrl+S`       | Lưu text    |
| `Ctrl+Q`       | Thoát       |

## 🧪 Test với ảnh mẫu

### Tạo 16 ảnh test

```bash
python create_test_images.py
```

Tạo ra 16 ảnh trong thư mục `test_images/`:

**Tiếng Anh:**

- 01_en_normal.png - Ảnh bình thường
- 02_en_noisy.png - Ảnh nhiễu
- 03_en_blurry.png - Ảnh mờ
- 04_en_dark.png - Ảnh tối
- 05_en_inverted.png - Text trắng nền đen
- 06_en_skewed.png - Ảnh nghiêng
- 07_en_low_contrast.png - Độ tương phản thấp
- 08_en_multiline.png - Nhiều dòng

**Tiếng Việt:**

- 09_vi_normal.png - Ảnh bình thường
- 10_vi_noisy.png - Ảnh nhiễu
- 11_vi_blurry.png - Ảnh mờ
- 12_vi_dark.png - Ảnh tối
- 13_vi_inverted.png - Text trắng nền đen
- 14_vi_skewed.png - Ảnh nghiêng
- 15_vi_low_contrast.png - Độ tương phản thấp
- 16_vi_multiline.png - Nhiều dòng

### Test tất cả ảnh

```bash
python demo_test.py
# Chọn option 2
```

## 💡 Tips

### Để có kết quả OCR tốt nhất:

1. **Luôn xử lý ảnh trước** khi OCR
2. **Bật "Apply Deskew"** nếu ảnh bị nghiêng/xoay
3. **Chụp ảnh rõ nét**, ánh sáng đủ
4. **Text càng lớn càng tốt**
5. **Nền trắng, chữ đen** cho kết quả tốt nhất

### Các loại ảnh VisionSpeak xử lý được:

✅ Ảnh nhiễu, mờ  
✅ Ảnh tối, thiếu sáng  
✅ Text trắng trên nền đen  
✅ Ảnh bị nghiêng  
✅ Độ tương phản thấp  
✅ Font chữ không đồng nhất

## 🐛 Xử lý lỗi

### "Tesseract not found"

```bash
# Kiểm tra Tesseract
tesseract --version

# Cài đặt lại nếu cần
brew install tesseract  # macOS
```

### Không nhận dạng được text

- Xử lý ảnh trước khi OCR
- Thử bật "Apply Deskew"
- Kiểm tra ảnh có text rõ ràng không

### TTS không hoạt động

```bash
pip install --upgrade pyttsx3
```

## 📞 Liên hệ & Hỗ trợ

- 📧 Email: [your-email]
- 📚 Tài liệu: Xem README.md và INSTALL.md
- 🐛 Báo lỗi: [GitHub Issues]

---

**Chúc bạn sử dụng VisionSpeak hiệu quả!** 🎉
