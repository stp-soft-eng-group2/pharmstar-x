"""
This modules extracts the summaries of pharmacogenomic annotations from ClinPGX database.
It uses input from PharmVar output and link different ClinPGX resources
- Drug-Variant-Chemical relationship
- Drug Label Annotation
- Summary Annotation 
- Drug Guidelines
link relevant information into a single JSON output

Input:
- Star Allele from PharmVar dataset output

Output:
A summary annotation for input variant and drug associated information such as:

    - Gene name
    - Haplotype/Variant
    - Drug/Chemical name
        - PGX level (glossary)(sorted)
        - Phenotype Category
        - Level of evidence (sorted descending)(glossary)
        - Summary of annotation
        - Guideline Link for CPIC and DPWG(pdf file link)

flow of functions
"""

from gene_drug_relationship import get_relationship
from drug_label import get_drug_label_information
from var_drug_summary import (get_summary_annotation , get_allele_summary, search_summary_annotations)
from drug_guidelines import get_guidelines
import logging

logger = logging.getLogger(__name__)

def get_clinpgx_data(star_allele):
    """
    This functin runs all the individual clinpgx modules as 'an API request response'
    and collates the relevant information for one star allele
    into json formatted file
    """
    logger.info("Creating ClinPGX dictionary..")
    #creates the dictionary output format
    output = {
        "star_allele": star_allele,
        "variant_summary": [],
    }

    try:
        variant_summary_records = search_summary_annotations(star_allele)
    except ValueError:
        logger.exception("Invalid star allele: %s", star_allele)
        raise

    for record in variant_summary_records:
        logger.info("Obtaining drug variant info...")
        clean_summary = {
            "drug": record["Drug(s)"],
            "level_of_evidence": record["Level of Evidence"],
            "phenotype_category": record["Phenotype Category"],
            "summary_annotation": record["Allele Matches"],
            "drug_labels": [],
            "guidelines": []
        }
        #combine variant summary and extract drug and gene record
        output["variant_summary"].append(clean_summary)

        gene_name = record["Gene"]
        drug_name = record["Drug(s)"]

        drug_label_record = get_drug_label_information(
                drug_name,
                gene_name
            )
        #combines drug label record using durg and gene record from variant summary
        for record in drug_label_record:
            logger.info("Obtaining drug label info...")
            clean_summary["drug_labels"].append({
                "source": record["Source"],
                "PGX Level": record["Testing Level"]
            })
        #combine guidelines through relationship records
        relationships = get_relationship(
            drug_name,
            gene_name
        )

        for relationship in relationships:
            guidelines_record = get_guidelines(
                    relationship["Chemical_id"],
                    relationship["Gene_id"]
                )

            for record in guidelines_record:
                logger.info("Obtaining guideline info...")
                clean_summary["guidelines"].append({
                    "source": record["source"],
                    "title": record["guideline_title"],
                    "literature_link": record["literature_file"]
                })
    
    logger.info("Successfully created ClinPGX dictionary for star allele %s", star_allele,)

    return output
    

