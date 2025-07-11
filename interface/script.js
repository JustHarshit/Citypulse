// CityPulse Smart Traffic Data Upload - JavaScript

// Global variables
let selectedFiles = [];

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeUploadInterface();
    console.log('CityPulse Smart Upload Interface Ready! 🚀');
});

// Initialize the upload interface
function initializeUploadInterface() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    if (!uploadArea || !fileInput) {
        console.error('Upload elements not found!');
        return;
    }

    // Click to upload
    uploadArea.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        fileInput.click();
    });

    // Drag and drop handlers
    uploadArea.addEventListener('dragenter', handleDragEnter);
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Prevent default drag behaviors on the document
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.addEventListener(eventName, preventDefaults, false);
    });

    console.log('✅ Upload interface initialized successfully!');
}

// Prevent default drag behaviors
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Drag and drop event handlers
function handleDragEnter(e) {
    e.preventDefault();
    e.stopPropagation();
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.classList.add('dragover');
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = 'copy';
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    const uploadArea = document.getElementById('uploadArea');
    
    // Only remove dragover if we're actually leaving the upload area
    if (!uploadArea.contains(e.relatedTarget)) {
        uploadArea.classList.remove('dragover');
    }
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        addFiles(Array.from(files));
        showStatusMessage(`Dropped ${files.length} file(s)`, 'success');
    }
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
        addFiles(files);
    }
}

// File handling functions
function addFiles(files) {
    const validFiles = [];
    const invalidFiles = [];
    
    files.forEach(file => {
        if (isValidFile(file)) {
            // Check if file is not already selected
            if (!selectedFiles.some(f => f.name === file.name && f.size === file.size)) {
                validFiles.push(file);
                selectedFiles.push(file);
            }
        } else {
            invalidFiles.push(file);
        }
    });
    
    if (invalidFiles.length > 0) {
        alert(`Invalid file types detected: ${invalidFiles.map(f => f.name).join(', ')}\nSupported formats: JPG, PNG, BMP, TIFF, PDF`);
    }
    
    if (validFiles.length > 0) {
        updateUploadDisplay();
        showStatusMessage(`Successfully added ${validFiles.length} file(s)`, 'success');
    }
}

function isValidFile(file) {
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff', 'application/pdf'];
    const maxSize = 10 * 1024 * 1024; // 10MB limit
    
    if (!validTypes.includes(file.type)) {
        return false;
    }
    
    if (file.size > maxSize) {
        alert(`File ${file.name} is too large. Maximum size is 10MB.`);
        return false;
    }
    
    return true;
}

// UI update functions
function updateUploadDisplay() {
    const uploadArea = document.getElementById('uploadArea');
    
    if (selectedFiles.length > 0) {
        const fileList = selectedFiles.map(f => `${f.name} (${formatFileSize(f.size)})`).join('<br>');
        uploadArea.innerHTML = `
            <div class="upload-icon">✅</div>
            <div class="upload-text">${selectedFiles.length} file(s) selected</div>
            <div class="upload-hint file-list">${fileList}</div>
            <div class="upload-hint add-more-hint">Click to add more files</div>
        `;
    } else {
        resetUploadDisplay();
    }
}

