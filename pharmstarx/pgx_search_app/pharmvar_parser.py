import json
from pathlib import Path

def data_load(path_to_dataset):
    """
This function loads the Pharmvar json database into memory

Outputs the data structure as the variable data
    """
    # defaults the path to start from the script's directory
    file_path = Path(__file__).parent.joinpath(path_to_dataset)
    # opens and reads the database 
    with open(file_path, "r") as file:
        # loads the data in json format
        data = json.load(file)
        return data

def search_star(data):

    """
This function searches the Pharmvar local json database and collates information

Input parameter "data" is the loaded Pharmvar output of the data_load() function

The output is the allele found as a result of the search
    """
    n = 0 # sets the counter to 0
    inp = input("Enter the Star allele or name: ").upper() # saves the input as the variable inp
    
    # if the user inputs an integer, a number is outputted
    if type(inp) == int:
        inp = str(inp)

    # iterates through the allele array to search alleles seperately as an object
    for object in data:
        # searches if the value corresponding to the alleleName key is equivilent to the input
        if object["alleleName"] == inp:
            # retrieves what was found and saves it to the variable user_dataset
            user_dataset = object
            # breaks the loop
            break
        else:
            # if the alleleName is not the same as the input, adds 1 to the counter
            n += 1
            continue # continues the loop to the next allele in the array.
    # if n and the length of the allele array are equal, the input was not found in the array 
    if n == len(data):
        user_dataset = "Un_available" # tells the user their input is unavailable

    return user_dataset

def filter(user_dataset, *keys):

    """
This function filters allele data to the data the user is interested in
including alleleName, geneSymbol, pvId, function, hgvs, variants,
url, and references.

The input parameters are user_dataset, *keys:

user_dataset = The primary use is to provide this function with the
allele retrieved from the Pharmvar json dataset. However, the function is dynamic
and can work with any object from a json structured dataset.

*keys = a comma seperated list of the keys from a json object that the user is
interested in.

The output is a filtered version of the allele information set in the form of a 
list of seperate dictionaries, each representing a field of interest
    """

    # An empty list to input dictionary fields that the user is interested in
    filtered_data = []

    # iterates through each outer key in the allele information set
    for dataset_key in keys:

        # appends the information the user is interested in onto the filtered dictionary array
        filtered_data.append({dataset_key: user_dataset[dataset_key]})
        
    return filtered_data

def main():
    """
This function controls the scripts output and when it is called
This prevents code being run from the top of the script to the bottom.

The output is the collection of outputs from the functions called.
    """

     # prints the filtered data for the allele the user inputs
    print(filter(search_star(data_load("data/pharmvar_dataset.json")),
        'alleleName', 'geneSymbol', 'pvId', 'function', 'hgvs',
        'variants', 'url', 'references'    
    ))

if __name__ == '__main__':
    main()