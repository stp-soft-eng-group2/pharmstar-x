import pytest
from gene_drug_relationship import get_relationship

#using monkeypatch to replace load_tsv function with fixture dataset
@pytest.fixture
def sample_relationship_dataset():
    return[{
        'Entity2_id': "PA123",
        'Entity2_name': "omeprazole",
        'Entity1_id': "PA001",
        'Entity1_name': "ABC",
        'Evidence': "VariantAnnotation,Guideline,SummaryAnnotation"
    },
    {
        'Entity2_id': "PA456",
        'Entity2_name': "clopidogrel",
        'Entity1_id': "PA001",
        'Entity1_name': "ABC",
        'Evidence': "VariantAnnotation,Guideline,SummaryAnnotation"
    },
    {
        'Entity2_id': "PA456",
        'Entity2_name': "paracetamol",
        'Entity1_id': "PA001",
        'Entity1_name': "ABC",
        'Evidence': "VariantAnnotation,SummaryAnnotation"
    }]

def test_happy_path(monkeypatch, sample_relationship_dataset):
    #act in place of load_tsv function
    monkeypatch.setattr(
        "gene_drug_relationship.load_tsv",
        lambda _:sample_relationship_dataset
    )

    test_result = get_relationship("clopidogrel","ABC")
    print(test_result)

    assert test_result[0]["Gene_id"] == "PA001"
    assert test_result[0]["Chemical_id"] == "PA456"
    assert test_result[0]["Evidence"] == "VariantAnnotation,Guideline,SummaryAnnotation"


def test_no_match_results(monkeypatch, sample_relationship_dataset):

    monkeypatch.setattr(
        "gene_drug_relationship.load_tsv",
        lambda _:sample_relationship_dataset
    )
    #drug does not match gene
    test_result = get_relationship("warfarin","ABC")
    #gene does not match drug
    test_result_2 = get_relationship("clopidogrel","DEF")

    assert test_result == []
    assert test_result_2 == []    


def test_case_insensitive(monkeypatch, sample_relationship_dataset):

    monkeypatch.setattr(
        "gene_drug_relationship.load_tsv",
        lambda _:sample_relationship_dataset
    )

    test_result = get_relationship("ClopidoGrel","AbC")
    print(test_result)

    assert test_result[0]["Gene_id"] == "PA001"

def test_no_guideline(monkeypatch, sample_relationship_dataset):
    
    # match successful but no guideline
    monkeypatch.setattr(
        "gene_drug_relationship.load_tsv",
        lambda _:sample_relationship_dataset
    )
    
    test_result = get_relationship("paracetamol","ABC")

    assert test_result == []



def test_output_structure(monkeypatch, sample_relationship_dataset):
    
    monkeypatch.setattr(
        "gene_drug_relationship.load_tsv",
        lambda _:sample_relationship_dataset
    )
    
    test_result = get_relationship("Clopidogrel","ABC")

    print(test_result)

    assert "Gene_id" in test_result[0]
    assert "Gene_name" in test_result[0]
    assert "Chemical_id" in test_result[0]
    assert "Chemical_name" in test_result[0]
    assert "Evidence" in test_result[0]