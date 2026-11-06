import csv
from pprint import pprint #added for debugging for development purposes, will remove later

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

def get_summary_annotation_list(clean_allele):

    """
    Gets relevzant info and summary annotation ID

    Input: Star Allele in forma i.e CYP2C19*3
    will not accept ie CYP2C19*3/*5
    reasoning: output will also include other associated diplotype combinations

    Output: list of Dictionary of summary record
    """

    #opens the csv file and puts it into a dict to search using python
    summary_annotation_list = []

    with open("summary_annotations.tsv" , encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        #list record that can have more than one haplotype
        for record in reader:
            haplotypes = [h.strip() for h in record["Variant/Haplotypes"].split(",")]
            
            #to get exact allele match
            if clean_allele in haplotypes:

                #adds match record into list
                summary_annotation_list.append({
                    "Gene": record["Gene"],
                    "Drug(s)": record["Drug(s)"],
                    "Level of Evidence": record["Level of Evidence"],
                    "Phenotype Category": record["Phenotype Category"],
                    #"Variant/Haplotypes": record["Variant/Haplotypes"],
                    "Summary Annotation ID": record["Summary Annotation ID"],
                    
                    #this creates an empty list for star allele summary function
                    "Allele Matches":[], 
                    })

    return summary_annotation_list


def get_allele_summary(summary_annotation_list, allele_star):

    """
    Inputs summary annotation ID into summary_ann_alleles.tsv
    and outputs association of
    - star allele
    - star allele combinations
    - drug chemical 
    - associated function and metabolism
    """
    
    #got  Copilot AI to help solve issue of output of allele_summary into Allele Matches
    summaries_by_id = {
        item["Summary Annotation ID"].strip(): item
        for item in summary_annotation_list
    }

    with open("summary_ann_alleles.tsv" , encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")


        for record in reader:

            annotation_id = record["Summary Annotation ID"].strip()

            #had copilot AI suggest solve issue of reading *20s together with *2 in the summary allele file
            genotype = record["Genotype/Allele"]

            #this will standardise genotype from *1/*2 or *2/*3 + *3/*3 to match allele_star
            tokens = (
                genotype
                .replace("/", " ")
                .replace("+", " ")
                .replace(",", " ")
                .split()
            )
            
            #filter record if annotation id matches and allele star present in record
            if annotation_id in summaries_by_id and allele_star in tokens:
                #only include relevant info
                summaries_by_id[annotation_id]["Allele Matches"].append({
                    "Genotype/Allele": record["Genotype/Allele"],
                    "Annotation Text": record["Annotation Text"],
                    "Allele Function": record["Allele Function"]
                })

    return summary_annotation_list


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

    summary_list = get_summary_annotation_list(clean_allele)

    return get_allele_summary(summary_list, allele_star)


#test if work
search = input("Insert star allele: ")
summary = search_summary_annotations(search)
pprint(summary, sort_dicts=False)

