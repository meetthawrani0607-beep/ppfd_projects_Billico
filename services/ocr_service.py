"""
OCR Service
Extract text from images using Tesseract OCR
"""
import pytesseract
import cv2
import os
from PIL import Image
from services.image_service import ImageService


class OCRService:
    """Service for OCR text extraction"""
    
    def __init__(self, tesseract_path=None):
        """Initialize OCR service"""
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def extract_text(self, image_path, preprocess=True, lang='eng'):
        """
        Extract text from image using Tesseract OCR
        
        Args:
            image_path: Path to the image file
            preprocess: Whether to preprocess image
            lang: Language for OCR (default: 'eng')
            
        Returns:
            Dictionary with 'text' and 'confidence'
        """
        try:
            if preprocess:
                # Preprocess image for better OCR
                processed_image = ImageService.preprocess_for_ocr(image_path)
                
                if processed_image is None:
                    # Fallback to original image
                    text = pytesseract.image_to_string(
                        Image.open(image_path),
                        lang=lang
                    )
                    data = pytesseract.image_to_data(
                        Image.open(image_path),
                        lang=lang,
                        output_type=pytesseract.Output.DICT
                    )
                else:
                    # Use preprocessed image
                    text = pytesseract.image_to_string(
                        processed_image,
                        lang=lang
                    )
                    data = pytesseract.image_to_data(
                        processed_image,
                        lang=lang,
                        output_type=pytesseract.Output.DICT
                    )
            else:
                # Use original image
                text = pytesseract.image_to_string(
                    Image.open(image_path),
                    lang=lang
                )
                data = pytesseract.image_to_data(
                    Image.open(image_path),
                    lang=lang,
                    output_type=pytesseract.Output.DICT
                )
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'text': text.strip(),
                'confidence': round(avg_confidence, 2),
                'success': True
            }
            
        except Exception as e:
            print(f"OCR Error: {str(e)}")
            return {
                'text': '',
                'confidence': 0,
                'success': False,
                'error': str(e)
            }
    
    def extract_with_boxes(self, image_path, preprocess=True, lang='eng'):
        """
        Extract text with bounding box information
        
        Args:
            image_path: Path to the image file
            preprocess: Whether to preprocess image
            lang: Language for OCR
            
        Returns:
            List of dictionaries with text, confidence, and coordinates
        """
        try:
            if preprocess:
                processed_image = ImageService.preprocess_for_ocr(image_path)
                if processed_image is None:
                    img = Image.open(image_path)
                else:
                    img = processed_image
            else:
                img = Image.open(image_path)
            
            # Get detailed data
            data = pytesseract.image_to_data(
                img,
                lang=lang,
                output_type=pytesseract.Output.DICT
            )
            
            # Parse results
            results = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                if int(data['conf'][i]) > 30:  # Only include if confidence > 30%
                    results.append({
                        'text': data['text'][i],
                        'confidence': int(data['conf'][i]),
                        'left': data['left'][i],
                        'top': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i],
                        'level': data['level'][i]
                    })
            
            return results
            
        except Exception as e:
            print(f"OCR Box Error: {str(e)}")
            return []
    
    def extract_lines(self, image_path, preprocess=True, lang='eng'):
        """
        Extract text line by line
        
        Args:
            image_path: Path to the image file
            preprocess: Whether to preprocess image
            lang: Language for OCR
            
        Returns:
            List of text lines
        """
        try:
            result = self.extract_text(image_path, preprocess, lang)
            if result['success']:
                lines = [line.strip() for line in result['text'].split('\n') if line.strip()]
                return lines
            return []
            
        except Exception as e:
            print(f"Line Extraction Error: {str(e)}")
            return []
    
    def is_tesseract_available(self):
        """
        Check if Tesseract is properly installed and accessible
        
        Returns:
            Boolean indicating availability
        """
        try:
            version = pytesseract.get_tesseract_version()
            return True
        except Exception as e:
            print(f"Tesseract not available: {str(e)}")
            return False
    
    def get_supported_languages(self):
        """
        Get list of supported languages
        
        Returns:
            List of language codes
        """
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception as e:
            print(f"Error getting languages: {str(e)}")
            return ['eng']  # Default to English
