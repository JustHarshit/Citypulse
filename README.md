# 🚗 CityPulse

> **Smart Traffic Data Analysis & Visualization Platform**

A comprehensive traffic monitoring and analysis platform that processes traffic data from multiple sources and creates interactive visualizations for urban mobility insights across major metropolitan areas.

## 🌆 Overview

CityPulse combines real-time traffic data analysis with intelligent image processing capabilities. Upload traffic maps, charts, or data files, and get instant insights through interactive dashboards and visualizations covering Amsterdam, New York, London, and Kuala Lumpur.

## ✨ Key Features

### 📊 **Smart Data Processing**
- **Intelligent Image Upload**: Drag & drop traffic maps, screenshots, charts, and reports
- **Computer Vision**: Automatic data extraction from images using OCR and pattern recognition
- **Multi-format Support**: JPG, PNG, PDF, and various chart formats
- **Real-time Processing**: Instant analysis with progress tracking

### 🌐 **Multi-City Traffic Analysis**
- **Global Coverage**: Amsterdam, New York, London, Kuala Lumpur
- **Zone-based Monitoring**: 5 zones per city with real coordinates
- **Traffic Conditions**: Color-coded status (Good/Moderate/Congested)
- **Route Performance**: Highway, main roads, secondary roads, local streets

### 📈 **Interactive Visualizations**
- **Live Dashboard**: Real-time traffic monitoring interface
- **Geographic Maps**: Interactive traffic condition mapping
- **Time Series Analysis**: 24-hour traffic patterns with rush hour detection
- **Performance Charts**: Route efficiency and speed comparisons
- **Data Export**: CSV, JSON, and visualization downloads

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd CityPulse
```

2. **Install core dependencies**
```bash
pip install pandas numpy plotly flask flask-cors
```

3. **Install image processing dependencies**
```bash
pip install opencv-python pytesseract pillow
```

4. **Install Tesseract OCR**
   - **Windows**: Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Mac**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

### Launch Application

1. **Start the web server**
```bash
cd scripts
python web_app.py
```

2. **Open browser**
```
http://localhost:5000
```

3. **Start uploading!**
   - Drag & drop traffic images
   - Click to browse files
   - Watch real-time processing
   - Download results

## 📁 Project Structure

```
CityPulse/
├── 📂 interface/           # Clean, modular web interface
│   ├── index.html         # Main HTML structure
│   ├── styles.css         # Pure CSS styling
│   ├── script.js          # JavaScript functionality
│   └── visualization.html # Interactive charts
├── 📂 scripts/            # Python backend
│   ├── web_app.py        # Flask web server
│   ├── data_gen.py       # Data generation
│   ├── viz.py            # Visualization creation
│   └── image_processor.py # AI image processing
├── 📂 data/              # Generated datasets
│   ├── traffic_network_data.csv
│   ├── traffic_flow_timeseries.csv
│   ├── route_performance.csv
│   └── extracted/        # Processed uploads
├── 📂 outputs/           # Generated visualizations
│   ├── dashboard.html
│   ├── traffic_map.html
│   └── *.html
└── 📂 uploads/           # Temporary storage
```

## 🎯 Use Cases

### 🏛️ **Urban Planning**
- Analyze traffic patterns for infrastructure decisions
- Identify congestion hotspots and bottlenecks
- Plan new roads and optimize existing ones

### 🚦 **Traffic Management**
- Real-time monitoring of traffic conditions
- Route optimization and alternative path suggestions
- Incident response and traffic flow management

### 📊 **Data Analysis**
- Extract data from traffic reports and screenshots
- Convert charts and graphs to structured datasets
- Analyze trends and patterns across cities

### 🔬 **Research & Policy**
- Study urban mobility patterns
- Evaluate traffic management strategies
- Compare transportation efficiency across cities

## 🛠️ Technology Stack

### **Frontend**
- **HTML5**: Semantic structure
- **CSS3**: Modern styling with flexbox/grid
- **JavaScript ES6+**: Interactive functionality
- **Plotly.js**: Data visualization

### **Backend**
- **Flask**: Web server framework
- **Flask-CORS**: Cross-origin support
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing

### **AI/Computer Vision**
- **OpenCV**: Image processing
- **Tesseract OCR**: Text extraction
- **PIL/Pillow**: Image manipulation
- **Pattern Recognition**: Chart detection

## 📊 Sample Data

### **Traffic Conditions Distribution**
- 🟢 **Good**: 40% (45-65 km/h)
- 🟡 **Moderate**: 40% (25-45 km/h)  
- 🔴 **Congested**: 20% (5-25 km/h)

### **Cities & Zones**
- **Amsterdam**: City Center, Noord, Zuidoost, West, Nieuw-West
- **New York**: Manhattan, Brooklyn, Queens, Bronx, Staten Island
- **London**: Central, North, South, East, West London
- **Kuala Lumpur**: KLCC, Chow Kit, Bangsar, Mont Kiara, Petaling Jaya

### **Route Types**
- **Highway**: High-speed arterial roads
- **Main Road**: Primary urban corridors
- **Secondary Road**: Local connector streets
- **Local Street**: Neighborhood roads

## 🎨 Screenshots & Demos

The application generates several interactive visualizations:

- **Main Dashboard**: Overview of all cities with filtering
- **Traffic Map**: Geographic view with color-coded conditions
- **Time Series**: 24-hour patterns with rush hour analysis
- **Performance Charts**: Route efficiency comparisons
- **Upload Interface**: Drag & drop with real-time processing

## 🚧 Advanced Features

### **Smart Image Processing**
- **Traffic Map Detection**: Extract speed and condition data from map screenshots
- **Chart Recognition**: Convert bar charts, line graphs, and pie charts to data
- **PDF Processing**: Extract tables and charts from traffic reports
- **Batch Upload**: Process multiple files simultaneously

### **Real-time Analytics**
- **Live Processing**: Watch data extraction in real-time
- **Progress Tracking**: Visual feedback during upload and processing
- **Error Handling**: Graceful fallback to demo mode
- **Status Messages**: Clear feedback on success/failure

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## � License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the browser console for errors
2. Ensure all dependencies are installed
3. Verify Tesseract OCR is properly configured
4. Try clearing browser cache
5. Open an issue with detailed error information

## � Roadmap

- [ ] Real-time traffic API integration
- [ ] Machine learning traffic predictions
- [ ] Mobile responsive design
- [ ] Advanced image recognition
- [ ] Weather impact analysis
- [ ] Public transportation data
- [ ] REST API endpoints
- [ ] User authentication
- [ ] Data persistence
- [ ] Cloud deployment

---

**CityPulse** - *Monitoring the heartbeat of urban traffic* 🚗📊🏙️

*Built with ❤️ for smarter cities and better transportation*
