# factions.py

from json_utils import load_json
from ansi_colors import CYAN, RESET, BOLD, RED # type: ignore

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
