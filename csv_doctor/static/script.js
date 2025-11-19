// script.js - JavaScript for CSV Doctor frontend

let currentSessionId = null;
let startTime = null;

// Show/Hide tabs
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected tab
    const tab = document.getElementById(`${tabName}-tab`);
    if (tab) {
        tab.classList.add('active');
    }

    // Scroll to top
    window.scrollTo(0, 0);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'block';

    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

// Show loading indicator
function showLoading(text = 'Processing...') {
    document.getElementById('loadingIndicator').classList.remove('hidden');
    document.getElementById('loadingText').textContent = text;
}

// Hide loading indicator
function hideLoading() {
    document.getElementById('loadingIndicator').classList.add('hidden');
}

// ============ UPLOAD FUNCTIONALITY ============

// Drag and drop setup
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        uploadFile(e.target.files[0]);
    }
});

// Upload file
async function uploadFile(file) {
    if (!file.name.endsWith('.csv')) {
        showNotification('Please upload a CSV file', 'error');
        return;
    }

    showLoading('Uploading file...');
    startTime = Date.now();

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            currentSessionId = data.session_id;

            // Display file info
            displayFileInfo(data.metadata, data.sample);

            // Display validation issues if any
            if (data.validation.issues.length > 0) {
                displayValidationIssues(data.validation.issues);
            }

            showNotification('File uploaded successfully!', 'success');
            hideLoading();
        } else {
            showNotification(data.error || 'Upload failed', 'error');
            hideLoading();
        }
    } catch (error) {
        console.error('Upload error:', error);
        showNotification('Upload failed: ' + error.message, 'error');
        hideLoading();
    }
}

// Display file info
function displayFileInfo(metadata, sample) {
    document.getElementById('fileInfo').classList.remove('hidden');
    document.getElementById('fileName').textContent = metadata.file_name;
    document.getElementById('rowCount').textContent = `${metadata.rows}`;
    document.getElementById('columnCount').textContent = `${metadata.columns}`;
    document.getElementById('fileSize').textContent = formatBytes(metadata.file_size);

    // Display sample data
    displaySampleData(sample, metadata.column_names);
}

// Display sample data
function displaySampleData(sample, columnNames) {
    const thead = document.getElementById('sampleHead');
    const tbody = document.getElementById('sampleBody');

    thead.innerHTML = '';
    tbody.innerHTML = '';

    // Add headers
    const headerRow = document.createElement('tr');
    columnNames.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Add rows
    sample.forEach(row => {
        const tr = document.createElement('tr');
        columnNames.forEach(col => {
            const td = document.createElement('td');
            td.textContent = row[col] || '-';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

// Display validation issues
function displayValidationIssues(issues) {
    document.getElementById('validationIssues').classList.remove('hidden');
    const issuesList = document.getElementById('issuesList');
    issuesList.innerHTML = '';

    issues.forEach(issue => {
        const li = document.createElement('li');
        li.textContent = issue;
        issuesList.appendChild(li);
    });
}

// Format bytes
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ============ CLEANING FUNCTIONALITY ============

// Toggle sub-options
document.getElementById('fillMissing').addEventListener('change', (e) => {
    document.getElementById('fillMethod').disabled = !e.target.checked;
});

document.getElementById('normalizeText').addEventListener('change', (e) => {
    document.getElementById('textCase').disabled = !e.target.checked;
});

document.getElementById('removeOutliers').addEventListener('change', (e) => {
    document.getElementById('outlierMethod').disabled = !e.target.checked;
});

// Clean data
async function cleanData() {
    if (!currentSessionId) {
        showNotification('Please upload a file first', 'error');
        return;
    }

    const options = {
        remove_empty_rows: document.getElementById('removeEmptyRows').checked,
        remove_empty_columns: document.getElementById('removeEmptyColumns').checked,
        trim_whitespace: document.getElementById('trimWhitespace').checked,
        remove_duplicates: document.getElementById('removeDuplicates').checked,
        standardize_column_names: document.getElementById('standardizeNames').checked,
        fill_missing: document.getElementById('fillMissing').checked,
        fill_method: document.getElementById('fillMethod').value,
        normalize_text_case: document.getElementById('normalizeText').checked,
        text_case: document.getElementById('textCase').value,
        remove_outliers: document.getElementById('removeOutliers').checked,
        outlier_method: document.getElementById('outlierMethod').value
    };

    showLoading('Cleaning data...');

    try {
        const response = await fetch('/api/clean', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: currentSessionId,
                options: options
            })
        });

        const data = await response.json();

        if (data.success) {
            displayCleaningResults(data.changes, data.new_shape, data.sample);
            showNotification('Data cleaned successfully!', 'success');
            hideLoading();
        } else {
            showNotification(data.error || 'Cleaning failed', 'error');
            hideLoading();
        }
    } catch (error) {
        console.error('Clean error:', error);
        showNotification('Cleaning failed: ' + error.message, 'error');
        hideLoading();
    }
}

// Display cleaning results
function displayCleaningResults(changes, newShape, sample) {
    const section = document.getElementById('cleaningResults');
    section.classList.remove('hidden');

    const changesList = document.getElementById('changesList');
    changesList.innerHTML = '';

    changes.forEach(change => {
        const li = document.createElement('li');
        li.textContent = change;
        changesList.appendChild(li);
    });

    document.getElementById('newRowCount').textContent = `${newShape.rows}`;
    document.getElementById('newColumnCount').textContent = `${newShape.columns}`;
}

// Preview cleaning (placeholder)
async function previewCleaning() {
    showNotification('Preview feature coming soon!', 'info');
}

// ============ VALIDATION & ANALYSIS ============

// Validate data
async function validateData() {
    if (!currentSessionId) {
        showNotification('Please upload and clean data first', 'error');
        return;
    }

    showLoading('Validating data...');

    try {
        const response = await fetch('/api/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: currentSessionId
            })
        });

        const data = await response.json();

        if (data.success) {
            displayQualityScore(data.quality_score);
            displayValidationReport(data.validation_report);
            showNotification('Validation completed!', 'success');
            hideLoading();
        } else {
            showNotification(data.error || 'Validation failed', 'error');
            hideLoading();
        }
    } catch (error) {
        console.error('Validation error:', error);
        showNotification('Validation failed: ' + error.message, 'error');
        hideLoading();
    }
}

