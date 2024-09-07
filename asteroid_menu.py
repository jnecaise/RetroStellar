# asteroid_menu.py

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
CYAN = "\033[36m"

def display_asteroid_menu(system_info, asteroid_index):
    """Displays detailed information about the selected asteroid field and allows returning to the System Menu."""
    try:
        asteroid = system_info['asteroid_fields'][asteroid_index]
        menu_width = 30

        def border_line():
            return "+" + "-" * (menu_width - 2) + "+"

        def format_line(text):
            return f"| {text:<{menu_width - 4}} |"

        while True:
            print(border_line())
            print(format_line(" Asteroid Field Menu ".center(menu_width - 4)))
            print(border_line())
            print(format_line(f"ID: {asteroid['id']}"))
            print(format_line(f"Density: {asteroid['density']}"))
            print(format_line(f"Type: {asteroid['resource_type']}"))
            print(format_line(f"Hazard Level: {asteroid['hazard_level']}"))
            print(border_line())
            print(format_line(" Resources ".center(menu_width - 4)))
            print(border_line())

            for resource, amount in asteroid['resources'].items():
                resource_line = f"{resource}: {amount}"
                print(format_line(resource_line))

            print(border_line())
            print(format_line(" [R] Return ".center(menu_width - 4)))
            print(border_line())

            choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()
            if choice == 'R':
                return  # Exit the Asteroid Menu and return to the System Menu
            else:
                print(f"{RED}Invalid input. Press R to go back to the System Menu.{RESET}")

    except IndexError:
        print(f"{RED}Invalid asteroid selection. Please try again.{RESET}")
