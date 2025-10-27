"""
Module xử lý ảnh nâng cao cho VisionSpeak
Tích hợp các thuật toán OpenCV để tiền xử lý ảnh trước khi OCR
"""

import cv2
import numpy as np
from PIL import Image
import os


class ImageProcessor:
    """
    Lớp xử lý ảnh với các thuật toán nâng cao để tối ưu hóa OCR
    """
    
    def __init__(self):
        self.debug_mode = False
        
    def set_debug_mode(self, enabled):
        """Bật/tắt chế độ debug để lưu các bước xử lý"""
        self.debug_mode = enabled
        
    def load_image(self, image_path):
        """
        Tải ảnh từ đường dẫn file
        
        Args:
            image_path (str): Đường dẫn đến file ảnh
            
        Returns:
            numpy.ndarray: Ảnh đã được tải
        """
        try:
            # Đọc ảnh bằng OpenCV
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Không thể tải ảnh từ {image_path}")
            return image
        except Exception as e:
            print(f"Lỗi khi tải ảnh: {e}")
            return None
    
    def resize_image(self, image, max_width=1200, max_height=800):
        """
        Thay đổi kích thước ảnh để tối ưu hóa OCR
        
        Args:
            image (numpy.ndarray): Ảnh đầu vào
            max_width (int): Chiều rộng tối đa
            max_height (int): Chiều cao tối đa
            
        Returns:
            numpy.ndarray: Ảnh đã được resize
        """
        height, width = image.shape[:2]
        
        # Tính tỷ lệ scale
        scale_w = max_width / width
        scale_h = max_height / height
        scale = min(scale_w, scale_h, 1.0)  # Không phóng to ảnh
        
        if scale < 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
        return image
    
    def denoise_image(self, image):
        """
        Giảm nhiễu trong ảnh bằng Gaussian và Median blur
        
        Args:
            image (numpy.ndarray): Ảnh đầu vào
            
        Returns:
            numpy.ndarray: Ảnh đã được làm sạch nhiễu
        """
        # Áp dụng Gaussian blur để làm mịn
        blurred = cv2.GaussianBlur(image, (3, 3), 0)
        
        # Áp dụng Median blur để loại bỏ nhiễu salt & pepper
        denoised = cv2.medianBlur(blurred, 3)
        
        if self.debug_mode:
            cv2.imwrite("debug_denoised.jpg", denoised)
            
        return denoised
    
    def enhance_contrast(self, image):
        """
        Tăng cường độ tương phản của ảnh bằng CLAHE
        
        Args:
            image (numpy.ndarray): Ảnh đầu vào
            
        Returns:
            numpy.ndarray: Ảnh đã được tăng cường độ tương phản
        """
        # Chuyển sang LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Áp dụng CLAHE trên kênh L
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Ghép lại các kênh
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        if self.debug_mode:
            cv2.imwrite("debug_enhanced.jpg", enhanced)
            
        return enhanced
    
    def adaptive_threshold(self, image):
        """
        Áp dụng adaptive thresholding để xử lý độ sáng không đồng đều
        
        Args:
            image (numpy.ndarray): Ảnh đầu vào
            
        Returns:
            numpy.ndarray: Ảnh đã được binarize
        """
        # Chuyển sang grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Áp dụng adaptive thresholding với Gaussian
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        if self.debug_mode:
            cv2.imwrite("debug_adaptive_thresh.jpg", binary)
            
        return binary
    
    def detect_and_fix_inversion(self, binary_image):
        """
        Phát hiện và sửa ảnh đảo ngược màu (chữ sáng trên nền tối)
        
        Args:
            binary_image (numpy.ndarray): Ảnh đã được binarize
            
        Returns:
            numpy.ndarray: Ảnh đã được sửa đảo ngược
        """
        # Tính tỷ lệ pixel trắng
        white_pixels = np.sum(binary_image == 255)
        total_pixels = binary_image.shape[0] * binary_image.shape[1]
        white_ratio = white_pixels / total_pixels
        
        # Nếu tỷ lệ pixel trắng > 50%, có thể là ảnh đảo ngược
        if white_ratio > 0.5:
            # Đảo ngược màu
            inverted = cv2.bitwise_not(binary_image)
            if self.debug_mode:
                cv2.imwrite("debug_inverted.jpg", inverted)
            return inverted
        
        return binary_image
    
    def morphological_operations(self, binary_image):
        """
        Áp dụng các phép toán hình thái học để làm sạch ảnh
        
        Args:
            binary_image (numpy.ndarray): Ảnh đã được binarize
            
        Returns:
            numpy.ndarray: Ảnh đã được làm sạch
        """
        # Kernel cho các phép toán hình thái học
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        
        # Loại bỏ nhiễu nhỏ
        cleaned = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
        
        # Làm mỏng các đường viền
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        if self.debug_mode:
            cv2.imwrite("debug_morphological.jpg", cleaned)
            
        return cleaned
    
    def process_image(self, image_path, output_path=None):
        """
        Xử lý ảnh hoàn chỉnh với pipeline tối ưu cho OCR
        
        Args:
            image_path (str): Đường dẫn đến ảnh đầu vào
            output_path (str): Đường dẫn lưu ảnh đã xử lý (tùy chọn)
            
        Returns:
            numpy.ndarray: Ảnh đã được xử lý tối ưu cho OCR
        """
        try:
            # Tải ảnh
            image = self.load_image(image_path)
            if image is None:
                return None
            
            # Thay đổi kích thước
            image = self.resize_image(image)
            
            # Giảm nhiễu
            image = self.denoise_image(image)
            
            # Tăng cường độ tương phản
            image = self.enhance_contrast(image)
            
            # Adaptive thresholding
            binary = self.adaptive_threshold(image)
            
            # Phát hiện và sửa đảo ngược
            binary = self.detect_and_fix_inversion(binary)
            
            # Phép toán hình thái học
            binary = self.morphological_operations(binary)
            
            # Lưu ảnh kết quả nếu có đường dẫn output
            if output_path:
                cv2.imwrite(output_path, binary)
                
            return binary
            
        except Exception as e:
            print(f"Lỗi trong quá trình xử lý ảnh: {e}")
            return None
    
    def process_from_array(self, image_array):
        """
        Xử lý ảnh từ numpy array (cho camera)
        
        Args:
            image_array (numpy.ndarray): Ảnh dạng numpy array
            
        Returns:
            numpy.ndarray: Ảnh đã được xử lý
        """
        try:
            # Thay đổi kích thước
            image = self.resize_image(image_array)
            
            # Giảm nhiễu
            image = self.denoise_image(image)
            
            # Tăng cường độ tương phản
            image = self.enhance_contrast(image)
            
            # Adaptive thresholding
            binary = self.adaptive_threshold(image)
            
            # Phát hiện và sửa đảo ngược
            binary = self.detect_and_fix_inversion(binary)
            
            # Phép toán hình thái học
            binary = self.morphological_operations(binary)
            
            return binary
            
        except Exception as e:
            print(f"Lỗi trong quá trình xử lý ảnh từ array: {e}")
            return None


def test_image_processor():
    """Hàm test cho ImageProcessor"""
    processor = ImageProcessor()
    processor.set_debug_mode(True)
    
    # Test với ảnh mẫu (nếu có)
    test_image_path = "test_image.jpg"
    if os.path.exists(test_image_path):
        result = processor.process_image(test_image_path, "processed_test.jpg")
        if result is not None:
            print("Xử lý ảnh thành công!")
        else:
            print("Lỗi trong quá trình xử lý ảnh!")
    else:
        print("Không tìm thấy ảnh test!")


if __name__ == "__main__":
    test_image_processor()
