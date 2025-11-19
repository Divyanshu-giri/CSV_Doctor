# CSV Doctor - Python Module Documentation

## Module Overview

CSV Doctor consists of 7 core Python modules designed to work together for complete CSV processing:

### 1. **csv_loader.py** - CSV File Loading
Responsible for loading and parsing CSV files with automatic format detection.

**Key Classes:**
- `CSVLoader` - Main class for loading CSV files

**Key Methods:**
- `load(encoding, sep)` - Load CSV with auto-delimiter detection
- `validate_structure()` - Check for common issues
- `get_metadata()` - Extract file information
- `get_sample(n)` - Get first n rows

**Example:**
```python
from csv_loader import CSVLoader

loader = CSVLoader('data.csv')
df = loader.load()
metadata = loader.get_metadata()
```

---

### 2. **cleaner.py** - Data Cleaning
Perform various cleaning operations on CSV data.

**Key Classes:**
- `CSVCleaner` - Main class for data cleaning

**Key Methods:**
- `remove_empty_rows()` - Remove all-null rows
- `remove_empty_columns()` - Remove all-null columns
- `trim_whitespace(columns)` - Remove leading/trailing spaces
- `remove_duplicates(subset, keep)` - Remove duplicate rows
- `fill_missing_values(method, columns)` - Fill nulls (mean/median/mode)
- `standardize_column_names()` - Normalize column names
- `normalize_text_case(columns, case)` - Convert text case
- `remove_outliers(columns, method)` - Remove outlier rows
- `get_cleaned_df()` - Return cleaned DataFrame

**Example:**
```python
from cleaner import CSVCleaner

cleaner = CSVCleaner(df)
cleaner.remove_empty_rows()
cleaner.trim_whitespace()
cleaner.fill_missing_values(method='mean')
cleaned_df = cleaner.get_cleaned_df()
```

---

### 3. **validator.py** - Data Validation
Validate data quality and check for issues.

**Key Classes:**
- `CSVValidator` - Main class for data validation

**Key Methods:**
- `detect_malformed_rows()` - Find rows with null values
- `check_column_types()` - Infer and report column types
- `get_null_distribution()` - Analyze null percentages
- `validate_against_schema(schema)` - Compare with expected structure
- `detect_duplicates()` - Count duplicate rows
- `detect_anomalies()` - Find suspicious patterns
- `get_data_quality_score()` - Calculate overall quality (0-100)
- `generate_validation_report()` - Comprehensive report

**Example:**
```python
from validator import CSVValidator

validator = CSVValidator(df)
quality = validator.get_data_quality_score()
issues = validator.detect_anomalies()
```

---

### 4. **analyzer.py** - Statistical Analysis
Perform statistical analysis on CSV data.

**Key Classes:**
- `CSVAnalyzer` - Main class for data analysis

**Key Methods:**
- `get_summary_stats()` - Descriptive statistics for numeric columns
- `get_null_distribution()` - Null value analysis
- `get_correlation_matrix()` - Correlation between columns
- `get_high_correlations(threshold)` - Find correlated pairs
- `get_frequency_distribution(column)` - Value counts
- `get_categorical_summary()` - Summary of categorical columns
- `get_column_insights(column)` - Detailed column analysis
- `get_overall_summary()` - Dataset overview
- `generate_analysis_report()` - Complete analysis

**Example:**
```python
from analyzer import CSVAnalyzer

analyzer = CSVAnalyzer(df)
stats = analyzer.get_summary_stats()
corr = analyzer.get_correlation_matrix()
```

---

### 5. **reporter.py** - Report Generation
Generate analysis reports in Markdown and HTML formats.

**Key Classes:**
- `CSVReporter` - Main class for report generation

**Key Methods:**
- `generate_markdown_report(analysis, validation)` - Markdown report
- `generate_html_report(markdown)` - Convert to HTML with styling
- `generate_summary_statistics_table(stats)` - Format statistics

**Example:**
```python
from reporter import CSVReporter

reporter = CSVReporter(df, 'data.csv')
markdown_report = reporter.generate_markdown_report(analysis, validation)
html_report = reporter.generate_html_report(markdown_report)
```

---

### 6. **visualizer.py** - Data Visualization
Create visualizations using matplotlib and seaborn.

**Key Classes:**
- `CSVVisualizer` - Main class for creating visualizations

**Key Methods:**
- `plot_histogram(column, bins)` - Histogram for numeric data
- `plot_bar_chart(column, top_n)` - Bar chart for categories
- `plot_null_heatmap()` - Heatmap of missing values
- `plot_correlation_heatmap()` - Correlation matrix heatmap
- `plot_box_plot(column)` - Box plot for numeric data
- `plot_scatter(column_x, column_y)` - Scatter plot
- `plot_missing_data()` - Missing data visualization
- `generate_dashboard_images()` - All visualizations at once

**Example:**
```python
from visualizer import CSVVisualizer

viz = CSVVisualizer(df)
images = viz.generate_dashboard_images()
```

---

