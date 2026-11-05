import json
from pathlib import Path

def data_load():
    """
This function loads the Pharmvar json database into memory

Outputs the data structure as the variable data
    """
    # defaults the path to start from the script's directory
    file_path = Path(__file__).parent.joinpath("data/pharmvar_dataset.json")
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

    print(user_dataset)

def main():
    """
This function controls the scripts output and when it is called
This prevents code being run from the top of the script to the bottom.

The output is the collection of outputs from the functions called.
    """

    search_star(data_load()) # uses the output of the data_load function as input for search_star

if __name__ == '__main__':
    main()