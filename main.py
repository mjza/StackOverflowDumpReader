import os
from dotenv import load_dotenv

def main():
    from colored import fg, attr
    from utils import list_xml_files, read_yes_no, read_integer, read_first_node
    from api import process_xml_file
    
    red = fg('red')    
    blue = fg('blue')
    green = fg('green')
    cyan = fg('cyan')
    reset = attr('reset')
    running = True   
    
    print(f"{blue}Welcome to the Stackoverflow CLI!{reset}")
    
    while running:
        
        print(f"{blue}Available commands:")
        print("0. Exit")
        print("1. Select the input folder")
        print("2. Select the input file")
        print("3. Select the output table")        
        command = input(f"Enter a command number: {reset}").strip()

        if command == "0":
            print(f"{green}Exiting the application. Goodbye!{reset}")
            running = False
        elif command == "1":            
            # Set a default input folder path
            default_input_folder = "./inputs"
            # Prompt the user, offering the default path
            input_folder = input(f"{blue}The default input folder path is `{default_input_folder}`, press enter to accept it or enter the input folder path: {reset}").strip()
            
            # If the user presses enter without typing anything, use the default path
            if not input_folder:
                input_folder = default_input_folder

            # Store the chosen path in an environment variable
            os.environ['INPUT_FOLDER'] = input_folder
        elif command == "2":
            input_folder = os.environ.get('INPUT_FOLDER', './inputs') 
            xml_files = list_xml_files(input_folder)
    
            for idx, file in enumerate(xml_files):
                print(f"{cyan}    {idx+1}: {file}")
            
            file_number = int(input(f"{blue}Enter the file number you want to check: {reset}"))
            
            if 0 < file_number <= len(xml_files):
                selected_file = xml_files[file_number-1]
                print(f"{blue}You selected: {green}{selected_file}{reset}")
                os.environ['SELECTED_FILE'] = selected_file
                read_first_node(selected_file)
            else:
                print(f"{red}Invalid file number. Try again.{reset}")                    
        elif command == "3":
            # Store the types in a list
            types = ["Votes", "Users", "Tags", "PostLinks", "Posts", "Comments"]
            
            # Display the options to the user
            print(f"{blue}Please select a type by entering the corresponding number:{reset}")
            for index, type in enumerate(types, start=1):
                print(f"{cyan}    {index}. {type}{reset}")
            
            # Prompt the user for a choice
            choice_input = input(f"{blue}Enter your choice (1-{len(types)}): {reset}").strip()
            
            try:
                # Convert the input to an integer and get the selected type
                choice = int(choice_input)
                if 1 <= choice <= len(types):
                    selected_type = types[choice - 1]
                    print(f"{green}You selected: {selected_type}{reset}")
                    os.environ['SELECTED_TYPE'] = selected_type
                    path = os.environ.get('SELECTED_FILE')
                    if path:                        
                        start_line_number = 1
                        should_read = read_yes_no(f"{blue}Do you want to enter a start line number (default is 1)?{reset}")
                        if should_read:
                            start_line_number = read_integer(f"{blue}Please enter the start line number: {reset}")
                        process_xml_file(path, selected_type, start_line_number)                        
                else:
                    print(f"{red}Invalid choice, please enter a number within the provided range.{reset}")
            except ValueError:
                print(f"{red}Invalid input, please enter a numerical value.{reset}")
        else:
            print(f"{red}Unknown command number. Please try again.{reset}")  

if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()
    
    # show the main menu
    main()
