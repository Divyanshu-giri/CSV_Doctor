"""
cleaner.py - Data cleaning functions for CSV files
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any


class CSVCleaner:
    """Perform data cleaning operations on CSV files"""
    
    def __init__(self, df):
        """
        Initialize the cleaner
        
        Args:
            df: pandas DataFrame to clean
        """
        self.df = df.copy()
        self.original_df = df.copy()
        self.changes = []
    
    def reset(self):
        """Reset to original DataFrame"""
        self.df = self.original_df.copy()
        self.changes = []
    
    def get_changes(self):
        """Return list of changes made"""
        return self.changes
    
    def remove_empty_rows(self):
        """
        Remove rows where all values are null
        
        Returns:
            Self for method chaining
        """
        initial_rows = len(self.df)
        self.df = self.df.dropna(how='all')
        removed = initial_rows - len(self.df)
        
        if removed > 0:
            self.changes.append(f"Removed {removed} completely empty rows")
        
        return self
    
    def remove_empty_columns(self):
        """
        Remove columns where all values are null
        
        Returns:
            Self for method chaining
        """
        initial_cols = len(self.df.columns)
        self.df = self.df.dropna(axis=1, how='all')
        removed = initial_cols - len(self.df.columns)
        
        if removed > 0:
            self.changes.append(f"Removed {removed} completely empty columns")
        
        return self
    
    def trim_whitespace(self, columns=None):
        """
        Trim leading/trailing whitespace
        
        Args:
            columns: Specific columns to clean (None = all string columns)
        
        Returns:
            Self for method chaining
        """
        if columns is None:
            columns = self.df.select_dtypes(include=['object']).columns
        
        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].str.strip()
        
        self.changes.append(f"Trimmed whitespace from {len(columns)} columns")
        return self
    
    def remove_duplicates(self, subset=None, keep='first'):
        """
        Remove duplicate rows
        
        Args:
            subset: Specific columns to consider for duplicates
            keep: 'first', 'last', or False (remove all duplicates)
        
        Returns:
            Self for method chaining
        """
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        removed = initial_rows - len(self.df)
        
        if removed > 0:
            self.changes.append(f"Removed {removed} duplicate rows")
        
        return self
    
    def fill_missing_values(self, method='mean', columns=None, fill_value=None):
        """
        Fill missing values using specified method
        
        Args:
            method: 'mean', 'median', 'mode', 'forward_fill', 'backward_fill', or 'value'
            columns: Specific columns to fill (None = all)
            fill_value: Value to use when method='value'
        
        Returns:
            Self for method chaining
        """
        if columns is None:
            columns = self.df.columns
        
        initial_nulls = self.df[columns].isna().sum().sum()
        
        for col in columns:
            if col not in self.df.columns:
                continue
            
            null_count = self.df[col].isna().sum()
            
            if null_count == 0:
                continue
            
            if method == 'mean':
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
            
            elif method == 'median':
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df[col].fillna(self.df[col].median(), inplace=True)
            
            elif method == 'mode':
                mode_val = self.df[col].mode()
                if len(mode_val) > 0:
                    self.df[col].fillna(mode_val[0], inplace=True)
            
            elif method == 'forward_fill':
                self.df[col].fillna(method='ffill', inplace=True)
            
            elif method == 'backward_fill':
                self.df[col].fillna(method='bfill', inplace=True)
            
            elif method == 'value' and fill_value is not None:
                self.df[col].fillna(fill_value, inplace=True)
        
        final_nulls = self.df[columns].isna().sum().sum()
        filled = initial_nulls - final_nulls
        
        if filled > 0:
            self.changes.append(f"Filled {filled} missing values using {method}")
        
        return self
    
    def standardize_column_names(self):
        """
        Standardize column names (lowercase, no spaces, remove special chars)
        
        Returns:
            Self for method chaining
        """
        new_columns = {}
        for col in self.df.columns:
            new_col = str(col).lower().strip()
            new_col = new_col.replace(' ', '_')
            new_col = ''.join(c for c in new_col if c.isalnum() or c == '_')
            new_columns[col] = new_col
        
        self.df.rename(columns=new_columns, inplace=True)
        self.changes.append("Standardized column names")
        return self
    
    def normalize_text_case(self, columns=None, case='lower'):
        """
        Normalize text case in specified columns
        
        Args:
            columns: Columns to normalize
            case: 'lower', 'upper', or 'title'
        
        Returns:
            Self for method chaining
        """
        if columns is None:
            columns = self.df.select_dtypes(include=['object']).columns
        
        for col in columns:
            if col in self.df.columns:
                if case == 'lower':
                    self.df[col] = self.df[col].str.lower()
                elif case == 'upper':
                    self.df[col] = self.df[col].str.upper()
                elif case == 'title':
                    self.df[col] = self.df[col].str.title()
        
        self.changes.append(f"Normalized text case to {case} in {len(columns)} columns")
        return self
    
    def remove_outliers(self, columns=None, method='iqr', threshold=1.5):
        """
        Remove outliers from numeric columns
        
        Args:
            columns: Numeric columns to process
            method: 'iqr' (Interquartile Range) or 'zscore'
            threshold: IQR multiplier (1.5) or zscore threshold (3)
        
        Returns:
            Self for method chaining
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns
        
        initial_rows = len(self.df)
        
        for col in columns:
            if col not in self.df.columns:
                continue
            
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
            
            elif method == 'zscore':
                from scipy import stats
                z_scores = np.abs(stats.zscore(self.df[col].dropna()))
                self.df = self.df[(np.abs(stats.zscore(self.df[col].fillna(self.df[col].mean()))) < threshold)]
        
        removed = initial_rows - len(self.df)
        if removed > 0:
            self.changes.append(f"Removed {removed} outlier rows using {method}")
        
        return self
    
    def convert_dtypes(self, columns_types: Dict[str, str]):
        """
        Convert column data types
        
        Args:
            columns_types: Dictionary of {column: dtype} to convert
        
        Returns:
            Self for method chaining
        """
        for col, dtype in columns_types.items():
            if col not in self.df.columns:
                continue
            
            try:
                if dtype == 'numeric':
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                elif dtype == 'datetime':
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                elif dtype in ['string', 'object']:
                    self.df[col] = self.df[col].astype(str)
                else:
                    self.df[col] = self.df[col].astype(dtype)
            except Exception as e:
                self.changes.append(f"Warning: Could not convert {col} to {dtype}: {str(e)}")
        
        return self
    
    def get_cleaned_df(self):
        """Return the cleaned DataFrame"""
        return self.df
