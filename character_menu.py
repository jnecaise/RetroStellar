# character_menu.py

import json
import sys

def load_character_data():
    """Loads character data from the character_data.json file."""
    with open('character_data.json', 'r') as file:
        return json.load(file)

def save_character_data(data):
    """Saves character data to the character_data.json file."""
    with open('character_data.json', 'w') as file:
        json.dump(data, file, indent=4)

def display_character_menu():
    """Displays the character menu with the current character details."""
    character_data = load_character_data()

    print(f"\n------======CHARACTER MENU======------\n")
    print(f"Character Name: {character_data.get('Character Name', 'N/A')}")
    print(f"Ship Name: {character_data.get('Ship Name', 'N/A')}")
    print(f"Faction: {character_data.get('Faction', 'N/A')}")
    print(f"Starting Credits: {character_data.get('Starting Credits', 'N/A')}")
    print(f"Current Credits: {character_data.get('Current Credits', 'N/A')}")
    
    # Display ship inventory
    inventory = character_data.get('inventory', [])
    if inventory:
        print(f"\nInventory:")
        for item in inventory:
            print(f" - {item['item_name']} (Cargo Space: {item['cargo_space_amount']})")
    else:
        print(f"\nInventory is empty.")
    
    print(f"\n------======CHARACTER MENU======------")
    print("\nPress M to return to the game or Q to quit.")

def handle_character_menu_input():
    """Handles user input within the character menu."""
    while True:
        choice = input("Your choice: ").strip().upper()
        if choice == 'M':
            return  # Return to the game
        elif choice == 'Q':
            print("Quitting the game. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Press M to return or Q to quit.")
