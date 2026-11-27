import pytest
from drug_label import get_drug_label_information

@pytest.fixture
def sample_drug_label_dataset():
    return [{
        'PharmGKB ID': "PA123",
        'Name': "Drug Label Info Clopidogrel",
        'Source': "FDA",
        'Testing Level': "Actionable PGX",
        'Chemicals': "clopidogrel",
        'Genes': "ABC",
        'Variants/Haplotypes': "ABC*1"
        },
        {
        'PharmGKB ID': "PA234",
        'Name': "Drug Label Info Clopidogrel",
        'Source': "EMA",
        'Testing Level': "Informative PGX",
        'Chemicals': "clopidogrel",
        'Genes': "ABC",
        'Variants/Haplotypes': "ABC*1,ABC*2"
        },
        {
        'PharmGKB ID': "PA345",
        'Name': "Drug Label Info Paracetamol",
        'Source': "EMA",
        'Testing Level': "Informative PGX",
        'Chemicals': "paracetamol",
        'Genes': "DEF",
        'Variants/Haplotypes': "DEF*1"
        }
    ]

def test_happy_path(monkeypatch, sample_drug_label_dataset):
    
    monkeypatch.setattr(
        "drug_label.load_tsv",
        lambda _:sample_drug_label_dataset
    )

    test_result = get_drug_label_information("clopidogrel","ABC")

    #also test multiple matches
    assert len(test_result) == 2
    assert test_result[1]["Drug Label ID"] == "PA234"
    assert test_result[0]["Testing Level"] == "Actionable PGX"
    assert test_result[0]["Chemicals"] == "clopidogrel"


def test_no_match_results(monkeypatch, sample_drug_label_dataset):

    monkeypatch.setattr(
        "drug_label.load_tsv",
        lambda _:sample_drug_label_dataset
    )
    #drug does not match gene
    test_result = get_drug_label_information("paracetamol","ABC")
    #gene does not match drug
    test_result_2 = get_drug_label_information("clopidogrel","DEF")

    assert test_result == []
    assert test_result_2 == []    


def test_case_insensitive(monkeypatch, sample_drug_label_dataset):

    monkeypatch.setattr(
        "drug_label.load_tsv",
        lambda _:sample_drug_label_dataset
    )

    test_result = get_drug_label_information("ClopidoGrel","ABC")

    assert len(test_result) == 2

def test_output_structure(monkeypatch, sample_drug_label_dataset):
    monkeypatch.setattr(
        "drug_label.load_tsv",
        lambda _:sample_drug_label_dataset
    )
    
    test_result = get_drug_label_information("Clopidogrel","ABC")

    assert "Drug Label ID" in test_result[0]
    assert "Name" in test_result[0]
    assert "Source" in test_result[0]
    assert "Testing Level" in test_result[0]


