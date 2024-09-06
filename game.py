import sys
import json
import help  
import importlib
import ship_menus  # type: ignore
import character_menu  # type: ignore
from header_display import display_header  # type: ignore
from planet_menu import display_planet_menu  # type: ignore
from system_menu import display_system_menu  # type: ignore

# ANSI color codes
RED = "\033[31m"
BOLD = "\033[1m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

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
                display_planet_menu(systems_data[current_system], planet_index)  # Use the imported function
                # After returning from Planet Menu, display the System Menu again
                display_system_menu(current_system, systems_data)
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
  S to Start the Game
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

def setup_character():
    """Handles the setup of character data and ship selection"""
    character_data = {}
    print(f"{CYAN}Please enter your character information!{RESET}")
    print()
    character_data['Character Name'] = input(f"{BOLD}Enter your Character Name: {RESET}").strip()
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

    # Use functions from ship_menus.py
    ships = ship_menus.load_ships(character_data['Faction'])
    ship_menus.display_ship_menu(ships)
    selected_ship, ship_name = ship_menus.choose_ship(ships)
    character_data['Ship Name'] = ship_name
    character_data['Ship Type'] = selected_ship

def navigate_systems():
    display_header()  # Correctly call display_header without module prefix
    while True:
        display_user_menu()  # Show the game menu at the start
        
        # Handle the initial user input from the game menu
        if handle_user_input(systems_data={}, current_system="1"):  # Correctly pass initial parameters
            # Proceed with game setup if 'S' is chosen
            display_welcome_message()  # Display the welcome message only after choosing to start
            setup_character()  # Function to handle character setup

            systems_data = load_json('systems.json')  # Load systems data correctly
            current_system = "1"  # Set the starting system

            # Start the game loop with the correct arguments
            start_game(systems_data, current_system)

if __name__ == "__main__":
    print("Initializing RetroStellar...")  # Debugging print
    navigate_systems()