### 7. **utils.py** - Utility Functions
Shared helper functions used across modules.

**Key Functions:**
- `get_timestamp()` - Generate timestamp strings
- `create_upload_dir()` - Create uploads directory
- `get_file_path(filename)` - Safe file path handling
- `safe_filename(filename)` - Generate safe filenames
- `format_bytes(bytes_size)` - Convert bytes to readable format
- `infer_column_type(series)` - Detect column data type
- `round_floats(obj, decimals)` - Round floats in dicts/lists
- `sanitize_dict(obj)` - Make dicts JSON-serializable

**Example:**
```python
from utils import infer_column_type, safe_filename

col_type = infer_column_type(df['column'])
safe_name = safe_filename('my file (2).csv')
```

---

## Complete Workflow Example

```python
import pandas as pd
from csv_loader import CSVLoader
from cleaner import CSVCleaner
from validator import CSVValidator
from analyzer import CSVAnalyzer
from reporter import CSVReporter
from visualizer import CSVVisualizer

# 1. Load CSV
loader = CSVLoader('sales_data.csv')
df = loader.load()
print(f"Loaded {len(df)} rows")

# 2. Clean Data
cleaner = CSVCleaner(df)
cleaner.remove_empty_rows()
cleaner.trim_whitespace()
cleaner.remove_duplicates()
cleaner.fill_missing_values(method='mean')
df_clean = cleaner.get_cleaned_df()

# 3. Validate Quality
validator = CSVValidator(df_clean)
quality_score = validator.get_data_quality_score()
print(f"Data Quality: {quality_score['overall_score']}/100")

# 4. Analyze Data
analyzer = CSVAnalyzer(df_clean)
analysis = analyzer.generate_analysis_report()

# 5. Generate Visualizations
visualizer = CSVVisualizer(df_clean)
images = visualizer.generate_dashboard_images()

# 6. Create Report
reporter = CSVReporter(df_clean, 'sales_data.csv')
validation = validator.generate_validation_report()
markdown = reporter.generate_markdown_report(analysis, validation)

# 7. Export
df_clean.to_csv('cleaned_sales_data.csv', index=False)
with open('report.md', 'w') as f:
    f.write(markdown)
```

---

## Data Type Inference

CSV Doctor automatically detects column types:
- **numeric** - Integer or floating-point numbers
- **categorical** - Low cardinality text (< 5% unique)
- **datetime** - Date/time formats
- **text** - General string text

This helps optimize cleaning and analysis operations.

---

## Quality Score Components

**Overall Score = 0.3 × Null Score + 0.2 × Duplicate Score + 0.2 × Type Score + 0.3 × Anomaly Score**

- **Null Score**: 100 - null_percentage (higher is better)
- **Duplicate Score**: 100 - duplicate_percentage (higher is better)
- **Type Score**: Based on type consistency across columns
- **Anomaly Score**: 100 - (anomalies × 15) (fewer anomalies is better)

---

## Error Handling

All modules include comprehensive error handling:

```python
try:
    df = loader.load()
except ValueError as e:
    print(f"Error loading file: {e}")
```

---

## Performance Tips

1. **For large files**: Use `chunksize` parameter in pandas
2. **Memory optimization**: Use `memory_usage(deep=True)` to monitor
3. **Visualization**: Limit to first 100 rows for heatmaps
4. **Analysis**: Cache results for repeated operations

---

## Extending CSV Doctor

### Add Custom Cleaning Operation

```python
class CSVCleaner:
    def custom_clean(self):
        # Your logic here
        self.df = self.df[self.df['column'] > 0]
        self.changes.append("Applied custom filter")
        return self
```

### Add Custom Analysis

```python
class CSVAnalyzer:
    def custom_metric(self):
        # Your analysis here
        return custom_result
```

### Add Custom Visualization

```python
class CSVVisualizer:
    def plot_custom(self):
        fig, ax = plt.subplots()
        # Your plotting code
        return self._fig_to_base64(fig)
```

---

## Module Dependencies

```
main.py (Flask routes)
├── csv_loader.py
├── cleaner.py
├── validator.py
├── analyzer.py
├── reporter.py
├── visualizer.py
└── utils.py

External Libraries:
├── pandas (data manipulation)
├── numpy (numerical computing)
├── matplotlib (visualization)
├── seaborn (statistical plots)
├── scipy (statistical functions)
└── Flask (web framework)
```

---

## Testing Modules

```python
# Test CSV Loader
loader = CSVLoader('test_data.csv')
df = loader.load()
assert len(df) > 0

# Test Cleaner
cleaner = CSVCleaner(df)
cleaner.remove_empty_rows()
assert len(cleaner.df) <= len(df)

# Test Validator
validator = CSVValidator(df)
score = validator.get_data_quality_score()
assert 0 <= score['overall_score'] <= 100

# Test Analyzer
analyzer = CSVAnalyzer(df)
stats = analyzer.get_summary_stats()
assert isinstance(stats, dict)
```

---

**CSV Doctor - Making Data Cleaning Simple! 🏥**
