
import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "clinpgx_data" 

def load_tsv(filename):

    """
    TSV reader/loader function 
    Input: TSV formatted file
    Output: Content of TSV file into a list of dictionaries
    """
    logger.info("loading %s TSV file.." , filename)
    with open(
        DATA_DIR / filename ,
        encoding = "utf-8"
    ) as f:
    
        reader = csv.DictReader(
            f, 
            delimiter = "\t"
            )
        records = list(reader)
        logger.info("%s records successfully parsed" , filename)

    if not records:
        raise ValueError(f"TSV file is empty: {filename}")

    return records
