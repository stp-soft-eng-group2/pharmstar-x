import pytest
import requests
from drug_guidelines import get_guidelines


def test_search_guidelines_happy_path():

    test_chemical_id = "PA450704"
    test_gene_id = "PA124"

    test_response = get_guidelines(test_chemical_id,test_gene_id)

    assert isinstance(test_response, list)
    assert len(test_response) > 0

def test_search_guidelines_fail():
    
    test_chemical_id = "PA450704"
    test_gene_id = "PA125"

    with pytest.raises(requests.HTTPError):
        get_guidelines(test_chemical_id,test_gene_id)


def test_output_structure():

    test_chemical_id = "PA450704"
    test_gene_id = "PA124"

    test_response = get_guidelines(test_chemical_id,test_gene_id)
    
    assert "guideline_id" in test_response[0]
    assert "guideline_title" in test_response[0]
    assert "literature_file" in test_response[0]


def test_output_all_sources():

    test_chemical_id = "PA450704"
    test_gene_id = "PA124"

    test_response = get_guidelines(test_chemical_id,test_gene_id)
    
    sources = {result["source"] for result in test_response}

    assert "cpic" in sources
    assert "dpwg" in sources

