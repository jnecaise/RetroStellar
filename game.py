import json
import sys
import importlib
import help  # type: ignore
import character_menu  # type: ignore

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def display_header():
    header = """\033[34m
██████  ███████ ████████ ██████   ██████  ███████ ████████ ███████ ██      ██       █████  ██████      
██   ██ ██         ██    ██   ██ ██    ██ ██         ██    ██      ██      ██      ██   ██ ██   ██     
██████  █████      ██    ██████  ██    ██ ███████    ██    █████   ██      ██      ███████ ██████      
██   ██ ██         ██    ██   ██ ██    ██      ██    ██    ██      ██      ██      ██   ██ ██   ██     
██   ██ ███████    ██    ██   ██  ██████  ███████    ██    ███████ ███████ ███████ ██   ██ ██   ██ 
\033[0m"""
    print(header)

def display_welcome_message():
    message = f"{GREEN}Welcome to RetroStellar! This game is an attempt to capture the retro feel of the early online games.{RESET}"
    print(message)
    print()

def display_user_menu():
    menu = """\033[33m
Press:
  S to Start the Game
  Q to Quit
  I to Display Character Menu
  H for Help
\033[0m"""
    print(menu)

def display_faction_options():
    factions = load_json('factions.json')
    print(f"{CYAN}Available Factions:{RESET}")
    for idx, faction in enumerate(factions.keys(), start=1):
        print(f"{BOLD}{idx}. {faction} - {GREEN}{factions[faction]['Description']}{RESET}")

def handle_user_input(systems_data, current_system, allow_game_menu=False):
    while True:
        choices = "S" if not allow_game_menu else "SMQHI"
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()
        if choice == 'Q':
            print("Quitting the game. Goodbye!")
            sys.exit()  # Exit the program entirely
        elif choice == 'I':
            reload_character_menu()  # Call the reload function for the character menu
        elif choice == 'H':
            help.display_help()  # Display the help screen from help.py
        elif choice == 'S' and not allow_game_menu:
            return True  # Signal to start the game
        elif choice == 'M' and allow_game_menu:
            return 'M'  # Signal to return to game menu
        else:
            print(f"{RED}Invalid option. Please choose {choices}.{RESET}")

def reload_character_menu():
    importlib.reload(character_menu)
    character_menu.display_character_menu()
    character_menu.handle_character_menu_input()

def display_character_menu():
    """ Displays the character menu with basic information """
    character_data = load_json('character_data.json')
    print(f"\n{CYAN}{BOLD}Character Menu{RESET}")
    print(f"{MAGENTA}Character Name: {GREEN}{character_data.get('Character Name', 'N/A')}{RESET}")
    print(f"{MAGENTA}Faction: {GREEN}{character_data.get('Faction', 'N/A')}{RESET}")
    print(f"{MAGENTA}Ship Name: {GREEN}{character_data.get('Ship Name', 'N/A')}{RESET}")
    print(f"{MAGENTA}Starting Credits: {GREEN}{character_data.get('Starting Credits', 'N/A')}{RESET}")
    print("\nPress M to return to the game or Q to quit.")

def handle_character_menu_input():
    """ Handles user input within the character menu """
    while True:
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()
        if choice == 'M':
            return
        elif choice == 'Q':
            print("Quitting the game. Goodbye!")
            sys.exit()
        else:
            print(f"{MAGENTA}Invalid option. Please choose 'M' to return to the game or 'Q' to quit.{RESET}")

def display_system_menu(current_system, systems_data):
    system_info = systems_data[current_system]
    
    # Display planets without showing letters A, B, C, D
    planets = ', '.join(planet['name'] for planet in system_info['planets'])

    stargates = ', '.join(system_info['connections'])
    star_type = system_info.get('star_type', 'Unknown')  # Default to 'Unknown' if not present
    hazard_level = system_info.get('hazard_level', 'Unknown')  # Default to 'Unknown' if not present
    ownership = system_info.get('owned_by', 'Unoccupied')  # Default to 'Unoccupied' if not present
    current_name = system_info.get('current_name', current_system)  # Use the current name of the system
    
    print(f"\n{CYAN}System: {current_name}{RESET}")
    print(f"{system_info['description']}")
    print(f"{GREEN}Owned by: {ownership}{RESET}")  # Display ownership
    print(f"{CYAN}Star Type: {star_type}{RESET}")  # Display the star type
    print(f"{MAGENTA}Planets: {planets}{RESET}")
    
    # Display asteroid fields names on the same line
    if 'asteroid_fields' in system_info:
        asteroid_fields = ', '.join(field['id'] for field in system_info['asteroid_fields'])
        print(f"{CYAN}Asteroid Fields: {asteroid_fields}{RESET}")
    
    print(f"{RED}Hazard Level: {hazard_level}{RESET}")
    print(f"{YELLOW}Stargates: {stargates}{RESET}")

