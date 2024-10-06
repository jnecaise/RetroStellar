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
