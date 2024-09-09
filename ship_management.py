
# ship_management.py

from ansi_colors import CYAN, BOLD, RESET, GREEN, RED  # Import necessary ANSI color codes
from json_utils import load_json  # Import JSON utility functions
from character_menu import save_character_data  # Import save character data function

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
