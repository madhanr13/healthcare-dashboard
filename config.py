"""
Configuration settings for Healthcare Data Cleaning and Visualization System
"""

# Vital Signs Valid Ranges
VITAL_SIGN_RANGES = {
    'heart_rate': (40, 200),              # bpm
    'blood_pressure_systolic': (70, 200),  # mmHg
    'blood_pressure_diastolic': (40, 130),  # mmHg
    'temperature': (35, 42),              # Celsius
    'respiratory_rate': (8, 40),          # breaths/min
    'oxygen_saturation': (80, 100)        # percentage
}

# Critical Alert Thresholds
CRITICAL_THRESHOLDS = {
    'heart_rate_high': 100,
    'heart_rate_low': 60,
    'oxygen_saturation_low': 90,
    'temperature_high': 38.5,
    'temperature_low': 36,
    'blood_pressure_systolic_high': 140,
    'blood_pressure_diastolic_high': 90
}

# Data Cleaning Configuration
CLEANING_CONFIG = {
    'missing_threshold': 0.5,
    'outlier_method': 'iqr',  # 'iqr' or 'zscore'
    'missing_value_strategy': 'median',  # 'mean', 'median', or 'forward_fill'
    'duplicate_subset': ['patient_id', 'timestamp'],
    'remove_duplicates': True
}

# Data Processing Configuration
PROCESSING_CONFIG = {
    'aggregation_period': '1D',  # '1D', '1H', '1W'
    'moving_average_window': 7,
    'enable_trend_analysis': True
}

# Visualization Configuration
VISUALIZATION_CONFIG = {
    'figure_size': (15, 10),
    'style': 'whitegrid',
    'color_palette': 'Set2',
    'dpi': 100,
    'save_plots': False,
    'output_format': 'png'
}

# Sample Data Generation
SAMPLE_DATA_CONFIG = {
    'num_patients': 15,
    'num_records': 1500,
    'random_seed': 42,
    'missing_value_percentage': 0.05,
    'outlier_percentage': 0.02
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'healthcare_system.log'
}

# System Configuration
SYSTEM_CONFIG = {
    'debug_mode': False,
    'verbose': True,
    'max_records_in_memory': 100000,
    'enable_caching': True,
    'cache_ttl': 3600  # seconds
}
