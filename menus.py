# menus.py

import sys
import importlib
import help_menu
from ansi_colors import RED, BOLD, CYAN, MAGENTA, GREEN, RESET  # Import necessary colors
from character_menu import display_character_menu, handle_character_menu_input
from header_display import display_header
from settings import display_settings_menu, save_settings  # Import settings-related functions
from system_menu import display_system_menu  # Import to display the system menu correctly
from json_utils import load_json

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

def reload_character_menu():
    """Reloads the character menu module and displays it."""
    importlib.reload(character_menu) # type: ignore
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

def display_game_menu():
    """Displays the in-game menu options."""
    menu = """
\033[33m
Game Menu:
  R to Return to Game
  Q to Quit
  I to Display Character Menu
  H for Help
  T for Settings Menu
\033[0m
    """
    print(menu)

def handle_user_input(systems_data, current_system, allow_game_menu=False, settings=None, create_new_game_func=None, load_existing_game_func=None):
    """Handles user input from the main menu or in-game menu."""
    while True:
        # Set valid choices based on context
        choices = "NCTQH" if not allow_game_menu else "RMQHIT"
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()  # Convert to uppercase

        if choice == 'Q':
            print("Quitting the game. Goodbye!")
            sys.exit()
        elif choice == 'R' and allow_game_menu:  # Return to game from in-game menu
            display_system_menu(current_system, systems_data)  # Explicitly display the system menu
            return  # Correctly exit and resume the main game loop
        elif choice == 'N' and not allow_game_menu:  # New Game
            if create_new_game_func:
                create_new_game_func()  # Use the passed function reference
            return True  # Signal to start the game
        elif choice == 'C' and not allow_game_menu:  # Continue Game
            if load_existing_game_func and load_existing_game_func():  # Use the passed function reference
                return True
            else:
                print(f"{RED}No saved game found. Please start a new game first.{RESET}")
        elif choice == 'T':  # Display Settings Menu
            if settings is None:
                settings = {}  # Default to an empty dictionary if not provided
            start_new = display_settings_menu(settings)
            save_settings(settings)  # Save settings after changes
            if start_new == 'NEW_GAME' and create_new_game_func:
                create_new_game_func()  # Start a new game immediately
                return True
        elif choice == 'H':
            help_menu.display_help()
        elif allow_game_menu and choice == 'I':  # Display Character Menu
            display_character_menu()  # Show the character menu
            character_menu_choice = handle_character_menu_input()  # Handle character menu input and return
            if character_menu_choice == 'R':
                display_system_menu(current_system, systems_data)  # Re-display the system menu
                return  # Correctly return to the game loop
        else:
            print(f"{RED}Invalid option. Please choose {choices}.{RESET}")
