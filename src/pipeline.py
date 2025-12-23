
import pandas as pd
import os
from datetime import datetime

def run_pipeline():
    """
    Runs the Atorvastatin Quality Control ETL pipeline.
    """
    # Create directories if they don't exist
    os.makedirs('data/bronze', exist_ok=True)
    os.makedirs('data/silver', exist_ok=True)
    os.makedirs('data/gold', exist_ok=True)

    # --- Bronze Layer ---
    df_raw = pd.read_csv('batch_logs.csv')
    df_raw['ingestion_time'] = datetime.utcnow()
    df_raw.to_parquet('data/bronze/raw.parquet')

    # --- Silver Layer ---
    df_silver = pd.read_parquet('data/bronze/raw.parquet')
    df_silver['purity'] = pd.to_numeric(df_silver['purity'], errors='coerce').fillna(0.0)
    df_silver = df_silver[df_silver['status'] != 'FAIL']
    df_silver = df_silver.drop_duplicates(subset=['batch_id'])
    df_silver.to_parquet('data/silver/clean.parquet')

    # --- Gold Layer ---
    df_gold = pd.read_parquet('data/silver/clean.parquet')
    df_gold['compliance_status'] = df_gold['purity'].apply(lambda x: 'Compliant' if x >= 98.0 else 'Non-Compliant')
    df_gold.to_parquet('data/gold/compliance_report.parquet')

    df_alerts = df_gold[df_gold['compliance_status'] == 'Non-Compliant']
    df_alerts.to_csv('data/gold/alerts.csv', index=False)

    print("ETL pipeline executed successfully.")

if __name__ == "__main__":
    run_pipeline()
