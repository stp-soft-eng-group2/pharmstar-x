import json

with open("data/pharmvar_dataset.json", "r") as file:
    data = json.load(file)

inp = input("Enter the Star allele or name")

def search_hgnc(inp, data):
    n = 0

    for object in data:
        if object["alleleName"] == inp:
            user_dataset = object
            break
        else:
            n += 1
            continue

    if n == len(data):
        user_dataset = "Un_available"

    print(user_dataset)

search_hgnc(inp, data)