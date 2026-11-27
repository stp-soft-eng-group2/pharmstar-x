# pharmstar-x
Pharmacogenomics Star Allele Search Tool for Clinical Scientist



To run the application as developer

pip install -e .


## Installation

This project uses a fully controlled and reproducible Conda environment
Please install and initialise miniconda if you do not already have it in your computer/laptop.
Link to download: https://www.anaconda.com/download


### 1. Create the Conda environment
May require additional steps to accept term and conditions, follow terminal prompt

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate pharmstarx
```

### 3. Install the project

```bash
pip install .
```


are these needed?
python manage.py migrate

python manage.py runserver