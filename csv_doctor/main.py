"""
main.py - Flask application for CSV Doctor
Entry point with routes for upload, clean, analyze, and export
"""

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import os
import json
from pathlib import Path
from werkzeug.utils import secure_filename
import traceback

from csv_loader import CSVLoader
from cleaner import CSVCleaner
from validator import CSVValidator
from analyzer import CSVAnalyzer
from reporter import CSVReporter
from visualizer import CSVVisualizer
from utils import (
    create_upload_dir, get_file_path, safe_filename, 
    format_bytes, sanitize_dict
)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload directory
create_upload_dir()

# Detect optional export engines
def _detect_optional_export_engines():
    engines = {
        'excel': False,
        'parquet': False
    }
    try:
        import openpyxl  # noqa: F401
        engines['excel'] = True
    except Exception:
        engines['excel'] = False

    try:
        import pyarrow  # noqa: F401
        engines['parquet'] = True
    except Exception:
        engines['parquet'] = False

    return engines

# Store export support info in app config
app.config['EXPORT_SUPPORT'] = _detect_optional_export_engines()

# Global storage for session data
sessions = {}


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handle CSV file upload
    
    Returns:
        JSON with upload status and file information
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Save file with timestamp
        filename = safe_filename(file.filename)
        filepath = get_file_path(filename)
        file.save(str(filepath))
        
        # Load and validate CSV
        loader = CSVLoader(str(filepath))
        df = loader.load()
        
        metadata = loader.get_metadata()
        validation = loader.validate_structure()
        
        # Store in session
        session_id = f"session_{safe_filename(file.filename).replace('.csv', '')}"
        sessions[session_id] = {
            'filepath': str(filepath),
            'df': df,
            'original_df': df.copy(),
            'filename': file.filename,
            'metadata': metadata
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'filename': file.filename,
            'metadata': metadata,
            'validation': validation,
            'sample': loader.get_sample()
        })
    
    except Exception as e:
        print(f"Upload error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/clean', methods=['POST'])
def clean_data():
    """
    Clean CSV data based on provided options
    
    Returns:
        JSON with cleaning results
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 400
        
        df = sessions[session_id]['df'].copy()
        cleaner = CSVCleaner(df)
        
        # Apply cleaning operations based on options
        options = data.get('options', {})
        
        if options.get('remove_empty_rows'):
            cleaner.remove_empty_rows()
        
        if options.get('remove_empty_columns'):
            cleaner.remove_empty_columns()
        
        if options.get('trim_whitespace'):
            cleaner.trim_whitespace()
        
        if options.get('remove_duplicates'):
            cleaner.remove_duplicates()
        
        if options.get('standardize_column_names'):
            cleaner.standardize_column_names()
        
        if options.get('fill_missing'):
            fill_method = options.get('fill_method', 'mean')
            cleaner.fill_missing_values(method=fill_method)
        
        if options.get('normalize_text_case'):
            case = options.get('text_case', 'lower')
            cleaner.normalize_text_case(case=case)
        
        if options.get('remove_outliers'):
            outlier_method = options.get('outlier_method', 'iqr')
            cleaner.remove_outliers(method=outlier_method)
        
        # Get cleaned dataframe
        cleaned_df = cleaner.get_cleaned_df()
        
        # Update session
        sessions[session_id]['df'] = cleaned_df
        sessions[session_id]['changes'] = cleaner.get_changes()
        
        return jsonify({
            'success': True,
            'changes': cleaner.get_changes(),
            'new_shape': {
                'rows': len(cleaned_df),
                'columns': len(cleaned_df.columns)
            },
            'sample': cleaned_df.head().to_dict('records')
        })
    
    except Exception as e:
        print(f"Clean error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate', methods=['POST'])
def validate_data():
    """
    Validate CSV data quality
    
    Returns:
        JSON with validation report
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 400
        
        df = sessions[session_id]['df']
        validator = CSVValidator(df)
        
        # Generate reports
        validation_report = validator.generate_validation_report()
        quality_score = validator.get_data_quality_score()
        
        return jsonify({
            'success': True,
            'validation_report': sanitize_dict(validation_report),
            'quality_score': sanitize_dict(quality_score)
        })
    
    except Exception as e:
        print(f"Validation error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """
    Analyze CSV data
    
    Returns:
        JSON with analysis results
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 400
        
        df = sessions[session_id]['df']
        analyzer = CSVAnalyzer(df)
        
        # Generate analysis report
        analysis_report = analyzer.generate_analysis_report()
        
        return jsonify({
            'success': True,
            'analysis': sanitize_dict(analysis_report)
        })
    
    except Exception as e:
        print(f"Analysis error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualize', methods=['POST'])
def visualize_data():
    """
    Generate visualizations
    
    Returns:
        JSON with base64 encoded images
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 400
        
        df = sessions[session_id]['df']
        visualizer = CSVVisualizer(df)
        
        # Generate dashboard images
        images = visualizer.generate_dashboard_images()
        
        return jsonify({
            'success': True,
            'images': images
        })
    
    except Exception as e:
        print(f"Visualization error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/data', methods=['POST'])
def export_data():
    """
    Export cleaned data in multiple formats
    
    Returns:
        File download in requested format
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        export_format = data.get('format', 'csv').lower()  # csv, excel, json, parquet, html
        
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 400
        
        df = sessions[session_id]['df']
        filename = sessions[session_id]['filename']
        base_name = filename.replace('.csv', '')
        
        if export_format == 'csv':
            export_filename = f"cleaned_{base_name}.csv"
            export_path = get_file_path(export_filename)
            df.to_csv(export_path, index=False)
            mimetype = 'text/csv'
            
        elif export_format == 'excel' or export_format == 'xlsx':
            export_filename = f"cleaned_{base_name}.xlsx"
            export_path = get_file_path(export_filename)
            df.to_excel(export_path, index=False, sheet_name='Data')
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
        elif export_format == 'json':
            export_filename = f"cleaned_{base_name}.json"
            export_path = get_file_path(export_filename)
            # Use sanitize_dict to ensure JSON serialization works
            safe_df = sanitize_dict(df.to_dict('records'))
            with open(export_path, 'w') as f:
                json.dump(safe_df, f, indent=2)
            mimetype = 'application/json'
            
        elif export_format == 'parquet':
            export_filename = f"cleaned_{base_name}.parquet"
            export_path = get_file_path(export_filename)
            df.to_parquet(export_path, index=False)
            mimetype = 'application/octet-stream'
            
        elif export_format == 'html':
            export_filename = f"cleaned_{base_name}.html"
            export_path = get_file_path(export_filename)
            html_content = df.to_html(index=False)
            # Wrap in basic HTML structure
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{export_filename}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #3498db; color: white; }}
                    tr:nth-child(even) {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h1>Cleaned Data: {base_name}</h1>
                <p>Total Rows: {len(df)} | Total Columns: {len(df.columns)}</p>
                {html_content}
            </body>
            </html>
            """
            with open(export_path, 'w') as f:
                f.write(full_html)
            mimetype = 'text/html'
            
        elif export_format == 'tsv':
            export_filename = f"cleaned_{base_name}.tsv"
            export_path = get_file_path(export_filename)
            df.to_csv(export_path, index=False, sep='\t')
            mimetype = 'text/tab-separated-values'
            
        else:
            return jsonify({'error': f'Unsupported format: {export_format}'}), 400
        
        return send_file(
            str(export_path),
            as_attachment=True,
            download_name=export_filename,
            mimetype=mimetype
        )
    
    except Exception as e:
        print(f"Export error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/features', methods=['GET'])
def get_features():
    """Return available optional features (e.g., export support)"""
    try:
        return jsonify({'export_support': app.config.get('EXPORT_SUPPORT', {})})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/csv', methods=['POST'])
def export_csv():
    """
    Legacy endpoint: Export cleaned CSV (redirects to /api/export/data)
    
    Returns:
        CSV file download
    """
    try:
        data = request.get_json()
        data['format'] = 'csv'
        
        # Create a request context for the new endpoint
        with app.test_request_context(
            '/api/export/data',
            method='POST',
            data=json.dumps(data),
            content_type='application/json'
        ):
            return export_data()
    
    except Exception as e:
        print(f"CSV Export error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/report', methods=['POST'])
def export_report():
    """
    Export analysis report (Markdown or HTML)
    
    Returns:
        Report file download
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        report_format = data.get('format', 'md')  # 'md' or 'html'
        
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 400
        
        df = sessions[session_id]['df']
        filename = sessions[session_id]['filename']
        
        # Generate analysis and validation
        analyzer = CSVAnalyzer(df)
        validator = CSVValidator(df)
        
        analysis_report = analyzer.generate_analysis_report()
        validation_report = validator.generate_validation_report()
        quality_score = validator.get_data_quality_score()
        validation_report['quality_score'] = quality_score
        
        # Generate report
        reporter = CSVReporter(df, filename)
        markdown_report = reporter.generate_markdown_report(analysis_report, validation_report)
        
        # Save report
        if report_format == 'html':
            html_report = reporter.generate_html_report(markdown_report)
            report_filename = f"report_{filename.replace('.csv', '.html')}"
            export_path = get_file_path(report_filename)
            
            with open(export_path, 'w') as f:
                f.write(html_report)
            
            return send_file(
                str(export_path),
                as_attachment=True,
                download_name=report_filename,
                mimetype='text/html'
            )
        else:
            report_filename = f"report_{filename.replace('.csv', '.md')}"
            export_path = get_file_path(report_filename)
            
            with open(export_path, 'w') as f:
                f.write(markdown_report)
            
            return send_file(
                str(export_path),
                as_attachment=True,
                download_name=report_filename,
                mimetype='text/markdown'
            )
    
    except Exception as e:
        print(f"Report Export error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session_info(session_id):
    """Get information about a session"""
    try:
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 404
        
        session_data = sessions[session_id]
        df = session_data['df']
        
        return jsonify({
            'session_id': session_id,
            'filename': session_data['filename'],
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 50MB'}), 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Create necessary directories
    Path('uploads').mkdir(exist_ok=True)
    
    # Run Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)
