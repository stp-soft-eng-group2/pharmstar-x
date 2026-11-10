"""
This function fetches relationship between gene and drug using
input of gene and drug name and
outputs the relevant IDs and type of evidence.
The drug/chemical ID is used to find guideline information and link
"""

import csv
from tsv_loader import load_tsv

def get_relationship(drug_name , gene_name):
    """
    This function extracts information from the ClinPGX database
    and outputs the related drug and name ID and evidence type 
    filtered to just Guideline
    """
    #opens the csv file and puts it into a dict to search using python
    relationship_records = load_tsv("relationships.tsv")

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
    
    guideline_list = []
    for record in relationship_list:
        if "Guideline".lower() in record['Evidence'].lower():
            guideline_list.append(record)
        
    return guideline_list


"""
from pprint import pprint

pprint(get_relationship("omeprazole","CYP2C19"))
    
pprint(get_relationship("lansoprazole","CYP2C19"))
    
pprint(get_relationship("mephenytoin","CYP2C19"))
    
"""


