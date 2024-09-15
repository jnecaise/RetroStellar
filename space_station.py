# space_station.py

from ansi_colors import CYAN, RESET, GREEN, YELLOW, BOLD, RED
from game_logger import game_logger

def display_space_station_menu(station_info):
    """Displays the space station menu with available services."""
    station_name = station_info.get('name', 'Unknown Station')
    station_type = station_info.get('type', 'Unknown Type')
    station_description = station_info.get('description', 'No description available.')
    station_services = station_info.get('services', [])

    print(f"\n{CYAN}{BOLD}Welcome to {station_name} ({station_type}){RESET}")
    print(f"{station_description}\n")
    print(f"{YELLOW}Available Services:{RESET}")
    for idx, service in enumerate(station_services, 1):
        print(f"  {idx}. {service}")
    print(f"\nPress the service number to select it, or 'R' to return to the system menu.")

    while True:
        choice = input(f"{BOLD}Your choice: {RESET}").strip().upper()
        if choice == 'R':
            return  # Return to the system menu
        elif choice.isdigit():
            service_idx = int(choice) - 1
            if 0 <= service_idx < len(station_services):
                selected_service = station_services[service_idx]
                handle_station_service(selected_service)
            else:
                print(f"{RED}Invalid service number. Please try again.{RESET}")
        else:
            print(f"{RED}Invalid input. Please enter a service number or 'R' to return.{RESET}")

def handle_station_service(service_name):
    """Handles the selected service at the space station."""
    print(f"\n{GREEN}You have selected the {service_name} service.{RESET}")
    # Implement service-specific functionalities here
    if service_name == 'Market':
        # Call the market menu function
        pass
    elif service_name == 'Missions':
        # Call the missions menu function
        pass
    elif service_name == 'Ship Dock':
        # Call the ship dock menu function
        pass
    else:
        print(f"{YELLOW}Service '{service_name}' is currently under development.{RESET}")
