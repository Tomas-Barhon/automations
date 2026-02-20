"""Data loading and processing functions."""

import pandas as pd


def get_sample_data() -> pd.DataFrame:
    """
    Generate sample financial data.

    Returns
    -------
    pd.DataFrame
        Sample financial data with date, income, expenses, and savings.
    """
    return pd.DataFrame(
        {
            "date": pd.date_range(start="2024-01-01", periods=12, freq="ME"),
            "income": [
                4500,
                4500,
                4500,
                5000,
                5000,
                4800,
                4800,
                5200,
                5200,
                5000,
                5000,
                5500,
            ],
            "expenses": [
                3200,
                2900,
                3400,
                3100,
                3600,
                3300,
                2800,
                3500,
                3200,
                3400,
                3700,
                4000,
            ],
            "savings": [
                1300,
                1600,
                1100,
                1900,
                1400,
                1500,
                2000,
                1700,
                2000,
                1600,
                1300,
                1500,
            ],
        }
    )
