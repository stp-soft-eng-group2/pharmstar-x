"""
This function fetches relationship between gene and drug using
input of gene and drug name and
outputs the relevant IDs and type of evidence.
The drug/chemical ID is used to find guideline information and link
"""
import logging
import csv
from tsv_loader import load_tsv

logger = logging.getLogger(__name__)

def get_relationship(drug_name , gene_name):
    """
    This function extracts information from the ClinPGX database
    and outputs the related drug and name ID and evidence type 
    filtered to just Guideline
    """
    logger.info("Obtaining relationship records of gene and chemical to get guideline records..")
    try:
        #opens the csv file and puts it into a dict to search using python
        relationship_records = load_tsv("relationships.tsv")
    except (csv.Error):
        logger.error("Could not load relationships.tsv")
        raise

    if not relationship_records:
        logger.warning("relationships.tsv contains no records")
        return []

    relationship_list =[]
    #search through the dictionary for search input. if true, adds result into the list
    for record in relationship_records:
        if gene_name.lower() == record["Entity1_name"].strip().lower() and drug_name.lower() == record["Entity2_name"].strip().lower():
            relationship_list.append({
                'Gene_id': record['Entity1_id'],
                'Gene_name': record['Entity1_name'],
                'Chemical_id': record['Entity2_id'],
                'Chemical_name': record['Entity2_name'],
                'Evidence': record['Evidence']
            })
    #filters evidence record for guideline only
    guideline_list = []
    for record in relationship_list:
        if "Guideline".lower() in record['Evidence'].lower():
            guideline_list.append(record)

    logger.info("Successfully created list of gene and chemical IDs needed to obtain guidelines")
    return guideline_list



