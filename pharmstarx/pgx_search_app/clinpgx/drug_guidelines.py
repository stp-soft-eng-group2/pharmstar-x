"""
This module uses ClinPGX guidelineAnnotation API 
to extract guideline pdf file related to the drug
and the gene.
Input: chemical/drug ID and Gene ID obtained from 
var_drug_relationship.py
and outputs:
        'guideline_id'
        'name'
        'literature'
        'source'
        'relatedChemicals'
        'relatedGenes'

"""

import requests

def get_guidelines(chemical_id, gene_id):
    """
    This function creates a guideline list of guideline information
    from an api GET request from ClinPGX database
    from CPIC and DPWG guidelines
    for drug-chemical relationship
    """

    guideline_list = []

    url = "https://api.clinpgx.org/v1/data/guidelineAnnotation"
    
    sources = ["cpic" , "dpwg"]    
    
    for source in sources:
        
        params = {
            "source": source,
            "relatedChemicals.accessionId": chemical_id,
            "relatedGenes.accessionId": gene_id,
            "view": "base"
        }
        
        headers = {
            "accept" : "*/*"
        }
    
        response = requests.get(
            url=url,
            params=params,
            headers=headers
        )

        response.raise_for_status()

        data = response.json()

        for record in data['data']:
            guideline_list.append({
                'source': source,
                'guideline_id': record['id'],
                'guideline_title': record['name'],
                'literature_file': record['literature'][0]['_sameAs'],
                'related_drug': record['relatedChemicals'],
                'related_gene': record['relatedGenes']
            })

    return guideline_list




