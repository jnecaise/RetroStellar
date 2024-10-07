# game.py

import re
import sys
import json
import random
import subprocess
from json_utils import load_json
from settings import load_settings
from script import save_systems_data
from header_display import display_header
from planet_menu import display_planet_menu
from system_menu import display_system_menu
from factions import display_faction_options
from asteroid_menu import display_asteroid_menu
from game_logger import game_logger, trim_log_file
from display_messages import display_welcome_message
from ship_management import setup_ship, setup_player_ship
from ansi_colors import RED, BOLD, CYAN, RESET, GREEN, YELLOW
from character_menu import save_character_data, load_character_data
from menus import display_user_menu, handle_user_input, display_game_menu
from space_station import display_space_station_menu  # Import the space station menu

# Load settings at the start
current_settings = load_settings()

def update_visited_systems():
    """Updates the character_data.json with visited systems based on game_log.txt."""
    log_file = 'game_log.txt'
    character_data_file = 'character_data.json'

    # Read log data
    with open(log_file, 'r') as log:
        log_lines = log.readlines()

    # Extract visited systems from log data
    visited_systems = set()
    for line in log_lines:
        match = re.search(r'System (\d+) visited status: True', line)
        if match:
            system_number = int(match.group(1))
            visited_systems.add(system_number)

    # Load existing character data
    try:
        with open(character_data_file, 'r') as json_file:
            character_data = json.load(json_file)
    except FileNotFoundError:
        print(f"{RED}Character data file not found. Creating a new one.{RESET}")
        character_data = {}

    # Ensure 'visited_systems' key exists in character data
    if 'visited_systems' not in character_data:
        character_data['visited_systems'] = []

    # Update visited systems in character data, avoiding duplicates
    current_visited = set(character_data['visited_systems'])
    current_visited.update(visited_systems)
    character_data['visited_systems'] = list(current_visited)

    # Save updated character data
    with open(character_data_file, 'w') as json_file:
        json.dump(character_data, json_file, indent=4)

    print(f"{GREEN}Visited systems have been updated in character_data.json.{RESET}")

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

   # Set Current Credits to match Starting Credits
    character_data['Current Credits'] = character_data.get('Starting Credits', 0)

    save_character_data(character_data)  # Save initial character data

    # Load the newly generated universe
    systems_data = load_json('systems.json')

    # Ensure ship data is set up after character creation
    if 'Ship Type' not in character_data or not character_data['Ship Type']:
        character_data = setup_ship(character_data)
        save_character_data(character_data)

    # Initialize an empty inventory (empty cargo hold)
    character_data['inventory'] = []  # Set inventory as an empty list

    # Retrieve player's chosen faction and select eligible starting systems
    player_faction = character_data.get('Faction', 'Unaligned')
    factions_rules = {
        "The Noringian Hive": {"star_types": ["O-type", "B-type", "A-type"], "planet_types": None},
        "Mandate of God": {"star_types": ["A-type", "F-type", "G-type"], "planet_types": ["Terrestrial"]},
        "Shogunate 3072": {"star_types": ["G-type", "K-type", "M-type"], "planet_types": ["Terrestrial"]},
        "United Systems of Man": {"star_types": ["A-type", "F-type", "G-type"], "planet_types": ["Terrestrial"]},
        "People of the River": {"star_types": ["F-type", "G-type", "K-type"], "planet_types": ["Terrestrial"]},
    }

    # Get faction-specific rules
    rules = factions_rules.get(player_faction, {})

    # Find eligible systems based on the player's faction
    eligible_systems = [
        sys_id for sys_id, sys_info in systems_data.items()
        if sys_info["star_type"] in rules["star_types"] and
        (rules["planet_types"] is None or any(
            planet["type"] in rules["planet_types"] for planet in sys_info["planets"]
        ))
    ]

    # Select a random eligible system for the player to start in
    if eligible_systems:
        starting_system = random.choice(eligible_systems)
        systems_data[starting_system]["owned_by"] = player_faction
        game_logger.info(f"Player's faction {player_faction} starts in system: {starting_system} with star type {systems_data[starting_system]['star_type']}")
    else:
        # Fallback in case no eligible system is found
        starting_system = random.choice(list(systems_data.keys()))
        game_logger.warning(f"No eligible systems found for faction {player_faction}. Starting in random system: {starting_system}")

    # Save updated systems data to ensure the player's starting system is marked correctly
    save_systems_data('systems.json', systems_data)

    # Initialize 'current_system' in character_data
    character_data['current_system'] = starting_system
    save_character_data(character_data)

    # Log the new game start
    log_game_start("New Game", character_data, current_settings.get("Universe Size", 64))
    game_logger.info(f"Player starting in system: {starting_system}")

    print(f"{GREEN}New game setup complete. Starting game at System {starting_system}...{RESET}")

    # Call update_visited_systems to ensure logs are reflected in character data
    update_visited_systems()

    navigate_systems(systems_data, starting_system, character_data)  # Start from the randomly selected system

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

        # Retrieve the last visited system; default to "1" if not found
        current_system = character_data.get('current_system', "1")

        # Retrieve visited systems
        visited_systems = character_data.get('visited_systems', [])

        # Apply visited status to systems_data
        for system_id in visited_systems:
            if system_id in systems_data:
                systems_data[system_id]['visited'] = True
            else:
                game_logger.warning(f"Visited system ID {system_id} not found in systems_data.")

        # Log the game continuation
        log_game_start("Continue Game", character_data, current_settings.get("Universe Size", 64))

        print(f"{GREEN}Loaded saved game. Continuing at System {current_system}...{RESET}")

        # Resume the game using the saved data
        navigate_systems(systems_data, current_system, character_data)  # Pass current_system

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
    start_game(systems_data, current_system, character_data)  # Pass character_data