def display_planet_menu(system_info, planet_index):
    """ Displays detailed information about the selected planet """
    try:
        planet = system_info['planets'][planet_index]
        print(f"\n{CYAN}Planet: {planet['name']}{RESET}")
        print(f"{MAGENTA}Type: {planet['type']}{RESET}")
        print(f"{YELLOW}Colonizable: {planet['colonizable']}{RESET}")
        resources = ', '.join(planet['resources'])
        print(f"{CYAN}Resources: {resources if resources else 'None'}{RESET}")
    except IndexError:
        print(f"{RED}Invalid planet selection. Please try again.{RESET}")

def get_user_command(valid_systems, systems_data, current_system):
    while True:
        command = input(f"{BOLD}Your command: {RESET}").strip().upper()
        # Check for valid system navigation
        if command in valid_systems:
            return command
        # Check for planet selection (A, B, C, D) using their index
        elif command in ['A', 'B', 'C', 'D']:
            planet_index = ord(command) - ord('A')  # Convert letter to index (A=0, B=1, ...)
            if planet_index < len(systems_data[current_system]['planets']):
                display_planet_menu(systems_data[current_system], planet_index)
            else:
                print(f"{RED}Invalid planet selection. Please try again.{RESET}")
        elif command.upper() == 'M':
            return 'M'
        else:
            print(f"{RED}Invalid input. Please enter a valid system number, planet letter (A-D), or 'M' for the menu.{RESET}")

def display_game_menu():
    menu = """
\033[33m
Game Menu:
  M to Return to the Game
  Q to Quit
  I to Display Character Menu
  H for Help
\033[0m
    """
    print(menu)

def start_game(systems_data, current_system):
    while current_system != "8":  # Change the objective to System 8
        display_system_menu(current_system, systems_data)
        
        # Player selects valid options: system numbers, or planet letters A-D
        while True:
            command = get_user_command(systems_data[current_system]['connections'], systems_data, current_system)
            if command == 'M':
                display_game_menu()
                handle_user_input(systems_data, current_system, allow_game_menu=True)
                break  # Exit loop to handle the menu
            elif command in systems_data[current_system]['connections']:
                current_system = command
                break  # Exit loop and navigate to the selected system
        
        # Check if player has reached the final destination
        if current_system == "8":
            print(f"{GREEN}You have reached your destination!{RESET}")
            break

def navigate_systems():
    display_header()
    display_welcome_message()
    
    character_data = {}
    print(f"{CYAN}Please enter your character information!{RESET}")
    print()
    character_data['Character Name'] = input(f"{BOLD}Enter your Character Name: {RESET}").strip()
    character_data['Ship Name'] = input(f"{BOLD}Enter your Ship Name: {RESET}").strip()
    print()

    display_faction_options()
    factions = load_json('factions.json')
    while True:
        print()
        faction_choice = input(f"{BOLD}Choose your faction by number: {RESET}").strip()
        try:
            faction_idx = int(faction_choice) - 1
            faction_names = list(factions.keys())
            if 0 <= faction_idx < len(faction_names):
                chosen_faction = faction_names[faction_idx]
                character_data['Faction'] = chosen_faction
                character_data['Starting Credits'] = factions[chosen_faction]['Starting Credits']
                break
            else:
                print(f"{RED}Invalid faction choice. Try again.{RESET}")
        except ValueError:
            print(f"{RED}Please enter a valid number.{RESET}")
    
    save_json('character_data.json', character_data)

    systems_data = load_json('systems.json')  # Load systems data correctly
    current_system = "1"  # Set the starting system

    while True:
        display_user_menu()
        if handle_user_input(systems_data, current_system):  # Correctly pass systems_data and current_system
            start_game(systems_data, current_system)  # Ensure correct arguments

if __name__ == "__main__":
    print("Initializing RetroStellar...")  # Debugging print
    navigate_systems()
