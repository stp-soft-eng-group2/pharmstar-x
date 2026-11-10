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


def get_clinpgx_data(star_allele):
    """
    This functin runs all the individual clinpgx modules as 'an API request response'
    and collates the relevant information for one star allele
    into json formatted file
    """

    output = {
        "star_allele": star_allele,
        "variant_summary": [],
    }

    variant_summary_records = search_summary_annotations(star_allele)

    for record in variant_summary_records:
        clean_summary = {
            "drug": record["Drug(s)"],
            "level_of_evidence": record["Level of Evidence"],
            "phenotype_category": record["Phenotype Category"],
            "summary_annotation": record["Allele Matches"],
            "drug_labels": [],
            "guidelines": []
        }

        output["variant_summary"].append(clean_summary)

        gene_name = record["Gene"]
        drug_name = record["Drug(s)"]

        drug_label_record = get_drug_label_information(
                drug_name,
                gene_name
            )

        for record in drug_label_record:
            clean_summary["drug_labels"].append({
                "source": record["Source"],
                "PGX Level": record["Testing Level"]
            })

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
                clean_summary["guidelines"].append({
                    "source": record["source"],
                    "title": record["guideline_title"],
                    "literature_link": record["literature_file"]
                })

    return output
    
