
import pandas as pd
import numpy as np

def generate_mock_data():
    """
    Generates a mock dataset for the Atorvastatin Quality Control pipeline.
    """
    data = {
        'batch_id': [f'B-{i:03d}' for i in range(1, 21)],
        'timestamp': pd.date_range(start='2024-01-01', periods=20, freq='D').strftime('%Y/%m/%d %H:%M'),
        'purity': [
            '99.5', '98.2', '97.9', '99.9', '98.0', '97.5', 'null', '99.1',
            '98.7', 'Error', '96.5', '99.3', '98.1', '97.8', '99.6', '98.4',
            '97.2', '99.0', '98.8', '97.0'
        ],
        'status': [
            'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'WARN', 'PASS',
            'PASS', 'FAIL', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'WARN',
            'PASS', 'PASS', 'PASS', 'FAIL'
        ]
    }
    df = pd.DataFrame(data)
    df.to_csv('batch_logs.csv', index=False)
    print("Mock data generated successfully.")

if __name__ == "__main__":
    generate_mock_data()
