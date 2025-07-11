# scripts/web_app.py

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import pandas as pd
from image_processor import TrafficImageProcessor
import tempfile
import traceback

app = Flask(__name__, static_folder='../interface', static_url_path='/static')
CORS(app)  # Enable CORS for all domains on all routes
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = '../uploads'
app.config['RESULTS_FOLDER'] = '../data/extracted'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main upload interface"""
    response = send_from_directory('../interface', 'index.html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/styles.css')
def serve_css():
    """Serve the CSS file"""
    response = send_from_directory('../interface', 'styles.css')
    response.headers['Content-Type'] = 'text/css'
    return response

@app.route('/script.js')
def serve_js():
    """Serve the JavaScript file"""
    response = send_from_directory('../interface', 'script.js')
    response.headers['Content-Type'] = 'application/javascript'
    return response

@app.route('/visualization.html')
def serve_visualization():
    """Serve the visualization HTML file"""
    response = send_from_directory('../interface', 'visualization.html')
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads and process them"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        if not files or all(file.filename == '' for file in files):
            return jsonify({'error': 'No files selected'}), 400
        
        results = []
        processor = TrafficImageProcessor()
        
        for file in files:
            if file and allowed_file(file.filename):
                # Secure the filename
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{filename}"
                
                # Save uploaded file
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    # Process the image
                    result = processor.process_image(filepath)
                    result['filename'] = file.filename
                    result['processed_at'] = datetime.now().isoformat()
                    
                    # Save extracted data
                    if 'error' not in result:
                        save_path = os.path.join(app.config['RESULTS_FOLDER'], 
                                               f"extracted_{timestamp}_{file.filename}.csv")
                        processor.save_extracted_data(result, save_path)
                        result['data_file'] = save_path
                        
                        # Create visualization
                        viz = processor.create_visualization_from_extracted_data(result)
                        if viz:
                            viz_path = os.path.join(app.config['RESULTS_FOLDER'], 
                                                  f"viz_{timestamp}_{file.filename}.html")
                            viz.write_html(viz_path)
                            result['visualization_file'] = viz_path
                    
                    results.append(result)
                    
                except Exception as e:
                    results.append({
                        'filename': file.filename,
                        'error': f'Processing failed: {str(e)}',
                        'processed_at': datetime.now().isoformat()
                    })
                
                # Clean up uploaded file
                try:
                    os.remove(filepath)
                except:
                    pass
        
        return jsonify({
            'success': True,
            'results': results,
            'processed_count': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Upload processing failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/download/<result_type>/<filename>')
def download_file(result_type, filename):
    """Download processed results"""
    try:
        if result_type == 'data':
            file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
        elif result_type == 'visualization':
            file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
        else:
            return jsonify({'error': 'Invalid result type'}), 400
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/demo-data')
def get_demo_data():
    """Get demo data for testing the interface"""
    demo_data = {
        'traffic_conditions': {
            'Good': 40,
            'Moderate': 35,
            'Congested': 25
        },
        'cities': ['Amsterdam', 'New York', 'London', 'Kuala Lumpur'],
        'sample_speeds': [45, 32, 28, 55, 38, 42, 29, 61, 35, 47],
        'sample_volumes': [1200, 2800, 3400, 1800, 2200, 1900, 3100, 1600, 2400, 2000]
    }
    return jsonify(demo_data)

@app.route('/api/process-demo')
def process_demo():
    """Process demo data to show how the system works"""
    
    # Create sample processed data
    sample_data = {
        'type': 'demo',
        'data': {
            'locations': ['Downtown', 'Highway 101', 'Main Street', 'City Center', 'Industrial Zone'],
            'speeds': [45, 32, 28, 55, 38],
            'conditions': ['Good', 'Moderate', 'Congested', 'Good', 'Moderate'],
            'volumes': [1200, 2800, 3400, 1800, 2200],
            'timestamp': datetime.now().isoformat()
        },
        'extracted_count': 5,
        'processing_time': '2.3 seconds'
    }
    
    return jsonify({
        'success': True,
        'demo_result': sample_data,
        'message': 'Demo processing complete!'
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting CityPulse Web Application...")
    print("📡 Interface will be available at: http://localhost:5000")
    print("📊 Upload interface ready for traffic image processing!")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
