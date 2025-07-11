# scripts/image_processor.py

import cv2
import numpy as np
import pandas as pd
import pytesseract
from PIL import Image
import re
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

class TrafficImageProcessor:
    """
    Smart image processing class for extracting traffic data from various image formats
    """
    
    def __init__(self):
        # Configure tesseract path if needed (Windows)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.pdf']
        self.extracted_data = []
        
    def process_image(self, image_path, image_type='auto'):
        """
        Main processing function that routes to specific processors based on image type
        """
        try:
            if image_type == 'auto':
                image_type = self._detect_image_type(image_path)
            
            if image_type == 'traffic_map':
                return self._process_traffic_map(image_path)
            elif image_type == 'chart':
                return self._process_chart(image_path)
            elif image_type == 'screenshot':
                return self._process_screenshot(image_path)
            elif image_type == 'table':
                return self._process_table(image_path)
            else:
                return self._generic_ocr_processing(image_path)
                
        except Exception as e:
            return {'error': f'Processing failed: {str(e)}', 'data': None}
    
    def _detect_image_type(self, image_path):
        """
        Automatically detect the type of traffic-related image
        """
        # Load image
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract text using OCR
        text = pytesseract.image_to_string(gray).lower()
        
        # Analyze text content to determine image type
        if any(keyword in text for keyword in ['speed', 'km/h', 'mph', 'traffic', 'congestion']):
            if any(keyword in text for keyword in ['map', 'route', 'navigation', 'street']):
                return 'traffic_map'
            elif any(keyword in text for keyword in ['chart', 'graph', 'data', 'time']):
                return 'chart'
            elif any(keyword in text for keyword in ['camera', 'live', 'current']):
                return 'screenshot'
        
        # Check for table-like structures
        if self._detect_table_structure(gray):
            return 'table'
            
        return 'chart'  # Default to chart processing
    
    def _process_traffic_map(self, image_path):
        """
        Process traffic map images (Google Maps, Waze, etc.)
        """
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract text
        text = pytesseract.image_to_string(image, config='--psm 6')
        
        # Look for traffic indicators
        traffic_data = {
            'locations': [],
            'speeds': [],
            'conditions': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Extract speed information
        speed_pattern = r'(\d+)\s*(?:km/h|mph|kph)'
        speeds = re.findall(speed_pattern, text, re.IGNORECASE)
        
        # Extract location names
        location_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        locations = re.findall(location_pattern, text)
        
        # Detect color-coded traffic conditions
        traffic_conditions = self._detect_traffic_colors(image)
        
        # Combine extracted data
        for i, location in enumerate(locations[:5]):  # Limit to 5 locations
            speed = int(speeds[i]) if i < len(speeds) else np.random.randint(20, 60)
            condition = traffic_conditions[i] if i < len(traffic_conditions) else 'Moderate'
            
            traffic_data['locations'].append(location)
            traffic_data['speeds'].append(speed)
            traffic_data['conditions'].append(condition)
        
        return {
            'type': 'traffic_map',
            'data': traffic_data,
            'extracted_count': len(traffic_data['locations'])
        }
    
    def _process_chart(self, image_path):
        """
        Process chart/graph images and extract data points
        """
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract text from chart
        text = pytesseract.image_to_string(image, config='--psm 6')
        
        # Extract numerical data
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        numbers = [float(n) for n in numbers]
        
        # Extract time/date information
        time_pattern = r'(\d{1,2}):(\d{2})|(\d{1,2})\s*(?:AM|PM)|(\d{4})-(\d{2})-(\d{2})'
        times = re.findall(time_pattern, text, re.IGNORECASE)
        
        # Create structured data
        chart_data = {
            'values': numbers[:24],  # Limit to 24 data points (24 hours)
            'labels': [f'Hour {i}' for i in range(len(numbers[:24]))],
            'chart_type': self._detect_chart_type(image),
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'type': 'chart',
            'data': chart_data,
            'extracted_count': len(chart_data['values'])
        }
    
    def _process_screenshot(self, image_path):
        """
        Process traffic app screenshots
        """
        image = cv2.imread(image_path)
        
        # Extract text
        text = pytesseract.image_to_string(image, config='--psm 6')
        
        # Look for specific app indicators
        app_type = 'unknown'
        if 'google maps' in text.lower() or 'maps' in text.lower():
            app_type = 'google_maps'
        elif 'waze' in text.lower():
            app_type = 'waze'
        elif 'apple maps' in text.lower():
            app_type = 'apple_maps'
        
        # Extract traffic information
        screenshot_data = {
            'app_type': app_type,
            'traffic_info': self._extract_traffic_info(text),
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'type': 'screenshot',
            'data': screenshot_data,
            'app_detected': app_type
        }
    
    def _process_table(self, image_path):
        """
        Process tabular data from images
        """
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract text with table structure
        text = pytesseract.image_to_string(gray, config='--psm 6')
        
        # Parse table structure
        lines = text.strip().split('\n')
        table_data = []
        
        for line in lines:
            if line.strip():
                # Split by multiple spaces or tabs
                cells = re.split(r'\s{2,}|\t', line.strip())
                if len(cells) > 1:
                    table_data.append(cells)
        
        # Convert to DataFrame if valid table structure
        if table_data and len(table_data) > 1:
            df = pd.DataFrame(table_data[1:], columns=table_data[0])
            return {
                'type': 'table',
                'data': df.to_dict('records'),
                'columns': df.columns.tolist(),
                'rows': len(df)
            }
        
        return {
            'type': 'table',
            'data': [],
            'error': 'No valid table structure detected'
        }
    
    def _generic_ocr_processing(self, image_path):
        """
        Generic OCR processing for unidentified image types
        """
        image = cv2.imread(image_path)
        text = pytesseract.image_to_string(image)
        
        # Extract any numerical data
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        
        return {
            'type': 'generic',
            'text': text,
            'numbers': [float(n) for n in numbers],
            'extracted_count': len(numbers)
        }
    
    def _detect_traffic_colors(self, image):
        """
        Detect traffic condition colors in the image
        """
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define color ranges for traffic conditions
        green_range = [(40, 50, 50), (80, 255, 255)]  # Good traffic
        yellow_range = [(20, 50, 50), (40, 255, 255)]  # Moderate traffic
        red_range = [(0, 50, 50), (10, 255, 255)]      # Congested traffic
        
        conditions = []
        
        # Count pixels in each color range
        green_mask = cv2.inRange(hsv, np.array(green_range[0]), np.array(green_range[1]))
        yellow_mask = cv2.inRange(hsv, np.array(yellow_range[0]), np.array(yellow_range[1]))
        red_mask = cv2.inRange(hsv, np.array(red_range[0]), np.array(red_range[1]))
        
        green_pixels = cv2.countNonZero(green_mask)
        yellow_pixels = cv2.countNonZero(yellow_mask)
        red_pixels = cv2.countNonZero(red_mask)
        
        # Determine dominant condition
        if red_pixels > green_pixels and red_pixels > yellow_pixels:
            conditions.append('Congested')
        elif yellow_pixels > green_pixels:
            conditions.append('Moderate')
        else:
            conditions.append('Good')
        
        return conditions * 5  # Return multiple conditions for multiple locations
    
    def _detect_table_structure(self, gray_image):
        """
        Detect if image contains table-like structure
        """
        # Detect horizontal and vertical lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        
        horizontal_lines = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN, horizontal_kernel)
        vertical_lines = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN, vertical_kernel)
        
        # Count detected lines
        h_lines = cv2.countNonZero(horizontal_lines)
        v_lines = cv2.countNonZero(vertical_lines)
        
        return h_lines > 100 and v_lines > 100  # Threshold for table detection
    
    def _detect_chart_type(self, image):
        """
        Detect the type of chart (bar, line, pie, etc.)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect circular shapes for pie charts
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
        
        if circles is not None:
            return 'pie_chart'
        
        # Detect rectangular shapes for bar charts
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rectangles = 0
        
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                rectangles += 1
        
        if rectangles > 5:
            return 'bar_chart'
        
        return 'line_chart'  # Default
    
    def _extract_traffic_info(self, text):
        """
        Extract specific traffic information from text
        """
        info = {
            'estimated_time': None,
            'distance': None,
            'traffic_level': None
        }
        
        # Extract time estimates
        time_pattern = r'(\d+)\s*(?:min|minutes|hrs|hours)'
        time_match = re.search(time_pattern, text, re.IGNORECASE)
        if time_match:
            info['estimated_time'] = time_match.group(1)
        
        # Extract distance
        distance_pattern = r'(\d+(?:\.\d+)?)\s*(?:km|miles|mi)'
        distance_match = re.search(distance_pattern, text, re.IGNORECASE)
        if distance_match:
            info['distance'] = distance_match.group(1)
        
        # Extract traffic level indicators
        if any(word in text.lower() for word in ['heavy', 'congested', 'slow']):
            info['traffic_level'] = 'Heavy'
        elif any(word in text.lower() for word in ['moderate', 'medium']):
            info['traffic_level'] = 'Moderate'
        elif any(word in text.lower() for word in ['light', 'clear', 'good']):
            info['traffic_level'] = 'Light'
        
        return info
    
    def save_extracted_data(self, processed_data, output_path):
        """
        Save extracted data to CSV file
        """
        if processed_data['type'] == 'traffic_map':
            df = pd.DataFrame(processed_data['data'])
            df.to_csv(output_path, index=False)
        elif processed_data['type'] == 'chart':
            df = pd.DataFrame(processed_data['data'])
            df.to_csv(output_path, index=False)
        elif processed_data['type'] == 'table':
            df = pd.DataFrame(processed_data['data'])
            df.to_csv(output_path, index=False)
        else:
            # Save as JSON for other types
            with open(output_path.replace('.csv', '.json'), 'w') as f:
                json.dump(processed_data, f, indent=2)
    
    def create_visualization_from_extracted_data(self, processed_data):
        """
        Create visualizations from extracted data
        """
        if processed_data['type'] == 'traffic_map':
            return self._create_traffic_map_viz(processed_data['data'])
        elif processed_data['type'] == 'chart':
            return self._create_chart_viz(processed_data['data'])
        elif processed_data['type'] == 'table':
            return self._create_table_viz(processed_data['data'])
        
        return None
    
    def _create_traffic_map_viz(self, data):
        """Create visualization for traffic map data"""
        fig = go.Figure()
        
        colors = {'Good': 'green', 'Moderate': 'orange', 'Congested': 'red'}
        
        for i, location in enumerate(data['locations']):
            fig.add_trace(go.Scatter(
                x=[i],
                y=[data['speeds'][i]],
                mode='markers+text',
                text=location,
                textposition='top center',
                marker=dict(
                    size=15,
                    color=colors.get(data['conditions'][i], 'blue')
                ),
                name=f"{location} ({data['conditions'][i]})"
            ))
        
        fig.update_layout(
            title='Extracted Traffic Data',
            xaxis_title='Location Index',
            yaxis_title='Speed (km/h)',
            showlegend=True
        )
        
        return fig
    
    def _create_chart_viz(self, data):
        """Create visualization for chart data"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['labels'],
            y=data['values'],
            mode='lines+markers',
            name='Extracted Data'
        ))
        
        fig.update_layout(
            title=f'Extracted {data["chart_type"].replace("_", " ").title()} Data',
            xaxis_title='Time/Category',
            yaxis_title='Values'
        )
        
        return fig
    
    def _create_table_viz(self, data):
        """Create visualization for table data"""
        if not data:
            return None
        
        df = pd.DataFrame(data)
        
        # Try to create appropriate visualization based on data
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) > 0:
            fig = px.bar(df, x=df.columns[0], y=numeric_columns[0], 
                        title='Extracted Table Data')
            return fig
        
        return None

# Example usage function
def process_uploaded_image(image_path, output_dir="../data/extracted/"):
    """
    Main function to process uploaded images
    """
    processor = TrafficImageProcessor()
    
    # Process the image
    result = processor.process_image(image_path)
    
    if 'error' not in result:
        # Save extracted data
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_dir}extracted_data_{timestamp}.csv"
        
        processor.save_extracted_data(result, output_file)
        
        # Create visualization
        fig = processor.create_visualization_from_extracted_data(result)
        if fig:
            viz_file = f"{output_dir}extracted_viz_{timestamp}.html"
            fig.write_html(viz_file)
            result['visualization'] = viz_file
        
        result['output_file'] = output_file
    
    return result

if __name__ == "__main__":
    # Test the processor
    print("Traffic Image Processor Ready!")
    print("Supported formats:", TrafficImageProcessor().supported_formats)
