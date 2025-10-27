"""
Module OCR Engine cho VisionSpeak
Sử dụng Pytesseract với các cấu hình tối ưu cho nhận dạng văn bản
"""

import pytesseract
import cv2
import numpy as np
from PIL import Image
import os
import re


class OCREngine:
    """
    Lớp xử lý OCR với các cấu hình tối ưu cho Tesseract
    """
    
    def __init__(self, tesseract_path=None):
        """
        Khởi tạo OCR Engine
        
        Args:
            tesseract_path (str): Đường dẫn đến tesseract executable (Windows)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Cấu hình mặc định cho Tesseract
        self.default_config = '--oem 3 --psm 6'
        
        # Các cấu hình PSM khác nhau cho các loại văn bản
        self.psm_configs = {
            'single_text_block': '--psm 6',      # Khối văn bản đơn nhất
            'single_text_line': '--psm 7',       # Dòng văn bản đơn
            'single_word': '--psm 8',            # Từ đơn
            'single_character': '--psm 10',      # Ký tự đơn
            'sparse_text': '--psm 11',           # Văn bản thưa thớt
            'orientation_detection': '--psm 0',  # Phát hiện hướng
            'automatic': '--psm 3'               # Tự động phát hiện
        }
        
        # Ngôn ngữ hỗ trợ
        self.supported_languages = {
            'vi': 'vie',  # Tiếng Việt
            'en': 'eng',  # Tiếng Anh
            'vi_en': 'vie+eng'  # Hỗn hợp Việt-Anh
        }
    
    def set_tesseract_path(self, path):
        """
        Thiết lập đường dẫn đến Tesseract executable
        
        Args:
            path (str): Đường dẫn đến tesseract.exe
        """
        pytesseract.pytesseract.tesseract_cmd = path
    
    def detect_text_orientation(self, image):
        """
        Phát hiện hướng của văn bản trong ảnh
        
        Args:
            image (numpy.ndarray): Ảnh đã được xử lý
            
        Returns:
            dict: Thông tin về hướng văn bản
        """
        try:
            # Sử dụng PSM 0 để phát hiện hướng
            osd = pytesseract.image_to_osd(image, config='--psm 0')
            
            # Parse kết quả OSD
            orientation_info = {}
            for line in osd.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    orientation_info[key.strip()] = value.strip()
            
            return orientation_info
        except Exception as e:
            print(f"Lỗi khi phát hiện hướng văn bản: {e}")
            return {}
    
    def rotate_image_if_needed(self, image, orientation_info):
        """
        Xoay ảnh nếu văn bản bị nghiêng
        
        Args:
            image (numpy.ndarray): Ảnh đầu vào
            orientation_info (dict): Thông tin hướng văn bản
            
        Returns:
            numpy.ndarray: Ảnh đã được xoay (nếu cần)
        """
        try:
            if 'Orientation' in orientation_info:
                orientation = int(orientation_info['Orientation'])
                
                # Xoay ảnh dựa trên góc nghiêng
                if orientation == 90:
                    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                elif orientation == 180:
                    image = cv2.rotate(image, cv2.ROTATE_180)
                elif orientation == 270:
                    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    
        except Exception as e:
            print(f"Lỗi khi xoay ảnh: {e}")
            
        return image
    
    def extract_text_with_config(self, image, config='--psm 6', language='vie+eng'):
        """
        Trích xuất văn bản với cấu hình cụ thể
        
        Args:
            image (numpy.ndarray): Ảnh đã được xử lý
            config (str): Cấu hình Tesseract
            language (str): Ngôn ngữ nhận dạng
            
        Returns:
            str: Văn bản đã được nhận dạng
        """
        try:
            # Chuyển đổi numpy array sang PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                pil_image = Image.fromarray(image)
            
            # Thực hiện OCR
            text = pytesseract.image_to_string(
                pil_image, 
                lang=language, 
                config=config
            )
            
            return text.strip()
            
        except Exception as e:
            print(f"Lỗi khi trích xuất văn bản: {e}")
            return ""
    
    def extract_text_multiple_configs(self, image, language='vie+eng'):
        """
        Thử nhiều cấu hình khác nhau để có kết quả tốt nhất
        
        Args:
            image (numpy.ndarray): Ảnh đã được xử lý
            language (str): Ngôn ngữ nhận dạng
            
        Returns:
            dict: Kết quả từ các cấu hình khác nhau
        """
        results = {}
        
        for config_name, config in self.psm_configs.items():
            try:
                text = self.extract_text_with_config(image, config, language)
                results[config_name] = text
            except Exception as e:
                print(f"Lỗi với cấu hình {config_name}: {e}")
                results[config_name] = ""
        
        return results
    
    def choose_best_result(self, results):
        """
        Chọn kết quả tốt nhất từ các cấu hình khác nhau
        
        Args:
            results (dict): Kết quả từ các cấu hình
            
        Returns:
            tuple: (text, config_name) - văn bản tốt nhất và cấu hình được sử dụng
        """
        best_text = ""
        best_config = ""
        max_length = 0
        
        for config_name, text in results.items():
            # Loại bỏ các ký tự không phải chữ cái/số
            clean_text = re.sub(r'[^\w\s]', '', text)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            
            # Chọn kết quả có độ dài hợp lý và chứa nhiều từ nhất
            if len(clean_text) > max_length and len(clean_text.split()) > 0:
                max_length = len(clean_text)
                best_text = clean_text
                best_config = config_name
        
        return best_text, best_config
    
    def post_process_text(self, text):
        """
        Hậu xử lý văn bản để cải thiện chất lượng
        
        Args:
            text (str): Văn bản thô từ OCR
            
        Returns:
            str: Văn bản đã được làm sạch
        """
        if not text:
            return ""
        
        # Loại bỏ các ký tự đặc biệt không cần thiết
        text = re.sub(r'[^\w\s.,!?;:()-]', '', text)
        
        # Chuẩn hóa khoảng trắng
        text = re.sub(r'\s+', ' ', text)
        
        # Loại bỏ các dòng trống
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Ghép lại thành đoạn văn
        processed_text = '\n'.join(lines)
        
        return processed_text.strip()
    
    def extract_text_from_image(self, image_path, language='vie+eng', auto_rotate=True):
        """
        Trích xuất văn bản từ file ảnh với pipeline hoàn chỉnh
        
        Args:
            image_path (str): Đường dẫn đến file ảnh
            language (str): Ngôn ngữ nhận dạng
            auto_rotate (bool): Tự động xoay ảnh nếu cần
            
        Returns:
            dict: Kết quả OCR với thông tin chi tiết
        """
        try:
            # Tải ảnh
            image = cv2.imread(image_path)
            if image is None:
                return {
                    'success': False,
                    'text': '',
                    'error': f'Không thể tải ảnh từ {image_path}'
                }
            
            # Phát hiện hướng văn bản nếu cần
            orientation_info = {}
            if auto_rotate:
                orientation_info = self.detect_text_orientation(image)
                image = self.rotate_image_if_needed(image, orientation_info)
            
            # Thử nhiều cấu hình
            results = self.extract_text_multiple_configs(image, language)
            
            # Chọn kết quả tốt nhất
            best_text, best_config = self.choose_best_result(results)
            
            # Hậu xử lý văn bản
            processed_text = self.post_process_text(best_text)
            
            return {
                'success': True,
                'text': processed_text,
                'raw_text': best_text,
                'config_used': best_config,
                'orientation_info': orientation_info,
                'all_results': results
            }
            
        except Exception as e:
            return {
                'success': False,
                'text': '',
                'error': f'Lỗi trong quá trình OCR: {e}'
            }
    
    def extract_text_from_array(self, image_array, language='vie+eng', auto_rotate=True):
        """
        Trích xuất văn bản từ numpy array (cho camera)
        
        Args:
            image_array (numpy.ndarray): Ảnh dạng numpy array
            language (str): Ngôn ngữ nhận dạng
            auto_rotate (bool): Tự động xoay ảnh nếu cần
            
        Returns:
            dict: Kết quả OCR với thông tin chi tiết
        """
        try:
            # Phát hiện hướng văn bản nếu cần
            orientation_info = {}
            if auto_rotate:
                orientation_info = self.detect_text_orientation(image_array)
                image_array = self.rotate_image_if_needed(image_array, orientation_info)
            
            # Thử nhiều cấu hình
            results = self.extract_text_multiple_configs(image_array, language)
            
            # Chọn kết quả tốt nhất
            best_text, best_config = self.choose_best_result(results)
            
            # Hậu xử lý văn bản
            processed_text = self.post_process_text(best_text)
            
            return {
                'success': True,
                'text': processed_text,
                'raw_text': best_text,
                'config_used': best_config,
                'orientation_info': orientation_info,
                'all_results': results
            }
            
        except Exception as e:
            return {
                'success': False,
                'text': '',
                'error': f'Lỗi trong quá trình OCR: {e}'
            }
    
    def get_confidence_score(self, image, text, language='vie+eng'):
        """
        Tính điểm tin cậy của kết quả OCR
        
        Args:
            image (numpy.ndarray): Ảnh đã được xử lý
            text (str): Văn bản đã nhận dạng
            language (str): Ngôn ngữ nhận dạng
            
        Returns:
            float: Điểm tin cậy (0-100)
        """
        try:
            # Chuyển đổi sang PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                pil_image = Image.fromarray(image)
            
            # Lấy thông tin chi tiết từ Tesseract
            data = pytesseract.image_to_data(
                pil_image, 
                lang=language, 
                config='--psm 6',
                output_type=pytesseract.Output.DICT
            )
            
            # Tính điểm tin cậy trung bình
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            if confidences:
                avg_confidence = sum(confidences) / len(confidences)
                return avg_confidence
            
            return 0.0
            
        except Exception as e:
            print(f"Lỗi khi tính điểm tin cậy: {e}")
            return 0.0


def test_ocr_engine():
    """Hàm test cho OCREngine"""
    ocr = OCREngine()
    
    # Test với ảnh mẫu (nếu có)
    test_image_path = "test_image.jpg"
    if os.path.exists(test_image_path):
        result = ocr.extract_text_from_image(test_image_path)
        if result['success']:
            print("OCR thành công!")
            print(f"Văn bản: {result['text']}")
            print(f"Cấu hình sử dụng: {result['config_used']}")
        else:
            print(f"Lỗi OCR: {result['error']}")
    else:
        print("Không tìm thấy ảnh test!")


if __name__ == "__main__":
    test_ocr_engine()