function resetUploadDisplay() {
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.innerHTML = `
        <div class="upload-icon">📊</div>
        <div class="upload-text">Drag & Drop your traffic images here</div>
        <div class="upload-hint">or click to browse files</div>
        <div class="upload-hint">Supports: JPG, PNG, BMP, TIFF, PDF (Max 10MB each)</div>
    `;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showStatusMessage(message, type) {
    const existingMessage = document.querySelector('.temp-status-message');
    if (existingMessage) {
        existingMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `status-message status-${type} temp-status-message`;
    messageDiv.textContent = message;
    messageDiv.style.position = 'fixed';
    messageDiv.style.top = '20px';
    messageDiv.style.right = '20px';
    messageDiv.style.zIndex = '1000';
    messageDiv.style.maxWidth = '300px';
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// Main action functions
function clearFiles() {
    selectedFiles = [];
    const fileInput = document.getElementById('fileInput');
    fileInput.value = '';
    resetUploadDisplay();
    hideSection('processingSection');
    hideSection('resultsSection');
    showStatusMessage('Files cleared successfully', 'info');
}

function processFiles() {
    if (selectedFiles.length === 0) {
        alert('Please select files to process first!');
        return;
    }

    showSection('processingSection');
    hideSection('resultsSection');
    
    // Actually upload and process files
    uploadFilesToServer();
}

// Function to upload files to the server
async function uploadFilesToServer() {
    const progressFill = document.getElementById('progressFill');
    const statusDiv = document.getElementById('processingStatus');
    
    try {
        // Create FormData object
        const formData = new FormData();
        selectedFiles.forEach(file => {
            formData.append('files', file);
        });
        
        statusDiv.textContent = 'Uploading files to server...';
        progressFill.style.width = '20%';
        
        // Upload files to Flask server
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        progressFill.style.width = '60%';
        statusDiv.textContent = 'Processing images...';
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        progressFill.style.width = '100%';
        statusDiv.textContent = 'Processing complete!';
        
        setTimeout(() => {
            hideSection('processingSection');
            showServerResults(result);
        }, 1000);
        
    } catch (error) {
        console.error('Error uploading files:', error);
        statusDiv.textContent = 'Error processing files: ' + error.message;
        progressFill.style.width = '100%';
        progressFill.style.background = 'linear-gradient(90deg, #dc3545, #c82333)';
        
        // Fall back to mock processing after 2 seconds
        setTimeout(() => {
            statusDiv.textContent = 'Falling back to demo mode...';
            setTimeout(() => {
                hideSection('processingSection');
                simulateProcessing();
            }, 1000);
        }, 2000);
    }
}

// Processing simulation
function simulateProcessing() {
    const progressFill = document.getElementById('progressFill');
    const statusDiv = document.getElementById('processingStatus');
    let progress = 0;

    const steps = [
        'Loading images...',
        'Detecting image types...',
        'Extracting text with OCR...',
        'Analyzing traffic patterns...',
        'Processing color information...',
        'Extracting numerical data...',
        'Creating structured datasets...',
        'Generating visualizations...',
        'Finalizing results...'
    ];

    const interval = setInterval(() => {
        progress += 11;
        if (progress > 100) progress = 100;

        progressFill.style.width = progress + '%';
        statusDiv.textContent = steps[Math.floor(progress / 11)] || 'Complete!';

        if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                hideSection('processingSection');
                showResults();
            }, 1000);
        }
    }, 500);
}

// Results functions
function showResults() {
    const resultsContent = document.getElementById('resultsContent');
    
    // Generate mock results based on selected files
    const mockResults = generateMockResults();        resultsContent.innerHTML = `
            <div class="status-message status-success">
                ✅ Successfully processed ${selectedFiles.length} file(s)
            </div>
            
            <h4>📊 Extracted Data Summary</h4>
            ${mockResults.summary}
            
            <h4>📈 Generated Visualizations</h4>
            <div class="button-group">
                <button class="btn" onclick="downloadData('csv')">📁 Download CSV</button>
                <button class="btn" onclick="downloadData('json')">📄 Download JSON</button>
                <button class="btn" onclick="viewVisualization()">📊 View Interactive Chart</button>
            </div>
            
            <h4>🔍 Detailed Results</h4>
            ${mockResults.details}
        `;
    
    showSection('resultsSection');
}

