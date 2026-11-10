"""
This modules extracts the drug label annotations for query star allele from
ClinPGX database. It uses inputs of chemical name and gene name

It outputs a summary of:
                'PharmGKB ID': record['PharmGKB ID'],
                'Name': record['Name'],
                'Source': record['Source'],
                'Testing Level': record['Testing Level'],
                'Chemicals': record['Chemicals'],
                'Genes': record['Genes'],
                'Variants/Haplotypes': record['Variants/Haplotypes']
"""

import csv
from tsv_loader import load_tsv

def get_drug_label_information(drug_name, gene_name):
    """
    This function extracts information from the ClinPGX database and outputs information
    relevant to drug label annotation
    """

    #opens the csv file and puts it into a dict to search using python
    drug_label_records = load_tsv("drugLabels.tsv")

    drug_label_list = []

    #search through the dictionary for search input. if true, adds result into the list
    for record in drug_label_records:
        if drug_name.lower() in record["Chemicals"].strip().lower() and gene_name.lower() in record["Genes"].lower():
            
            drug_label_list.append({
                'Drug Label ID': record['PharmGKB ID'],
                'Name': record['Name'],
                'Source': record['Source'],
                'Testing Level': record['Testing Level'],
                'Chemicals': record['Chemicals'],
                'Genes': record['Genes'],
                'Variants/Haplotypes': record['Variants/Haplotypes']
                })
    return drug_label_list
