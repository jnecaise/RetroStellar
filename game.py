# game.py

import subprocess
import sys
import json
import help
import importlib
import ship_menus  # type: ignore
import character_menu
from character_menu import display_character_menu, save_character_data, load_character_data, handle_character_menu_input
from header_display import display_header  # type: ignore
from planet_menu import display_planet_menu  # type: ignore
from system_menu import display_system_menu  # type: ignore
from asteroid_menu import display_asteroid_menu  # type: ignore
from settings import default_settings, display_settings_menu  # type: ignore

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
        # Set valid choices based on context
        choices = "NCTQH" if not allow_game_menu else "RMQHIT"
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()  # Convert to uppercase

        if choice == 'Q':
            print("Quitting the game. Goodbye!")
            sys.exit()
        elif choice == 'R' and allow_game_menu:  # Return to game from in-game menu
            display_system_menu(current_system, systems_data)
            return  # Exit the function to resume the main game loop
        elif choice == 'N' and not allow_game_menu:  # New Game
            create_new_game()
            return True  # Signal to start the game
        elif choice == 'C' and not allow_game_menu:  # Continue Game
            if load_existing_game():
                return True
            else:
                print(f"{RED}No saved game found. Please start a new game first.{RESET}")
        elif choice == 'T' and not allow_game_menu:
            display_settings_menu(settings)
        elif choice == 'H':
            help.display_help()
        elif allow_game_menu and choice == 'I':  # Display Character Menu
            display_character_menu()  # Show the character menu
            character_menu_choice = handle_character_menu_input()  # Handle character menu input and return
            if character_menu_choice == 'R':
                display_system_menu(current_system, systems_data)  # Return to the system menu
                continue  # Continue the game loop
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

def reload_character_menu():
    """Reloads the character menu module and displays it."""
    importlib.reload(character_menu)
    display_character_menu()
    handle_character_menu_input()

def display_character_menu():
    """Displays the character menu with detailed information including all ship details."""
    character_data = load_json('character_data.json')

    # Extract ship data from character data
    ship_data = character_data.get('Ship Type', {})
    if not ship_data:
        print(f"{RED}No ship data available. Please select a ship first.{RESET}")
        return

    # Define faction-specific colors
    faction_colors = {
        "Mandate of God": "\033[33m",  # Yellow
        "Shogunate 3072": "\033[31m",  # Red
        "People of the River": "\033[34m",  # Blue
        "The Noringian Hive": "\033[32m",  # Green
        "United Systems of Man": "\033[35m",  # Magenta
    }

    faction = character_data.get('Faction', 'Unknown')
    faction_color = faction_colors.get(faction, RESET)

    # Display character information
    print(f"\n{CYAN}{BOLD}Character Menu{RESET}")
    print(f"{MAGENTA}Character Name: {GREEN}{character_data.get('Character Name', 'N/A')}{RESET}")
    print(f"{MAGENTA}Faction: {faction_color}{faction}{RESET}")
    print(f"{MAGENTA}Ship Name: {faction_color}{character_data.get('Ship Name', 'N/A')}{RESET}")
    print(f"{MAGENTA}Starting Credits: {GREEN}{character_data.get('Starting Credits', 'N/A')}{RESET}")

    # Display ship details
    print(f"\n{MAGENTA}Ship Details:{RESET}")
    print(f"   {ship_data.get('description', 'No description available.')}")
    print(f"   Class: {ship_data.get('class', 'Unknown')}")
    print(f"   Faction of Origin: {ship_data.get('faction_of_origin', 'Unknown')}")
    print(f"   Required Rank to Pilot: {ship_data.get('required_rank_to_pilot', 'Unknown')}")
    print(f"   Size: {ship_data.get('size', 'Unknown')}")
    print(f"   Cost: {ship_data.get('ship_cost', 'Unknown')}")
    print(f"   Cargo: {ship_data.get('min_cargo', 'Unknown')} - {ship_data.get('max_cargo', 'Unknown')}")
    print(f"   Shields: {ship_data.get('max_shields', 'Unknown')}")
    print(f"   Armor: {ship_data.get('max_armor', 'Unknown')}")
    print(f"   Hull: {ship_data.get('max_hull', 'Unknown')}")
    print(f"   System Scanner: {ship_data.get('system_scanner_type', 'Unknown')} Level {ship_data.get('system_scanner_level', 'Unknown')}")
    print(f"   Planet Scanner: {ship_data.get('planet_scanner', 'Unknown')} Level {ship_data.get('planet_scanner_level', 'Unknown')}")
    print(f"   Resource Scanner: {ship_data.get('resource_scanner', 'Unknown')} Level {ship_data.get('resource_scanner_level', 'Unknown')}")
    print(f"   Weapon Type: {ship_data.get('weapon_type', 'Unknown')}")
    print(f"   Combat Bonus: {ship_data.get('combat_bonus', 'Unknown')}")
    print(f"   Mining Attachment: {ship_data.get('mining_attachment', 'Unknown')} Level {ship_data.get('mining_attachment_level', 'Unknown')}")
    print("\nPress R to return to the game or Q to quit.")

def handle_character_menu_input():
    """Handles user input within the character menu."""
    while True:
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()  # Convert to uppercase
        if choice == 'R':
            return 'R'  # Return to signal that the player wants to return to the game
        elif choice == 'Q':
            print("Quitting the game. Goodbye!")
            sys.exit()
        else:
            print(f"{MAGENTA}Invalid option. Please choose 'R' to return to the game or 'Q' to quit.{RESET}")

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
  R to Return to Game
  Q to Quit
  I to Display Character Menu
  H for Help
\033[0m
    """
    print(menu)


def start_game(systems_data, current_system):
    """Starts the game loop and handles system navigation."""
    while current_system != "8":  # Assuming "8" is a special destination
        display_system_menu(current_system, systems_data)
        while True:
            command = get_user_command(systems_data[current_system]['connections'], systems_data, current_system).upper()  # Convert to uppercase
            if command == 'M':
                display_game_menu()
                menu_choice = handle_user_input(systems_data, current_system, allow_game_menu=True)
                if menu_choice == 'R':  # Return to system menu
                    display_system_menu(current_system, systems_data)  # Explicitly show the system menu
                continue  # Continue to accept commands for system navigation
            elif command in systems_data[current_system]['connections']:
                current_system = command  # Update current system based on navigation
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

if __name__ == "__main__":
    print("Initializing RetroStellar...")
    display_header()  # Display the welcome header once at the start
    display_welcome_message()  # Show the introductory text
    display_user_menu()        # Show the main user menu immediately
    handle_user_input(systems_data={}, current_system="1")
