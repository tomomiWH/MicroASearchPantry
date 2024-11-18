import os 
import time

USER_COMMAND_FILE = "MicroAUserCommPipe.txt"
SEARCH_RESULT = "SearchResult.txt"

def main():

    print("------- TEST PROGRAM microservice Search services --------")
    while True:
        print("Please select search type:")
        print("N - Search by Name")
        print("I - Search by Item ID")
        print("E - Search by Expiration Date")
        print("Exit to exit the program")

        # prompt user and capture user input for search type and search value
        user_search_type = input("Enter N/I/E (e.g. N) or Exit: ").strip()
        if user_search_type =="exit":
            with open(USER_COMMAND_FILE, "w") as command_file:
                command_file.write("Exit")
            print("Exiting...")
            break
       
        user_search_value = input("Please type search value (e.g. Almond Flour/002/08-27-2025): ").strip()

        save_command_values = f"{user_search_type},{user_search_value}"
        with open(USER_COMMAND_FILE, "w") as file:
            file.write(save_command_values)
        print(f"Saved user input values sending: {save_command_values}")

        print("waiting for result back...")
        while not os.path.exists(SEARCH_RESULT) or os.stat(SEARCH_RESULT).st_size ==0:
            time.sleep(2)

        # Display results
        with open(SEARCH_RESULT, 'r') as file:
            print("--------------- Search Result display -----------------")
            file.read()
        
        with open(SEARCH_RESULT, "w") as file:
            file.write("")




if __name__ == "__main__":
    main()