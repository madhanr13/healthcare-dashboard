"""
Main execution script for Healthcare Data Cleaning and Visualization System
Demonstrates complete workflow from data loading to visualization
"""

from config import SAMPLE_DATA_CONFIG, CRITICAL_THRESHOLDS
from main import HealthcareAnalyticsSystem
import sys
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProjectRunner:
    """Main project execution class"""

    def __init__(self):
        self.system = HealthcareAnalyticsSystem()
        self.execution_report = {
            'start_time': datetime.now(),
            'steps_completed': [],
            'errors': [],
            'statistics': {}
        }

    def print_header(self):
        """Display project header"""
        header = """
        ╔═══════════════════════════════════════════════════════════════╗
        ║                                                               ║
        ║  HEALTHCARE DATA CLEANING & VISUALIZATION SYSTEM              ║
        ║  Clinical Insights Analytics Platform                        ║
        ║                                                               ║
        ║  Architecture: Modular Layered Architecture                   ║
        ║  Status: Production Ready                                     ║
        ║                                                               ║
        ╚═══════════════════════════════════════════════════════════════╝
        """
        print(header)

    def step_1_load_data(self):
        """Step 1: Load sample healthcare data"""
        print("\n" + "="*70)
        print("STEP 1: DATA LOADING")
        print("="*70)

        try:
            num_patients = SAMPLE_DATA_CONFIG['num_patients']
            num_records = SAMPLE_DATA_CONFIG['num_records']

            print(f"\n📊 Generating sample healthcare data...")
            print(f"   • Patients: {num_patients}")
            print(f"   • Total Records: {num_records}")
            print(
                f"   • Records per Patient (avg): {num_records // num_patients}")

            self.system.load_sample_data(
                num_patients=num_patients,
                num_records=num_records
            )

            # Display data statistics
            df = self.system.raw_data
            print(f"\n✓ Data loaded successfully")
            print(f"   • Data Shape: {df.shape}")
            print(f"   • Columns: {', '.join(df.columns.tolist())}")
            print(
                f"   • Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

            # Show sample records
            print(f"\n📋 Sample Records (first 5):")
            print(df.head().to_string())

            self.execution_report['steps_completed'].append('Data Loading')
            self.execution_report['statistics']['raw_records'] = len(df)

        except Exception as e:
            error_msg = f"Error during data loading: {str(e)}"
            print(f"\n✗ {error_msg}")
            self.execution_report['errors'].append(error_msg)
            raise

    def step_2_data_cleaning(self):
        """Step 2: Execute data cleaning pipeline"""
        print("\n" + "="*70)
        print("STEP 2: DATA CLEANING & VALIDATION")
        print("="*70)

        try:
            print(f"\n🧹 Executing data cleaning pipeline...")

            self.system.clean_data()

            cleaned_df = self.system.cleaned_data
            raw_df = self.system.raw_data

            print(f"\n✓ Data cleaning completed")
            print(f"   • Records before: {len(raw_df)}")
            print(f"   • Records after: {len(cleaned_df)}")
            print(f"   • Records removed: {len(raw_df) - len(cleaned_df)}")
            print(
                f"   • Data quality improvement: {((len(raw_df) - len(cleaned_df)) / len(raw_df) * 100):.2f}%")

            # Display cleaned data sample
            print(f"\n📋 Sample of Cleaned Data (first 5):")
            print(cleaned_df.head().to_string())

            self.execution_report['steps_completed'].append('Data Cleaning')
            self.execution_report['statistics']['cleaned_records'] = len(
                cleaned_df)
            self.execution_report['statistics']['records_removed'] = len(
                raw_df) - len(cleaned_df)

        except Exception as e:
            error_msg = f"Error during data cleaning: {str(e)}"
            print(f"\n✗ {error_msg}")
            self.execution_report['errors'].append(error_msg)
            raise

    def step_3_critical_analysis(self):
        """Step 3: Analyze critical patients"""
        print("\n" + "="*70)
        print("STEP 3: CRITICAL PATIENT ANALYSIS")
        print("="*70)

        try:
            print(f"\n⚠️  Identifying critical patients...")

            critical_df = self.system.analyze_critical_patients()

            if len(critical_df) > 0:
                print(f"\n✓ Critical analysis completed")
                print(f"   • Critical events found: {len(critical_df)}")
                print(
                    f"   • Unique patients with critical events: {critical_df['patient_id'].nunique()}")

                # Show critical events breakdown
                print(f"\n📊 Critical Events Breakdown:")
                critical_counts = critical_df['patient_id'].value_counts().head(
                    5)
                for patient_id, count in critical_counts.items():
                    print(f"   • {patient_id}: {count} events")

                self.execution_report['statistics']['critical_events'] = len(
                    critical_df)
                self.execution_report['statistics']['critical_patients'] = critical_df['patient_id'].nunique(
                )
            else:
                print(f"\n✓ No critical events detected in current dataset")
                self.execution_report['statistics']['critical_events'] = 0

            self.execution_report['steps_completed'].append(
                'Critical Analysis')

        except Exception as e:
            error_msg = f"Error during critical analysis: {str(e)}"
            print(f"\n✗ {error_msg}")
            self.execution_report['errors'].append(error_msg)
            raise

    def step_4_patient_reports(self):
        """Step 4: Generate individual patient reports"""
        print("\n" + "="*70)
        print("STEP 4: PATIENT REPORTS GENERATION")
        print("="*70)

        try:
            print(f"\n📄 Generating detailed patient reports...")

            # Get unique patients
            patients = self.system.cleaned_data['patient_id'].unique()[:3]

            print(
                f"\n✓ Generating reports for sample patients ({len(patients)} shown):")

            for i, patient_id in enumerate(patients, 1):
                print(f"\n{i}. {patient_id}")
                print("-" * 50)
                stats = self.system.get_patient_report(patient_id)
                self.execution_report['steps_completed'].append(
                    f'Report for {patient_id}')

        except Exception as e:
            error_msg = f"Error during report generation: {str(e)}"
            print(f"\n✗ {error_msg}")
            self.execution_report['errors'].append(error_msg)
            raise

    def step_5_aggregated_analysis(self):
        """Step 5: Generate aggregated statistics"""
        print("\n" + "="*70)
        print("STEP 5: AGGREGATED STATISTICS & INSIGHTS")
        print("="*70)

        try:
            print(f"\n📊 Computing aggregated statistics...")

            aggregated = self.system.processor.aggregate_by_patient()

            print(f"\n✓ Aggregation completed")
            print(f"   • Total unique patients: {len(aggregated)}")
            print(f"\n📈 Top 10 Patients by Average Heart Rate:")
            print("-" * 70)

            # Get mean heart rate
            if ('heart_rate', 'mean') in aggregated.columns:
                hr_means = aggregated[('heart_rate', 'mean')].sort_values(
                    ascending=False).head(10)
                for rank, (patient_id, hr) in enumerate(hr_means.items(), 1):
                    print(f"   {rank:2d}. {patient_id}: {hr:.1f} bpm")

            self.execution_report['steps_completed'].append(
                'Aggregated Analysis')
            self.execution_report['statistics']['total_patients'] = len(
                aggregated)

        except Exception as e:
            error_msg = f"Error during aggregated analysis: {str(e)}"
            print(f"\n✗ {error_msg}")
            self.execution_report['errors'].append(error_msg)
            raise

    def step_6_summary(self):
        """Step 6: Display execution summary"""
        print("\n" + "="*70)
        print("STEP 6: EXECUTION SUMMARY & CONCLUSION")
        print("="*70)

        execution_time = (
            datetime.now() - self.execution_report['start_time']).total_seconds()

        print(f"\n✓ PROJECT EXECUTION COMPLETED")
        print(f"\n📊 Execution Statistics:")
        print(f"   • Total Execution Time: {execution_time:.2f} seconds")
        print(
            f"   • Steps Completed: {len(self.execution_report['steps_completed'])}")
        print(
            f"   • Errors Encountered: {len(self.execution_report['errors'])}")

        print(f"\n📈 Data Processing Statistics:")
        stats = self.execution_report['statistics']
        print(f"   • Raw Records: {stats.get('raw_records', 0):,}")
        print(f"   • Cleaned Records: {stats.get('cleaned_records', 0):,}")
        print(f"   • Records Removed: {stats.get('records_removed', 0):,}")
        print(f"   • Total Patients: {stats.get('total_patients', 0)}")
        print(f"   • Critical Events: {stats.get('critical_events', 0)}")

        print(f"\n🎯 System Capabilities Demonstrated:")
        capabilities = [
            "Data Loading & Validation",
            "Duplicate Detection & Removal",
            "Missing Value Imputation",
            "Outlier Detection & Removal",
            "Clinical Range Validation",
            "Critical Patient Identification",
            "Patient Statistics Calculation",
            "Data Aggregation & Analysis",
            "Report Generation"
        ]
        for capability in capabilities:
            print(f"   ✓ {capability}")

        print(f"\n💡 Next Steps:")
        print(f"   • Use visualize_patient() to generate patient vital sign charts")
        print(f"   • Use visualize_critical_alerts() for alert dashboard")
        print(f"   • Load real data using load_data_from_csv()")
        print(f"   • Customize thresholds in config.py")
        print(f"   • Deploy to production environment")

        print(f"\n" + "="*70)
        print("Thank you for using the Healthcare Analytics System!")
        print("="*70 + "\n")

    def run(self):
        """Execute complete workflow"""
        try:
            self.print_header()

            self.step_1_load_data()
            self.step_2_data_cleaning()
            self.step_3_critical_analysis()
            self.step_4_patient_reports()
            self.step_5_aggregated_analysis()
            self.step_6_summary()

            return True

        except Exception as e:
            print(f"\n\n✗ FATAL ERROR: {str(e)}")
            print("\nExecution halted due to critical error.")
            return False


def main():
    """Main entry point"""
    runner = ProjectRunner()
    success = runner.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
