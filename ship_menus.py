# ship_menus.py

import json
from character_menu import save_character_data  # Import save_character_data to save character info

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"

# Define specific colors for each faction
faction_colors = {
    "Mandate of God": YELLOW,  # Yellow
    "Shogunate 3072": RED,  # Red
    "People of the River": BLUE,  # Blue
    "The Noringian Hive": GREEN,  # Green
    "United Systems of Man": MAGENTA,  # Magenta
}

def load_json(filename):
    """Loads JSON data from a file."""
    with open(filename, 'r') as file:
        return json.load(file)

def save_json(filename, data):
    """Saves JSON data to a file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def load_ships(faction):
    """Loads available ships from ships.json and filters them by faction and rank."""
    ships = load_json('ships.json')
    faction_ships = ships["Starter Craft"].get(faction, [])

    # Filter ships by required rank (assuming 'Civilian' is the initial rank)
    available_ships = [ship for ship in faction_ships if ship['required_rank_to_pilot'] == 'Civilian']
    return available_ships

def display_ship_menu(ships, faction_color):
    """Displays a menu of starter ships for the player to choose from in the faction's color."""
    print(f"\n{CYAN}Choose your first ship from the available options below:{RESET}")
    for idx, ship in enumerate(ships, start=1):
        ship_name = ship.get('name', 'Unnamed Ship')
        description = ship.get('description', 'No description available')
        size = ship.get('size', 'Unknown size')
        min_cargo = ship.get('min_cargo', 'N/A')
        max_cargo = ship.get('max_cargo', 'N/A')
        max_shields = ship.get('max_shields', 'N/A')

        # Print ship name in faction color
        print(f"{BOLD}{idx}. {faction_color}{ship_name}{RESET}")
        print(f"   {description}")
        print(f"   Size: {size}, Cargo: {min_cargo} - {max_cargo}, Shields: {max_shields}\n")

def choose_ship(ships, faction_color):
    """Allows the player to select a ship from the list and name it, displaying ship names in faction color."""
    while True:
        try:
            choice = int(input(f"{BOLD}Enter the number of the ship you want to select: {RESET}").strip())
            if 1 <= choice <= len(ships):
                selected_ship = ships[choice - 1]
                ship_name = selected_ship.get('name', 'Unnamed Ship')
                print(f"{faction_color}You have selected: {ship_name}{RESET}")
                player_ship_name = input(f"{BOLD}Enter a name for your ship: {RESET}").strip()
                print(f"{faction_color}Your ship {player_ship_name} is ready for the journey!{RESET}")
                return selected_ship, player_ship_name
            else:
                print(f"{RED}Invalid choice. Please select a valid ship number.{RESET}")
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number.{RESET}")

def setup_ship(character_data):
    """Handles the ship selection process based on the chosen faction."""
    faction = character_data['Faction']
    ships = load_ships(faction)

    # Get the color for the chosen faction
    faction_color = faction_colors.get(faction, RESET)

    display_ship_menu(ships, faction_color)  # Display the ship menu with faction color
    selected_ship, ship_name = choose_ship(ships, faction_color)  # Choose the ship with faction color
    character_data['Ship Name'] = ship_name
    character_data['Ship Type'] = selected_ship

    save_character_data(character_data)  # Save updated character data
