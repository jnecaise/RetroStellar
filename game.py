# game.py

import json
import subprocess
import random
from json_utils import load_json
from settings import load_settings
from header_display import display_header
from planet_menu import display_planet_menu  
from system_menu import display_system_menu
from factions import display_faction_options
from asteroid_menu import display_asteroid_menu
from display_messages import display_welcome_message
from ship_management import setup_ship, setup_player_ship 
from ansi_colors import RED, BOLD, CYAN, RESET, GREEN, YELLOW
from character_menu import save_character_data, load_character_data
from menus import (display_user_menu, handle_user_input, display_game_menu)
from game_logger import game_logger  # Import the modularized logger

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

    # Randomly select a starting system
    starting_system = random.choice(list(systems_data.keys()))

    # Log the new game start
    log_game_start("New Game", character_data, current_settings.get("Universe Size", 16))
    game_logger.info(f"Player starting in system: {starting_system}")

    print(f"{GREEN}New game setup complete. Starting game...{RESET}")
    navigate_systems(systems_data, starting_system, character_data)  # Pass the randomly chosen starting system

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

        # Log the game continuation
        log_game_start("Continue Game", character_data, current_settings.get("Universe Size", 16))

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

def log_game_start(game_type, character_data, universe_size):
    """Logs the details of the game start."""
    game_logger.info(f"Game Start: {game_type} Selected")
    game_logger.info(f"Universe Size: {universe_size} systems")
    game_logger.info(f"Character Name: {character_data.get('Character Name', 'Unknown')}")
    game_logger.info(f"Faction: {character_data.get('Faction', 'None')}")
    game_logger.info(f"Ship Type: {character_data.get('Ship Type', 'Unknown')}")
    game_logger.info(f"Ship Name: {character_data.get('Ship Name', 'Unnamed')}")

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
    ship_data = character_data.get('Ship Type', {})
    if not ship_data:
        print(f"{YELLOW}No ship data found. Initializing ship selection.{RESET}")
        character_data = setup_ship(character_data)
        save_character_data(character_data)
        ship_data = character_data.get('Ship Type', {})

    player_ship = setup_player_ship(ship_data)  # Set up the ship after character creation
    start_game(systems_data, current_system)  # Start the game loop

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
