import pytest

from clinpgx_service import get_clinpgx_data


def test_clinpgx_happy_path():

    test_allele = "CYP2C19*5"

    test_result = get_clinpgx_data(test_allele)

    assert len(test_result) > 0
    assert isinstance(test_result, dict)


def test_empty_input():
    
    with pytest.raises(ValueError):
        get_clinpgx_data("")



def test_invalid_input():

    with pytest.raises(ValueError):
        get_clinpgx_data("$$$")


def test_no_match_found():
    
    test_allele = "ABC*2"

    test_result = get_clinpgx_data(test_allele)

    assert test_result == {
        "star_allele": "ABC*2",
        "variant_summary": [],
        }


def test_clinpgx_return_correct_output():
    
    test_allele = "CYP2C19*5"

    test_result = get_clinpgx_data(test_allele)

    assert len(test_result["variant_summary"]) == 2
    for summary in test_result["variant_summary"]:
        assert "drug" in summary
        assert "drug_labels" in summary
        assert "guidelines" in summary
        assert "level_of_evidence" in summary
        assert "phenotype_category" in summary
        assert "summary_annotation" in summary