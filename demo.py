"""
Demo Script cho VisionSpeak
Minh họa cách sử dụng các module một cách đơn giản
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
    print("Vui lòng cài đặt dependencies: pip install -r requirements.txt")
    sys.exit(1)


def create_demo_image():
    """
    Tạo ảnh demo với văn bản mẫu
    """
    print("Tạo ảnh demo...")
    
    # Tạo ảnh với văn bản demo
    width, height = 600, 300
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Văn bản demo
    demo_texts = [
        "VisionSpeak Demo",
        "Hệ thống OCR và TTS",
        "Nhận dạng văn bản từ ảnh",
        "Chuyển đổi thành giọng nói"
    ]
    
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    y_position = 50
    for text in demo_texts:
        draw.text((50, y_position), text, fill='black', font=font)
        y_position += 50
    
    # Lưu ảnh demo
    demo_path = "demo_image.jpg"
    image.save(demo_path, "JPEG")
    print(f"Đã tạo ảnh demo: {demo_path}")
    
    return demo_path


def demo_basic_workflow():
    """
    Demo workflow cơ bản của VisionSpeak
    """
    print("\n" + "="*50)
    print("DEMO VISIONSPEAK - WORKFLOW CƠ BẢN")
    print("="*50)
    
    # Bước 1: Tạo ảnh demo
    print("\n1. Tạo ảnh demo...")
    demo_image_path = create_demo_image()
    
    # Bước 2: Khởi tạo các engine
    print("\n2. Khởi tạo các engine...")
    processor = ImageProcessor()
    ocr = OCREngine()
    tts = TTSEngine()
    
    try:
        # Bước 3: Xử lý ảnh
        print("\n3. Xử lý ảnh...")
        processed_image = processor.process_image(demo_image_path)
        
        if processed_image is None:
            print("❌ Lỗi khi xử lý ảnh!")
            return
        
        print("✅ Xử lý ảnh thành công!")
        
        # Bước 4: OCR
        print("\n4. Nhận dạng văn bản (OCR)...")
        ocr_result = ocr.extract_text_from_image(demo_image_path, language="vie+eng")
        
        if not ocr_result['success']:
            print(f"❌ Lỗi OCR: {ocr_result['error']}")
            return
        
        recognized_text = ocr_result['text']
        print("✅ OCR thành công!")
        print(f"📝 Văn bản nhận dạng: {recognized_text}")
        
        # Bước 5: TTS
        print("\n5. Chuyển đổi thành giọng nói (TTS)...")
        print("🔊 Đang phát âm...")
        
        success = tts.speak_processed_text(recognized_text, blocking=True)
        
        if success:
            print("✅ Phát âm thành công!")
        else:
            print("❌ Lỗi khi phát âm!")
        
        # Bước 6: Lưu kết quả
        print("\n6. Lưu kết quả...")
        
        # Lưu văn bản
        with open("demo_result.txt", "w", encoding="utf-8") as f:
            f.write(recognized_text)
        print("✅ Đã lưu văn bản vào demo_result.txt")
        
        # Lưu audio
        audio_success = tts.save_to_file(recognized_text, "demo_audio.wav")
        if audio_success:
            print("✅ Đã lưu audio vào demo_audio.wav")
        else:
            print("❌ Lỗi khi lưu audio")
        
        print("\n" + "="*50)
        print("DEMO HOÀN THÀNH THÀNH CÔNG!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Lỗi trong demo: {e}")
    
    finally:
        # Dọn dẹp
        tts.cleanup()


def demo_advanced_features():
    """
    Demo các tính năng nâng cao
    """
    print("\n" + "="*50)
    print("DEMO TÍNH NĂNG NÂNG CAO")
    print("="*50)
    
    # Khởi tạo engines
    processor = ImageProcessor()
    ocr = OCREngine()
    tts = TTSEngine()
    
    try:
        # Demo xử lý ảnh với debug mode
        print("\n1. Demo xử lý ảnh với debug mode...")
        processor.set_debug_mode(True)
        
        demo_image_path = "demo_image.jpg"
        if not os.path.exists(demo_image_path):
            demo_image_path = create_demo_image()
        
        processed_image = processor.process_image(demo_image_path, "debug_processed.jpg")
        print("✅ Đã lưu các bước xử lý debug")
        
        # Demo OCR với nhiều cấu hình
        print("\n2. Demo OCR với nhiều cấu hình...")
        results = ocr.extract_text_multiple_configs(processed_image)
        
        print("📊 Kết quả từ các cấu hình khác nhau:")
        for config_name, text in results.items():
            if text.strip():
                print(f"  - {config_name}: {text[:50]}...")
        
        # Demo TTS settings
        print("\n3. Demo điều chỉnh TTS...")
        
        # Thay đổi tốc độ
        tts.set_rate(150)  # Chậm hơn
        print("🔊 Phát âm với tốc độ chậm...")
        tts.speak_processed_text("Tốc độ chậm", blocking=True)
        
        tts.set_rate(250)  # Nhanh hơn
        print("🔊 Phát âm với tốc độ nhanh...")
        tts.speak_processed_text("Tốc độ nhanh", blocking=True)
        
        # Reset về mặc định
        tts.set_rate(200)
        
        print("\n✅ Demo tính năng nâng cao hoàn thành!")
        
    except Exception as e:
        print(f"\n❌ Lỗi trong demo nâng cao: {e}")
    
    finally:
        tts.cleanup()


def cleanup_demo_files():
    """
    Dọn dẹp các file demo
    """
    demo_files = [
        "demo_image.jpg",
        "demo_result.txt",
        "demo_audio.wav",
        "debug_processed.jpg",
        "debug_denoised.jpg",
        "debug_enhanced.jpg",
        "debug_adaptive_thresh.jpg",
        "debug_inverted.jpg",
        "debug_morphological.jpg"
    ]
    
    print("\n🧹 Dọn dẹp file demo...")
    for file in demo_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Đã xóa: {file}")
            except Exception as e:
                print(f"❌ Lỗi khi xóa {file}: {e}")


def main():
    """
    Chạy demo chính
    """
    print("🎯 VISIONSPEAK DEMO")
    print("Minh họa các tính năng của hệ thống OCR và TTS")
    
    try:
        # Demo workflow cơ bản
        demo_basic_workflow()
        
        # Demo tính năng nâng cao
        demo_advanced_features()
        
        print("\n🎉 Tất cả demo đã hoàn thành!")
        print("\n📋 Các file đã tạo:")
        print("  - demo_result.txt: Văn bản đã nhận dạng")
        print("  - demo_audio.wav: File audio")
        print("  - debug_*.jpg: Các bước xử lý ảnh")
        
        # Hỏi có muốn dọn dẹp không
        response = input("\n❓ Bạn có muốn xóa các file demo? (y/n): ")
        if response.lower() in ['y', 'yes', 'có']:
            cleanup_demo_files()
        else:
            print("📁 Các file demo được giữ lại để tham khảo")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo bị hủy bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {e}")
    
    print("\n👋 Cảm ơn bạn đã sử dụng VisionSpeak Demo!")


if __name__ == "__main__":
    main()
