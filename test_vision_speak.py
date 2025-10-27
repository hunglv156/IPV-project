"""
File test cho VisionSpeak
Kiểm tra các module và tính năng cơ bản
"""

import sys
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Thêm thư mục hiện tại vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from image_processor import ImageProcessor
    from ocr_engine import OCREngine
    from tts_engine import TTSEngine
except ImportError as e:
    print(f"Lỗi import: {e}")
    sys.exit(1)


def create_test_image():
    """
    Tạo ảnh test với văn bản mẫu
    """
    print("Đang tạo ảnh test...")
    
    # Tạo ảnh trắng
    width, height = 800, 400
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Thêm văn bản test
    test_texts = [
        "VisionSpeak - Hệ Thống OCR và TTS",
        "Đây là văn bản test cho nhận dạng ký tự",
        "Text recognition and speech synthesis",
        "Hỗ trợ tiếng Việt và tiếng Anh"
    ]
    
    try:
        # Sử dụng font mặc định
        font = ImageFont.load_default()
    except:
        font = None
    
    y_position = 50
    for text in test_texts:
        draw.text((50, y_position), text, fill='black', font=font)
        y_position += 60
    
    # Lưu ảnh test
    test_image_path = "test_image.jpg"
    image.save(test_image_path, "JPEG")
    print(f"Đã tạo ảnh test: {test_image_path}")
    
    return test_image_path


def test_image_processor():
    """
    Test module xử lý ảnh
    """
    print("\n=== Test Image Processor ===")
    
    processor = ImageProcessor()
    processor.set_debug_mode(True)
    
    # Tạo ảnh test
    test_image_path = create_test_image()
    
    try:
        # Test xử lý ảnh
        processed_image = processor.process_image(test_image_path, "processed_test.jpg")
        
        if processed_image is not None:
            print("✓ Xử lý ảnh thành công")
            print(f"  Kích thước ảnh đã xử lý: {processed_image.shape}")
        else:
            print("✗ Lỗi khi xử lý ảnh")
            
    except Exception as e:
        print(f"✗ Lỗi trong test xử lý ảnh: {e}")


def test_ocr_engine():
    """
    Test module OCR
    """
    print("\n=== Test OCR Engine ===")
    
    ocr = OCREngine()
    
    # Test với ảnh test
    test_image_path = "test_image.jpg"
    
    if not os.path.exists(test_image_path):
        print("Không tìm thấy ảnh test, đang tạo...")
        test_image_path = create_test_image()
    
    try:
        # Test OCR
        result = ocr.extract_text_from_image(test_image_path, language="vie+eng")
        
        if result['success']:
            print("✓ OCR thành công")
            print(f"  Văn bản nhận dạng: {result['text'][:100]}...")
            print(f"  Cấu hình sử dụng: {result['config_used']}")
        else:
            print(f"✗ Lỗi OCR: {result['error']}")
            
    except Exception as e:
        print(f"✗ Lỗi trong test OCR: {e}")


def test_tts_engine():
    """
    Test module TTS
    """
    print("\n=== Test TTS Engine ===")
    
    tts = TTSEngine()
    
    try:
        # Test các tính năng cơ bản
        voices = tts.get_available_voices()
        print(f"✓ Số lượng giọng nói có sẵn: {len(voices)}")
        
        settings = tts.get_current_settings()
        print(f"✓ Cài đặt hiện tại: {settings}")
        
        # Test phát âm
        test_text = "Đây là test hệ thống Text-to-Speech của VisionSpeak."
        print("Đang test phát âm...")
        
        success = tts.speak_processed_text(test_text, blocking=True)
        if success:
            print("✓ Phát âm thành công")
        else:
            print("✗ Lỗi khi phát âm")
        
        # Test lưu file audio
        success = tts.save_to_file(test_text, "test_audio.wav")
        if success:
            print("✓ Lưu file audio thành công")
        else:
            print("✗ Lỗi khi lưu file audio")
            
    except Exception as e:
        print(f"✗ Lỗi trong test TTS: {e}")
    
    finally:
        tts.cleanup()


def test_integration():
    """
    Test tích hợp các module
    """
    print("\n=== Test Tích Hợp ===")
    
    try:
        # Tạo ảnh test
        test_image_path = create_test_image()
        
        # Xử lý ảnh
        processor = ImageProcessor()
        processed_image = processor.process_image(test_image_path)
        
        if processed_image is None:
            print("✗ Lỗi trong xử lý ảnh")
            return
        
        # OCR
        ocr = OCREngine()
        result = ocr.extract_text_from_array(processed_image)
        
        if not result['success']:
            print(f"✗ Lỗi OCR: {result['error']}")
            return
        
        text = result['text']
        print(f"✓ Văn bản nhận dạng: {text[:100]}...")
        
        # TTS
        tts = TTSEngine()
        success = tts.speak_processed_text(text[:50], blocking=True)  # Chỉ đọc 50 ký tự đầu
        
        if success:
            print("✓ Tích hợp thành công!")
        else:
            print("✗ Lỗi trong TTS")
            
        tts.cleanup()
        
    except Exception as e:
        print(f"✗ Lỗi trong test tích hợp: {e}")


def cleanup_test_files():
    """
    Dọn dẹp các file test
    """
    test_files = [
        "test_image.jpg",
        "processed_test.jpg", 
        "test_audio.wav",
        "debug_denoised.jpg",
        "debug_enhanced.jpg",
        "debug_adaptive_thresh.jpg",
        "debug_inverted.jpg",
        "debug_morphological.jpg"
    ]
    
    print("\n=== Dọn Dẹp File Test ===")
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✓ Đã xóa: {file}")
            except Exception as e:
                print(f"✗ Lỗi khi xóa {file}: {e}")


def main():
    """
    Chạy tất cả các test
    """
    print("=== VisionSpeak - Test Suite ===")
    print("Kiểm tra các module và tính năng cơ bản\n")
    
    try:
        # Test từng module
        test_image_processor()
        test_ocr_engine()
        test_tts_engine()
        test_integration()
        
        print("\n=== Kết Quả Test ===")
        print("Các test đã hoàn thành!")
        print("Nếu có lỗi, vui lòng kiểm tra:")
        print("1. Đã cài đặt đầy đủ dependencies: pip install -r requirements.txt")
        print("2. Đã cài đặt Tesseract OCR")
        print("3. Có quyền ghi file trong thư mục hiện tại")
        
    except KeyboardInterrupt:
        print("\nTest bị hủy bởi người dùng")
    except Exception as e:
        print(f"\nLỗi không mong muốn: {e}")
    finally:
        # Dọn dẹp
        cleanup_test_files()


if __name__ == "__main__":
    main()
