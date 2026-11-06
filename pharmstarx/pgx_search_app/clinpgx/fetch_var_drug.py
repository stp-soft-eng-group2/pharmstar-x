import csv
from pprint import pprint

"""
Fetch Var-Drug Annotation from variantAnnotations.zip
This function uses star allele to fetch a record of variant-drug annotation from ClinPGX file

Input = Star Allele

Output =  record of variant annotation from ClinPGX file

"""

search =  "CYP2C19*5"

results = []

#opens the csv file and puts it into a dict to search using python
with open("var_drug_ann.tsv" , encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    print(reader.fieldnames)


#search through the dictionary for search input. if true, adds result into the list
    for record in reader:
        if search in record["Variant/Haplotypes"].strip():
            results.append(record)




print(f"Found {len(results)} matches")
pprint(results, sort_dicts=False)