def start_game(systems_data, current_system, character_data):
    """Starts the game loop and handles system navigation."""
    while True:
        display_system_menu(current_system, systems_data)  # Display the current system menu

        # Mark the current system as visited
        systems_data[current_system]['visited'] = True
        if 'visited_systems' not in character_data:
            character_data['visited_systems'] = []
        if current_system not in character_data['visited_systems']:
            character_data['visited_systems'].append(current_system)
        save_character_data(character_data)

        while True:
            command = get_user_command(
                systems_data[current_system]['connections'],
                systems_data,
                current_system,
                character_data  # Pass character_data here
            ).upper()  # Convert to uppercase

            if command == 'M':
                display_game_menu()
                menu_choice = handle_user_input(
                    allow_game_menu=True,
                    settings=current_settings,
                    create_new_game_func=create_new_game,
                    load_existing_game_func=load_existing_game,
                    systems_data=systems_data,
                    current_system=current_system
                )
                if menu_choice == 'R':  # Return to system menu
                    break  # Exit to the main game loop
            elif command in systems_data[current_system]['connections']:
                current_system = command  # Update current system based on navigation

                # Mark the new system as visited
                systems_data[current_system]['visited'] = True
                if 'visited_systems' not in character_data:
                    character_data['visited_systems'] = []
                if current_system not in character_data['visited_systems']:
                    character_data['visited_systems'].append(current_system)

                # Update the current system in character_data
                character_data['current_system'] = current_system
                save_character_data(character_data)  # Save updated character data

                break
            else:
                # Handle other commands if necessary
                pass

def get_user_command(valid_systems, systems_data, current_system, character_data):
    """Prompts user for commands related to system navigation, planet selection, asteroid fields, and space stations."""
    while True:
        command = input(f"{BOLD}Your command: {RESET}").strip().upper()

        # Check for the secret admin shortcut to instantly jump to any system
        if command.startswith('@'):
            try:
                target_system = command[1:]  # Extract system number
                if target_system in systems_data:
                    current_system = target_system
                    print(f"{GREEN}Admin shortcut activated: You are now in system {current_system}.{RESET}")
                    game_logger.info(f"Admin shortcut: Moved to system {current_system}.")

                    # Update the current system in character_data
                    character_data['current_system'] = current_system
                    save_character_data(character_data)  # Save updated character data

                    # Display the system menu for the new system to confirm the move
                    display_system_menu(current_system, systems_data)

                else:
                    print(f"{RED}System {target_system} does not exist.{RESET}")
            except ValueError:
                print(f"{RED}Invalid system number. Please enter a valid system after '@'.{RESET}")
            continue  # Prompt again for input after using the shortcut

        # Check for valid system navigation
        elif command in valid_systems:
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

        # Check for space station access
        elif command == 'S':
            system_info = systems_data[current_system]
            if 'space_station' in system_info:
                station_info = system_info['space_station']
                display_space_station_menu(station_info)
                display_system_menu(current_system, systems_data)  # Return to system menu after station interaction
            else:
                print(f"{RED}There is no space station in this system.{RESET}")

        # Return to game menu
        elif command == 'M':
            return 'M'

        # Handle invalid inputs
        else:
            print(f"{RED}Invalid input. Please enter a valid system number, planet letter (A-D), asteroid field ID, 'S' for space station, or 'M' for the menu.{RESET}")

if __name__ == "__main__":
    print("Initializing RetroStellar.........")
    display_header()  # Display the welcome header once at the start
    display_welcome_message()  # Show the introductory text

    while True:
        display_user_menu()  # Show the main user menu
        action = handle_user_input(
            create_new_game_func=create_new_game,
            load_existing_game_func=load_existing_game
        )

        # After handling user input, check if the game should continue
        if action == 'START_GAME':
            # The game functions (create_new_game or load_existing_game) will handle starting the game
            break
        elif action == 'QUIT':
            print("Quitting the game. Goodbye!")
            sys.exit()
        else:
            # Continue looping to display the main menu again
            continue
