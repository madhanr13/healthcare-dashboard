import pandas as pd
import numpy as np
from datetime import datetime
from typing import Tuple, List


class HealthcareDataCleaner:

    def __init__(self, missing_threshold: float = 0.5):
        self.missing_threshold = missing_threshold
        self.cleaning_report = {}

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate records based on patient_id and timestamp."""
        initial_rows = len(df)
        df = df.drop_duplicates(
            subset=['patient_id', 'timestamp'], keep='first')
        self.cleaning_report['duplicates_removed'] = initial_rows - len(df)
        return df

    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """Handle missing values using specified strategy."""
        missing_counts = df.isnull().sum()
        self.cleaning_report['missing_before'] = missing_counts.to_dict()

        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if strategy == 'mean':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == 'median':
            df[numeric_cols] = df[numeric_cols].fillna(
                df[numeric_cols].median())
        elif strategy == 'forward_fill':
            df = df.fillna(method='ffill')

        self.cleaning_report['missing_after'] = df.isnull().sum().to_dict()
        return df

    def remove_outliers(self, df: pd.DataFrame, columns: List[str], method: str = 'iqr') -> pd.DataFrame:
        """Remove outliers using IQR or Z-score method."""
        initial_rows = len(df)

        for col in columns:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                df = df[(df[col] >= Q1 - 1.5 * IQR) &
                        (df[col] <= Q3 + 1.5 * IQR)]

            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                df = df[z_scores < 3]

        self.cleaning_report['outliers_removed'] = initial_rows - len(df)
        return df

    def validate_vital_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate vital signs within acceptable ranges."""
        # Normal vital sign ranges
        df = df[(df['heart_rate'] >= 40) & (df['heart_rate'] <= 200)]
        df = df[(df['temperature'] >= 35) & (df['temperature'] <= 42)]
        df = df[(df['oxygen_saturation'] >= 80) &
                (df['oxygen_saturation'] <= 100)]
        df = df[(df['respiratory_rate'] >= 8) & (df['respiratory_rate'] <= 40)]

        return df

    def clean_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """Execute full cleaning pipeline."""
        df = self.remove_duplicates(df)
        df = self.handle_missing_values(df, strategy='median')
        df = self.remove_outliers(
            df, columns=['heart_rate', 'temperature', 'oxygen_saturation'])
        df = self.validate_vital_ranges(df)

        return df, self.cleaning_report

    def get_cleaning_summary(self) -> dict:
        """Return cleaning summary statistics."""
        return self.cleaning_report
