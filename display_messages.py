# display_messages.py

from ansi_colors import GREEN, RESET  # type: ignore # Import necessary colors from ansi_colors

def display_welcome_message():
    """Displays the introductory text without the header ASCII art."""
    print(f"{GREEN}Welcome to RetroStellar! This game is an attempt to capture the retro feel of the early online games.{RESET}\n")
