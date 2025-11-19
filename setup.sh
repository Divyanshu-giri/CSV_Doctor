#!/bin/bash
# setup.sh - Quick setup script for CSV Doctor

echo "🏥 CSV Doctor - Setup Script"
echo "============================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Create uploads directory
mkdir -p csv_doctor/uploads
echo "✅ Created uploads directory"
echo ""

# Display instructions
echo "🚀 Setup complete! To start CSV Doctor:"
echo ""
echo "1. Navigate to the project directory:"
echo "   cd csv_doctor"
echo ""
echo "2. Run the Flask application:"
echo "   python main.py"
echo ""
echo "3. Open your browser and go to:"
echo "   http://localhost:5000"
echo ""
echo "📁 Sample CSV files are available in:"
echo "   csv_doctor/assets/sample_sales_data.csv"
echo "   csv_doctor/assets/sample_student_data.csv"
echo ""
echo "Happy data cleaning! 🎉"
