"""
VisionSpeak Demo Script
Demonstrates programmatic usage of VisionSpeak modules
"""

import sys
from image_processor import ImageProcessor
from ocr_engine import OCREngine
from tts_engine import TTSEngine


def demo_image_processing(image_path):
    """
    Demonstrate image processing capabilities.
    
    Args:
        image_path (str): Path to input image
    """
    print("=" * 60)
    print("VisionSpeak - Image Processing Demo")
    print("=" * 60)
    
    # Initialize image processor
    processor = ImageProcessor()
    
    print(f"\n1. Loading image: {image_path}")
    try:
        processor.load_image(image_path)
        print("   ✓ Image loaded successfully")
    except Exception as e:
        print(f"   ✗ Error loading image: {e}")
        return None
    
    print("\n2. Converting to grayscale...")
    gray = processor.convert_to_grayscale(processor.original_image)
    print(f"   ✓ Grayscale image shape: {gray.shape}")
    
    print("\n3. Enhancing contrast...")
    enhanced = processor.enhance_contrast(gray)
    print("   ✓ Contrast enhanced")
    
    print("\n4. Reducing noise...")
    denoised = processor.reduce_noise(enhanced, method='bilateral')
    print("   ✓ Noise reduced")
    
    print("\n5. Applying adaptive thresholding...")
    binary = processor.apply_adaptive_threshold(denoised)
    print("   ✓ Adaptive threshold applied")
    
    print("\n6. Detecting text inversion...")
    is_inverted = processor.detect_inverted_text(binary)
    print(f"   {'✓' if is_inverted else '○'} Text is {'inverted' if is_inverted else 'normal'}")
    
    if is_inverted:
        print("\n7. Inverting image...")
        binary = processor.invert_image(binary)
        print("   ✓ Image inverted")
    
    print("\n8. Processing complete!")
    processor.processed_image = binary
    
    return processor


def demo_ocr(processor):
    """
    Demonstrate OCR capabilities.
    
    Args:
        processor (ImageProcessor): Image processor with processed image
    """
    print("\n" + "=" * 60)
    print("OCR Demo")
    print("=" * 60)
    
    if processor is None or processor.processed_image is None:
        print("No processed image available!")
        return None
    
    # Initialize OCR engine
    ocr = OCREngine()
    
    print("\n1. Checking Tesseract installation...")
    if ocr.check_tesseract_installed():
        version = ocr.get_tesseract_version()
        print(f"   ✓ Tesseract version: {version}")
    else:
        print("   ✗ Tesseract not found! Please install Tesseract OCR.")
        return None
    
    print("\n2. Running OCR with PSM 6 (uniform text block)...")
    try:
        text = ocr.recognize_text(processor.processed_image, psm=6)
        print(f"   ✓ OCR completed - {len(text)} characters recognized")
    except Exception as e:
        print(f"   ✗ OCR failed: {e}")
        return None
    
    print("\n3. Recognized Text:")
    print("-" * 60)
    if text.strip():
        print(text)
    else:
        print("   (No text recognized)")
    print("-" * 60)
    
    return text


def demo_tts(text):
    """
    Demonstrate Text-to-Speech capabilities.
    
    Args:
        text (str): Text to speak
    """
    print("\n" + "=" * 60)
    print("Text-to-Speech Demo")
    print("=" * 60)
    
    if not text or not text.strip():
        print("No text available for TTS!")
        return
    
    # Initialize TTS engine
    tts = TTSEngine()
    
    print("\n1. Initializing TTS engine...")
    print("   ✓ TTS engine initialized")
    
    print("\n2. Available voices:")
    voices = tts.get_voice_info()
    for i, voice in enumerate(voices[:3]):  # Show first 3 voices
        print(f"   {i + 1}. {voice['name']}")
    if len(voices) > 3:
        print(f"   ... and {len(voices) - 3} more")
    
    print(f"\n3. Current settings:")
    settings = tts.get_current_settings()
    print(f"   - Rate: {settings['rate']} words per minute")
    print(f"   - Volume: {settings['volume'] * 100:.0f}%")
    
    print("\n4. Speaking text...")
    print("   (You should hear the text being spoken)")
    try:
        tts.speak(text, blocking=True)
        print("   ✓ Speech completed")
    except Exception as e:
        print(f"   ✗ TTS failed: {e}")


def main():
    """Main demo function."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "      VisionSpeak - Adaptive OCR & TTS Demo".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python demo.py <image_path>")
        print("\nExample:")
        print("  python demo.py sample_image.png")
        print("\nThis script demonstrates:")
        print("  1. Advanced image pre-processing")
        print("  2. Optical Character Recognition")
        print("  3. Text-to-Speech conversion")
        print("\nPlease provide an image file path to continue.")
        return
    
    image_path = sys.argv[1]
    
    # Run demos
    processor = demo_image_processing(image_path)
    
    if processor is not None:
        text = demo_ocr(processor)
        
        if text is not None and text.strip():
            response = input("\n\nWould you like to hear the text spoken? (y/n): ")
            if response.lower() == 'y':
                demo_tts(text)
            else:
                print("Skipping TTS demo.")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print("\nTo use the full GUI application, run:")
    print("  python gui.py")
    print("\n")


if __name__ == "__main__":
    main()

