# settings.py

import json

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RED = "\033[31m"
GREEN = "\033[32m"

# Default settings for RetroStellar
default_settings = {
    "Universe Size": 16,  # Universe size can be adjusted here
}

# File name for saving settings
SETTINGS_FILE = 'settings.json'

def load_settings(filename=SETTINGS_FILE):
    """Loads the settings from a JSON file if it exists, otherwise uses default settings."""
    try:
        with open(filename, 'r') as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:
        print(f"{MAGENTA}Settings file not found. Using default settings.{RESET}")
        return default_settings
    except json.JSONDecodeError:
        print(f"{RED}Error reading settings file. Using default settings.{RESET}")
        return default_settings

def save_settings(settings, filename=SETTINGS_FILE):
    """Saves the settings to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(settings, file, indent=4)

def display_settings_menu(settings):
    """Displays the settings menu and allows adjustments."""
    while True:
        print(f"\n{CYAN}--- RetroStellar Settings ---{RESET}")
        for index, (key, value) in enumerate(settings.items(), start=1):
            print(f"{BOLD}{index}. {key}: {RESET}{value}")
        print(f"\nPress the number to change a setting, R to return to the main menu, or Q to quit.")

        choice = input(f"{BOLD}Enter your choice: {RESET}").strip().upper()
        if choice == 'Q':
            break
        elif choice == 'R':
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(settings):
            index = int(choice) - 1
            key = list(settings.keys())[index]

            if key == "Universe Size":
                new_size = input("Enter new universe size: ").strip()
                if new_size.isdigit() and int(new_size) > 0:
                    settings[key] = int(new_size)
                    save_settings(settings)  # Save updated settings
                    print(f"{MAGENTA}Universe size updated to {new_size}. Start a new game for these changes to take effect.{RESET}")
                    
                    # Prompt to start a new universe immediately
                    start_new = input(f"{BOLD}Do you want to start a new universe now? (Y or N): {RESET}").strip().upper()
                    if start_new == 'Y':
                        return 'NEW_GAME'  # Indicate that a new game should be started
                    else:
                        print(f"{CYAN}Returning to the current game...{RESET}")
                        return  # Return to the current game
                else:
                    print(f"{RED}Invalid input. Please enter a positive integer for the universe size.{RESET}")
            else:
                print(f"{RED}Changing this setting is not implemented yet.{RESET}")
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")

# Load settings at the start
current_settings = load_settings()
