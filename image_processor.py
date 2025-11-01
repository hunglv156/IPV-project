"""
Image Processor Module for VisionSpeak
Handles advanced image pre-processing including noise reduction, 
adaptive thresholding, and automatic inversion detection.
"""

import cv2
import numpy as np
from PIL import Image


class ImageProcessor:
    """
    Advanced image processor for OCR pre-processing.
    Handles various image quality issues including noise, blur, 
    uneven lighting, and inverted text.
    """
    
    def __init__(self):
        """Initialize the image processor."""
        self.original_image = None
        self.processed_image = None
        self.grayscale_image = None
        
    def load_image(self, image_path):
        """
        Load an image from file path.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            numpy.ndarray: Loaded image in BGR format
        """
        self.original_image = cv2.imread(image_path)
        if self.original_image is None:
            raise ValueError(f"Could not load image from {image_path}")
        return self.original_image
    
    def convert_to_grayscale(self, image):
        """
        Convert image to grayscale.
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Grayscale image
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        self.grayscale_image = gray
        return gray
    
    def reduce_noise(self, image, method='bilateral'):
        """
        Apply noise reduction to the image.
        
        Args:
            image (numpy.ndarray): Input grayscale image
            method (str): Noise reduction method ('bilateral', 'gaussian', 'median')
            
        Returns:
            numpy.ndarray: Denoised image
        """
        if method == 'bilateral':
            # Bilateral filter preserves edges while reducing noise
            denoised = cv2.bilateralFilter(image, 9, 75, 75)
        elif method == 'gaussian':
            # Gaussian blur for general noise reduction
            denoised = cv2.GaussianBlur(image, (5, 5), 0)
        elif method == 'median':
            # Median blur effective for salt-and-pepper noise
            denoised = cv2.medianBlur(image, 5)
        else:
            denoised = image
        
        return denoised
    
    def apply_adaptive_threshold(self, image, block_size=11, C=2):
        """
        Apply adaptive thresholding to handle uneven lighting.
        
        Args:
            image (numpy.ndarray): Input grayscale image
            block_size (int): Size of pixel neighborhood (must be odd)
            C (int): Constant subtracted from weighted mean
            
        Returns:
            numpy.ndarray: Binary thresholded image
        """
        # Ensure block_size is odd
        if block_size % 2 == 0:
            block_size += 1
        
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size,
            C
        )
        
        return binary
    
    def detect_inverted_text(self, image):
        """
        Detect if text is inverted (light text on dark background).
        Should be called on GRAYSCALE image, not binary.
        
        Args:
            image (numpy.ndarray): Grayscale or binary image
            
        Returns:
            bool: True if text appears to be inverted, False otherwise
        """
        # Calculate mean brightness
        mean_brightness = np.mean(image)
        
        # If mean brightness < 127 (darker image), likely inverted
        # Dark background with light text = low mean brightness
        is_inverted = mean_brightness < 127
        
        return is_inverted
    
    def invert_image(self, image):
        """
        Invert image colors (bitwise NOT operation).
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Inverted image
        """
        return cv2.bitwise_not(image)
    
    def enhance_contrast(self, image, strength='normal'):
        """
        Enhance image contrast using histogram equalization.
        
        Args:
            image (numpy.ndarray): Input grayscale image
            strength (str): 'normal' or 'strong' for very dark images
            
        Returns:
            numpy.ndarray: Contrast-enhanced image
        """
        if strength == 'strong':
            # Stronger enhancement for very dark images
            clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
            enhanced = clahe.apply(image)
            
            # Additional brightness adjustment for dark images
            mean_brightness = np.mean(enhanced)
            if mean_brightness < 100:
                # Boost brightness
                alpha = 1.3  # Contrast
                beta = 30   # Brightness
                enhanced = cv2.convertScaleAbs(enhanced, alpha=alpha, beta=beta)
        else:
            # Normal CLAHE
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(image)
        
        return enhanced
    
    def deskew_image(self, image):
        """
        Detect and correct skew in the image.
        
        Args:
            image (numpy.ndarray): Input binary image
            
        Returns:
            numpy.ndarray: Deskewed image
        """
        # Find all non-zero points (text pixels)
        coords = np.column_stack(np.where(image > 0))
        
        if len(coords) < 5:
            # Not enough points to determine skew
            return image
        
        # Calculate the angle of skew
        angle = cv2.minAreaRect(coords)[-1]
        
        # Normalize the angle
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # Only deskew if angle is significant (more than 0.5 degrees)
        if abs(angle) < 0.5:
            return image
        
        # Rotate the image to deskew
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image,
            M,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated
    
    def remove_borders(self, image, border_size=10):
        """
        Remove borders from the image.
        
        Args:
            image (numpy.ndarray): Input image
            border_size (int): Size of border to remove (pixels)
            
        Returns:
            numpy.ndarray: Image with borders removed
        """
        h, w = image.shape[:2]
        if h <= 2 * border_size or w <= 2 * border_size:
            return image
        
        return image[border_size:h-border_size, border_size:w-border_size]
    
    def upscale_image(self, image, target_dpi=300):
        """
        Upscale image to optimal DPI for OCR (Tesseract works best at ~300 DPI).
        
        Args:
            image (numpy.ndarray): Input image
            target_dpi (int): Target DPI (default 300)
            
        Returns:
            numpy.ndarray: Upscaled image
        """
        height, width = image.shape[:2]
        
        # Estimate current DPI (assume 72 DPI if unknown)
        estimated_dpi = 72
        
        # Calculate scale factor
        scale_factor = target_dpi / estimated_dpi
        
        # Only upscale if image is small (< 1000px width)
        if width < 1000 and scale_factor > 1:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            # Use INTER_CUBIC for upscaling (better quality)
            upscaled = cv2.resize(image, (new_width, new_height), 
                                 interpolation=cv2.INTER_CUBIC)
            return upscaled
        
        return image
    
    def sharpen_image(self, image, strength='normal'):
        """
        Sharpen image to enhance text edges.
        
        Args:
            image (numpy.ndarray): Input grayscale image
            strength (str): 'normal' or 'strong' for very blurry images
            
        Returns:
            numpy.ndarray: Sharpened image
        """
        if strength == 'strong':
            # Stronger sharpening for very blurry images
            kernel = np.array([[-1, -1, -1, -1, -1],
                              [-1,  2,  2,  2, -1],
                              [-1,  2,  8,  2, -1],
                              [-1,  2,  2,  2, -1],
                              [-1, -1, -1, -1, -1]]) / 8
        else:
            # Normal sharpening kernel
            kernel = np.array([[-1, -1, -1],
                              [-1,  9, -1],
                              [-1, -1, -1]])
        
        sharpened = cv2.filter2D(image, -1, kernel)
        
        # Prevent over-sharpening artifacts
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        
        return sharpened
    
    def detect_blur(self, image):
        """
        Detect if image is blurry using Laplacian variance.
        
        Args:
            image (numpy.ndarray): Grayscale image
            
        Returns:
            float: Blur score (lower = more blurry, < 100 = blurry)
        """
        laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
        return laplacian_var
    
    def remove_small_noise(self, binary_image):
        """
        Remove small noise particles using morphological operations.
        
        Args:
            binary_image (numpy.ndarray): Input binary image
            
        Returns:
            numpy.ndarray: Cleaned binary image
        """
        # Remove small white noise (opening)
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
        
        # Close small gaps in text (closing)
        kernel2 = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel2)
        
        return cleaned
    
    def process_image(self, image_path, apply_deskew='auto'):
        """
        Complete image processing pipeline for OCR optimization.
        
        Args:
            image_path (str): Path to the input image
            apply_deskew (str/bool): 'auto' for automatic detection, True/False for manual
            
        Returns:
            numpy.ndarray: Processed image ready for OCR
        """
        # Step 1: Load image
        image = self.load_image(image_path)
        
        # Step 2: Convert to grayscale
        gray = self.convert_to_grayscale(image)
        
        # Step 3: DETECT INVERTED EARLY (on grayscale, before processing)
        is_inverted = self.detect_inverted_text(gray)
        
        # Step 3b: If inverted, invert the grayscale image FIRST
        if is_inverted:
            gray = self.invert_image(gray)
        
        # Step 4: Detect if image is dark
        mean_brightness = np.mean(gray)
        is_dark = mean_brightness < 90
        
        # Step 5: Upscale if image is too small (IMPORTANT for OCR accuracy)
        upscaled = self.upscale_image(gray, target_dpi=300)
        
        # Step 6: Detect blur level
        blur_score = self.detect_blur(upscaled)
        is_blurry = blur_score < 100
        
        # Step 7: Detect noise level
        noise_level = self._estimate_noise(upscaled)
        is_noisy = noise_level > 15
        
        # Step 8: Adaptive denoising based on noise level
        if noise_level > 25:  # Very high noise
            # Triple filtering for extremely noisy images
            denoised1 = cv2.fastNlMeansDenoising(upscaled, h=10)
            denoised2 = cv2.medianBlur(denoised1, 5)
            denoised = cv2.bilateralFilter(denoised2, 9, 75, 75)
        elif noise_level > 15:  # High noise
            # Double filtering for noisy images
            denoised1 = cv2.medianBlur(upscaled, 5)
            denoised = cv2.bilateralFilter(denoised1, 9, 75, 75)
        else:
            # Normal bilateral filter for clean images
            denoised = self.reduce_noise(upscaled, method='bilateral')
        
        # Step 9: Adaptive contrast enhancement
        if is_dark:
            enhanced = self.enhance_contrast(denoised, strength='strong')
        else:
            enhanced = self.enhance_contrast(denoised, strength='normal')
        
        # Step 10: Adaptive sharpening based on blur and noise
        if is_blurry and not is_noisy:
            # Strong sharpening for blurry images
            sharpened = self.sharpen_image(enhanced, strength='strong')
        elif not is_noisy:
            # Normal sharpening for clean images
            sharpened = self.sharpen_image(enhanced, strength='normal')
        else:
            # Skip sharpening for very noisy images
            sharpened = enhanced
        
        # Step 11: Apply adaptive thresholding with dynamic block size
        # Calculate block size based on image size (larger image = larger block)
        height, width = sharpened.shape
        block_size = max(11, min(31, int(width / 50)))
        if block_size % 2 == 0:
            block_size += 1  # Ensure odd
        
        binary = self.apply_adaptive_threshold(sharpened, block_size=block_size, C=2)
        
        # Step 12: Remove small noise particles
        cleaned = self.remove_small_noise(binary)
        
        # Step 13: Optional deskewing
        # Note: Auto-deskew is disabled by default as it can make things worse
        # Only apply if user explicitly requests
        if apply_deskew == True:
            # Force deskew
            cleaned = self.deskew_image(cleaned)
        # 'auto' and False both skip deskewing
        
        # Store processed image
        self.processed_image = cleaned
        
        return cleaned
    
    def _estimate_noise(self, image):
        """
        Estimate noise level in grayscale image using Laplacian variance.
        
        Args:
            image (numpy.ndarray): Grayscale image
            
        Returns:
            float: Noise level estimate (higher = more noisy)
        """
        # Use Laplacian to detect edges/noise
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        variance = laplacian.var()
        
        # Normalize to 0-100 range (approximate)
        noise_level = min(100, variance / 10)
        
        return noise_level
    
    def get_processed_image_pil(self):
        """
        Get the processed image as a PIL Image object.
        
        Returns:
            PIL.Image: Processed image
        """
        if self.processed_image is None:
            return None
        return Image.fromarray(self.processed_image)
    
    def get_original_image_pil(self):
        """
        Get the original image as a PIL Image object.
        
        Returns:
            PIL.Image: Original image
        """
        if self.original_image is None:
            return None
        # Convert BGR to RGB for PIL
        rgb_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_image)
    
    def save_processed_image(self, output_path):
        """
        Save the processed image to file.
        
        Args:
            output_path (str): Path to save the processed image
        """
        if self.processed_image is not None:
            cv2.imwrite(output_path, self.processed_image)
        else:
            raise ValueError("No processed image to save. Process an image first.")

