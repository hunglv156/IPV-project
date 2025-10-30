# ⚡ BẮT ĐẦU NHANH - VISIONSPEAK

## 🎯 3 Bước để chạy

### 1️⃣ Cài đặt (lần đầu tiên)

```bash
# Cài Tesseract
brew install tesseract

# Cài thư viện Python
pip install -r requirements.txt
```

### 2️⃣ Tạo ảnh test mẫu

```bash
python create_test_images.py
```

→ Tạo 16 ảnh test (8 tiếng Anh + 8 tiếng Việt) trong `test_images/`

### 3️⃣ Chạy ứng dụng

```bash
# GUI
python gui.py

# Hoặc test command-line
python demo_test.py
```

## 📱 Sử dụng GUI đơn giản

1. **Mở ảnh**: Click "📁 Open Image"
2. **Xử lý & OCR**: Click "⚡ Process & OCR"
3. **Xem kết quả**: Text hiện ở khung dưới
4. **Nghe text**: Click "🔊 Speak"

## 🧪 Test nhanh

```bash
# Test 1 ảnh
python demo_test.py test_images/01_en_normal.png

# Test tất cả
python demo_test.py
# → Chọn option 2
```

## 📁 Các file quan trọng

| File                    | Mô tả                      |
| ----------------------- | -------------------------- |
| `gui.py`                | Ứng dụng GUI chính         |
| `create_test_images.py` | Tạo ảnh test mẫu           |
| `demo_test.py`          | Script demo & test         |
| `test_images/`          | 16 ảnh test case           |
| `README.md`             | Tài liệu đầy đủ            |
| `HUONG_DAN_SU_DUNG.md`  | Hướng dẫn sử dụng chi tiết |

## ⌨️ Phím tắt hữu ích

- `Ctrl+O` - Mở ảnh
- `Ctrl+Shift+P` - Xử lý & OCR (nhanh nhất!)
- `Ctrl+Space` - Đọc text
- `Ctrl+S` - Lưu text

## 🎨 Các loại ảnh test

**Tiếng Anh:** 01-08  
**Tiếng Việt:** 09-16

Mỗi loại gồm:

- Normal (bình thường)
- Noisy (nhiễu)
- Blurry (mờ)
- Dark (tối)
- Inverted (đảo ngược)
- Skewed (nghiêng)
- Low contrast (tương phản thấp)
- Multiline (nhiều dòng)

## 💡 Lưu ý

- ✅ Luôn **xử lý ảnh** trước khi OCR
- ✅ Bật **"Apply Deskew"** nếu ảnh nghiêng
- ✅ Ảnh rõ nét → kết quả tốt hơn

## 🚀 Bắt đầu ngay!

```bash
python gui.py
```

---

**Xem thêm:** `HUONG_DAN_SU_DUNG.md` | `README.md`
