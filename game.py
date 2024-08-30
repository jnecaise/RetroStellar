import json
import sys
import importlib
import character_menu  # type: ignore # Ensure this module is correctly set up

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
  C to Display Character Menu
  H for Help
\033[0m"""
    print(menu)

def display_faction_options():
    factions = load_json('factions.json')
    print(f"{CYAN}Available Factions:{RESET}")
    for idx, faction in enumerate(factions.keys(), start=1):
        print(f"{BOLD}{idx}. {faction} - {GREEN}{factions[faction]['Description']}{RESET}")

def handle_user_input(allow_game_menu=False):
    while True:
        choices = "S" if not allow_game_menu else "SMQCH"
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()
        if choice == 'Q':
            print("Quitting the game. Goodbye!")
            sys.exit()
        elif choice == 'C':
            reload_character_menu()
        elif choice == 'H':
            print("THIS IS HELP SECTION")
        elif choice == 'S' and not allow_game_menu:
            return True
        elif choice == 'M' and allow_game_menu:
            return 'M'
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

def display_system_menu(current_system, connections):
    system_info = connections[current_system]
    
    planets = ', '.join(planet['name'] for planet in system_info['planets'])
    stargates = ', '.join(system_info['connections'])
    star_type = system_info.get('star_type', 'Unknown')  # Default to 'Unknown' if not present
    hazard_level = system_info.get('hazard_level', 'Unknown')  # Default to 'Unknown' if not present
    
    print(f"\n{CYAN}System: {current_system}{RESET}")
    print(f"{system_info['description']}")
    print(f"{BLUE}Star Type: {star_type}{RESET}")  # Display the star type
    print(f"{MAGENTA}Planets: {planets}{RESET}")
    # Display asteroid fields names on the same line
    if 'asteroid_fields' in system_info:
        asteroid_fields = ', '.join(field['id'] for field in system_info['asteroid_fields'])
    print(f"{CYAN}Asteroid Fields: {asteroid_fields}{RESET}")
    print(f"{RED}Hazard Level: {hazard_level}{RESET}")
    print(f"{YELLOW}Stargates: {stargates}{RESET}")

def get_user_command(valid_systems):
    while True:
        command = input(f"{BOLD}Your command: {RESET}").strip()
        if command in valid_systems:
            return command
        elif command.upper() == 'M':
            return 'M'
        else:
            print(f"{RED}Invalid system. Please enter a valid system or 'M' to access the menu.{RESET}")

def display_game_menu():
    menu = """
\033[33m
Game Menu:
  M to Return to the Game
  Q to Quit
  C to Display Character Menu
  H for Help
\033[0m
    """
    print(menu)

def start_game():
    connections = load_json('systems.json')
    current_system = "1"
    while current_system != "8":
        display_system_menu(current_system, connections)
        if connections[current_system]['connections']:
            command = get_user_command(connections[current_system]['connections'])
            if command == 'M':
                display_game_menu()
                handle_user_input(allow_game_menu=True)
            else:
                current_system = command
        else:
            print(f"{RED}No available connections. Game Over.{RESET}")
            break
        if current_system == "8":
            print(f"{GREEN}You have reached your destination!{RESET}")

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

    while True:
        display_user_menu()
        if handle_user_input():
            start_game()

if __name__ == "__main__":
    navigate_systems()
