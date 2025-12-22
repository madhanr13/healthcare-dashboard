import pandas as pd
from datetime import datetime, timedelta


class HealthcareDataProcessor:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def aggregate_by_patient(self) -> pd.DataFrame:
        """Aggregate vital signs statistics by patient."""
        aggregated = self.df.groupby('patient_id').agg({
            'heart_rate': ['mean', 'min', 'max', 'std'],
            'blood_pressure_systolic': ['mean', 'min', 'max'],
            'blood_pressure_diastolic': ['mean', 'min', 'max'],
            'temperature': ['mean', 'min', 'max'],
            'oxygen_saturation': ['mean', 'min', 'max']
        }).round(2)

        return aggregated

    def aggregate_by_time_period(self, period: str = '1D') -> pd.DataFrame:
        """Aggregate data by time period (daily, hourly, etc.)."""
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])

        aggregated = self.df.set_index('timestamp').groupby(
            [pd.Grouper(freq=period), 'patient_id']
        ).agg({
            'heart_rate': 'mean',
            'temperature': 'mean',
            'oxygen_saturation': 'mean'
        }).round(2)

        return aggregated

    def calculate_trend(self, patient_id: str, metric: str, window: int = 7) -> pd.DataFrame:
        """Calculate moving average trend for a patient metric."""
        patient_data = self.df[self.df['patient_id'] == patient_id].copy()
        patient_data['timestamp'] = pd.to_datetime(patient_data['timestamp'])
        patient_data = patient_data.sort_values('timestamp')

        patient_data[f'{metric}_ma'] = patient_data[metric].rolling(
            window=window).mean()

        return patient_data[['timestamp', metric, f'{metric}_ma']]

    def identify_critical_patients(self, thresholds: dict = None) -> pd.DataFrame:
        """Identify patients with critical vital signs."""
        if thresholds is None:
            thresholds = {
                'heart_rate_high': 100,
                'heart_rate_low': 60,
                'oxygen_saturation_low': 90,
                'temperature_high': 38.5
            }

        critical = self.df[
            (self.df['heart_rate'] > thresholds['heart_rate_high']) |
            (self.df['heart_rate'] < thresholds['heart_rate_low']) |
            (self.df['oxygen_saturation'] < thresholds['oxygen_saturation_low']) |
            (self.df['temperature'] > thresholds['temperature_high'])
        ]

        return critical.sort_values('timestamp', ascending=False)

    def get_patient_statistics(self, patient_id: str) -> dict:
        """Get comprehensive statistics for a single patient."""
        patient_data = self.df[self.df['patient_id'] == patient_id]

        stats = {
            'patient_id': patient_id,
            'total_records': len(patient_data),
            'heart_rate_avg': patient_data['heart_rate'].mean(),
            'temperature_avg': patient_data['temperature'].mean(),
            'oxygen_saturation_avg': patient_data['oxygen_saturation'].mean(),
            'blood_pressure_avg': f"{patient_data['blood_pressure_systolic'].mean():.0f}/{patient_data['blood_pressure_diastolic'].mean():.0f}"
        }

        return stats