// Display quality score
function displayQualityScore(qualityScore) {
    const section = document.getElementById('qualityScoreSection');
    section.classList.remove('hidden');

    document.getElementById('overallScore').textContent = Math.round(qualityScore.overall_score);
    document.getElementById('nullScore').textContent = `${qualityScore.scores.null_score}/100`;
    document.getElementById('duplicateScore').textContent = `${qualityScore.scores.duplicate_score}/100`;
    document.getElementById('typeScore').textContent = `${qualityScore.scores.type_score}/100`;
    document.getElementById('anomalyScore').textContent = `${qualityScore.scores.anomaly_score}/100`;
}

// Display validation report
function displayValidationReport(report) {
    // Display anomalies as issues
    if (report.anomalies && report.anomalies.length > 0) {
        const issuesSection = document.getElementById('issuesSection');
        issuesSection.classList.remove('hidden');

        const issuesList = document.getElementById('issuesList2');
        issuesList.innerHTML = '';

        report.anomalies.forEach(anomaly => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${anomaly.type}:</strong> ${anomaly.message}`;
            issuesList.appendChild(li);
        });
    }
}

// Analyze data
async function analyzeData() {
    if (!currentSessionId) {
        showNotification('Please upload data first', 'error');
        return;
    }

    showLoading('Analyzing data...');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: currentSessionId
            })
        });

        const data = await response.json();

        if (data.success) {
            displayStatistics(data.analysis);
            showNotification('Analysis completed!', 'success');
            hideLoading();
        } else {
            showNotification(data.error || 'Analysis failed', 'error');
            hideLoading();
        }
    } catch (error) {
        console.error('Analysis error:', error);
        showNotification('Analysis failed: ' + error.message, 'error');
        hideLoading();
    }
}

// Display statistics
function displayStatistics(analysis) {
    const section = document.getElementById('statisticsSection');
    section.classList.remove('hidden');

    const container = document.getElementById('statsContainer');
    container.innerHTML = '';

    const stats = analysis.summary_stats || {};

    for (const [column, stats_data] of Object.entries(stats)) {
        const card = document.createElement('div');
        card.className = 'stat-card';

        let html = `<h4>${column}</h4>`;
        for (const [key, value] of Object.entries(stats_data)) {
            html += `<div class="stat-row">
                        <span class="stat-label">${key}</span>
                        <span class="stat-value">${value}</span>
                    </div>`;
        }

        card.innerHTML = html;
        container.appendChild(card);
    }
}

// Visualize data
async function visualizeData() {
    if (!currentSessionId) {
        showNotification('Please upload data first', 'error');
        return;
    }

    showLoading('Generating visualizations...');

    try {
        const response = await fetch('/api/visualize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: currentSessionId
            })
        });

        const data = await response.json();

        if (data.success) {
            displayVisualizations(data.images);
            showNotification('Visualizations generated!', 'success');
            hideLoading();
        } else {
            showNotification(data.error || 'Visualization failed', 'error');
            hideLoading();
        }
    } catch (error) {
        console.error('Visualization error:', error);
        showNotification('Visualization failed: ' + error.message, 'error');
        hideLoading();
    }
}

// Display visualizations
function displayVisualizations(images) {
    const section = document.getElementById('visualizationsSection');
    section.classList.remove('hidden');

    if (images.correlation_heatmap) {
        document.getElementById('correlationHeatmap').src = `data:image/png;base64,${images.correlation_heatmap}`;
    }
    if (images.null_heatmap) {
        document.getElementById('nullHeatmap').src = `data:image/png;base64,${images.null_heatmap}`;
    }
    if (images.missing_data) {
        document.getElementById('missingDataChart').src = `data:image/png;base64,${images.missing_data}`;
    }
    if (images.data_types) {
        document.getElementById('dataTypesChart').src = `data:image/png;base64,${images.data_types}`;
    }
}

// ============ EXPORT FUNCTIONALITY ============

// Export data in selected format
async function exportData() {
    if (!currentSessionId) {
        showNotification('Please upload and clean data first', 'error');
        return;
    }

    const format = document.getElementById('exportFormat').value;
    
    showLoading(`Exporting data as ${format.toUpperCase()}...`);

    try {
        const response = await fetch('/api/export/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: currentSessionId,
                format: format
            })
        });

        if (response.ok) {
            const blob = await response.blob();
            const ext = getFileExtension(format);
            downloadFile(blob, `cleaned_data.${ext}`);
            showNotification(`Data exported as ${format.toUpperCase()} successfully!`, 'success');
            hideLoading();
        } else {
            showNotification('Export failed', 'error');
            hideLoading();
        }
    } catch (error) {
        console.error('Export error:', error);
        showNotification('Export failed: ' + error.message, 'error');
        hideLoading();
    }
}

// Get file extension for format
function getFileExtension(format) {
    const extensions = {
        'csv': 'csv',
        'excel': 'xlsx',
        'xlsx': 'xlsx',
        'json': 'json',
        'tsv': 'tsv',
        'html': 'html',
        'parquet': 'parquet'
    };
    return extensions[format] || format;
}

// Export CSV (legacy function)
async function exportCSV() {
    document.getElementById('exportFormat').value = 'csv';
    await exportData();
}

// Export report
async function exportReport(format) {
    if (!currentSessionId) {
        showNotification('Please upload and analyze data first', 'error');
        return;
    }

    showLoading(`Generating ${format.toUpperCase()} report...`);

    try {
        const response = await fetch('/api/export/report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: currentSessionId,
                format: format
            })
        });

        if (response.ok) {
            const blob = await response.blob();
            const filename = format === 'html' ? 'report.html' : 'report.md';
            downloadFile(blob, filename);
            showNotification('Report exported successfully!', 'success');
            hideLoading();
        } else {
            showNotification('Export failed', 'error');
            hideLoading();
        }
    } catch (error) {
        console.error('Export error:', error);
        showNotification('Export failed: ' + error.message, 'error');
        hideLoading();
    }
}

// Download file
function downloadFile(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    showTab('upload');
    // Check server features (optional export engines) and adjust UI
    (async function(){
        try{
            const res = await fetch('/api/features');
            if (!res.ok) return;
            const data = await res.json();
            const support = data.export_support || {};
            // Disable Excel option if not supported
            if (!support.excel) {
                const opt = document.querySelector('#exportFormat option[value="excel"]');
                if (opt) {
                    opt.disabled = true;
                    opt.textContent += ' (unavailable)';
                }
            }
            // Disable Parquet option if not supported
            if (!support.parquet) {
                const optp = document.querySelector('#exportFormat option[value="parquet"]');
                if (optp) {
                    optp.disabled = true;
                    optp.textContent += ' (unavailable)';
                }
            }
            // Notify user if any optional exporters are unavailable
            const unavailable = [];
            if (!support.excel) unavailable.push('Excel');
            if (!support.parquet) unavailable.push('Parquet');
            if (unavailable.length > 0) {
                showNotification(`Optional exporters unavailable: ${unavailable.join(', ')}. Install server dependencies for full support.`, 'info');
            }
        } catch (e) {
            console.warn('Could not fetch server features:', e);
        }
    })();
});