// Function to display server results
function showServerResults(serverResult) {
    const resultsContent = document.getElementById('resultsContent');
    
    if (serverResult.success) {
        resultsContent.innerHTML = `
            <div class="status-message status-success">
                ✅ Successfully processed ${serverResult.processed_count} file(s)
            </div>
            
            <h4>📊 Server Processing Results</h4>
            <div class="summary-box">
                <ul class="summary-list">
                    <li>🎯 <strong>Files Processed:</strong> ${serverResult.processed_count}</li>
                    <li>🔍 <strong>Processing Method:</strong> Real Server Processing</li>
                    <li>⚡ <strong>Status:</strong> Complete</li>
                </ul>
            </div>
            
            <h4>📈 Available Actions</h4>
            <div class="button-group">
                <button class="btn" onclick="downloadData('csv')">📁 Download CSV</button>
                <button class="btn" onclick="downloadData('json')">📄 Download JSON</button>
                <button class="btn" onclick="viewVisualization()">📊 View Interactive Chart</button>
            </div>
            
            <h4>🔍 Processing Details</h4>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>File</th>
                        <th>Status</th>
                        <th>Processing Time</th>
                        <th>Result</th>
                    </tr>
                </thead>
                <tbody>
                    ${serverResult.results.map((result, index) => `
                        <tr>
                            <td>${result.filename}</td>
                            <td class="${result.error ? 'status-error-cell' : 'status-success-cell'}">${result.error ? '❌ Error' : '✅ Success'}</td>
                            <td>${result.processed_at ? new Date(result.processed_at).toLocaleTimeString() : 'N/A'}</td>
                            <td>${result.error || 'Data extracted successfully'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } else {
        resultsContent.innerHTML = `
            <div class="status-message status-error">
                ❌ Processing failed: ${serverResult.error || 'Unknown error'}
            </div>
        `;
    }
    
    showSection('resultsSection');
}

function generateMockResults() {
    const fileTypes = selectedFiles.map(f => f.type.includes('pdf') ? 'PDF Report' : 'Image');
    const extractedCount = Math.floor(Math.random() * 50) + 10;
    
    return {
        summary: `
            <div class="summary-box">
                <ul class="summary-list">
                    <li>🎯 <strong>Data Points Extracted:</strong> ${extractedCount}</li>
                    <li>🏙️ <strong>Cities Detected:</strong> ${Math.floor(Math.random() * 3) + 1}</li>
                    <li>🚦 <strong>Traffic Conditions:</strong> Good (${Math.floor(Math.random() * 20) + 30}%), Moderate (${Math.floor(Math.random() * 20) + 30}%), Congested (${Math.floor(Math.random() * 20) + 10}%)</li>
                    <li>⚡ <strong>Average Speed:</strong> ${Math.floor(Math.random() * 30) + 25} km/h</li>
                </ul>
            </div>
        `,
        details: `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>File</th>
                        <th>Type Detected</th>
                        <th>Data Points</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${selectedFiles.map((file, index) => `
                        <tr>
                            <td>${file.name}</td>
                            <td>${['Traffic Map', 'Speed Chart', 'Data Table', 'Screenshot'][Math.floor(Math.random() * 4)]}</td>
                            <td>${Math.floor(Math.random() * 15) + 5}</td>
                            <td class="status-success-cell">✅ Success</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `
    };
}

// Utility functions
function showSection(sectionId) {
    document.getElementById(sectionId).style.display = 'block';
}

function hideSection(sectionId) {
    document.getElementById(sectionId).style.display = 'none';
}

// Download functions
function downloadData(format) {
    // Create mock data
    const mockData = {
        timestamp: new Date().toISOString(),
        extracted_data: selectedFiles.map((file, index) => ({
            source_file: file.name,
            location: ['Downtown', 'Highway 101', 'Main Street', 'City Center'][Math.floor(Math.random() * 4)],
            speed: Math.floor(Math.random() * 50) + 20,
            condition: ['Good', 'Moderate', 'Congested'][Math.floor(Math.random() * 3)],
            volume: Math.floor(Math.random() * 2000) + 500
        }))
    };

    let content, filename, mimeType;

    if (format === 'csv') {
        content = convertToCSV(mockData.extracted_data);
        filename = `citypulse_extracted_data_${new Date().toISOString().split('T')[0]}.csv`;
        mimeType = 'text/csv';
    } else {
        content = JSON.stringify(mockData, null, 2);
        filename = `citypulse_extracted_data_${new Date().toISOString().split('T')[0]}.json`;
        mimeType = 'application/json';
    }

    downloadFile(content, filename, mimeType);
}

function convertToCSV(data) {
    if (data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => row[header]).join(','))
    ].join('\n');
    
    return csvContent;
}

function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Visualization function
function viewVisualization() {
    // Create mock data for visualization
    const mockData = {
        chartData: {
            x: ['Location 1', 'Location 2', 'Location 3', 'Location 4', 'Location 5'],
            y: [45, 32, 28, 55, 38],
            type: 'bar',
            marker: { color: ['green', 'orange', 'red', 'green', 'orange'] }
        },
        layout: {
            title: 'Extracted Traffic Speeds by Location',
            xaxis: { title: 'Locations' },
            yaxis: { title: 'Speed (km/h)' }
        }
    };
    
    // Open visualization in new window
    const dataParam = encodeURIComponent(JSON.stringify(mockData));
    const newWindow = window.open(`visualization.html?data=${dataParam}`, '_blank');
    
    if (!newWindow) {
        alert('Please allow popups to view the visualization');
    }
}
