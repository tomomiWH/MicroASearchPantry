import csv
from datetime import datetime 
import time
import os


"""
CS361 Microservice A: Search Pantry Items
Description: Search functionality
input:  PantryItems.txt                    Read this file contains all Pantry Items which was generated from teammate's main program
input/output:  MicroAUserCommPipe.txt      Read this file contains User command values from teammate's main program and also writes result temporarily
                                            (e.g.  N,Almond   I,004   E,05-17-2025)
"""
PANTRY_ITEMS_DATA = "PantryItems.txt"               # input file
USER_REQUEST_COMMAND = "MicroAUserCommPipe.txt"     # user command


def load_pantry_items(file_path):
    pantry_items = []
    with open(file_path, 'r') as pantryfile:
        reader = csv.DictReader(pantryfile)
        for row in reader:          
            # append as dictionary items Item ID,item_name,quantity,expiration_date,details
            pantry_items.append({"Item ID":row["Item ID"], "item_name": row["item_name"], "quantity": row["quantity"], "expiration_date": row["expiration_date"], "details": row["details"]})
    return pantry_items

# search by Name
def search_by_item_name(pantry_items, name):
    return [item for item in pantry_items if item["item_name"].lower() == name.lower()] or [item for item in pantry_items if item["item_name"].lower().startswith(name.lower())] 
#pantry = load_pantry_items(PANTRY_ITEMS_DATA)
#print("Search Result by Item Name ---- ", search_by_item_name(pantry, "Almond Flour"))

# search by ID
def search_by_item_id(pantry_items, pantry_id):
    return [item for item in pantry_items if item["Item ID"] == pantry_id]
#print("Search Result by Item ID---- ", search_by_item_id(pantry, "002"))

def search_by_expiration_date(pantry_items, expiration_date):
    check_date = datetime.strptime(expiration_date, "%m-%d-%Y")
    expired_items = [item for item in pantry_items if datetime.strptime(item["expiration_date"], "%m-%d-%Y") < check_date]
    return expired_items
#print("Search Result by Expiration Date ---- ", search_by_expiration_date(pantry, "09-30-2026"))


def write_results_to_pipe(results):
    """Write serach results to MicroAUserCommPipe.txt temporarily"""
    with open(USER_REQUEST_COMMAND, "w") as pipeline_file:
        if results:
            writer = csv.DictWriter(pipeline_file, fieldnames=results[0].keys())   # writ with header column
            writer.writeheader()
            writer.writerows(results)
            print(f"wrote results to pipeline {results}")
        # else:
        #     pipeline_file.write("Not Found\n")

# microservive program function
def pantry_microservice():
    #load pantry items
    pantry_items = load_pantry_items(PANTRY_ITEMS_DATA)
    print("microservice starting...")

    while True:
        time.sleep(2)

        # Read user command file
        with open(USER_REQUEST_COMMAND, 'r') as command_file:
            user_command = command_file.read().strip()

        # # parse the user input command value
        command_data = user_command.split(",")     # N,Almond Flour

        # get search type N for Search by Name, I for search by Item ID, E for search by Expiration date, convert all into lower case for consistent string values for rest of function to pass in
        search_command_type = command_data[0].lower()
        search_command_value = command_data[1].lower()

        # # execte search functionality based on user command
        if search_command_type == 'n':                          # Search by Name        N for Name serach
            result = search_by_item_name(pantry_items, search_command_value)   

        elif search_command_type == 'i':                        # Search by Item ID     I for Item ID search
            result = search_by_item_id(pantry_items, search_command_value)     

        elif search_command_type == 'e':                        # Seaerh by Expiration Date     E for Expiration date
            result = search_by_expiration_date(pantry_items, search_command_value)

        # else:
        #     print("Please be advised invalid search type. Search type must be N, I or E")
        #     result = []
        if result:
            write_results_to_pipe(result)


if __name__ == "__main__":

    pantry_microservice()
    