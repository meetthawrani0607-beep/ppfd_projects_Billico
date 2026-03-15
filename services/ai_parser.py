"""
AI Parser Service
Intelligent parsing of OCR text to extract structured inventory data
"""
import re
from datetime import datetime
from dateutil import parser as date_parser


class AIParser:
    """AI-powered parser for converting OCR text to structured data"""
    
    # Common item indicators
    ITEM_INDICATORS = ['item', 'product', 'description', 'particulars', 'goods']
    
    # Quantity indicators
    QTY_INDICATORS = ['qty', 'quantity', 'nos', 'pcs', 'units', 'count']
    
    # Price indicators
    PRICE_INDICATORS = ['price', 'rate', 'amount', 'cost', 'value', 'rs', 'inr', '$']
    
    # Total indicators
    TOTAL_INDICATORS = ['total', 'sum', 'subtotal', 'grand total', 'net amount']
    
    def __init__(self):
        """Initialize parser"""
        pass
    
    def parse_bill(self, ocr_text):
        """
        Parse OCR text to extract structured bill data
        
        Args:
            ocr_text: Raw OCR-extracted text
            
        Returns:
            Dictionary with parsed data
        """
        lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
        
        result = {
            'bill_number': self._extract_bill_number(lines),
            'bill_date': self._extract_date(lines),
            'supplier_name': self._extract_supplier_name(lines),
            'items': self._extract_items(lines),
            'total_amount': self._extract_total_amount(lines),
            'raw_text': ocr_text
        }
        
        return result
    
    def _extract_bill_number(self, lines):
        """Extract bill/invoice number"""
        patterns = [
            r'bill\s*(?:no|number|#)[:\s]*([a-z0-9\-/]+)',
            r'invoice\s*(?:no|number|#)[:\s]*([a-z0-9\-/]+)',
            r'receipt\s*(?:no|number|#)[:\s]*([a-z0-9\-/]+)',
            r'ref\s*(?:no|number|#)[:\s]*([a-z0-9\-/]+)'
        ]
        
        for line in lines[:10]:  # Check first 10 lines
            line_lower = line.lower()
            for pattern in patterns:
                match = re.search(pattern, line_lower)
                if match:
                    return match.group(1).upper()
        
        return None
    
    def _extract_date(self, lines):
        """Extract bill date"""
        patterns = [
            r'date[:\s]*(.+)',
            r'dated[:\s]*(.+)',
            r'bill\s*date[:\s]*(.+)',
            r'invoice\s*date[:\s]*(.+)'
        ]
        
        for line in lines[:15]:  # Check first 15 lines
            line_lower = line.lower()
            for pattern in patterns:
                match = re.search(pattern, line_lower)
                if match:
                    date_str = match.group(1).strip()
                    try:
                        # Try to parse the date
                        parsed_date = date_parser.parse(date_str, fuzzy=True)
                        return parsed_date.date()
                    except:
                        continue
        
        # Try to find any date-like pattern
        date_patterns = [
            r'\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}',
            r'\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{2,4}'
        ]
        
        for line in lines[:20]:
            for pattern in date_patterns:
                match = re.search(pattern, line.lower())
                if match:
                    try:
                        parsed_date = date_parser.parse(match.group(0), fuzzy=True)
                        return parsed_date.date()
                    except:
                        continue
        
        return None
    
    def _extract_supplier_name(self, lines):
        """Extract supplier/vendor name"""
        # Usually the supplier name is in the first few lines
        # and is in all caps or title case
        
        skip_words = ['tax', 'invoice', 'bill', 'receipt', 'gstin', 'gst', 'phone', 'mobile']
        
        for line in lines[:8]:
            # Skip lines with skip words
            if any(word in line.lower() for word in skip_words):
                continue
            
            # Check if line looks like a company name
            if len(line) > 3 and (line.isupper() or line.istitle()):
                # Check if it doesn't look like an address
                if not re.search(r'\d{6}', line):  # No pincode
                    return line.strip()
        
        # Fallback: return first non-empty line
        if lines:
            return lines[0].strip()
        
        return None
    
    def _extract_items(self, lines):
        """Extract line items from bill"""
        items = []
        
        # Try structured parsing first
        structured_items = self._parse_structured_items(lines)
        if structured_items:
            return structured_items
        
        # Fallback: try to find items with numbers
        return self._parse_unstructured_items(lines)
    
    def _parse_structured_items(self, lines):
        """Parse items from structured table format"""
        items = []
        in_table = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if we're entering a table (header found)
            if any(indicator in line_lower for indicator in self.ITEM_INDICATORS):
                in_table = True
                continue
            
            # Check if we're exiting table
            if in_table and any(indicator in line_lower for indicator in self.TOTAL_INDICATORS):
                break
            
            # If in table, try to parse line as item
            if in_table:
                item = self._parse_item_line(line)
                if item:
                    items.append(item)
        
        return items
    
    def _parse_unstructured_items(self, lines):
        """Parse items from unstructured text"""
        items = []
        
        # Look for lines with numbers that could be quantities and prices
        for line in lines:
            # Skip very short lines
            if len(line) < 5:
                continue
            
            # Look for patterns like: "Item Name 2 100.00 200.00"
            # This regex finds: text followed by numbers
            numbers = re.findall(r'\d+\.?\d*', line)
            
            if len(numbers) >= 2:
                # Extract text (item name)
                text_part = re.sub(r'\d+\.?\d*', '', line).strip()
                text_part = re.sub(r'\s+', ' ', text_part)  # Clean whitespace
                
                if len(text_part) > 2:
                    try:
                        # Try to identify quantity and price
                        # Usually: quantity (small int), price (decimal), total (decimal)
                        qty = int(float(numbers[0]))
                        price = float(numbers[1]) if len(numbers) > 1 else 0.0
                        
                        item = {
                            'item_name': text_part,
                            'quantity': qty,
                            'unit_price': price
                        }
                        items.append(item)
                    except:
                        continue
        
        return items
    
    def _parse_item_line(self, line):
        """Parse a single item line"""
        # Try to extract: Item Name, Quantity, Price
        # Common formats:
        # "Item Name    2    100.00    200.00"
        # "Item Name | 2 | 100.00 | 200.00"
        
        # Split by multiple spaces or pipes
        parts = re.split(r'\s{2,}|\|', line.strip())
        parts = [p.strip() for p in parts if p.strip()]
        
        if len(parts) >= 3:
            try:
                # First part is likely the item name
                item_name = parts[0]
                
                # Find numbers in remaining parts
                numbers = []
                for part in parts[1:]:
                    try:
                        numbers.append(float(part))
                    except:
                        # If not a number, it might be part of item name
                        if not numbers:
                            item_name += ' ' + part
                
                if len(numbers) >= 2:
                    return {
                        'item_name': item_name,
                        'quantity': int(numbers[0]),
                        'unit_price': numbers[1]
                    }
            except:
                pass
        
        return None
    
    def _extract_total_amount(self, lines):
        """Extract total amount from bill"""
        # Look for total in last 10 lines
        for line in reversed(lines[-15:]):
            line_lower = line.lower()
            
            # Check if line contains total indicator
            if any(indicator in line_lower for indicator in self.TOTAL_INDICATORS):
                # Extract number
                numbers = re.findall(r'\d+\.?\d*', line)
                if numbers:
                    try:
                        # Return the largest number (likely the total)
                        amounts = [float(n) for n in numbers]
                        return max(amounts)
                    except:
                        continue
        
        return None
    
    def validate_and_enrich_items(self, items):
        """
        Validate and enrich parsed items
        
        Args:
            items: List of parsed items
            
        Returns:
            List of validated and enriched items
        """
        enriched_items = []
        
        for item in items:
            # Validate required fields
            if not item.get('item_name'):
                continue
            
            # Set defaults
            if 'quantity' not in item or item['quantity'] <= 0:
                item['quantity'] = 1
            
            if 'unit_price' not in item or item['unit_price'] < 0:
                item['unit_price'] = 0.0
            
            # Clean item name
            item['item_name'] = self._clean_item_name(item['item_name'])
            
            # Skip if item name is too short or invalid
            if len(item['item_name']) < 2:
                continue
            
            enriched_items.append(item)
        
        return enriched_items
    
    def _clean_item_name(self, name):
        """Clean and normalize item name"""
        # Remove special characters
        name = re.sub(r'[^\w\s-]', '', name)
        
        # Remove extra whitespace
        name = re.sub(r'\s+', ' ', name)
        
        # Title case
        name = name.strip().title()
        
        return name
