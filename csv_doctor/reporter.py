"""
reporter.py - Generate analysis reports (Markdown and HTML)
"""

import pandas as pd
from datetime import datetime
from utils import sanitize_dict


class CSVReporter:
    """Generate reports from CSV analysis"""
    
    def __init__(self, df, filename="unknown"):
        """
        Initialize the reporter
        
        Args:
            df: pandas DataFrame
            filename: Name of the CSV file
        """
        self.df = df
        self.filename = filename
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_markdown_report(self, analysis_data, validation_data):
        """
        Generate Markdown report with analysis results
        
        Args:
            analysis_data: Dictionary from analyzer
            validation_data: Dictionary from validator
        
        Returns:
            Markdown formatted report string
        """
        report = []
        
        # Header
        report.append(f"# CSV Doctor - Analysis Report")
        report.append(f"\n**File:** {self.filename}")
        report.append(f"\n**Generated:** {self.timestamp}")
        report.append("\n" + "---" + "\n")
        
        # Executive Summary
        report.append("## 📊 Executive Summary\n")
        overview = analysis_data.get('overview', {})
        quality_score = validation_data.get('quality_score', {})
        
        report.append(f"- **Total Rows:** {overview.get('total_rows', 0):,}")
        report.append(f"- **Total Columns:** {overview.get('total_columns', 0)}")
        report.append(f"- **Data Quality Score:** {quality_score.get('overall_score', 0)}/100")
        report.append(f"- **Null Values:** {overview.get('null_cells', 0):,} ({overview.get('null_percentage', 0)}%)")
        report.append(f"- **Duplicate Rows:** {overview.get('duplicate_rows', 0):,}")
        report.append("\n" + "---" + "\n")
        
        # Column Overview
        report.append("## 📋 Column Overview\n")
        report.append("| Column | Type | Unique Values | Nulls | Null % |")
        report.append("|--------|------|---------------|-------|--------|")
        
        column_types = validation_data.get('column_types', {})
        for col, info in column_types.items():
            report.append(f"| {col} | {info.get('inferred_type', 'unknown')} | "
                         f"{info.get('unique_values', 0)} | "
                         f"{info.get('null_count', 0)} | "
                         f"{info.get('null_percentage', 0)}% |")
        
        report.append("\n" + "---" + "\n")
        
        # Summary Statistics
        if 'summary_stats' in analysis_data:
            report.append("## 📈 Summary Statistics\n")
            stats = analysis_data['summary_stats']
            
            for col, col_stats in stats.items():
                report.append(f"\n### {col}\n")
                report.append(f"| Metric | Value |")
                report.append("|--------|-------|")
                report.append(f"| Count | {col_stats.get('count', 0)} |")
                report.append(f"| Mean | {col_stats.get('mean', 0)} |")
                report.append(f"| Median | {col_stats.get('median', 0)} |")
                report.append(f"| Std Dev | {col_stats.get('std_dev', 0)} |")
                report.append(f"| Min | {col_stats.get('min', 0)} |")
                report.append(f"| Max | {col_stats.get('max', 0)} |")
                report.append(f"| 25% Quartile | {col_stats.get('q25', 0)} |")
                report.append(f"| 75% Quartile | {col_stats.get('q75', 0)} |")
            
            report.append("\n" + "---" + "\n")
        
        # Null Distribution
        report.append("## 🔍 Null Value Distribution\n")
        null_dist = analysis_data.get('null_distribution', {})
        
        report.append("| Column | Null Count | Null % | Non-Null Count |")
        report.append("|--------|-----------|--------|--------|")
        
        for col, null_info in null_dist.items():
            if col == 'total':
                continue
            report.append(f"| {col} | {null_info.get('null_count', 0)} | "
                         f"{null_info.get('null_percentage', 0)}% | "
                         f"{null_info.get('non_null_count', 0)} |")
        
        report.append("\n" + "---" + "\n")
        
        # Correlation Analysis
        if 'high_correlations' in analysis_data and analysis_data['high_correlations']:
            report.append("## 🔗 High Correlations\n")
            report.append("| Column 1 | Column 2 | Correlation |")
            report.append("|----------|----------|-------------|")
            
            for corr in analysis_data['high_correlations'][:10]:
                report.append(f"| {corr.get('column_1', '')} | {corr.get('column_2', '')} | "
                             f"{corr.get('correlation', 0)} |")
            
            report.append("\n" + "---" + "\n")
        
        # Data Quality Issues
        if 'anomalies' in validation_data and validation_data['anomalies']:
            report.append("## ⚠️ Data Quality Issues\n")
            
            for idx, anomaly in enumerate(validation_data['anomalies'][:10], 1):
                report.append(f"\n{idx}. **{anomaly.get('type', 'Unknown')}**")
                report.append(f"   - Column: {anomaly.get('column', 'N/A')}")
                report.append(f"   - {anomaly.get('message', '')}")
            
            report.append("\n" + "---" + "\n")
        
        # Duplicates
        duplicates = validation_data.get('duplicates', {})
        report.append("## 🔄 Duplicate Analysis\n")
        report.append(f"- **Duplicate Rows:** {duplicates.get('duplicate_count', 0)} "
                     f"({duplicates.get('duplicate_percentage', 0)}%)")
        report.append(f"- **Unique Duplicate Sets:** {duplicates.get('duplicate_rows', 0)}")
        report.append("\n" + "---" + "\n")
        
        # Data Quality Score Details
        report.append("## 🎯 Quality Score Breakdown\n")
        scores = quality_score.get('scores', {})
        
        report.append("| Category | Score |")
        report.append("|----------|-------|")
        report.append(f"| Null Score | {scores.get('null_score', 0)}/100 |")
        report.append(f"| Duplicate Score | {scores.get('duplicate_score', 0)}/100 |")
        report.append(f"| Type Consistency | {scores.get('type_score', 0)}/100 |")
        report.append(f"| Anomaly Score | {scores.get('anomaly_score', 0)}/100 |")
        
        report.append("\n" + "---" + "\n")
        
        # Footer
        report.append("\n*Report generated by CSV Doctor - Smart CSV Cleaner and Analyzer*")
        
        return "\n".join(report)
    
    def generate_html_report(self, markdown_report):
        """
        Generate HTML report from Markdown
        
        Args:
            markdown_report: Markdown report string
        
        Returns:
            HTML formatted report string
        """
        # Simple HTML conversion from Markdown
        html = markdown_report
        
        # Convert headers
        html = html.replace("# ", "<h1>").replace("\n", "</h1>\n") if "# " in html else html
        html = html.replace("## ", "<h2>").replace("\n", "</h2>\n") if "## " in html else html
        html = html.replace("### ", "<h3>").replace("\n", "</h3>\n") if "### " in html else html
        
        # Convert bold
        import re
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # Convert tables
        lines = html.split('\n')
        in_table = False
        table_html = []
        
        for line in lines:
            if '|' in line and not in_table:
                table_html.append('<table border="1" cellpadding="5" cellspacing="0">')
                in_table = True
            
            if '|' in line and in_table:
                # Skip separator lines
                if '-' in line and '|' in line:
                    continue
                
                cells = line.split('|')[1:-1]  # Remove empty first/last elements
                row_html = '<tr>'
                for cell in cells:
                    cell = cell.strip()
                    row_html += f'<td>{cell}</td>'
                row_html += '</tr>'
                table_html.append(row_html)
            
            elif in_table and '|' not in line:
                table_html.append('</table>')
                in_table = False
            
            if in_table:
                table_html.append(line)
        
        if in_table:
            table_html.append('</table>')
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>CSV Doctor Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }}
                h1 {{
                    text-align: center;
                    color: #3498db;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }}
                td {{
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                ul {{
                    list-style-position: inside;
                }}
                li {{
                    margin: 8px 0;
                }}
                strong {{
                    color: #2c3e50;
                }}
                hr {{
                    border: none;
                    border-top: 2px solid #ecf0f1;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 12px;
                    margin-top: 40px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                {html}
                <div class="footer">
                    <p>Report generated by CSV Doctor - Smart CSV Cleaner and Analyzer</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def generate_summary_statistics_table(self, stats):
        """
        Generate formatted statistics table
        
        Args:
            stats: Dictionary of statistics
        
        Returns:
            Markdown formatted table
        """
        table = "| Statistic | Value |\n|-----------|-------|\n"
        
        for key, value in stats.items():
            table += f"| {key} | {value} |\n"
        
        return table
