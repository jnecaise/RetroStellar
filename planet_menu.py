# planet_menu.py

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
CYAN = "\033[36m"

def display_planet_menu(system_info, planet_index):
    """ Displays detailed information about the selected planet and allows returning to the System Menu """
    try:
        planet = system_info['planets'][planet_index]
        # Fixed menu width for consistency
        menu_width = 30

        # Function to create a border line
        def border_line():
            return "+" + "-" * (menu_width - 2) + "+"

        # Function to format and center text within the menu
        def format_line(text):
            return f"| {text:<{menu_width - 4}} |"

        while True:
            # Print the Planet Menu with hardcoded borders and proper formatting
            print(border_line())
            print(format_line(" Planet Menu ".center(menu_width - 4)))
            print(border_line())
            print(format_line(f"Name: {planet['name']}"))
            print(format_line(f"Type: {planet['type']}"))
            print(format_line(f"Colonizable: {planet['colonizable']}"))
            print(border_line())
            print(format_line(" Resources ".center(menu_width - 4)))
            print(border_line())

            # Define resources without using symbols for a classic look
            for resource, amount in planet['resources'].items():
                # Adjust spacing dynamically for neat alignment
                resource_line = f"{resource}: {amount}"
                print(format_line(resource_line))

            print(border_line())
            print(format_line(" [R] Return ".center(menu_width - 4)))
            print(border_line())

            # Handle user input to go back
            choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()
            if choice == 'R':
                return  # Exit the Planet Menu and return to the System Menu
            else:
                print(f"{RED}Invalid input. Press R to go back to the System Menu.{RESET}")

    except IndexError:
        print(f"{RED}Invalid planet selection. Please try again.{RESET}")
