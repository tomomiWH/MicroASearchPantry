import csv
from datetime import datetime 

"""
CS361 Microservice A: Search Pantry Items
input:  PantryItems.txt             Read this file contains all Pantry Items which was generated from teammate's main program
output:  MicroAUserCommPipe.txt      Read this file contains User command values from teammate's main program 
                                    (e.g.  N,Almond   I,004   E,05-17-2025)
output: SearchResults.txt           Produces serach results in same format
"""
PANTRY_ITEMS_DATA = "PantryItems.txt"               # input file
USER_REQUEST_COMMAND = "MicroAUserCommPipe.txt"     # user command
SEARCH_RESULT = "SearchResult.txt"                  # output fil

def load_pantry_items(file_path):
    pantry_items = []
    with open(file_path, 'r') as pantryfile:
        reader = csv.DictReader(pantryfile)
        for row in reader:          
            # append as dictionary items Item ID,item_name,quantity,expiration_date,details
            pantry_items.append({"Item ID":row["Item ID"], "item_name": row["item_name"], "quantity": row["quantity"], "expiration_date": row["expiration_date"], "details": row["details"]})
    return pantry_items
#print(load_pantry_items(PANTRY_ITEMS_DATA))

# search by Name
def search_by_item_name(pantry_items, name):
    return [item for item in pantry_items if item["item_name"].lower() == name.lower()] or\
          [item for item in pantry_items if item["item_name"].lower().startswith(name.lower())] 
pantry = load_pantry_items(PANTRY_ITEMS_DATA)
#print("Search Result by Item Name ---- ", search_by_item_name(pantry, "Almond Flour"))

# search by ID
def search_by_item_id(pantry_items, pantry_id):
    return [item for item in pantry_items if item["Item ID"] == pantry_id]
#print("Search Result by Item ID---- ", search_by_item_id(pantry, "002"))

def search_by_expiration_date(pantry_items, expiration_date):
    #return [item for item in pantry_items if item["expiration_date"] == expiration_date ]
    check_date = datetime.strptime(expiration_date, "%m-%d-%Y")
    expired_items = [item for item in pantry_items if datetime.strptime(item["expiration_date"], "%m-%d-%Y") < check_date]
    return expired_items
#print("Search Result by Expiration Date ---- ", search_by_expiration_date(pantry, "09-30-2026"))

def read_search_request(file_path):
    with open(file_path, 'r') as file:
        #print(file.read().strip().split(','))
        return file.read().strip().split(',')   # strip space
#read_search_request(USER_REQUEST_COMMAND)

def write_search_result(file_path, search_results):
    with open(SEARCH_RESULT, 'w', newline='') as outfile:
        if search_results:   # search result exists
            #json.dump(search_results, file)   #[{"Item ID": "001", "item_name": "Almond Flour", "quantity": "1", "expiration_date": "01-01-2025", "details": "1 lb bag"}]
            col_head_names = search_results[0].keys()
            dict_writer = csv.DictWriter(outfile, col_head_names)
            dict_writer.writeheader()
            dict_writer.writerows(search_results)

result = search_by_item_name(pantry, "Almond")                  # search by item
#result = search_by_item_id(pantry, "014")                      # search by id
#result = search_by_expiration_date(pantry, "09-30-2026")   # search by expiration date
write_search_result(SEARCH_RESULT, result)

# microservive program function
def pantry_micro_service():
    #load pantry items
    pantry = load_pantry_items(PANTRY_ITEMS_DATA)
    if not pantry:
        return          # get out of the program
    
    # get data user command
    user_command = read_search_request(USER_REQUEST_COMMAND)
    print(user_command, type(user_command))
    if not user_command:
        return          # get out of the program
       
    # get search type N for Search by Name, I for search by Item ID, E for search by Expiration date, convert all ito lower case for consistent string values for rest of function to pass in
    search_command_type = user_command[0].lower()
    search_command_value = user_command[1].lower()

    # execte search functionality based on user command
    if search_command_type == 'n':                          # Search by Name        N for Name serach
        result = search_by_item_name(pantry, search_command_value)   

    elif search_command_type == 'i':                        # Search by Item ID     I for Item ID search
        result = search_by_item_id(pantry, search_command_value)     

    elif search_command_type == 'e':                        # Seaerh by Expiration Date     E for Expiration date
        result = search_by_expiration_date(pantry, search_command_value)

    else:
        print("Please be advised invalid search type. Search time must be N, I or E")
        return                                               # invalid search type and get out 

    write_search_result(SEARCH_RESULT, result)
        

if __name__ == "__main__":

    pantry_micro_service()
    