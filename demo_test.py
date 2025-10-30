"""
VisionSpeak - Demo Test Script
Script demo để test tất cả các tính năng của VisionSpeak
"""

import os
import sys
from image_processor import ImageProcessor
from ocr_engine import OCREngine
from tts_engine import TTSEngine


def print_header(text):
    """In header đẹp"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_step(step, text):
    """In từng bước"""
    print(f"\n{step}. {text}")
    print("-" * 70)


def demo_single_image(image_path):
    """Demo xử lý 1 ảnh"""
    
    if not os.path.exists(image_path):
        print(f"❌ Không tìm thấy ảnh: {image_path}")
        return False
    
    print_header(f"DEMO: {os.path.basename(image_path)}")
    
    # Bước 1: Khởi tạo
    print_step("1", "Khởi tạo các module")
    processor = ImageProcessor()
    ocr = OCREngine()
    tts = TTSEngine()
    print("✓ Đã khởi tạo ImageProcessor, OCREngine, TTSEngine")
    
    # Bước 2: Load ảnh
    print_step("2", "Load ảnh")
    try:
        processor.load_image(image_path)
        print(f"✓ Đã load ảnh: {image_path}")
    except Exception as e:
        print(f"❌ Lỗi load ảnh: {e}")
        return False
    
    # Bước 3: Xử lý ảnh
    print_step("3", "Xử lý ảnh (pre-processing)")
    try:
        processed = processor.process_image(image_path, apply_deskew=True)
        print("✓ Đã xử lý ảnh:")
        print("  - Chuyển grayscale")
        print("  - Tăng cường độ tương phản")
        print("  - Giảm nhiễu")
        print("  - Adaptive thresholding")
        print("  - Kiểm tra và đảo ngược (nếu cần)")
        print("  - Deskew (nếu bị nghiêng)")
    except Exception as e:
        print(f"❌ Lỗi xử lý ảnh: {e}")
        return False
    
    # Bước 4: OCR
    print_step("4", "Nhận dạng text (OCR)")
    try:
        text = ocr.recognize_text(processed, psm=6)
        print("✓ Đã nhận dạng text:")
        print("-" * 70)
        if text.strip():
            print(text)
        else:
            print("  (Không nhận dạng được text)")
        print("-" * 70)
        print(f"  Số ký tự: {len(text)}")
    except Exception as e:
        print(f"❌ Lỗi OCR: {e}")
        return False
    
    # Bước 5: TTS (tùy chọn)
    if text.strip():
        response = input("\n💬 Bạn có muốn nghe text được đọc lên? (y/n): ")
        if response.lower() == 'y':
            print_step("5", "Text-to-Speech")
            try:
                print("🔊 Đang phát âm thanh...")
                tts.speak(text[:200], blocking=True)  # Chỉ đọc 200 ký tự đầu
                print("✓ Đã phát âm thanh")
            except Exception as e:
                print(f"❌ Lỗi TTS: {e}")
    
    print("\n✅ Hoàn thành demo cho ảnh này!")
    return True


def demo_all_test_images():
    """Demo tất cả các ảnh test"""
    
    test_dir = "test_images"
    
    if not os.path.exists(test_dir):
        print(f"❌ Không tìm thấy thư mục {test_dir}/")
        print("💡 Chạy 'python create_test_images.py' để tạo ảnh test")
        return
    
    images = sorted([f for f in os.listdir(test_dir) if f.endswith('.png')])
    
    if not images:
        print(f"❌ Không có ảnh trong thư mục {test_dir}/")
        return
    
    print_header("DEMO TẤT CẢ ẢNH TEST")
    print(f"\nTìm thấy {len(images)} ảnh test")
    
    # Khởi tạo 1 lần
    processor = ImageProcessor()
    ocr = OCREngine()
    
    results = []
    
    for i, img_name in enumerate(images, 1):
        img_path = os.path.join(test_dir, img_name)
        
        print(f"\n[{i}/{len(images)}] Xử lý: {img_name}")
        print("-" * 70)
        
        try:
            # Xử lý ảnh
            processed = processor.process_image(img_path, apply_deskew=True)
            
            # OCR
            text = ocr.recognize_text(processed, psm=6)
            
            # Lưu kết quả
            results.append({
                'file': img_name,
                'text': text.strip(),
                'length': len(text.strip()),
                'success': len(text.strip()) > 0
            })
            
            if text.strip():
                print(f"✓ Text: {text.strip()[:50]}...")
                print(f"  Độ dài: {len(text)} ký tự")
            else:
                print("⚠ Không nhận dạng được text")
                
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            results.append({
                'file': img_name,
                'text': '',
                'length': 0,
                'success': False
            })
    
    # Tổng kết
    print_header("KẾT QUẢ TỔNG HỢP")
    
    success_count = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"\nThành công: {success_count}/{total} ảnh ({success_count/total*100:.1f}%)")
    print("\nChi tiết:")
    print("-" * 70)
    print(f"{'File':<30} {'Số ký tự':<15} {'Trạng thái':<15}")
    print("-" * 70)
    
    for r in results:
        status = "✓ Thành công" if r['success'] else "✗ Thất bại"
        print(f"{r['file']:<30} {r['length']:<15} {status:<15}")
    
    print("-" * 70)
    print(f"\nTổng số ký tự nhận dạng: {sum(r['length'] for r in results)}")


def demo_interactive():
    """Demo interactive - người dùng chọn ảnh"""
    
    print_header("VISIONSPEAK - DEMO INTERACTIVE")
    
    print("\n📋 Menu:")
    print("  1. Test 1 ảnh cụ thể")
    print("  2. Test tất cả ảnh trong test_images/")
    print("  3. Thoát")
    
    choice = input("\n👉 Chọn (1-3): ")
    
    if choice == '1':
        image_path = input("\n📁 Nhập đường dẫn ảnh: ")
        demo_single_image(image_path)
        
    elif choice == '2':
        demo_all_test_images()
        
    elif choice == '3':
        print("\n👋 Tạm biệt!")
        sys.exit(0)
    else:
        print("\n❌ Lựa chọn không hợp lệ!")


def main():
    """Main function"""
    
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  VisionSpeak - Demo Test Script".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    if len(sys.argv) > 1:
        # Nếu có argument, test ảnh đó
        image_path = sys.argv[1]
        demo_single_image(image_path)
    else:
        # Interactive mode
        demo_interactive()


if __name__ == "__main__":
    main()

