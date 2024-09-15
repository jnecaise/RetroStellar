# system_menu.py

from game_logger import game_logger  # Import the modularized logger
from factions import faction_colors  # Import faction colors from factions.py

# ANSI color codes
RED = "\033[31m"
BOLD = "\033[1m"
CYAN = "\033[36m"
RESET = "\033[0m"
WHITE = "\033[37m"
GREEN = "\033[32m"
BLACK = "\033[30m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
BG_BLACK = "\033[40m"
BG_YELLOW = "\033[43m"
BLINK = "\033[5m"        # Note: Not widely supported
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLACK = "\033[90m"   # Gray
BG_BRIGHT_BLUE = "\033[104m"

# Set to track systems that have already been logged as visited
logged_visited_systems = set()

def display_system_menu(current_system, systems_data):
    """Displays detailed information about the selected system."""
    # Mark the current system as visited
    systems_data[current_system]['visited'] = True  # Ensure the system is marked as visited

    system_info = systems_data[current_system]
    
    planets = get_planet_names(system_info)
    star_type = system_info.get('star_type', 'Unknown')
    hazard_level = system_info.get('hazard_level', 'Unknown')
    ownership = system_info.get('owned_by', 'Unoccupied')
    current_name = system_info.get('current_name', current_system)

    # Get the color for the faction from faction_colors, defaulting to RESET if not found
    faction_color = faction_colors.get(ownership, RESET)
    colored_ownership = f"{faction_color}{ownership}{RESET}"

    # Format and display stargates with adjusted colors based on visited status
    formatted_stargates = format_stargates(system_info, systems_data)

    print_system_details(current_name, system_info, colored_ownership, star_type, planets, hazard_level, formatted_stargates)
    display_asteroid_fields(system_info)
    display_space_station(system_info)  # Display the space station if present

def get_planet_names(system_info):
    """Returns a string of planet names in the system."""
    return ', '.join(planet['name'] for planet in system_info['planets'])

def get_stargates(system_info):
    """Returns a string of stargates connections."""
    return ', '.join(system_info['connections'])

def print_system_details(current_name, system_info, ownership, star_type, planets, hazard_level, formatted_stargates):
    """Prints the basic details of the system including name, description, ownership, and connections."""
    print(f"\n{CYAN}System: {current_name}{RESET}")
    print(f"{system_info['description']}")
    print(f"{GREEN}Owned by: {ownership}{RESET}")
    print(f"{CYAN}Star Type: {star_type}{RESET}")
    print(f"{MAGENTA}Planets: {planets}{RESET}")
    print(f"{RED}Hazard Level: {hazard_level}{RESET}")
    print(f"{YELLOW}Stargates: {formatted_stargates}{RESET}")

def format_stargates(system_info, systems_data):
    """Formats stargate connections with white color for visited systems."""
    connections = system_info.get('connections', [])

    # Format each stargate connection based on the visited status
    formatted_stargates = []
    for conn in connections:
        connected_system = systems_data.get(conn, {})
        is_visited = connected_system.get('visited', False)  # Check if the connected system is visited

        # Log visited status to game_log.txt only if the system is visited and not yet logged
        if is_visited and conn not in logged_visited_systems:
            game_logger.debug(f"System {conn} visited status: {is_visited}")
            logged_visited_systems.add(conn)  # Add the system to the set to prevent duplicate logging

        # Set color to white if visited, otherwise keep default (YELLOW)
        conn_color = BRIGHT_BLACK if is_visited else WHITE
        formatted_stargates.append(f"{conn_color}{conn}{RESET}")

    return ', '.join(formatted_stargates)

def display_asteroid_fields(system_info):
    """Displays the asteroid fields present in the system."""
    if 'asteroid_fields' in system_info:
        asteroid_fields = ', '.join(field['id'] for field in system_info['asteroid_fields'])
        print(f"{CYAN}Asteroid Fields: {asteroid_fields}{RESET}")

def display_space_station(system_info):
    """Displays the space station present in the system if it exists."""
    if 'space_station' in system_info:
        station = system_info['space_station']
        # Apply bright blue background and bold styling with white foreground
        print(f"\n{BLINK}{BG_BLACK}{BOLD}{BRIGHT_YELLOW}*** STATION: {station['name'].upper()}, {station['type'].upper()}{RESET} *** \n")