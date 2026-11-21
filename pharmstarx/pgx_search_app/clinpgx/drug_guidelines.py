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
import logging

logger = logging.getLogger(__name__)

def get_guidelines(chemical_id, gene_id):
    """
    This function creates a guideline list of guideline information
    from an api GET request from ClinPGX database
    from CPIC and DPWG guidelines
    for drug-chemical relationship
    """
    logger.info("calling ClinPGX API request for guideline info...")
    guideline_list = []

    url = "https://api.clinpgx.org/v1/data/guidelineAnnotation"
    
    sources = ["cpic" , "dpwg"]    
    
    #loops through each source
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
    
        try:
            response = requests.get(
                url=url,
                params=params,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

        except requests.RequestException:
            logger.exception(
                "ClinPGx guideline request failed for: %s and %s",chemical_id,gene_id)
            raise

        #had ai fix for me due to an error if file returns empty url, added a loop, if not return[]
        for record in data['data']:
            literature_file = next(
                (
                    literature.get('_sameAs')
                    for literature in (record.get('literature') or [])
                    if literature.get('_sameAs')
                ),
                None
            )
            guideline_list.append({
                'source': source,
                'guideline_id': record['id'],
                'guideline_title': record['name'],
                'literature_file': literature_file,
                'related_drug': record['relatedChemicals'],
                'related_gene': record['relatedGenes']
            })
    
    logger.info("API request successfully obtained guideline records")
    
    return guideline_list


