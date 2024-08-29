import json
import sys

def load_character_data():
    with open('character_data.json', 'r') as file:
        return json.load(file)

def display_character_menu():
    character_data = load_character_data()
    print(f"\n------======CHARACTER MENU======------")
    print()
    print(f"Character Name: {character_data.get('Character Name', 'N/A')}")
    print(f"Ship Name: {character_data.get('Ship Name', 'N/A')}")
    print(f"Faction: {character_data.get('Faction', 'N/A')}")
    print(f"Starting Credits: {character_data.get('Starting Credits', 'N/A')}")
    print(f"\n------======CHARACTER MENU======------")
    print("\nPress M to return to the game or Q to quit.")

def handle_character_menu_input():
    choice = input("Your choice: ").strip().upper()
    if choice == 'M':
        return  # Return to game
    elif choice == 'Q':
        print("Quitting the game. Goodbye!")
        sys.exit()
    else:
        print("Invalid choice. Press M to return or Q to quit.")
