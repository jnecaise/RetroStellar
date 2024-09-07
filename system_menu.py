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
    """Displays detailed information about the selected system."""
    system_info = systems_data[current_system]

    planets = get_planet_names(system_info)
    stargates = get_stargates(system_info)
    star_type = system_info.get('star_type', 'Unknown')
    hazard_level = system_info.get('hazard_level', 'Unknown')
    ownership = system_info.get('owned_by', 'Unoccupied')
    current_name = system_info.get('current_name', current_system)

    print_system_details(current_name, system_info, ownership, star_type, planets, hazard_level, stargates)
    display_asteroid_fields(system_info)

def get_planet_names(system_info):
    """Returns a string of planet names in the system."""
    return ', '.join(planet['name'] for planet in system_info['planets'])

def get_stargates(system_info):
    """Returns a string of stargates connections."""
    return ', '.join(system_info['connections'])

def print_system_details(current_name, system_info, ownership, star_type, planets, hazard_level, stargates):
    """Prints the basic details of the system including name, description, ownership, and connections."""
    print(f"\n{CYAN}System: {current_name}{RESET}")
    print(f"{system_info['description']}")
    print(f"{GREEN}Owned by: {ownership}{RESET}")
    print(f"{CYAN}Star Type: {star_type}{RESET}")
    print(f"{MAGENTA}Planets: {planets}{RESET}")
    print(f"{RED}Hazard Level: {hazard_level}{RESET}")
    print(f"{YELLOW}Stargates: {stargates}{RESET}")

def display_asteroid_fields(system_info):
    """Displays the asteroid fields present in the system."""
    if 'asteroid_fields' in system_info:
        asteroid_fields = ', '.join(field['id'] for field in system_info['asteroid_fields'])
        print(f"{CYAN}Asteroid Fields: {asteroid_fields}{RESET}")
