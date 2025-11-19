"""
utils.py - Shared helper functions for CSV Doctor
"""

import os
from datetime import datetime
from pathlib import Path


def get_timestamp():
    """Generate a timestamp string for file naming"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def create_upload_dir():
    """Create uploads directory if it doesn't exist"""
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    return upload_dir


def get_file_path(filename, directory="uploads"):
    """Get safe file path"""
    base_path = Path(directory)
    base_path.mkdir(exist_ok=True)
    file_path = base_path / filename
    return file_path


def safe_filename(filename):
    """Generate a safe filename"""
    timestamp = get_timestamp()
    name, ext = os.path.splitext(filename)
    return f"{name}_{timestamp}{ext}"


def format_bytes(bytes_size):
    """Format bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def infer_column_type(series):
    """
    Infer the data type of a pandas Series
    Returns: 'numeric', 'categorical', 'datetime', or 'text'
    """
    import pandas as pd
    
    # Remove null values for type inference
    non_null = series.dropna()
    
    if len(non_null) == 0:
        return 'unknown'
    
    # Check for numeric
    try:
        pd.to_numeric(non_null, errors='coerce')
        if pd.to_numeric(non_null, errors='coerce').notna().sum() / len(non_null) > 0.8:
            return 'numeric'
    except:
        pass
    
    # Check for datetime
    try:
        pd.to_datetime(non_null, errors='coerce')
        if pd.to_datetime(non_null, errors='coerce').notna().sum() / len(non_null) > 0.8:
            return 'datetime'
    except:
        pass
    
    # Check if categorical (low cardinality)
    unique_ratio = len(non_null.unique()) / len(non_null)
    if unique_ratio < 0.05 or len(non_null.unique()) < 20:
        return 'categorical'
    
    return 'text'


def round_floats(obj, decimals=2):
    """Round all floats in a dictionary or list to specified decimal places"""
    if isinstance(obj, dict):
        return {k: round_floats(v, decimals) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [round_floats(item, decimals) for item in obj]
    elif isinstance(obj, float):
        return round(obj, decimals)
    return obj


def sanitize_dict(obj):
    """
    Sanitize dictionary for JSON serialization
    Converts NaN, Inf, and other non-serializable types
    """
    import pandas as pd
    import numpy as np
    
    if isinstance(obj, dict):
        return {k: sanitize_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_dict(item) for item in obj]
    elif pd.isna(obj) or (isinstance(obj, float) and np.isnan(obj)):
        return None
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    return str(obj)
