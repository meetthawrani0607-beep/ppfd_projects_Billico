"""
Image Service
Image preprocessing and enhancement for OCR
"""
import cv2
import numpy as np
from PIL import Image
import io
import os


class ImageService:
    """Service for image preprocessing and enhancement"""
    
    @staticmethod
    def preprocess_for_ocr(image_path):
        """
        Preprocess image for better OCR results
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            
            if img is None:
                raise ValueError("Could not read image")
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                denoised, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 
                11, 2
            )
            
            # Deskew if needed
            processed = ImageService._deskew(thresh)
            
            # Remove borders
            processed = ImageService._remove_borders(processed)
            
            return processed
            
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            # Return original grayscale if preprocessing fails
            img = cv2.imread(image_path)
            if img is not None:
                return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return None
    
    @staticmethod
    def _deskew(image):
        """Deskew image to correct rotation"""
        coords = np.column_stack(np.where(image > 0))
        if len(coords) == 0:
            return image
            
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # Only deskew if angle is significant
        if abs(angle) > 0.5:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(
                image, M, (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )
            return rotated
        
        return image
    
    @staticmethod
    def _remove_borders(image):
        """Remove black borders from image"""
        # Find all non-zero points
        coords = cv2.findNonZero(image)
        if coords is None:
            return image
            
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(coords)
        
        # Crop to bounding rectangle
        cropped = image[y:y+h, x:x+w]
        return cropped
    
    @staticmethod
    def resize_image(image_path, max_width=2000, max_height=2000):
        """
        Resize image if it's too large
        
        Args:
            image_path: Path to the image
            max_width: Maximum width
            max_height: Maximum height
            
        Returns:
            True if successful
        """
        try:
            with Image.open(image_path) as img:
                # Get current dimensions
                width, height = img.size
                
                # Check if resize is needed
                if width <= max_width and height <= max_height:
                    return True
                
                # Calculate new dimensions maintaining aspect ratio
                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                
                # Resize
                resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save
                resized.save(image_path, quality=95, optimize=True)
                
                return True
                
        except Exception as e:
            print(f"Error resizing image: {str(e)}")
            return False
    
    @staticmethod
    def enhance_image(image_path):
        """
        Enhance image contrast and sharpness
        
        Args:
            image_path: Path to the image
            
        Returns:
            True if successful
        """
        try:
            from PIL import ImageEnhance
            
            with Image.open(image_path) as img:
                # Enhance contrast
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.5)
                
                # Enhance sharpness
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.3)
                
                # Save
                img.save(image_path, quality=95)
                
                return True
                
        except Exception as e:
            print(f"Error enhancing image: {str(e)}")
            return False
    
    @staticmethod
    def convert_to_binary(image_path):
        """
        Convert image to binary (black and white)
        
        Args:
            image_path: Path to the image
            
        Returns:
            Binary image as numpy array
        """
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            if img is None:
                return None
            
            # Apply Otsu's thresholding
            _, binary = cv2.threshold(
                img, 0, 255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
            
            return binary
            
        except Exception as e:
            print(f"Error converting to binary: {str(e)}")
            return None
    
    @staticmethod
    def save_preprocessed(image_array, output_path):
        """
        Save preprocessed image array to file
        
        Args:
            image_array: Numpy array of image
            output_path: Path to save image
            
        Returns:
            True if successful
        """
        try:
            cv2.imwrite(output_path, image_array)
            return True
        except Exception as e:
            print(f"Error saving preprocessed image: {str(e)}")
            return False
