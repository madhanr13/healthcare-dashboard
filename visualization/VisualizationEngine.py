import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Tuple

sns.set_style("whitegrid")


class VisualizationEngine:

    def __init__(self, figsize: Tuple[int, int] = (15, 10)):
        self.figsize = figsize

    def plot_patient_vitals(self, df: pd.DataFrame, patient_id: str) -> None:
        """Plot all vital signs for a specific patient."""
        patient_data = df[df['patient_id'] == patient_id].copy()
        patient_data['timestamp'] = pd.to_datetime(patient_data['timestamp'])
        patient_data = patient_data.sort_values('timestamp')

        fig, axes = plt.subplots(2, 2, figsize=self.figsize)
        fig.suptitle(
            f'Vital Signs - Patient {patient_id}', fontsize=16, fontweight='bold')

        axes[0, 0].plot(patient_data['timestamp'],
                        patient_data['heart_rate'], marker='o')
        axes[0, 0].set_title('Heart Rate (bpm)')
        axes[0, 0].set_ylabel('BPM')

        axes[0, 1].plot(patient_data['timestamp'],
                        patient_data['temperature'], marker='s', color='orange')
        axes[0, 1].set_title('Temperature (°C)')
        axes[0, 1].set_ylabel('Celsius')

        axes[1, 0].plot(patient_data['timestamp'],
                        patient_data['oxygen_saturation'], marker='^', color='green')
        axes[1, 0].set_title('Oxygen Saturation (%)')
        axes[1, 0].set_ylabel('Percentage')

        axes[1, 1].plot(patient_data['timestamp'],
                        patient_data['blood_pressure_systolic'], label='Systolic', marker='d')
        axes[1, 1].plot(patient_data['timestamp'],
                        patient_data['blood_pressure_diastolic'], label='Diastolic', marker='d')
        axes[1, 1].set_title('Blood Pressure (mmHg)')
        axes[1, 1].set_ylabel('mmHg')
        axes[1, 1].legend()

        for ax in axes.flat:
            ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()

    def plot_patient_comparison(self, df: pd.DataFrame, metric: str, patient_ids: List[str]) -> None:
        """Compare a metric across multiple patients."""
        fig, ax = plt.subplots(figsize=self.figsize)

        for patient_id in patient_ids:
            patient_data = df[df['patient_id'] == patient_id].copy()
            patient_data['timestamp'] = pd.to_datetime(
                patient_data['timestamp'])
            patient_data = patient_data.sort_values('timestamp')
            ax.plot(patient_data['timestamp'],
                    patient_data[metric], marker='o', label=patient_id)

        ax.set_title(f'{metric.replace("_", " ").title()} Comparison',
                     fontsize=14, fontweight='bold')
        ax.set_xlabel('Time')
        ax.set_ylabel(metric.replace('_', ' ').title())
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_distribution(self, df: pd.DataFrame, metric: str) -> None:
        """Plot distribution of a metric across all patients."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        axes[0].hist(df[metric], bins=30, color='skyblue', edgecolor='black')
        axes[0].set_title(
            f'Distribution of {metric.replace("_", " ").title()}')
        axes[0].set_xlabel(metric)
        axes[0].set_ylabel('Frequency')

        axes[1].boxplot(df[metric])
        axes[1].set_title(f'Box Plot of {metric.replace("_", " ").title()}')
        axes[1].set_ylabel(metric)

        plt.tight_layout()
        plt.show()

    def plot_heatmap(self, aggregated_data: pd.DataFrame) -> None:
        """Plot heatmap of aggregated patient statistics."""
        fig, ax = plt.subplots(figsize=self.figsize)

        sns.heatmap(aggregated_data, annot=True, fmt='.1f',
                    cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Value'})
        ax.set_title('Patient Vital Signs Heatmap',
                     fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.show()

    def plot_critical_alerts(self, critical_df: pd.DataFrame) -> None:
        """Visualize critical alerts by patient."""
        fig, ax = plt.subplots(figsize=(12, 6))

        alert_counts = critical_df['patient_id'].value_counts().head(10)
        alert_counts.plot(kind='barh', ax=ax, color='red')

        ax.set_title('Top 10 Patients with Critical Alerts',
                     fontsize=14, fontweight='bold')
        ax.set_xlabel('Number of Critical Events')
        ax.set_ylabel('Patient ID')

        plt.tight_layout()
        plt.show()
