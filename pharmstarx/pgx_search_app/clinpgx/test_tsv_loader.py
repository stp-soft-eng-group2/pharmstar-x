import io
import pytest
from tsv_loader import load_tsv


# check the file returns records
def test_load_returns_records():
    records = load_tsv("drugLabels.tsv")

    assert len(records) > 0
    assert records



# check if file is empty, raise error. had Copilot Fusion (gpt-6-luna)
# to help create a mock empty file to catch raise value error.
def test_load_empty_tsv(monkeypatch):
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: io.StringIO(""))

    with pytest.raises(ValueError):
        load_tsv("empty.tsv")



#check if file is missing
def test_load_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_tsv("fake.tsv")

