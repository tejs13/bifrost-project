# created by Patel Tejaskumar
# export.py

import os
import pandas as pd
from constants import OUTPUT_DIR


def export_tracking_data(tracking_data):
    """
    Export the data into CSV
    :param tracking_data:
    :return:
    """
    tracking_df = pd.DataFrame(tracking_data)
    tracking_csv_path = os.path.join(OUTPUT_DIR, 'tracking_data.csv')
    tracking_df.to_csv(tracking_csv_path, index=False)
    return tracking_csv_path
