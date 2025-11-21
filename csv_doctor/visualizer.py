"""
visualizer.py - Generate visualizations for CSV data using matplotlib and seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from pathlib import Path


class CSVVisualizer:
    """Generate visualizations for CSV analysis"""
    
    def __init__(self, df):
        """
        Initialize the visualizer
        
        Args:
            df: pandas DataFrame to visualize
        """
        self.df = df
        # Set style for better-looking plots
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
    
    @staticmethod
    def _fig_to_base64(fig):
        """
        Convert matplotlib figure to base64 encoded string
        
        Args:
            fig: matplotlib figure
        
        Returns:
            Base64 encoded image string
        """
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        return image_base64
    
    def plot_histogram(self, column, bins=30, title=None):
        """
        Create histogram for numeric column
        
        Args:
            column: Column name
            bins: Number of bins
            title: Plot title
        
        Returns:
            Base64 encoded image
        """
        if column not in self.df.columns:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        self.df[column].hist(bins=bins, ax=ax, color='steelblue', edgecolor='black')
        
        ax.set_title(title or f'Histogram of {column}', fontsize=14, fontweight='bold')
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        return self._fig_to_base64(fig)
    
    def plot_bar_chart(self, column, top_n=10, title=None):
        """
        Create bar chart for categorical column
        
        Args:
            column: Column name
            top_n: Top N values to display
            title: Plot title
        
        Returns:
            Base64 encoded image
        """
        if column not in self.df.columns:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        value_counts = self.df[column].value_counts().head(top_n)
        value_counts.plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
        
        ax.set_title(title or f'Top {top_n} Values in {column}', fontsize=14, fontweight='bold')
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def plot_null_heatmap(self, title=None):
        """
        Create heatmap showing null value distribution
        
        Args:
            title: Plot title
        
        Returns:
            Base64 encoded image
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Create null matrix for first 100 rows
        display_df = self.df.head(100)
        null_matrix = display_df.isna().astype(int)
        
        sns.heatmap(null_matrix.T, cbar=True, cmap='RdYlGn_r', ax=ax,
                   yticklabels=True, xticklabels=False)
        
        ax.set_title(title or 'Null Value Heatmap (First 100 Rows)', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Row Index', fontsize=12)
        ax.set_ylabel('Columns', fontsize=12)
        
        return self._fig_to_base64(fig)
    
    def plot_correlation_heatmap(self, title=None):
        """
        Create correlation matrix heatmap
        
        Args:
            title: Plot title
        
        Returns:
            Base64 encoded image
        """
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        corr_matrix = numeric_df.corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, ax=ax, cbar_kws={'label': 'Correlation'})
        
        ax.set_title(title or 'Correlation Matrix', fontsize=14, fontweight='bold')
        
        return self._fig_to_base64(fig)
    
    def plot_box_plot(self, column, title=None):
        """
        Create box plot for numeric column
        
        Args:
            column: Column name
            title: Plot title
        
        Returns:
            Base64 encoded image
        """
        if column not in self.df.columns:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        self.df[[column]].boxplot(ax=ax)
        
        ax.set_title(title or f'Box Plot of {column}', fontsize=14, fontweight='bold')
        ax.set_ylabel(column, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        return self._fig_to_base64(fig)
    
    def plot_scatter(self, column_x, column_y, title=None):
        """
        Create scatter plot for two numeric columns
        
        Args:
            column_x: X-axis column name
            column_y: Y-axis column name
            title: Plot title
        
        Returns:
            Base64 encoded image
        """
        if column_x not in self.df.columns or column_y not in self.df.columns:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.scatter(self.df[column_x], self.df[column_y], alpha=0.6, color='steelblue')
        
        ax.set_title(title or f'{column_x} vs {column_y}', fontsize=14, fontweight='bold')
        ax.set_xlabel(column_x, fontsize=12)
        ax.set_ylabel(column_y, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        return self._fig_to_base64(fig)
    
    def plot_distribution_comparison(self, numeric_columns=None, title=None):
        """
        Create distribution comparison for numeric columns
        
        Args:
            numeric_columns: List of columns to compare (None = all numeric)
            title: Plot title
        
        Returns:
            Base64 encoded image
        """
        if numeric_columns is None:
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_columns) == 0:
            return None
        
        # Limit to 5 columns for readability
        numeric_columns = numeric_columns[:5]
        
        fig, axes = plt.subplots(len(numeric_columns), 1, figsize=(12, 4*len(numeric_columns)))
        
        if len(numeric_columns) == 1:
            axes = [axes]
        
        for ax, col in zip(axes, numeric_columns):
            self.df[col].hist(bins=30, ax=ax, color='steelblue', edgecolor='black')
            ax.set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
            ax.set_xlabel(col, fontsize=10)
            ax.set_ylabel('Frequency', fontsize=10)
            ax.grid(True, alpha=0.3)
        
        fig.suptitle(title or 'Distribution Comparison', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def plot_missing_data(self, title=None):
        """
        Create visualization of missing data
        
        Args:
            title: Plot title
        
        Returns:
            Base64 encoded image
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        missing_data = self.df.isna().sum()
        # Avoid division by zero if df is empty
        total_rows = len(self.df) if len(self.df) > 0 else 1
        missing_percent = (missing_data / total_rows * 100).sort_values(ascending=False)

        # Filter only columns with missing percentage > 0
        missing_percent_nonzero = missing_percent[missing_percent > 0]

        # If there's nothing to plot, return None so caller can skip this image
        if missing_percent_nonzero.empty:
            plt.close(fig)
            return None

        missing_percent_nonzero.plot(kind='barh', ax=ax, color='coral', edgecolor='black')

        ax.set_title(title or 'Missing Data Percentage', fontsize=14, fontweight='bold')
        ax.set_xlabel('Percentage (%)', fontsize=12)
        ax.set_ylabel('Columns', fontsize=12)
        ax.grid(True, alpha=0.3, axis='x')

        return self._fig_to_base64(fig)
    
    def plot_data_types_distribution(self, title=None):
        """
        Create visualization of data type distribution
        
        Args:
            title: Plot title
        
        Returns:
            Base64 encoded image
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        dtype_counts = self.df.dtypes.astype(str).value_counts()
        dtype_counts.plot(kind='bar', ax=ax, color='lightgreen', edgecolor='black')
        
        ax.set_title(title or 'Data Type Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel('Data Type', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        return self._fig_to_base64(fig)
    
    def save_figure(self, fig, filepath):
        """
        Save matplotlib figure to file
        
        Args:
            fig: matplotlib figure
            filepath: Path to save file
        """
        fig.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close(fig)
    
    def generate_dashboard_images(self):
        """
        Generate all dashboard images at once
        
        Returns:
            Dictionary with all visualization images
        """
        dashboard = {
            'correlation_heatmap': self.plot_correlation_heatmap(),
            'null_heatmap': self.plot_null_heatmap(),
            'missing_data': self.plot_missing_data(),
            'data_types': self.plot_data_types_distribution()
        }
        
        # Add distribution comparison for numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            dashboard['distribution_comparison'] = self.plot_distribution_comparison(numeric_cols)
        
        return dashboard
