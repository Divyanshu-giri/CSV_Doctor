# 🏥 CSV Doctor - Smart CSV Cleaner and Analyzer

A comprehensive, student-friendly web application for cleaning, validating, analyzing, and visualizing CSV files. CSV Doctor helps you transform messy data into insights with an intuitive interface and powerful backend.

## ✨ Key Features

### 🧹 **CSV Cleaning**
- **Remove empty rows and columns** - Delete rows where all values are null
- **Trim whitespace** - Remove leading/trailing spaces from headers and values
- **Detect and fix inconsistent delimiters** - Auto-detect CSV format
- **Normalize date and number formats** - Standardize data types
- **Handle missing values** - Fill nulls using mean, median, mode, or forward/backward fill
- **Identify and remove duplicates** - Keep data unique
- **Standardize column names** - Convert to lowercase, remove spaces and special chars
- **Normalize text case** - Convert to lowercase, uppercase, or title case
- **Remove outliers** - Detect anomalous rows using IQR or Z-score methods

### ✅ **CSV Validation**
- **Detect malformed rows** - Identify rows with missing values
- **Check column types** - Infer and validate data types
- **Validate against schema** - Compare with expected structure
- **Flag anomalies** - Detect constant columns, high null percentages, unusual distributions
- **Generate quality score** - Overall data quality assessment (0-100)

### 📊 **CSV Analysis**
- **Generate descriptive statistics** - Mean, median, mode, std dev, min, max, quartiles
- **Infer column types** - Automatically detect numeric, categorical, datetime, text
- **Frequency distribution** - Analyze value counts for categorical columns
- **Correlation matrix** - Find relationships between numeric columns
- **Null value heatmap visualization** - Visual representation of missing data
- **Data quality insights** - Comprehensive analysis report

### 💡 **Smart Suggestions**
- **Recommend clearer column names** - Based on current naming patterns
- **Suggest transformations** - Log scale, binning, normalization recommendations
- **Flag suspicious patterns** - Repeated identical values, impossible ranges
- **Data quality tips** - Actionable recommendations for improvement

### 📤 **Export Options**
- **Download cleaned CSV** - Save processed data
- **Export Markdown report** - Summary with tables and statistics
- **Export HTML report** - Interactive, styled report with full analysis
- **Generate visualizations** - Correlation heatmaps, histograms, bar charts

### 🎨 **Friendly UX**
- **Drag-and-drop CSV upload** - Easy file selection
- **Toggle switches for cleaning options** - Granular control
- **Visual summary dashboard** - Real-time insights
- **"Fix All" button with preview** - One-click cleaning
- **Responsive design** - Works on desktop and mobile

## 📁 Project Structure

