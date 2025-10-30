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
    
    def detect_inverted_text(self, binary_image):
        """
        Detect if text is inverted (light text on dark background).
        
        Args:
            binary_image (numpy.ndarray): Binary thresholded image
            
        Returns:
            bool: True if text appears to be inverted, False otherwise
        """
        # Calculate the ratio of white pixels to total pixels
        total_pixels = binary_image.size
        white_pixels = np.sum(binary_image == 255)
        white_ratio = white_pixels / total_pixels
        
        # If more than 50% of pixels are white (dark text on light background),
        # the image is likely NOT inverted
        # If less than 50%, the text is likely inverted
        is_inverted = white_ratio < 0.5
        
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
    
    def enhance_contrast(self, image):
        """
        Enhance image contrast using histogram equalization.
        
        Args:
            image (numpy.ndarray): Input grayscale image
            
        Returns:
            numpy.ndarray: Contrast-enhanced image
        """
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
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
    
    def process_image(self, image_path, apply_deskew=False):
        """
        Complete image processing pipeline for OCR optimization.
        
        Args:
            image_path (str): Path to the input image
            apply_deskew (bool): Whether to apply deskewing
            
        Returns:
            numpy.ndarray: Processed image ready for OCR
        """
        # Step 1: Load image
        image = self.load_image(image_path)
        
        # Step 2: Convert to grayscale
        gray = self.convert_to_grayscale(image)
        
        # Step 3: Enhance contrast
        enhanced = self.enhance_contrast(gray)
        
        # Step 4: Reduce noise
        denoised = self.reduce_noise(enhanced, method='bilateral')
        
        # Step 5: Apply adaptive thresholding
        binary = self.apply_adaptive_threshold(denoised, block_size=11, C=2)
        
        # Step 6: Detect and handle inverted text
        if self.detect_inverted_text(binary):
            binary = self.invert_image(binary)
        
        # Step 7: Optional deskewing
        if apply_deskew:
            binary = self.deskew_image(binary)
        
        # Store processed image
        self.processed_image = binary
        
        return binary
    
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

