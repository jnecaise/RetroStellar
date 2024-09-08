# game.py

import subprocess
import sys
import json
import importlib
from ansi_colors import RED, BOLD, BLUE, CYAN, RESET, GREEN, YELLOW, MAGENTA  # Import ANSI color codes
from menus import (  # Import the menu functions
    display_user_menu,
    reload_character_menu,
    display_character_menu,
    handle_character_menu_input,
    handle_user_input,
    display_game_menu,
)
from display_messages import display_welcome_message  # Import display message functions
from settings import default_settings, display_settings_menu, save_settings, load_settings  # Import settings functions
from header_display import display_header  # Import header display function
from planet_menu import display_planet_menu  # Import planet menu function
from system_menu import display_system_menu  # Import system menu function
from asteroid_menu import display_asteroid_menu  # Import asteroid menu function
from json_utils import load_json, save_json  # Import JSON utility functions
from character_menu import save_character_data, load_character_data  # Import character data functions

# Load settings at the start
current_settings = load_settings()

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

    # Ensure ship data is set up after character creation
    if 'Ship Type' not in character_data or not character_data['Ship Type']:
        character_data = setup_ship(character_data)
        save_character_data(character_data)

    print(f"{GREEN}New game setup complete. Starting game...{RESET}")
    navigate_systems(systems_data, "1", character_data)  # Pass the necessary data to navigate_systems

def load_existing_game():
    """Loads the existing universe and player data if available."""
    try:
        # Load the saved universe and character data
        systems_data = load_json('systems.json')  # Load saved universe data
        character_data = load_character_data()  # Load saved character data

        # Check if ship data is present; if not, prompt for ship selection
        if 'Ship Type' not in character_data or not character_data['Ship Type']:
            print(f"{YELLOW}No ship data found. You need to select a ship first.{RESET}")
            character_data = setup_ship(character_data)
            save_character_data(character_data)

        print(f"{GREEN}Loaded saved game. Continuing...{RESET}")

        # Resume the game using the saved data
        navigate_systems(systems_data, "1", character_data)  # Resume at the correct system
        return True
    except FileNotFoundError:
        print(f"{RED}Save files not found. Unable to continue the game.{RESET}")
        return False
    except json.JSONDecodeError:
        print(f"{RED}Error loading save files. The data may be corrupted.{RESET}")
        return False

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

def setup_ship(character_data):
    """Handles ship selection and updates the character data with chosen ship details."""
    ships = load_json('ships.json')
    faction = character_data['Faction']
    faction_ships = ships.get("Starter Craft", {}).get(faction, [])

    # Define faction-specific colors
    faction_colors = {
        "Mandate of God": "\033[33m",  # Yellow
        "Shogunate 3072": "\033[31m",  # Red
        "People of the River": "\033[34m",  # Blue
        "The Noringian Hive": "\033[32m",  # Green
        "United Systems of Man": "\033[35m",  # Magenta
    }

    faction_color = faction_colors.get(faction, RESET)

    # Display available ships for the faction with the faction color applied only to ship names
    print(f"{CYAN}Choose your first ship from the available options below:{RESET}")
    for idx, ship in enumerate(faction_ships, start=1):
        print(f"{idx}. {faction_color}{ship['name']}{RESET}")
        print(f"   {ship['description']}")
        print(f"   Size: {ship['size']}, Cargo: {ship['min_cargo']} - {ship['max_cargo']}, Shields: {ship['max_shields']}\n")

    # Prompt for ship selection
    while True:
        ship_choice = input(f"{BOLD}Enter the number of the ship you want to select: {RESET}").strip()
        try:
            ship_idx = int(ship_choice) - 1
            if 0 <= ship_idx < len(faction_ships):
                chosen_ship = faction_ships[ship_idx]
                print(f"\n{faction_color}You have selected: {chosen_ship['name']}{RESET}")
                
                # Prompt for ship name
                ship_name = input(f"{BOLD}Enter a name for your ship: {RESET}").strip()
                character_data['Ship Name'] = ship_name
                character_data['Ship Type'] = chosen_ship
                print(f"{GREEN}Your ship {ship_name} is ready for the journey!{RESET}")
                break
            else:
                print(f"{RED}Invalid ship choice. Try again.{RESET}")
        except ValueError:
            print(f"{RED}Please enter a valid number.{RESET}")

    return character_data

def navigate_systems(systems_data, current_system, character_data):
    """Navigates the main game loop, starting with user menu and setting up game components."""
    ship_data = character_data.get('Ship Type', {})
    if not ship_data:
        print(f"{YELLOW}No ship data found. Initializing ship selection.{RESET}")
        character_data = setup_ship(character_data)
        save_character_data(character_data)
        ship_data = character_data.get('Ship Type', {})

    player_ship = setup_player_ship(ship_data)  # Set up the ship after character creation
    current_system = "1"  # Set the starting system
    start_game(systems_data, current_system)  # Start the game loop

def setup_player_ship(ship_data):
    """Set up the player's ship based on the loaded data."""
    print(f"Setting up player ship: {ship_data.get('name', 'Unknown Ship')}")
    player_ship = {
        'name': ship_data.get('name'),
        'class': ship_data.get('class'),
        'max_shields': ship_data.get('max_shields'),
        'max_armor': ship_data.get('max_armor'),
        'max_hull': ship_data.get('max_hull'),
        # Add more attributes as needed
    }
    return player_ship

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

def start_game(systems_data, current_system):
    """Starts the game loop and handles system navigation."""
    while True:
        display_system_menu(current_system, systems_data)  # Display the current system menu
        while True:
            command = get_user_command(systems_data[current_system]['connections'], systems_data, current_system).upper()  # Convert to uppercase
            if command == 'M':
                display_game_menu()
                menu_choice = handle_user_input(
                    systems_data,
                    current_system,
                    allow_game_menu=True,
                    settings=current_settings,
                    create_new_game_func=create_new_game,
                    load_existing_game_func=load_existing_game,
                )
                if menu_choice == 'R':  # Return to system menu
                    break  # Exit to the main game loop
            elif command in systems_data[current_system]['connections']:
                current_system = command  # Update current system based on navigation
                break

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

if __name__ == "__main__":
    print("Initializing RetroStellar...")
    display_header()  # Display the welcome header once at the start
    display_welcome_message()  # Show the introductory text
    display_user_menu()  # Show the main user menu immediately
    handle_user_input(
        systems_data={},
        current_system="1",
        create_new_game_func=create_new_game,
        load_existing_game_func=load_existing_game,
    )
