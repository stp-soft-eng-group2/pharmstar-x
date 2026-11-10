
import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent / "clinpgx_data" 

def load_tsv(filename):

    """
    TSV reader/loader function 

    Input: TSV formatted file

    Output: Content of TSV file into a list of dictionaries
    
    """

    with open(
        DATA_DIR / filename ,
        encoding = "utf-8"
    ) as f:
    
        reader = csv.DictReader(
            f, 
            delimiter = "\t"
            )
        return list(reader)