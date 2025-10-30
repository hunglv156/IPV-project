"""
Script để tạo các ảnh test case cho VisionSpeak
Tạo ảnh với nhiều điều kiện khác nhau: tiếng Anh, tiếng Việt, nhiễu, tối, nghiêng, v.v.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np


def create_test_images_folder():
    """Tạo thư mục test_images nếu chưa có"""
    if not os.path.exists('test_images'):
        os.makedirs('test_images')
        print("✓ Đã tạo thư mục test_images/")


def create_normal_image(text, filename, language='en'):
    """Tạo ảnh bình thường với text rõ ràng"""
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Thử dùng font hệ thống
        if language == 'vi':
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        else:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()
    
    # Vẽ text ở giữa
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((800 - text_width) // 2, (400 - text_height) // 2)
    
    draw.text(position, text, fill='black', font=font)
    
    img.save(f'test_images/{filename}')
    print(f"✓ Đã tạo: {filename}")


def create_noisy_image(text, filename, language='en'):
    """Tạo ảnh có nhiễu"""
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        if language == 'vi':
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        else:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((800 - text_width) // 2, (400 - text_height) // 2)
    
    draw.text(position, text, fill='black', font=font)
    
    # Thêm nhiễu
    img_array = np.array(img)
    noise = np.random.normal(0, 25, img_array.shape)
    noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(noisy_img)
    
    img.save(f'test_images/{filename}')
    print(f"✓ Đã tạo: {filename}")


def create_blurry_image(text, filename, language='en'):
    """Tạo ảnh bị mờ"""
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        if language == 'vi':
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        else:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((800 - text_width) // 2, (400 - text_height) // 2)
    
    draw.text(position, text, fill='black', font=font)
    
    # Làm mờ
    img = img.filter(ImageFilter.GaussianBlur(radius=3))
    
    img.save(f'test_images/{filename}')
    print(f"✓ Đã tạo: {filename}")


def create_dark_image(text, filename, language='en'):
    """Tạo ảnh tối, độ tương phản thấp"""
    img = Image.new('RGB', (800, 400), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    
    try:
        if language == 'vi':
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        else:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((800 - text_width) // 2, (400 - text_height) // 2)
    
    draw.text(position, text, fill=(120, 120, 120), font=font)
    
    img.save(f'test_images/{filename}')
    print(f"✓ Đã tạo: {filename}")


def create_inverted_image(text, filename, language='en'):
    """Tạo ảnh với text màu sáng trên nền tối (inverted)"""
    img = Image.new('RGB', (800, 400), color='black')
    draw = ImageDraw.Draw(img)
    
    try:
        if language == 'vi':
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        else:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((800 - text_width) // 2, (400 - text_height) // 2)
    
    draw.text(position, text, fill='white', font=font)
    
    img.save(f'test_images/{filename}')
    print(f"✓ Đã tạo: {filename}")


def create_skewed_image(text, filename, language='en'):
    """Tạo ảnh bị nghiêng"""
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        if language == 'vi':
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        else:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((800 - text_width) // 2, (400 - text_height) // 2)
    
    draw.text(position, text, fill='black', font=font)
    
    # Xoay 15 độ
    img = img.rotate(15, fillcolor='white', expand=False)
    
    img.save(f'test_images/{filename}')
    print(f"✓ Đã tạo: {filename}")


def create_low_contrast_image(text, filename, language='en'):
    """Tạo ảnh độ tương phản thấp"""
    img = Image.new('RGB', (800, 400), color=(200, 200, 200))
    draw = ImageDraw.Draw(img)
    
    try:
        if language == 'vi':
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        else:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((800 - text_width) // 2, (400 - text_height) // 2)
    
    draw.text(position, text, fill=(100, 100, 100), font=font)
    
    img.save(f'test_images/{filename}')
    print(f"✓ Đã tạo: {filename}")


def create_multiline_image(lines, filename, language='en'):
    """Tạo ảnh với nhiều dòng text"""
    img = Image.new('RGB', (800, 500), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        if language == 'vi':
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 35)
        else:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 35)
    except:
        font = ImageFont.load_default()
    
    y_offset = 50
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        position = ((800 - text_width) // 2, y_offset)
        draw.text(position, line, fill='black', font=font)
        y_offset += 60
    
    img.save(f'test_images/{filename}')
    print(f"✓ Đã tạo: {filename}")


def main():
    """Tạo tất cả các ảnh test case"""
    print("\n🎨 Bắt đầu tạo ảnh test case...\n")
    
    create_test_images_folder()
    
    print("\n📝 Tạo ảnh tiếng Anh:")
    print("-" * 50)
    
    # Ảnh tiếng Anh
    create_normal_image("Hello World! VisionSpeak OCR", "01_en_normal.png", 'en')
    create_noisy_image("This is a noisy text image", "02_en_noisy.png", 'en')
    create_blurry_image("Blurry text for testing OCR", "03_en_blurry.png", 'en')
    create_dark_image("Dark image with low light", "04_en_dark.png", 'en')
    create_inverted_image("White text on black background", "05_en_inverted.png", 'en')
    create_skewed_image("Skewed text at 15 degrees", "06_en_skewed.png", 'en')
    create_low_contrast_image("Low contrast gray text", "07_en_low_contrast.png", 'en')
    
    create_multiline_image([
        "VisionSpeak OCR Test",
        "Multiple lines of text",
        "For comprehensive testing"
    ], "08_en_multiline.png", 'en')
    
    print("\n📝 Tạo ảnh tiếng Việt:")
    print("-" * 50)
    
    # Ảnh tiếng Việt
    create_normal_image("Xin chào Việt Nam!", "09_vi_normal.png", 'vi')
    create_noisy_image("Ảnh có nhiễu tiếng Việt", "10_vi_noisy.png", 'vi')
    create_blurry_image("Chữ bị mờ cần xử lý", "11_vi_blurry.png", 'vi')
    create_dark_image("Ảnh tối độ sáng thấp", "12_vi_dark.png", 'vi')
    create_inverted_image("Chữ trắng nền đen", "13_vi_inverted.png", 'vi')
    create_skewed_image("Chữ bị nghiêng 15 độ", "14_vi_skewed.png", 'vi')
    create_low_contrast_image("Độ tương phản thấp", "15_vi_low_contrast.png", 'vi')
    
    create_multiline_image([
        "VisionSpeak - OCR Tiếng Việt",
        "Nhận dạng văn bản chính xác",
        "Hỗ trợ nhiều điều kiện ảnh"
    ], "16_vi_multiline.png", 'vi')
    
    print("\n✅ Hoàn thành! Đã tạo 16 ảnh test case")
    print(f"📁 Vị trí: {os.path.abspath('test_images')}/")
    print("\n💡 Sử dụng các ảnh này để test VisionSpeak!")


if __name__ == "__main__":
    main()

