"""
This modules extracts the summaries of pharmacogenomic annotations for query star allele from
ClinPGX database. It uses summary annotation id to link all relevant information such as:
    - Gene
    - Drug
    - Level of evidence
    - Phenotype Category
    - Allele Matches: 
        - Allele combinations
        - Drug
        - Function and metabolism

Input = Star Allele

Output =  summary of annotation in dictinary format

"""

import csv
from tsv_loader import load_tsv



def get_summary_annotation(star_allele):

    """
    Gets relevant info and summary annotation ID

    Input: Star Allele in format i.e CYP2C19*3
   

    Output: list of Dictionary of summary record
    """

    #load list of dataset
    annotation_records = load_tsv("summary_annotations.tsv")

    #empty list to load dict with relevant information
    summary_annotation_list = []

    #list record that can have more than one haplotype
    for record in annotation_records:
        haplotypes = [h.strip() for h in record["Variant/Haplotypes"].split(",")]
            
        #to get exact allele match
        if star_allele in haplotypes:

            #adds match record into list
            summary_annotation_list.append({
                "Gene": record["Gene"],
                "Drug(s)": record["Drug(s)"],
                "Level of Evidence": record["Level of Evidence"],
                "Phenotype Category": record["Phenotype Category"],
                "Variant/Haplotypes": record["Variant/Haplotypes"],
                "Summary Annotation ID": record["Summary Annotation ID"],
                #this creates an empty list for star allele summary function                    
                "Allele Matches":[], 
                })

    return summary_annotation_list


def get_allele_summary(summary_annotation_list, allele_star):

    """
    Inputs summary annotation ID into summary_ann_alleles.tsv
    Outputs association of:
    - star allele
    - star allele combinations
    - drug chemical 
    - associated function and metabolism
    """
    
    #got  Copilot AI to help solve issue of output of allele_summary into Allele Matches. if more than 1 summary annotation id
    summaries_by_id = {}

    for record in summary_annotation_list:
        annotation_id = record["Summary Annotation ID"].strip()
        summaries_by_id[annotation_id] = record
    

    #load list of dataset
    allele_summary_records = load_tsv("summary_ann_alleles.tsv")


    for record in allele_summary_records:

        annotation_id = record["Summary Annotation ID"].strip()

        #had copilot AI suggest solve issue of reading *20s together with *2 in the summary allele file
        genotype = record["Genotype/Allele"]


            
        #filter record if annotation id matches and allele star present in record
        if annotation_id in summaries_by_id and allele_star == genotype:
            #only include relevant info
            summaries_by_id[annotation_id]["Allele Matches"].append({
                "Genotype/Allele": record["Genotype/Allele"],
                "Annotation Text": record["Annotation Text"],
            })

    return [record for record in summary_annotation_list if record["Allele Matches"]]


def search_summary_annotations(allele):

    """
    combines get_summary_annotation_list and get_allele_summary
    cleans query and separates gene from star
    """
    #remove whitespaces
    clean_allele = allele.strip()

    # separates * to use as inout in get_allele_summary function
    allele_gene, star = clean_allele.split("*", 1)
    allele_star = "*" + star

    summary_list = get_summary_annotation(clean_allele)

    return get_allele_summary(summary_list, allele_star)

"""
from pprint import pprint

pprint(search_summary_annotations("CYP2C19*5"),  sort_dicts=False)"""