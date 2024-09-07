
# game.py

import subprocess
import sys
import json
import help  
import importlib
import ship_menus   # type: ignore
import character_menu  
from character_menu import display_character_menu, save_character_data, load_character_data, handle_character_menu_input
from header_display import display_header  # type: ignore # Use this to display the welcome header
from planet_menu import display_planet_menu   # type: ignore
from system_menu import display_system_menu   # type: ignore
from asteroid_menu import display_asteroid_menu   # type: ignore
from settings import default_settings, display_settings_menu   # type: ignore

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
    """Loads JSON data from a file."""
    with open(filename, 'r') as file:
        return json.load(file)

def save_json(filename, data):
    """Saves JSON data to a file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def display_welcome_message():
    """Displays the introductory text without the header ASCII art."""
    print(f"{GREEN}Welcome to RetroStellar! This game is an attempt to capture the retro feel of the early online games.{RESET}\n")

def display_user_menu():
    """Displays the main user menu options."""
    menu = """\033[33m
Press:
  N to Start a New Game
  C to Continue Game
  T for Settings
  H for Help
  Q to Quit
\033[0m"""
    print(menu)

def display_faction_options():
    """Displays available factions for the player to choose from, with each description in a specific color."""
    factions = load_json('factions.json')  # Load factions data
    print(f"{CYAN}Available Factions:{RESET}")
    
    # Define specific colors for each faction
    faction_colors = {
        "Mandate of God": "\033[33m",  # Yellow
        "Shogunate 3072": "\033[31m",  # Red
        "People of the River": "\033[34m",  # Blue
        "The Noringian Hive": "\033[32m",  # Green
        "United Systems of Man": "\033[35m",  # Magenta
    }
    
    for idx, (faction_name, faction_info) in enumerate(factions.items(), start=1):
        description = faction_info['Description']
        # Get the color for the faction, defaulting to RESET if not found
        color = faction_colors.get(faction_name, RESET)
        colored_description = f"{color}{description}{RESET}"
        print(f"{BOLD}{idx}. {faction_name} - {colored_description}")

def handle_user_input(systems_data, current_system, allow_game_menu=False, settings=default_settings):
    """Handles user input from the main menu or in-game menu."""
    while True:
        choices = "NCTQH" if not allow_game_menu else "SMQHIT"
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()
        if choice == 'Q':
            print("Quitting the game. Goodbye!")
            sys.exit()
        elif choice == 'N':  # New Game
            create_new_game()
            return True  # Signal to start the game
        elif choice == 'C':  # Continue Game
            if load_existing_game():
                return True
            else:
                print(f"{RED}No saved game found. Please start a new game first.{RESET}")
        elif choice == 'T':
            display_settings_menu(settings)
        elif choice == 'H':
            help.display_help()
        else:
            print(f"{RED}Invalid option. Please choose {choices}.{RESET}")

def create_new_game():
    """Generates a new universe by running script.py and initializes player data."""
    print()
    print(f"{GREEN}Generating a new universe...{RESET}")
    
    # Run script.py to generate the universe
    try:
        subprocess.run(['python', 'script.py'], check=True)  # Run script.py
        print(f"{GREEN}Universe generated successfully!{RESET}")
        print("--------------------------------")
        print()
    except subprocess.CalledProcessError as e:
        print(f"{RED}Failed to generate the universe: {e}{RESET}")
        return
    
    # Initialize character data
    character_data = setup_character()  # Initialize new character data
    save_character_data(character_data)  # Save initial character data
    
    # Load the newly generated universe
    systems_data = load_json('systems.json')
    
    print(f"{GREEN}New game setup complete. Starting game...{RESET}")
    navigate_systems(systems_data, "1", character_data)  # Pass the necessary data to navigate_systems

def load_existing_game():
    """Loads the existing universe and player data if available."""
    try:
        systems_data = load_json('universe.json')  # Load the saved universe
        character_data = load_character_data()  # Load the saved character data
        print(f"{GREEN}Loaded saved game. Continuing...{RESET}")
        navigate_systems(systems_data, "1", character_data)
        return True
    except FileNotFoundError:
        return False

def reload_character_menu():
    """Reloads the character menu module and displays it."""
    importlib.reload(character_menu)
    display_character_menu()
    handle_character_menu_input()

def display_character_menu():
    """Displays the character menu with basic information."""
    character_data = load_json('character_data.json')
    print(f"\n{CYAN}{BOLD}Character Menu{RESET}")
    print(f"{MAGENTA}Character Name: {GREEN}{character_data.get('Character Name', 'N/A')}{RESET}")
    print(f"{MAGENTA}Faction: {GREEN}{character_data.get('Faction', 'N/A')}{RESET}")
    print(f"{MAGENTA}Ship Name: {GREEN}{character_data.get('Ship Name', 'N/A')}{RESET}")
    print(f"{MAGENTA}Starting Credits: {GREEN}{character_data.get('Starting Credits', 'N/A')}{RESET}")
    print("\nPress M to return to the game or Q to quit.")

def handle_character_menu_input():
    """Handles user input within the character menu."""
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
    """Prompts user for commands related to system navigation, planet selection, and asteroid field selection."""
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
                display_system_menu(current_system, systems_data)  # Return to system menu after viewing planet
            else:
                print(f"{RED}Invalid planet selection. Please try again.{RESET}")

        # Check for asteroid field selection by ID (e.g., 1A, 2B)
        elif command in [field['id'] for field in systems_data[current_system].get('asteroid_fields', [])]:
            # Find the index of the selected asteroid field
            asteroid_index = next((i for i, field in enumerate(systems_data[current_system]['asteroid_fields']) if field['id'] == command), None)
            if asteroid_index is not None:
                display_asteroid_menu(systems_data[current_system], asteroid_index)
                display_system_menu(current_system, systems_data)  # Return to system menu after viewing asteroid field
            else:
                print(f"{RED}Invalid asteroid field selection. Please try again.{RESET}")
        
        # Return to game menu
        elif command == 'M':
            return 'M'
        
        # Handle invalid inputs
        else:
            print(f"{RED}Invalid input. Please enter a valid system number, planet letter (A-D), asteroid field ID, or 'M' for the menu.{RESET}")

def display_game_menu():
    """Displays the in-game menu options."""
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
    """Starts the game loop and handles system navigation."""
    while current_system != "8":
        display_system_menu(current_system, systems_data)
        while True:
            command = get_user_command(systems_data[current_system]['connections'], systems_data, current_system)
            if command == 'M':
                display_game_menu()
                handle_user_input(systems_data, current_system, allow_game_menu=True)
                break
            elif command in systems_data[current_system]['connections']:
                current_system = command
                break
        if current_system == "8":
            print(f"{GREEN}You have reached your destination!{RESET}")
            break

def setup_character():
    """Handles the setup of character data."""
    character_data = {}
    print(f"{CYAN}Please enter your character information!{RESET}")
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
    save_character_data(character_data)
    return character_data

def navigate_systems(systems_data, current_system, character_data):
    """Navigates the main game loop, starting with user menu and setting up game components."""
    ship_menus.setup_ship(character_data)  # Set up the ship after character creation
    current_system = "1"  # Set the starting system
    start_game(systems_data, current_system)  # Start the game loop

if __name__ == "__main__":
    print("Initializing RetroStellar...")
    display_header()  # Display the welcome header once at the start
    display_welcome_message()  # Show the introductory text
    display_user_menu()        # Show the main user menu immediately
    handle_user_input(systems_data={}, current_system="1")
