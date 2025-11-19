"""
analyzer.py - Data analysis functions for CSV files
"""

import pandas as pd
import numpy as np
from typing import Dict, List


class CSVAnalyzer:
    """Analyze and extract insights from CSV data"""
    
    def __init__(self, df):
        """
        Initialize the analyzer
        
        Args:
            df: pandas DataFrame to analyze
        """
        self.df = df
    
    def get_summary_stats(self):
        """
        Get descriptive statistics for numeric columns
        
        Returns:
            Dictionary with summary statistics
        """
        stats = {}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            col_data = self.df[col].dropna()
            
            if len(col_data) == 0:
                continue
            
            stats[col] = {
                'count': int(len(col_data)),
                'mean': round(float(col_data.mean()), 4),
                'median': round(float(col_data.median()), 4),
                'std_dev': round(float(col_data.std()), 4),
                'min': round(float(col_data.min()), 4),
                'max': round(float(col_data.max()), 4),
                'q25': round(float(col_data.quantile(0.25)), 4),
                'q75': round(float(col_data.quantile(0.75)), 4),
                'iqr': round(float(col_data.quantile(0.75) - col_data.quantile(0.25)), 4),
                'variance': round(float(col_data.var()), 4),
                'skewness': round(float(col_data.skew()), 4),
                'kurtosis': round(float(col_data.kurtosis()), 4)
            }
        
        return stats
    
    def get_null_distribution(self):
        """
        Get null value distribution across columns
        
        Returns:
            Dictionary with null statistics
        """
        null_dist = {}
        
        for col in self.df.columns:
            null_count = self.df[col].isna().sum()
            null_dist[col] = {
                'null_count': int(null_count),
                'null_percentage': round(100 * null_count / len(self.df), 2),
                'non_null_count': int(len(self.df) - null_count),
                'non_null_percentage': round(100 * (len(self.df) - null_count) / len(self.df), 2)
            }
        
        return null_dist
    
    def get_correlation_matrix(self):
        """
        Get correlation matrix for numeric columns
        
        Returns:
            Correlation matrix as dictionary
        """
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) == 0:
            return {}
        
        corr_matrix = numeric_df.corr().round(3)
        
        # Convert to dictionary format
        corr_dict = corr_matrix.to_dict()
        
        return corr_dict
    
    def get_high_correlations(self, threshold=0.7):
        """
        Get pairs of highly correlated columns
        
        Args:
            threshold: Correlation threshold (0-1)
        
        Returns:
            List of highly correlated column pairs
        """
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            return []
        
        corr_matrix = numeric_df.corr().abs()
        
        # Get upper triangle of correlation matrix
        upper = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        # Find columns with correlation > threshold
        high_corr = []
        for column in upper.columns:
            col_corr = upper[column]
            corr_cols = col_corr[col_corr > threshold]
            
            for idx, corr_val in corr_cols.items():
                high_corr.append({
                    'column_1': str(idx),
                    'column_2': str(column),
                    'correlation': round(float(corr_val), 3)
                })
        
        return sorted(high_corr, key=lambda x: abs(x['correlation']), reverse=True)
    
    def get_frequency_distribution(self, column):
        """
        Get frequency distribution for a column
        
        Args:
            column: Column name
        
        Returns:
            Dictionary with value counts
        """
        if column not in self.df.columns:
            return {}
        
        value_counts = self.df[column].value_counts()
        
        dist = {}
        for value, count in value_counts.items():
            dist[str(value)] = {
                'count': int(count),
                'percentage': round(100 * count / len(self.df), 2)
            }
        
        return dist
    
    def get_categorical_summary(self):
        """
        Get summary of categorical columns
        
        Returns:
            Dictionary with categorical column information
        """
        categorical_summary = {}
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            # Convert most_common counts to int
            most_common = {str(k): int(v) for k, v in self.df[col].value_counts().head(5).items()}
            
            categorical_summary[col] = {
                'unique_values': int(self.df[col].nunique()),
                'top_value': str(self.df[col].mode()[0]) if len(self.df[col].mode()) > 0 else None,
                'top_value_count': int(self.df[col].value_counts().iloc[0]) if len(self.df[col].value_counts()) > 0 else 0,
                'null_count': int(self.df[col].isna().sum()),
                'most_common': most_common
            }
        
        return categorical_summary
    
    def get_distribution_shape(self, column):
        """
        Get distribution shape information for numeric column
        
        Args:
            column: Column name
        
        Returns:
            Dictionary with distribution characteristics
        """
        if column not in self.df.columns or not pd.api.types.is_numeric_dtype(self.df[column]):
            return {}
        
        col_data = self.df[column].dropna()
        skewness = float(col_data.skew())
        kurtosis = float(col_data.kurtosis())
        
        return {
            'mean': round(float(col_data.mean()), 4),
            'median': round(float(col_data.median()), 4),
            'mode': round(float(col_data.mode()[0]), 4) if len(col_data.mode()) > 0 else None,
            'skewness': round(skewness, 4),
            'kurtosis': round(kurtosis, 4),
            'is_normal': abs(skewness) < 0.5 and abs(kurtosis) < 3
        }
    
    def get_column_insights(self, column):
        """
        Get detailed insights for a specific column
        
        Args:
            column: Column name
        
        Returns:
            Dictionary with column insights
        """
        from utils import infer_column_type
        
        if column not in self.df.columns:
            return {}
        
        col_data = self.df[column]
        inferred_type = infer_column_type(col_data)
        
        insights = {
            'column_name': column,
            'data_type': str(col_data.dtype),
            'inferred_type': inferred_type,
            'total_values': len(col_data),
            'null_count': int(col_data.isna().sum()),
            'null_percentage': round(100 * col_data.isna().sum() / len(col_data), 2),
            'unique_values': int(col_data.nunique()),
            'duplicates': int(len(col_data) - col_data.nunique())
        }
        
        if inferred_type == 'numeric':
            insights['numeric_stats'] = self.get_summary_stats().get(column, {})
            insights['distribution'] = self.get_distribution_shape(column)
        
        elif inferred_type == 'categorical':
            insights['frequency_distribution'] = self.get_frequency_distribution(column)
            insights['top_5_values'] = dict(col_data.value_counts().head(5))
        
        return insights
    
    def get_overall_summary(self):
        """
        Get overall dataset summary
        
        Returns:
            Dictionary with dataset overview
        """
        summary = {
            'total_rows': int(len(self.df)),
            'total_columns': int(len(self.df.columns)),
            'total_cells': int(len(self.df) * len(self.df.columns)),
            'null_cells': int(self.df.isna().sum().sum()),
            'null_percentage': round(float(100 * self.df.isna().sum().sum() / 
                                    (len(self.df) * len(self.df.columns))), 2),
            'duplicate_rows': int(self.df.duplicated().sum()),
            'memory_usage_bytes': int(self.df.memory_usage(deep=True).sum()),
            'numeric_columns': int(len(self.df.select_dtypes(include=[np.number]).columns)),
            'categorical_columns': int(len(self.df.select_dtypes(include=['object']).columns)),
            'column_names': [str(col) for col in self.df.columns]
        }
        
        return summary
    
    def generate_analysis_report(self):
        """
        Generate comprehensive analysis report
        
        Returns:
            Complete analysis report
        """
        report = {
            'overview': self.get_overall_summary(),
            'summary_stats': self.get_summary_stats(),
            'null_distribution': self.get_null_distribution(),
            'correlation_matrix': self.get_correlation_matrix(),
            'high_correlations': self.get_high_correlations(),
            'categorical_summary': self.get_categorical_summary()
        }
        
        return report
