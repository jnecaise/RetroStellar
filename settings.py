# settings.py

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"

# Default settings for RetroStellar
default_settings = {
    "Game Type": "Open",
    "Time Per Day": "Unlimited",
    "Initial Fighters": 30,
    "Initial Credits": 300,
    "Initial Holds": 20,
    "Sectors In Game": 1000,
}

def display_settings_menu(settings):
    """Display the settings menu."""
    print(f"\n{CYAN}--- RetroStellar Settings ---{RESET}")
    for key, value in settings.items():
        print(f"{BOLD}{key}: {RESET}{value}")
    print("\nPress M to return to the main menu or Q to quit.")
