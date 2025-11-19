"""
csv_loader.py - Load and parse CSV files using pandas
"""

import pandas as pd
import numpy as np
from pathlib import Path


class CSVLoader:
    """Load and parse CSV files"""
    
    def __init__(self, filepath):
        """
        Initialize the CSV loader
        
        Args:
            filepath: Path to the CSV file
        """
        self.filepath = Path(filepath)
        self.df = None
        self.metadata = {}
    
    def load(self, encoding='utf-8', sep=None, **kwargs):
        """
        Load CSV file with automatic delimiter detection
        
        Args:
            encoding: File encoding (default: utf-8)
            sep: Delimiter (auto-detect if None)
            **kwargs: Additional pandas read_csv parameters
        
        Returns:
            pandas DataFrame
        """
        try:
            if sep is None:
                # Auto-detect delimiter
                with open(self.filepath, 'r', encoding=encoding) as f:
                    first_line = f.readline()
                sep = self._detect_delimiter(first_line)
            
            self.df = pd.read_csv(
                self.filepath,
                encoding=encoding,
                sep=sep,
                **kwargs
            )
            
            self._extract_metadata()
            return self.df
        
        except Exception as e:
            raise ValueError(f"Error loading CSV: {str(e)}")
    
    @staticmethod
    def _detect_delimiter(line):
        """
        Detect the most likely delimiter
        
        Args:
            line: First line of CSV file
        
        Returns:
            Detected delimiter (comma, semicolon, tab, or pipe)
        """
        delimiters = [',', ';', '\t', '|']
        max_count = 0
        detected_sep = ','
        
        for sep in delimiters:
            count = line.count(sep)
            if count > max_count:
                max_count = count
                detected_sep = sep
        
        return detected_sep
    
    def _extract_metadata(self):
        """Extract metadata from loaded CSV"""
        if self.df is not None:
            # Convert dtypes to strings to avoid JSON serialization issues
            dtypes_dict = {col: str(dtype) for col, dtype in self.df.dtypes.items()}
            self.metadata = {
                'file_name': self.filepath.name,
                'file_size': self.filepath.stat().st_size,
                'rows': len(self.df),
                'columns': len(self.df.columns),
                'column_names': list(self.df.columns),
                'dtypes': dtypes_dict,
                'memory_usage': int(self.df.memory_usage(deep=True).sum())
            }
    
    def get_metadata(self):
        """Return file metadata"""
        return self.metadata
    
    def validate_structure(self):
        """
        Validate CSV structure
        
        Returns:
            Dictionary with validation results
        """
        validation = {
            'is_valid': True,
            'issues': []
        }
        
        if self.df is None:
            validation['is_valid'] = False
            validation['issues'].append('CSV not loaded')
            return validation
        
        # Check for empty DataFrame
        if len(self.df) == 0:
            validation['issues'].append('CSV is empty')
        
        # Check for empty columns
        empty_cols = [col for col in self.df.columns if self.df[col].isna().all()]
        if empty_cols:
            validation['issues'].append(f'Empty columns found: {empty_cols}')
        
        # Check for unnamed columns
        unnamed_cols = [col for col in self.df.columns if 'Unnamed' in str(col)]
        if unnamed_cols:
            validation['issues'].append(f'Unnamed columns found: {unnamed_cols}')
        
        return validation
    
    def get_sample(self, n=5):
        """Get first n rows of CSV"""
        return self.df.head(n).to_dict('records') if self.df is not None else []
    
    @staticmethod
    def from_string(csv_string, **kwargs):
        """
        Load CSV from string
        
        Args:
            csv_string: CSV content as string
            **kwargs: Additional pandas read_csv parameters
        
        Returns:
            pandas DataFrame
        """
        from io import StringIO
        return pd.read_csv(StringIO(csv_string), **kwargs)
