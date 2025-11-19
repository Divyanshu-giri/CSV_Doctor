# 🎉 CSV Doctor - Installation & Execution Guide

## Project Statistics

- **Total Code**: 3,700+ lines
- **Python Modules**: 8 files (cleaner, validator, analyzer, etc.)
- **Frontend Files**: 3 files (HTML, CSS, JavaScript)
- **Documentation**: 5 comprehensive guides
- **Sample Data**: 2 datasets ready to test
- **Core Features**: 25+ data operations

---

## ✅ Pre-Installation Checklist

- [ ] Python 3.8 or higher installed
- [ ] pip package manager available
- [ ] 100MB+ free disk space
- [ ] Network access for package downloads
- [ ] Text editor or IDE (VS Code recommended)

---

## 🔧 Installation Steps

### Step 1: Verify Python Installation

```bash
python3 --version
# Should output Python 3.8.0 or higher
```

If not installed, download from: https://www.python.org/downloads/

### Step 2: Navigate to Project

```bash
cd /workspaces/CSV_Doctor
```

### Step 3: Create Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed Flask-3.0.0 pandas-2.0.3 numpy-1.24.3 ...
```

### Step 5: Verify Installation

```bash
python -c "import flask, pandas, numpy, matplotlib, seaborn; print('✅ All packages installed!')"
```

---

## 🚀 Running the Application

### Option 1: Simple Start

```bash
cd csv_doctor
python main.py
```

### Option 2: With Custom Port

```bash
cd csv_doctor
python main.py --port 8000
```

### Option 3: Using Setup Script

```bash
bash setup.sh
cd csv_doctor
python main.py
```

### Expected Output

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
WARNING: This is a development server. Do not use it in production.
 * Restarting with reloader
 * Debugger is active!
```

---

## 🌐 Access the Application

Open your web browser and visit:

**http://localhost:5000**

Or if using custom port:

**http://localhost:8000**

---

## 🧪 Test the Application

### Test 1: Upload Sample Data

1. Go to **Upload** tab
2. Drag and drop: `csv_doctor/assets/sample_sales_data.csv`
3. Verify: Should show 25 rows, 9 columns
4. ✅ Validation: No critical issues (some empty cells expected)

### Test 2: Clean Data

1. Go to **Clean** tab
2. Enable these options:
   - ☑️ Remove Empty Rows
   - ☑️ Trim Whitespace
   - ☑️ Remove Duplicates
   - ☑️ Standardize Column Names
3. Click **Clean Data**
4. ✅ Should show changes made

### Test 3: Validate Data

1. Go to **Analyze** tab
2. Click **Validate Data**
3. ✅ Should see Quality Score (typically 70-85)

### Test 4: Analyze Statistics

1. Click **Analyze Statistics**
2. ✅ Should display stats for numeric columns

### Test 5: Generate Visualizations

1. Click **Generate Visualizations**
2. ✅ Should display 4 charts

### Test 6: Export Results

1. Go to **Export** tab
2. Click **Download CSV**
3. ✅ Should download `cleaned_sample_sales_data.csv`
4. Click **Download HTML**
5. ✅ Should download `report_sample_sales_data.html`

---

## 📊 Sample Data Reference

### sample_sales_data.csv
- **Rows**: 25 products
- **Columns**: product_id, product_name, category, price, quantity_sold, rating, date, stock_level, supplier_id
- **Issues**: Missing price (row 6), missing stock level (rows 10, 20)
- **Purpose**: E-commerce dataset with missing values

### sample_student_data.csv
- **Rows**: 20 students
- **Columns**: student_id, name, age, gpa, math_score, english_score, science_score, attendance, scholarship
- **Issues**: Missing scores (row 5, 15)
- **Purpose**: Academic dataset with performance metrics

---

## 🔍 Troubleshooting

### Issue: Port 5000 Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Kill process using port 5000
lsof -i :5000
kill -9 <PID>

