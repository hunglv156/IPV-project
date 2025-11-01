"""
OCR Engine Module for VisionSpeak
Handles Optical Character Recognition using Tesseract OCR.
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np


class OCREngine:
    """
    OCR Engine wrapper for Tesseract OCR with optimized configurations.
    """
    
    def __init__(self, tesseract_path=None):
        """
        Initialize the OCR engine.
        
        Args:
            tesseract_path (str, optional): Path to Tesseract executable
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        self.last_recognized_text = ""
        self.confidence_scores = []
    
    def recognize_text(self, image, psm=6, lang='eng', config='', oem=3):
        """
        Perform OCR on the given image with optimized configuration.
        
        Args:
            image: Input image (PIL Image, numpy array, or file path)
            psm (int): Page Segmentation Mode for Tesseract
                       6 = Assume a single uniform block of text (default)
                       3 = Fully automatic page segmentation
                       11 = Sparse text. Find as much text as possible
            lang (str): Language for OCR (default: 'eng')
            config (str): Additional Tesseract configuration
            oem (int): OCR Engine Mode (0=Legacy, 1=LSTM, 2=Legacy+LSTM, 3=Default)
            
        Returns:
            str: Recognized text
        """
        # Convert input to PIL Image if necessary
        if isinstance(image, str):
            # File path
            pil_image = Image.open(image)
        elif isinstance(image, np.ndarray):
            # Numpy array (OpenCV image)
            if len(image.shape) == 2:
                # Grayscale
                pil_image = Image.fromarray(image)
            else:
                # Color image (BGR to RGB)
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        elif isinstance(image, Image.Image):
            # Already a PIL Image
            pil_image = image
        else:
            raise ValueError("Unsupported image type")
        
        # Build optimized configuration
        # OEM 3 = Default (best available engine)
        # OEM 1 = LSTM only (neural network, usually best for modern text)
        custom_config = f'--oem {oem} --psm {psm}'
        if config:
            custom_config += f' {config}'
        
        # Perform OCR
        try:
            text = pytesseract.image_to_string(
                pil_image,
                lang=lang,
                config=custom_config
            )
            self.last_recognized_text = text.strip()
            return self.last_recognized_text
        except Exception as e:
            raise RuntimeError(f"OCR failed: {str(e)}")
    
    def recognize_text_with_confidence(self, image, psm=6, lang='eng'):
        """
        Perform OCR and get confidence scores for each word.
        
        Args:
            image: Input image (PIL Image, numpy array, or file path)
            psm (int): Page Segmentation Mode for Tesseract
            lang (str): Language for OCR
            
        Returns:
            tuple: (recognized_text, data_dict)
                   data_dict contains detailed OCR results including confidence
        """
        # Convert input to PIL Image if necessary
        if isinstance(image, str):
            pil_image = Image.open(image)
        elif isinstance(image, np.ndarray):
            if len(image.shape) == 2:
                pil_image = Image.fromarray(image)
            else:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        elif isinstance(image, Image.Image):
            pil_image = image
        else:
            raise ValueError("Unsupported image type")
        
        # Build custom configuration
        custom_config = f'--psm {psm}'
        
        # Get detailed OCR data
        try:
            data = pytesseract.image_to_data(
                pil_image,
                lang=lang,
                config=custom_config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text and confidence scores
            text_parts = []
            confidences = []
            
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 0:  # Valid confidence
                    text_parts.append(data['text'][i])
                    confidences.append(int(data['conf'][i]))
            
            text = ' '.join(text_parts)
            self.last_recognized_text = text.strip()
            self.confidence_scores = confidences
            
            return self.last_recognized_text, data
        except Exception as e:
            raise RuntimeError(f"OCR with confidence failed: {str(e)}")
    
    def get_average_confidence(self):
        """
        Get the average confidence score from the last OCR operation.
        
        Returns:
            float: Average confidence (0-100), or 0 if no scores available
        """
        if not self.confidence_scores:
            return 0.0
        return sum(self.confidence_scores) / len(self.confidence_scores)
    
    def recognize_with_multiple_psm(self, image, lang='eng'):
        """
        Try multiple PSM modes and return the result with highest confidence.
        This is SLOWER but more accurate for difficult images.
        
        Args:
            image: Input image (PIL Image, numpy array, or file path)
            lang (str): Language for OCR
            
        Returns:
            dict: Best OCR result with text, psm mode, and confidence
        """
        # PSM modes to try (in order of preference)
        # 6 = Uniform block of text (most common)
        # 3 = Fully automatic (good for complex layouts)
        # 11 = Sparse text (good for few words)
        # 4 = Single column of text
        psm_modes = [6, 3, 11, 4]
        
        best_result = {
            'text': '',
            'psm': 6,
            'confidence': 0.0
        }
        
        for psm in psm_modes:
            try:
                text, _ = self.recognize_text_with_confidence(image, psm=psm, lang=lang)
                confidence = self.get_average_confidence()
                
                if confidence > best_result['confidence']:
                    best_result['text'] = text
                    best_result['psm'] = psm
                    best_result['confidence'] = confidence
                
                # If confidence is very high, no need to try other modes
                if confidence > 90:
                    break
            except Exception:
                continue
        
        return best_result
    
    def recognize_optimized(self, image, lang='eng', auto_psm=False):
        """
        Optimized OCR with best practices applied.
        
        Args:
            image: Input image (PIL Image, numpy array, or file path)
            lang (str): Language for OCR
            auto_psm (bool): Automatically try multiple PSM modes (slower but more accurate)
            
        Returns:
            str: Recognized text with best configuration
        """
        if auto_psm:
            # Try multiple PSM modes and return best result
            result = self.recognize_with_multiple_psm(image, lang=lang)
            return result['text']
        else:
            # Use optimized default: OEM 1 (LSTM only) for best accuracy
            return self.recognize_text(image, psm=6, lang=lang, oem=1)
    
    def get_supported_languages(self):
        """
        Get list of languages supported by installed Tesseract.
        
        Returns:
            list: List of language codes
        """
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception as e:
            return ['eng']  # Default to English if detection fails
    
    def check_tesseract_installed(self):
        """
        Check if Tesseract is properly installed and accessible.
        
        Returns:
            bool: True if Tesseract is installed, False otherwise
        """
        try:
            version = pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False
    
    def get_tesseract_version(self):
        """
        Get the version of installed Tesseract OCR.
        
        Returns:
            str: Tesseract version string
        """
        try:
            version = pytesseract.get_tesseract_version()
            return str(version)
        except Exception as e:
            return f"Error: {str(e)}"

