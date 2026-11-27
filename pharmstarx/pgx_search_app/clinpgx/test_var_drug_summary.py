import pytest

from var_drug_summary import get_summary_annotation , get_allele_summary , search_summary_annotations

#need to use monkeypatch to mock the dependencies in this case the load.tsv
#use fixture as mock dataset

@pytest.fixture
def sample_summary_dataset():
    return [{
        "Gene": "ABC",
        "Drug(s)": "clopidogrel",
        "Level of Evidence": "1A",
        "Phenotype Category": "Toxicity",
        "Variant/Haplotypes": "ABC*1",
        "Summary Annotation ID": "123", 
        "Allele Matches":[], 
        } ,
        {
        "Gene": "ABC",
        "Drug(s)": "paracetamol",
        "Level of Evidence": "3",
        "Phenotype Category": "Metabolism",
        "Variant/Haplotypes": "ABC*1 , ABC*2, ABC*23",
        "Summary Annotation ID": "456", 
        "Allele Matches":[], 
        } ,
        {
        "Gene": "ABC",
        "Drug(s)": "omeprazole",
        "Level of Evidence": "3",
        "Phenotype Category": "Metabolism",
        "Variant/Haplotypes": "ABC*2 , ABC*23",
        "Summary Annotation ID": "789", 
        "Allele Matches":[], 
        } ,
    ]

@pytest.fixture
def sample_allele_dataset():
    return [{
        "Summary Annotation ID": "123",
        "Genotype/Allele": "*1",
        "Annotation Text": "Reduced function"
        },
        {
        "Summary Annotation ID": "123",
        "Genotype/Allele": "*11",
        "Annotation Text": "Increased function"
        },
        {
        "Summary Annotation ID": "456",
        "Genotype/Allele": "*1",
        "Annotation Text": "Reduced function"
        }
    ]



#use monkeypatch to mock load_tsvin get_summary_annotation function
def test_return_summary_valid_allele(monkeypatch, sample_summary_dataset):
    
    monkeypatch.setattr(
        #fucntion to replace, pythonfile.function, sample dataset
        "var_drug_summary.load_tsv", 
        #lambda used to substitute load_tsv function to use dataset
        lambda _:sample_summary_dataset
    )
    
    test_result = get_summary_annotation("ABC*1")

    assert len(test_result) == 2
    assert test_result[0]["Drug(s)"] == "clopidogrel"
    assert test_result[1]["Drug(s)"] == "paracetamol"



def test_return_empty_if_not_allele(monkeypatch, sample_summary_dataset):

    monkeypatch.setattr(
    #fucntion to replace, pythonfile.function, sample dataset
    "var_drug_summary.load_tsv",
    #lambda used to substitute load_tsv function to use dataset
    lambda _:sample_summary_dataset
    )
    
    test_result = get_summary_annotation("ABC*5")

    assert test_result == []



def test_matching_summary_annotation_id(monkeypatch, sample_summary_dataset, sample_allele_dataset):
    
    monkeypatch.setattr(
    #function to replace, pythonfile.function, sample dataset
    "var_drug_summary.load_tsv",
    #lambda used to substitute load_tsv function to use dataset
    lambda _:sample_allele_dataset
    )

    test_result = get_allele_summary(sample_summary_dataset, "*1")

    assert test_result[0]["Summary Annotation ID"] == "123"
    assert len(test_result[0]["Allele Matches"]) == 1


def test_exact_allele_match_only(monkeypatch, sample_summary_dataset, sample_allele_dataset):

    monkeypatch.setattr(
    #function to replace, pythonfile.function, sample dataset
    "var_drug_summary.load_tsv",
    #lambda used to substitute load_tsv function to use dataset
    lambda _:sample_allele_dataset
    )

    test_result = get_allele_summary(sample_summary_dataset, "*1")

    assert test_result[0]["Allele Matches"][0]["Genotype/Allele"] == "*1"
    assert test_result[0]["Summary Annotation ID"] == "123"
    assert len(test_result[0]["Allele Matches"]) == 1


def test_functions_happy_path():
    #uses real dataset
    result = search_summary_annotations("CYP2C19*5")

    assert len(result) > 0

def test_correct_final_output():
    #uses real dataset
    result = search_summary_annotations("CYP2C19*5")

    assert "Gene" in result[0]
    assert "Drug(s)" in result[0]
    assert "Allele Matches" in result[0]


def test_invalid_input_format():

    with pytest.raises(ValueError):
        search_summary_annotations("ABC")    #valueError?

def test_empty_string_input():

    with pytest.raises(ValueError):
        search_summary_annotations("")   #valueEror?