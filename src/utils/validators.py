# src/utils/validators.py

import pandas as pd
from config import DataConfig


def check_nulls(df):
    null_count = df.isnull().sum().sum()
    total_values = df.size
    null_percentage = (null_count / total_values) * 100

    return {
        'has_nulls': null_count > 0,
        'null_count': null_count,
        'null_percentage': round(null_percentage, 2)
    }


def check_duplicates(df):
    duplicate_count = df.duplicated().sum()
    total_rows = len(df)
    duplicate_percentage = (duplicate_count / total_rows) * \
        100 if total_rows > 0 else 0

    return {
        'has_duplicates': duplicate_count > 0,
        'duplicate_count': duplicate_count,
        'duplicate_percentage': round(duplicate_percentage, 2)
    }


def check_outliers(df, column, threshold=3):
    mean = df[column].mean()
    std = df[column].std()

    outliers = df[(df[column] < mean - threshold * std) |
                  (df[column] > mean + threshold * std)]
    outlier_count = len(outliers)
    total_rows = len(df)
    outlier_percentage = (outlier_count / total_rows) * \
        100 if total_rows > 0 else 0

    return {
        'has_outliers': outlier_count > 0,
        'outlier_count': outlier_count,
        'outlier_percentage': round(outlier_percentage, 2)
    }


def validate_data(df):
    results = {
        'nulls': check_nulls(df),
        'duplicates': check_duplicates(df),
        'close_outliers': check_outliers(df, 'close') if 'close' in df.columns else None
    }

    # Overall pass/fail
    results['passed'] = (
        not results['nulls']['has_nulls'] and
        not results['duplicates']['has_duplicates']
    )

    return results
