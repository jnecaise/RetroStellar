import os
import json
import textwrap

from ansi_colors import CYAN, RESET, GREEN, YELLOW, BOLD, RED
from game_logger import game_logger

def display_space_station_menu(station_info):
    """Displays the space station menu with available services and graphical borders."""
    station_name = station_info.get('name', 'Unknown Station')
    station_type = station_info.get('type', 'Unknown Type')
    station_description = station_info.get('description', 'No description available.')
    station_services = station_info.get('services', [])
    menu_width = 60  # Adjust menu width to fit your needs

    # Function for top/bottom border
    def border_line():
        return "+" + "-" * (menu_width - 2) + "+"

    # Function for formatting text lines inside the menu
    def format_line(text):
        return f"| {text:<{menu_width - 4}} |"

    # Wrap long text to fit inside the border
    wrapped_description = textwrap.wrap(station_description, width=menu_width - 4)

    # Print the station info with a graphical border
    print(border_line())
    print(format_line(f"Welcome to {station_name} ({station_type})".center(menu_width - 4)))
    print(border_line())
    
    # Print each line of the wrapped description
    for line in wrapped_description:
        print(format_line(line))
    
    print(border_line())
    print(format_line("Available Services:"))
    for idx, service in enumerate(station_services, 1):
        print(format_line(f"  {idx}. {service}"))
    print(border_line())
    print(format_line("Press the service number to select it, or 'R' to return."))
    print(border_line())

    # Handle user input
    while True:
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()
        if choice == 'R':
            return  # Return to the system menu
        elif choice.isdigit():
            service_idx = int(choice) - 1
            if 0 <= service_idx < len(station_services):
                selected_service = station_services[service_idx]
                handle_station_service(selected_service, station_name)
            else:
                print(f"{RED}Invalid service number. Please try again.{RESET}")
        else:
            print(f"{RED}Invalid input. Please enter a service number or 'R' to return.")


# New Market Menu Functions
def display_market_menu(station_name):
    """Displays the Market menu for the space station."""
    market_title = f"{station_name} Market"
    
    print(f"\n{CYAN}{BOLD}{market_title}{RESET}")
    print(f"{YELLOW}Welcome to the Market!{RESET}")
    print("Available options:")
    print("  B. Buy Items")
    print("  S. Sell Items")
    print("  R. Return to the station menu")

    while True:
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()

        if choice == 'B':
            display_buy_menu()
        elif choice == 'S':
            display_sell_menu()
        elif choice == 'R':
            print(f"\nReturning to {station_name} menu...")
            return  # Exit to the main station menu
        else:
            print(f"{RED}Invalid choice. Please select B, S, or R.{RESET}")

def load_inventory():
    """Loads the shop inventory from a JSON file."""
    inventory_file = 'C:/RetroStellar/shop_inventory.json'
    
    game_logger.info(f"Looking for file at: {inventory_file}")
    
    if not os.path.exists(inventory_file):
        game_logger.error("CAN'T FIND INVENTORY - File not found")
        return []  # Return an empty list if file is missing
    
    try:
        with open(inventory_file, 'r') as file:
            inventory = json.load(file)
        game_logger.info(f"Inventory successfully loaded: {inventory}")
        return inventory
    except json.JSONDecodeError as e:
        game_logger.error(f"Error in JSON structure: {e}")
        return []  # Return an empty list if there's a JSON decoding issue
    except IOError as e:
        game_logger.error(f"Error reading file: {e}")
        return []  # Return an empty list if there's an issue opening the file

def display_buy_menu():
    """Displays the Buy menu with items loaded from the JSON file."""
    inventory = load_inventory()
    
    if not inventory:
        print(f"{RED}No items available for purchase.{RESET}")
        return

    print(f"\n{CYAN}{BOLD}Items for sale:{RESET}")
    
    for idx, item in enumerate(inventory, 1):
        print(f"  {idx}. {item['name']} - {item['price']} Credits")
    
    print("\nPress R to return to the market menu.")
    
    while True:
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()

        if choice == 'R':
            return  # Return to the market menu
        elif choice.isdigit() and 1 <= int(choice) <= len(inventory):
            selected_item = inventory[int(choice) - 1]
            print(f"{GREEN}You selected {selected_item['name']} for {selected_item['price']} credits.{RESET} (Buying functionality not implemented yet)")
        else:
            print(f"{RED}Invalid choice. Please select a valid item number or R.{RESET}")

def display_sell_menu():
    """Displays the Sell menu with placeholder items."""
    print(f"\n{CYAN}{BOLD}Items available to sell:{RESET}")
    print("  1. Sell Test 1")
    print("  2. Sell Test 2")
    print("  3. Sell Test 3")
    print("\nPress R to return to the market menu.")
    
    while True:
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()

        if choice == 'R':
            return  # Return to the market menu
        elif choice in ['1', '2', '3']:
            print(f"{GREEN}You selected item {choice}.{RESET} (Selling functionality not implemented yet)")
        else:
            print(f"{RED}Invalid choice. Please select 1, 2, 3 or R.{RESET}")

def handle_station_service(service_name, station_name):
    """Handles the selected service at the space station."""
    print(f"\n{GREEN}You have selected the {service_name} service.{RESET}")
    
    # Adjusting to handle variations of 'Market'
    if 'market' in service_name.lower():
        display_market_menu(station_name)
    elif 'mission' in service_name.lower():
        # Call the missions menu function (to be implemented)
        pass
    elif 'ship dock' in service_name.lower():
        # Call the ship dock menu function (to be implemented)
        pass
    else:
        print(f"{YELLOW}Service '{service_name}' is currently under development.{RESET}")
