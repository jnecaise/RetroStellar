import json

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RED = "\033[31m"

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Updated load_ships function to handle multiple ships per faction
def load_ships(faction):
    """ Load available ships from ships.json and filter by faction and rank """
    ships = load_json('ships.json')
    available_ships = []

    # Extract the array of ships for the chosen faction
    faction_ships = ships["Starter Craft"].get(faction, [])

    # Filter ships by required rank (here we assume 'Civilian' is the initial rank)
    for ship in faction_ships:
        if ship['required_rank_to_pilot'] == 'Civilian':
            available_ships.append(ship)

    return available_ships

# Updated display_ship_menu function to handle the list of ships correctly
def display_ship_menu(ships):
    """ Display a menu of starter ships for the player to choose from """
    print(f"\n{CYAN}Choose your first ship from the available options below:{RESET}")
    for idx, ship in enumerate(ships, start=1):
        ship_name = ship.get('name', 'Unnamed Ship')
        description = ship.get('description', 'No description available')
        size = ship.get('size', 'Unknown size')
        min_cargo = ship.get('min_cargo', 'N/A')
        max_cargo = ship.get('max_cargo', 'N/A')
        max_shields = ship.get('max_shields', 'N/A')
        print(f"{BOLD}{idx}. {ship_name}{RESET}")
        print(f"   {description}")
        print(f"   Size: {size}, Cargo: {min_cargo} - {max_cargo}, Shields: {max_shields}\n")

# Updated choose_ship function to handle the selection from the list correctly
def choose_ship(ships):
    """ Let the player select a ship and name it """
    while True:
        try:
            choice = int(input(f"{BOLD}Enter the number of the ship you want to select: {RESET}").strip())
            if 1 <= choice <= len(ships):
                selected_ship = ships[choice - 1]  # Correctly fetch the ship from the list
                ship_name = selected_ship.get('name', 'Unnamed Ship')
                print(f"{GREEN}You have selected: {ship_name}{RESET}")
                player_ship_name = input(f"{BOLD}Enter a name for your ship: {RESET}").strip()
                print(f"{GREEN}Your ship {player_ship_name} is ready for the journey!{RESET}")
                return selected_ship, player_ship_name
            else:
                print(f"{RED}Invalid choice. Please select a valid ship number.{RESET}")
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number.{RESET}")
