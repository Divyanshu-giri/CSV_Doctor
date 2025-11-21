"""
validator.py - Data validation functions for CSV files
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class CSVValidator:
    """Validate CSV data quality and structure"""
    
    def __init__(self, df):
        """
        Initialize the validator
        
        Args:
            df: pandas DataFrame to validate
        """
        self.df = df
        self.issues = []
    
    def detect_malformed_rows(self):
        """
        Detect malformed rows (missing values, inconsistent columns)
        
        Returns:
            Dictionary with malformed rows info
        """
        malformed = {
            'count': 0,
            'rows': [],
            'issues': {}
        }
        
        # Find rows with NaN values
        rows_with_nulls = self.df[self.df.isna().any(axis=1)].index.tolist()
        
        if rows_with_nulls:
            malformed['issues']['missing_values'] = {
                'count': int(len(rows_with_nulls)),
                'sample_rows': [int(x) for x in rows_with_nulls[:10]]
            }
            malformed['count'] += len(rows_with_nulls)
        
        return malformed
    
    def check_column_types(self):
        """
        Check and infer column data types
        
        Returns:
            Dictionary with type information for each column
        """
        from utils import infer_column_type
        
        type_report = {}
        
        for col in self.df.columns:
            inferred_type = infer_column_type(self.df[col])
            current_dtype = str(self.df[col].dtype)
            
            type_report[col] = {
                'current_dtype': current_dtype,
                'inferred_type': inferred_type,
                'unique_values': int(len(self.df[col].unique())),
                'null_count': int(self.df[col].isna().sum()),
                'null_percentage': round(100 * self.df[col].isna().sum() / len(self.df), 2)
            }
        
        return type_report
    
    def get_null_distribution(self):
        """
        Get null value distribution across columns
        
        Returns:
            Dictionary with null statistics
        """
        null_dist = {}
        total_cells = len(self.df) * len(self.df.columns)
        
        for col in self.df.columns:
            null_count = int(self.df[col].isna().sum())
            null_dist[col] = {
                'null_count': null_count,
                'null_percentage': round(100 * null_count / len(self.df), 2),
                'non_null_count': int(len(self.df) - null_count)
            }
        
        null_dist['total'] = {
            'null_count': int(self.df.isna().sum().sum()),
            'null_percentage': round(100 * self.df.isna().sum().sum() / total_cells, 2)
        }
        
        return null_dist
    
    def validate_against_schema(self, schema: Dict[str, str]):
        """
        Validate DataFrame against provided schema
        
        Args:
            schema: Dictionary of {column: expected_type}
        
        Returns:
            Validation results
        """
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check for missing columns
        missing_cols = set(schema.keys()) - set(self.df.columns)
        if missing_cols:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Missing columns: {missing_cols}")
        
        # Check column types
        for col, expected_type in schema.items():
            if col not in self.df.columns:
                continue
            
            current_type = str(self.df[col].dtype)
            if expected_type.lower() == 'numeric':
                if not pd.api.types.is_numeric_dtype(self.df[col]):
                    validation_result['warnings'].append(
                        f"Column '{col}' expected numeric but got {current_type}"
                    )
            elif expected_type.lower() == 'string':
                if not pd.api.types.is_string_dtype(self.df[col]) and \
                   not pd.api.types.is_object_dtype(self.df[col]):
                    validation_result['warnings'].append(
                        f"Column '{col}' expected string but got {current_type}"
                    )
        
        return validation_result
    
    def detect_duplicates(self):
        """
        Detect duplicate rows
        
        Returns:
            Duplicate statistics
        """
        duplicates = self.df.duplicated(keep=False)
        duplicate_count = int(duplicates.sum())
        
        return {
            'duplicate_count': duplicate_count,
            'duplicate_percentage': round(100 * duplicate_count / len(self.df), 2),
            'duplicate_rows': int(self.df.duplicated(keep=False).sum() / 2) if duplicate_count > 0 else 0
        }
    
    def detect_anomalies(self):
        """
        Detect potential anomalies in the data
        
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        # Check for columns with only one unique value
        for col in self.df.columns:
            unique_count = self.df[col].nunique()
            if unique_count == 1:
                anomalies.append({
                    'type': 'constant_column',
                    'column': col,
                    'value': str(self.df[col].iloc[0]),
                    'message': f"Column '{col}' has only one unique value"
                })
        
        # Check for columns with very high null percentage
        for col in self.df.columns:
            null_pct = 100 * self.df[col].isna().sum() / len(self.df)
            if null_pct > 50:
                anomalies.append({
                    'type': 'high_null_percentage',
                    'column': col,
                    'null_percentage': round(null_pct, 2),
                    'message': f"Column '{col}' has {null_pct:.2f}% null values"
                })
        
        # Check for numeric columns with unusual distributions
        for col in self.df.select_dtypes(include=[np.number]).columns:
            if len(self.df[col].dropna()) > 0:
                std = float(self.df[col].std())
                mean = float(self.df[col].mean())
                if mean != 0 and std / abs(mean) > 2:
                    anomalies.append({
                        'type': 'high_variance',
                        'column': col,
                        'std_dev': round(std, 2),
                        'mean': round(mean, 2),
                        'message': f"Column '{col}' has high variance (std/mean = {std/abs(mean):.2f})"
                    })
        
        return anomalies
    
    def generate_validation_report(self):
        """
        Generate comprehensive validation report
        
        Returns:
            Complete validation report
        """
        report = {
            'data_shape': {
                'rows': len(self.df),
                'columns': len(self.df.columns)
            },
            'null_distribution': self.get_null_distribution(),
            'column_types': self.check_column_types(),
            'duplicates': self.detect_duplicates(),
            'malformed_rows': self.detect_malformed_rows(),
            'anomalies': self.detect_anomalies()
        }
        
        return report
    
    def get_data_quality_score(self):
        """
        Calculate an overall data quality score (0-100)
        
        Returns:
            Quality score and breakdown
        """
        total_cells = len(self.df) * len(self.df.columns)
        
        # Null percentage score (30% weight)
        null_pct = 100 * self.df.isna().sum().sum() / total_cells
        null_score = max(0, 100 - null_pct)
        
        # Duplicate score (20% weight)
        dup_pct = 100 * self.df.duplicated().sum() / len(self.df) if len(self.df) > 0 else 0
        dup_score = max(0, 100 - dup_pct)
        
        # Type consistency score (20% weight)
        type_issues = 0
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                try:
                    pd.to_numeric(self.df[col], errors='coerce')
                    non_numeric_pct = 100 * self.df[col].isna().sum() / len(self.df)
                    if non_numeric_pct > 10:
                        type_issues += 1
                except:
                    pass
        
        type_score = max(0, 100 - (type_issues * 10))
        
        # Anomaly score (20% weight)
        anomalies = self.detect_anomalies()
        anomaly_score = max(0, 100 - (len(anomalies) * 15))
        
        # Calculate weighted score
        overall_score = (null_score * 0.3 + dup_score * 0.2 + 
                        type_score * 0.2 + anomaly_score * 0.3)
        
        return {
            'overall_score': round(float(overall_score), 2),
            'scores': {
                'null_score': round(float(null_score), 2),
                'duplicate_score': round(float(dup_score), 2),
                'type_score': round(float(type_score), 2),
                'anomaly_score': round(float(anomaly_score), 2)
            },
            'issues_count': int(len(anomalies) + (1 if dup_pct > 0 else 0) + (1 if null_pct > 0 else 0))
        }
