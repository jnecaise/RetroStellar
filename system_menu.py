# system_menu.py

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

def display_system_menu(current_system, systems_data):
    """ Displays detailed information about the selected system """
    system_info = systems_data[current_system]
    
    # Display planets without showing letters A, B, C, D
    planets = ', '.join(planet['name'] for planet in system_info['planets'])

    stargates = ', '.join(system_info['connections'])
    star_type = system_info.get('star_type', 'Unknown')  # Default to 'Unknown' if not present
    hazard_level = system_info.get('hazard_level', 'Unknown')  # Default to 'Unknown' if not present
    ownership = system_info.get('owned_by', 'Unoccupied')  # Default to 'Unoccupied' if not present
    current_name = system_info.get('current_name', current_system)  # Use the current name of the system
    
    print(f"\n{CYAN}System: {current_name}{RESET}")
    print(f"{system_info['description']}")
    print(f"{GREEN}Owned by: {ownership}{RESET}")  # Display ownership
    print(f"{CYAN}Star Type: {star_type}{RESET}")  # Display the star type
    print(f"{MAGENTA}Planets: {planets}{RESET}")
    
    # Display asteroid fields names on the same line
    if 'asteroid_fields' in system_info:
        asteroid_fields = ', '.join(field['id'] for field in system_info['asteroid_fields'])
        print(f"{CYAN}Asteroid Fields: {asteroid_fields}{RESET}")
    
    print(f"{RED}Hazard Level: {hazard_level}{RESET}")
    print(f"{YELLOW}Stargates: {stargates}{RESET}")