# Or use different port
python main.py --port 5001
```

### Issue: Module Not Found

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Permission Denied on setup.sh

**Error**: `Permission denied`

**Solution**:
```bash
chmod +x setup.sh
bash setup.sh
```

### Issue: Visualization Not Displaying

**Error**: Empty image boxes in dashboard

**Solution**:
1. Check browser console (F12)
2. Ensure data has numeric columns
3. Try with sample_sales_data.csv
4. Restart application

### Issue: File Upload Not Working

**Error**: Upload hangs or fails

**Solution**:
1. Check file is actual CSV (not .xlsx or .txt)
2. File size < 50MB
3. No special characters in filename
4. Try sample data first

### Issue: Large File Processing

**Error**: Browser timeout or crash

**Solution**:
1. Split large files
2. Open in text editor, save as proper CSV
3. Remove unnecessary columns
4. Process in chunks

---

## 📁 File Locations

### Important Directories

| Path | Purpose |
|------|---------|
| `/workspaces/CSV_Doctor/` | Project root |
| `/workspaces/CSV_Doctor/csv_doctor/` | Application code |
| `/workspaces/CSV_Doctor/csv_doctor/main.py` | Flask app start here |
| `/workspaces/CSV_Doctor/csv_doctor/uploads/` | Uploaded files stored here |
| `/workspaces/CSV_Doctor/csv_doctor/assets/` | Sample CSV files |
| `/workspaces/CSV_Doctor/csv_doctor/templates/` | HTML templates |
| `/workspaces/CSV_Doctor/csv_doctor/static/` | CSS & JavaScript |

---

## 🛠️ Development Commands

### Run with Debug Enabled

```bash
cd csv_doctor
export FLASK_ENV=development
export FLASK_DEBUG=1
python main.py
```

### Run with Logging

```bash
cd csv_doctor
python -u main.py 2>&1 | tee app.log
```

### Test Individual Module

```bash
python -c "
from csv_loader import CSVLoader
loader = CSVLoader('assets/sample_sales_data.csv')
df = loader.load()
print(f'✅ Loaded {len(df)} rows, {len(df.columns)} columns')
"
```

### Interactive Python Shell

```bash
python
>>> from csv_doctor import *
>>> loader = CSVLoader('csv_doctor/assets/sample_sales_data.csv')
>>> df = loader.load()
>>> print(df.head())
```

---

## 📊 API Testing

### Test Upload Endpoint

```bash
curl -X POST -F "file=@csv_doctor/assets/sample_sales_data.csv" http://localhost:5000/api/upload
```

### Test Session Info

```bash
curl http://localhost:5000/api/session/session_sample_sales_data
```

---

## 🎯 Next Steps After Installation

1. **Read the Docs**
   - `README_COMPLETE.md` - Full documentation
   - `MODULES.md` - API reference
   - `PROJECT_STRUCTURE.md` - Architecture overview

2. **Explore the Code**
   - Start with `main.py`
   - Review module docstrings
   - Examine sample data

3. **Try All Features**
   - Upload different CSV files
   - Try all cleaning operations
   - Generate reports
   - Export in different formats

4. **Customize**
   - Add new cleaning functions
   - Create custom analyses
   - Modify visualizations

5. **Deploy**
   - Consider production server (Gunicorn)
   - Add database backend
   - Implement user authentication

---

## 🚀 Performance Tips

### For Large Files
```python
# In main.py, increase max file size
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### For Better Performance
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 main:app
```

### Memory Monitoring
```bash
# Check memory usage
ps aux | grep python
```

---

## 📱 Browser Compatibility

✅ **Recommended**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

⚠️ **May have issues**
- IE 11
- Old mobile browsers

---

## 🔐 Security Notes

- Application is for **local use only**
- Do NOT expose to internet without authentication
- File uploads are stored in `/uploads` directory
- Consider adding rate limiting for production
- Implement CORS policies if needed

---

## 📞 Quick Reference

| Action | Command |
|--------|---------|
| Start app | `python main.py` |
| Install deps | `pip install -r requirements.txt` |
| Run tests | `python -m pytest` |
| Check Python | `python3 --version` |
| View help | `python main.py --help` |
| Stop app | `Ctrl+C` |

---

## ✨ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] Application starts without errors
- [ ] Web interface loads at localhost:5000
- [ ] Sample CSV uploads successfully
- [ ] Can perform cleaning operations
- [ ] Validation/Analysis works
- [ ] Visualizations display
- [ ] Can export reports
- [ ] Can access documentation

---

## 🎉 You're All Set!

If you see the CSV Doctor interface in your browser, **Installation is complete!**

Start by uploading a sample CSV file and exploring the features.

**Happy data cleaning! 🏥💊**

---

## 📚 Documentation Quick Links

- **[Quick Start](QUICKSTART.md)** - 5 minute setup
- **[Complete README](README_COMPLETE.md)** - Full features
- **[Module Guide](MODULES.md)** - API reference
- **[Project Structure](PROJECT_STRUCTURE.md)** - Architecture

---

**Need Help?**
- Check error messages in browser console (F12)
- Review troubleshooting section above
- Examine sample data first
- Check documentation files
- Review module docstrings in code
