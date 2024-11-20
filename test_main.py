import os 
import time

USER_COMMAND_FILE = "MicroAUserCommPipe.txt"
SEARCH_RESULT = "SearchResult.txt"

def main():

    print("\n------- TEST PROGRAM microservice Search services --------")
    while True:
        print("Please select search type:")
        print("N - Search by Name")
        print("I - Search by Item ID")
        print("E - Search by Expiration Date")
        print("Exit - Exit the program\n")

        # prompt user and capture user input for search type and search value
        user_search_type = input("Enter search (e.g. N, I or E) or Exit: ").strip()  
        user_search_value = input("Please type search value (e.g. Almond Flour, 002 or 08-27-2025): ").strip()

        save_command_values = f"{user_search_type},{user_search_value}"
        with open(USER_COMMAND_FILE, "w") as file:
            file.write(save_command_values)
            time.sleep(1)
        print(f"\nsaved command value to the MicroAUserCommPipe.txt : {save_command_values}")

        time.sleep(10)
        # Read results from MicroAUserCommPipe.txt pipeline
        with open(USER_COMMAND_FILE, "r") as command_file:
            results = command_file.readlines()
         
            print("waiting results back...")
            time.sleep(5)

            # Check result if contains header column "Item ID"
            # Write out to SearchResults.txt
            if results and "Item ID" in results[0]:
                with open(SEARCH_RESULT, "w") as result_file:
                    result_file.writelines(results)
                print("search results wrote to SearchResults.txt: ", results)

        # Display results
        with open(SEARCH_RESULT, 'r') as file:
            print("--------------- Search Result display -----------------")
            results = file.read()
            print("read results from SearchResults.txt : ",results)
            time.sleep(5)
        
        with open(SEARCH_RESULT, "w") as file:
            file.write("")




if __name__ == "__main__":
    main()