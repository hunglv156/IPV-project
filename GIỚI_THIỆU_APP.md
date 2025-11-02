# Giới thiệu VisionSpeak

## Tổng quan
**VisionSpeak** là ứng dụng desktop chuyên nghiệp kết hợp **OCR (Nhận dạng ký tự quang học)** và **TTS (Text-to-Speech)** với khả năng xử lý ảnh thông minh. Ứng dụng được thiết kế đặc biệt để xử lý các ảnh chất lượng thấp, nhiễu, hoặc điều kiện ánh sáng không tốt.

## Mục đích chính
- Chuyển đổi văn bản từ ảnh thành văn bản số
- Đọc văn bản đã nhận dạng thành giọng nói
- Hỗ trợ người khiếm thị, học tập, và làm việc với tài liệu

## Tính năng nổi bật

### 1. Xử lý ảnh nâng cao (v1.2)
- **Upscaling tự động**: Tăng độ phân giải cho ảnh chất lượng thấp (+20-30% độ chính xác)
- **Adaptive thresholding**: Xử lý ảnh có ánh sáng không đều
- **Tự động phát hiện đảo ngược**: Nhận diện text trắng trên nền đen
- **Giảm nhiễu & tăng độ tương phản**: Cải thiện chất lượng ảnh trước khi OCR
- **Deskewing**: Tự động chỉnh ảnh bị nghiêng

### 2. OCR chính xác
- **Tesseract OCR** với LSTM engine tối ưu
- **Hỗ trợ đa ngôn ngữ**: Tiếng Anh, Tiếng Việt, hoặc kết hợp
- **Auto multiple PSM modes**: Tự động thử nhiều chế độ cho ảnh khó
- **Cải thiện 10-30% độ chính xác** so với OCR thông thường

### 3. Text-to-Speech thông minh
- **Tự động nhận diện ngôn ngữ**: Phát hiện tiếng Anh/Việt tự động
- **Google TTS cho tiếng Việt**: Chất lượng giọng đọc cao
- **pyttsx3 cho tiếng Anh**: Offline, nhanh chóng
- **Tùy chỉnh tốc độ, âm lượng, giọng nói**

### 4. Giao diện trực quan
- Xem ảnh gốc và ảnh đã xử lý cạnh nhau
- Hiển thị văn bản đã nhận dạng trong text area
- Thanh công cụ với các nút chức năng chính
- Menu và phím tắt đầy đủ

## Công nghệ sử dụng
- **Python 3.8+**
- **Tesseract OCR 5.0+**
- **OpenCV** - Xử lý ảnh
- **PIL/Pillow** - Thao tác ảnh
- **Tkinter** - Giao diện desktop
- **pyttsx3 & gTTS** - Text-to-Speech
- **langdetect** - Nhận diện ngôn ngữ

## Ứng dụng thực tế
- 📚 Số hóa tài liệu, sách, giấy tờ
- 👁️ Hỗ trợ người khiếm thị đọc tài liệu
- 📝 Chuyển đổi hình ảnh thành văn bản có thể chỉnh sửa
- 🎓 Học tập và nghiên cứu
- 🏢 Xử lý tài liệu trong doanh nghiệp

## Điểm mạnh
✅ Xử lý được ảnh chất lượng thấp (nhiễu, mờ, tối, nghiêng)  
✅ Hỗ trợ tiếng Việt có dấu chính xác  
✅ Giao diện đơn giản, dễ sử dụng  
✅ Hoạt động offline (trừ Google TTS tiếng Việt)  
✅ Miễn phí và mã nguồn mở  

## Yêu cầu hệ thống
- Python 3.8+
- Tesseract OCR (với Vietnamese language pack)
- Kết nối Internet (cho Google TTS tiếng Việt - tùy chọn)

---

## Cách chạy
```bash
python gui.py
```

