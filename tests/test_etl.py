
import pytest
import pandas as pd
import os
from src.generate_mock_data import generate_mock_data
from src.pipeline import run_pipeline

@pytest.fixture(scope='module')
def setup_data():
    """
    Fixture to set up the data for testing.
    """
    generate_mock_data()
    run_pipeline()

def test_boundary_value_analysis(setup_data):
    """
    Verify that a batch with exactly 97.9% purity is correctly classified as "Non-Compliant".
    """
    df_alerts = pd.read_csv('data/gold/alerts.csv')
    assert 'B-003' in df_alerts['batch_id'].values

def test_data_integrity_check(setup_data):
    """
    Confirm that no records with "FAIL" status exist in the Silver layer.
    """
    df_silver = pd.read_parquet('data/silver/clean.parquet')
    assert 'FAIL' not in df_silver['status'].values

def test_artifact_verification(setup_data):
    """
    Validate that all required output files are generated in their respective directories.
    """
    assert os.path.exists('data/bronze/raw.parquet')
    assert os.path.exists('data/silver/clean.parquet')
    assert os.path.exists('data/gold/compliance_report.parquet')
    assert os.path.exists('data/gold/alerts.csv')
