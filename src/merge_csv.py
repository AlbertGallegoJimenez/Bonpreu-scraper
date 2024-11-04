import pandas as pd
from pathlib import Path
import time
import os

def merge_csv():
    """
    Merge all csv files in the data directory into a single csv file.
    """
    # Get all csv files in the data directory
    data_dir = Path(__file__).parent.parent / "data"
    files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv') and not f.startswith('bonpreu_products_')]

    # Read all csv files and merge them
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

    # Save the merged dataframe to a new csv file
    df.to_csv(os.path.join(data_dir, f'bonpreu_products_{time.strftime("%Y%m%d_%H%M%S")}.csv'), index=False)
    
if __name__ == '__main__':
    merge_csv()