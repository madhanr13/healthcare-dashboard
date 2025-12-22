import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys

from cleaning.DataCleaner import HealthcareDataCleaner
from processing.DataProcessor import HealthcareDataProcessor
from visualization.VisualizationEngine import VisualizationEngine


class HealthcareAnalyticsSystem:

    def __init__(self):
        self.raw_data = None
        self.cleaned_data = None
        self.processor = None
        self.visualizer = VisualizationEngine()

    def load_sample_data(self, num_patients: int = 10, num_records: int = 1000) -> pd.DataFrame:
        """Generate sample healthcare data for demonstration."""
        np.random.seed(42)

        data = {
            'patient_id': np.random.choice([f'P{str(i).zfill(5)}' for i in range(1, num_patients + 1)], num_records),
            'timestamp': [datetime.now() - timedelta(hours=np.random.randint(0, 720)) for _ in range(num_records)],
            'heart_rate': np.random.normal(75, 12, num_records),
            'blood_pressure_systolic': np.random.normal(120, 15, num_records),
            'blood_pressure_diastolic': np.random.normal(80, 10, num_records),
            'temperature': np.random.normal(37.0, 0.5, num_records),
            'respiratory_rate': np.random.normal(16, 2, num_records),
            'oxygen_saturation': np.random.normal(97, 1.5, num_records)
        }

        # Introduce some missing values and outliers
        df = pd.DataFrame(data)
        missing_idx = np.random.choice(
            df.index, size=int(0.05 * len(df)), replace=False)
        df.loc[missing_idx, 'heart_rate'] = np.nan

        outlier_idx = np.random.choice(
            df.index, size=int(0.02 * len(df)), replace=False)
        df.loc[outlier_idx, 'heart_rate'] = np.random.choice(
            [25, 250], len(outlier_idx))

        self.raw_data = df
        print(
            f"✓ Generated sample data: {len(df)} records for {num_patients} patients")
        return df

    def load_data_from_csv(self, filepath: str) -> pd.DataFrame:
        """Load healthcare data from CSV file."""
        self.raw_data = pd.read_csv(filepath)
        print(f"✓ Loaded data from {filepath}: {len(self.raw_data)} records")
        return self.raw_data

    def clean_data(self) -> pd.DataFrame:
        """Execute data cleaning pipeline."""
        if self.raw_data is None:
            raise ValueError(
                "No data loaded. Use load_sample_data() or load_data_from_csv().")

        cleaner = HealthcareDataCleaner()
        self.cleaned_data, report = cleaner.clean_data(self.raw_data)

        print("\n" + "="*50)
        print("DATA CLEANING REPORT")
        print("="*50)
        print(f"Duplicates removed: {report.get('duplicates_removed', 0)}")
        print(f"Outliers removed: {report.get('outliers_removed', 0)}")
        print(f"Records before cleaning: {len(self.raw_data)}")
        print(f"Records after cleaning: {len(self.cleaned_data)}")
        print("="*50 + "\n")

        self.processor = HealthcareDataProcessor(self.cleaned_data)
        return self.cleaned_data

    def analyze_critical_patients(self) -> pd.DataFrame:
        """Identify and analyze critical patients."""
        if self.processor is None:
            raise ValueError("Data must be cleaned first. Use clean_data().")

        critical_df = self.processor.identify_critical_patients()
        print(f"\n✓ Identified {len(critical_df)} critical vital sign records")
        print(
            f"  Affecting {critical_df['patient_id'].nunique()} unique patients\n")

        return critical_df

    def get_patient_report(self, patient_id: str) -> dict:
        """Generate detailed report for a patient."""
        if self.processor is None:
            raise ValueError("Data must be cleaned first. Use clean_data().")

        stats = self.processor.get_patient_statistics(patient_id)
        print(f"\nPATIENT REPORT: {patient_id}")
        print("-" * 40)
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print("-" * 40 + "\n")

        return stats

    def visualize_patient(self, patient_id: str) -> None:
        """Visualize vital signs for a patient."""
        if self.cleaned_data is None:
            raise ValueError("Data must be cleaned first. Use clean_data().")

        self.visualizer.plot_patient_vitals(self.cleaned_data, patient_id)

    def visualize_critical_alerts(self) -> None:
        """Visualize critical alerts across patients."""
        if self.processor is None:
            raise ValueError("Data must be cleaned first. Use clean_data().")

        critical_df = self.processor.identify_critical_patients()
        self.visualizer.plot_critical_alerts(critical_df)


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("HEALTHCARE DATA CLEANING & VISUALIZATION SYSTEM")
    print("Clinical Insights Analytics Platform")
    print("="*60 + "\n")

    # Initialize system
    system = HealthcareAnalyticsSystem()

    # Load sample data
    system.load_sample_data(num_patients=15, num_records=1500)

    # Clean data
    system.clean_data()

    # Analyze critical patients
    critical_patients = system.analyze_critical_patients()

    # Get report for sample patient
    sample_patient = system.cleaned_data['patient_id'].iloc[0]
    system.get_patient_report(sample_patient)

    # Display aggregated statistics
    print("\nAGGREGATED PATIENT STATISTICS:")
    print("-" * 40)
    aggregated = system.processor.aggregate_by_patient()
    print(aggregated.head(10))
    print("-" * 40 + "\n")

    print("✓ System execution completed successfully!")
    print("✓ Data cleaning and analysis pipeline ready for use\n")


if __name__ == "__main__":
    main()