```
csv_doctor/
│
├── main.py                  # Flask entry point with routes
├── csv_loader.py            # Load and parse CSV files
├── cleaner.py               # Data cleaning functions
├── validator.py             # Data validation functions
├── analyzer.py              # Statistical analysis functions
├── reporter.py              # Generate reports (Markdown/HTML)
├── visualizer.py            # Create visualizations
├── utils.py                 # Shared helper functions
│
├── templates/
│   └── index.html          # Main UI template
│
├── static/
│   ├── style.css           # Frontend styling
│   └── script.js           # Frontend logic
│
└── assets/
    ├── sample_sales_data.csv      # Sample dataset 1
    └── sample_student_data.csv    # Sample dataset 2
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project**
```bash
cd /workspaces/CSV_Doctor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
cd csv_doctor
python main.py
```

4. **Open in browser**
```
http://localhost:5000
```

## 📚 Usage Guide

### Step 1: Upload CSV
1. Go to the **Upload** tab
2. Drag and drop a CSV file or click to select
3. View file information and sample data
4. Check for any validation issues

### Step 2: Clean Data
1. Go to the **Clean** tab
2. Select cleaning operations:
   - Toggle switches for predefined operations
   - Configure options for filling missing values, removing outliers, etc.
3. Click **Clean Data** to apply changes
4. Review the cleaning summary

### Step 3: Validate & Analyze
1. Go to the **Analyze** tab
2. Click **Validate Data** to check data quality
3. View quality score breakdown (0-100)
4. Click **Analyze Statistics** for descriptive statistics
5. Click **Generate Visualizations** for dashboard

### Step 4: Export Results
1. Go to the **Export** tab
2. Download cleaned CSV, Markdown report, or HTML report
3. Share results with stakeholders

## 🔧 API Endpoints

### Upload
- **POST** `/api/upload` - Upload and parse CSV file

### Cleaning
- **POST** `/api/clean` - Apply cleaning operations

### Validation
- **POST** `/api/validate` - Validate data quality

### Analysis
- **POST** `/api/analyze` - Generate statistical analysis

### Visualization
- **POST** `/api/visualize` - Generate charts and heatmaps

### Export
- **POST** `/api/export/csv` - Download cleaned CSV
- **POST** `/api/export/report` - Download report (markdown/html)

## 📊 Data Quality Score Calculation

The quality score (0-100) is calculated from:
- **Null Score (30%)** - Percentage of missing values
- **Duplicate Score (20%)** - Percentage of duplicate rows
- **Type Consistency (20%)** - Consistency of data types
- **Anomaly Score (30%)** - Absence of unusual patterns

## 🎨 Sample Visualizations

- **Correlation Heatmap** - Shows relationships between numeric columns
- **Null Heatmap** - Visual distribution of missing values
- **Missing Data Chart** - Bar chart of null percentages by column
- **Data Types Chart** - Distribution of data types

## 📦 Dependencies

- **Flask 3.0.0** - Web framework
- **pandas 2.0.3** - Data manipulation
- **numpy 1.24.3** - Numerical computing
- **matplotlib 3.7.2** - Visualization
- **seaborn 0.12.2** - Statistical visualizations
- **scipy 1.11.2** - Scientific computing
- **Werkzeug 3.0.0** - WSGI utilities

## 🎓 Student-Friendly Features

✅ **Modular Code** - Easy to understand and modify
✅ **Clear Comments** - Comprehensive documentation
✅ **Reusable Classes** - Object-oriented design
✅ **Error Handling** - Graceful error messages
✅ **Type Hints** - Code clarity with type annotations
✅ **Sample Data** - Pre-included test datasets
✅ **Responsive UI** - Works on all screen sizes

## 💡 Learning Outcomes

By using CSV Doctor, you'll learn:
- Data cleaning and preprocessing techniques
- Statistical analysis and data visualization
- Flask web application development
- Frontend/backend integration
- Data validation and quality assessment
- Report generation (Markdown/HTML)

## 🐛 Troubleshooting

### File upload limit exceeded
- Maximum file size is 50MB. Split large files into smaller chunks.

### Visualizations not displaying
- Ensure matplotlib and seaborn are properly installed
- Check browser console for JavaScript errors

### "Session not found" error
- Upload a file again - sessions are stored in memory
- Restart the application if needed

### Port 5000 already in use
```bash
python main.py --port 5001
```

## 📝 Sample Workflow

1. **Load Sample Data**
   - Use `csv_doctor/assets/sample_sales_data.csv` or `sample_student_data.csv`

2. **Explore Issues**
   - Upload the file
   - Review validation issues and sample data

3. **Clean the Data**
   - Enable cleaning options as needed
   - Remove empty rows/columns, trim whitespace, handle missing values

4. **Validate Quality**
   - Check data quality score
   - Review identified anomalies

5. **Analyze Statistics**
   - View summary statistics for numeric columns
   - Check correlation between variables

6. **Generate Insights**
   - View visualizations
   - Identify patterns and relationships

7. **Export Results**
   - Download cleaned CSV
   - Export comprehensive HTML or Markdown report

## 🚀 Advanced Features

### Custom Cleaning Functions
Extend `cleaner.py` with domain-specific cleaning logic:
```python
class CSVCleaner:
    def custom_transform(self):
        # Add your custom logic
        pass
```

### Custom Analysis
Add custom analyses to `analyzer.py`:
```python
class CSVAnalyzer:
    def custom_analysis(self):
        # Add your analysis
        pass
```

### Custom Visualizations
Create new visualizations in `visualizer.py`:
```python
class CSVVisualizer:
    def plot_custom_chart(self):
        # Create your visualization
        pass
```

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Improve documentation
- Optimize code

## ❓ FAQ

**Q: Can I upload multiple files at once?**
A: Currently, one file at a time. You can upload and process multiple files sequentially.

**Q: What's the maximum file size?**
A: 50MB. For larger files, consider splitting them.

**Q: Can I use custom delimiters?**
A: Yes, the CSV loader auto-detects delimiters (`,`, `;`, `\t`, `|`).

**Q: Are uploaded files deleted after processing?**
A: Files are stored in the `uploads/` folder during the session and can be manually deleted.

**Q: Can I integrate CSV Doctor into my own application?**
A: Yes! The modules are modular and can be imported into your own projects.

## 📧 Support

For questions or issues:
1. Check the Troubleshooting section
2. Review the code documentation
3. Examine sample datasets and workflows

---

**Built with ❤️ for students and data enthusiasts**

Happy data cleaning! 🎉
