# 🚀 Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
cd /workspaces/CSV_Doctor
pip install -r requirements.txt
```

### 2. Run the Application
```bash
cd csv_doctor
python main.py
```

### 3. Open in Browser
Visit: **http://localhost:5000**

---

## 📝 First Steps

### Test with Sample Data

1. **Upload Sample File**
   - Click the Upload tab
   - Drag and drop `csv_doctor/assets/sample_sales_data.csv`
   - Review the sample data

2. **Clean the Data**
   - Go to Clean tab
   - Enable: Remove Empty Rows, Trim Whitespace, Remove Duplicates
   - Click "Clean Data"

3. **Validate Quality**
   - Go to Analyze tab
   - Click "Validate Data"
   - Check your quality score

4. **Analyze & Visualize**
   - Click "Analyze Statistics"
   - Click "Generate Visualizations"
   - See your data insights

5. **Export Results**
   - Go to Export tab
   - Download cleaned CSV and HTML report

---

## 🎯 Key Features to Try

✅ **Drag-and-drop upload** - Upload CSV files easily
✅ **Toggle cleaning options** - Choose which operations to apply
✅ **Quality scoring** - See your data quality at a glance
✅ **Statistics** - Mean, median, std dev for each column
✅ **Visualizations** - Correlation heatmaps, null distribution
✅ **Smart report generation** - Markdown and HTML exports

---

## 📂 File Structure

```
csv_doctor/
├── main.py                          # Flask app (start here!)
├── csv_loader.py, cleaner.py, ...   # Core modules
├── templates/index.html              # Web interface
├── static/style.css, script.js        # Frontend files
├── assets/sample_*.csv               # Sample data
└── uploads/                          # (auto-created)
```

---

## 🔍 Troubleshooting

**Port 5000 already in use?**
```bash
python main.py --port 5001
```

**Module import errors?**
```bash
pip install --upgrade -r requirements.txt
```

**Visualizations not showing?**
- Check browser console for errors
- Ensure matplotlib/seaborn are installed

---

## 📚 Learn More

- Read `README_COMPLETE.md` for full documentation
- Check `MODULES.md` for API reference
- Explore sample CSVs in `assets/` folder

---

## 💡 Common Workflows

### Cleaning Messy Customer Data
1. Upload CSV → Clean (remove duplicates, trim whitespace) → Export

### Analyzing Sales Performance  
1. Upload → Analyze → View correlations → Export report

### Data Quality Audit
1. Upload → Validate → Review quality score → Check anomalies

### Data Preparation for ML
1. Upload → Clean → Analyze → Export cleaned data

---

## ⚙️ Configuration

Edit `main.py` to customize:

```python
# Maximum file size
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# Port number
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## 📞 Quick Reference

| Task | Action |
|------|--------|
| Start app | `python main.py` |
| Upload CSV | Drag file to upload zone |
| Clean data | Check options, click "Clean Data" |
| Check quality | Go to Analyze → "Validate Data" |
| View stats | Click "Analyze Statistics" |
| See charts | Click "Generate Visualizations" |
| Export CSV | Go to Export → "Download CSV" |
| Export report | Go to Export → "Download HTML" |

---

## 🎓 Learning Tips

1. **Start simple** - Use sample data first
2. **Try each feature** - Click all buttons to understand functionality
3. **Read error messages** - They guide you on what to fix
4. **Experiment** - Try different cleaning options
5. **Review reports** - Understand what the analysis tells you

---

**Ready to clean some data? Let's go! 🏥**
