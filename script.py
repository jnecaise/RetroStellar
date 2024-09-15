import json
import random
import string
from multiprocessing import Pool, Manager
from game_logger import game_logger, trim_log_file

# Define star types and their associated hazard levels
STAR_TYPES = {
    "O-type": "Very High",
    "B-type": "High",
    "A-type": "Moderate",
    "F-type": "Mild",
    "G-type": "Low",
    "K-type": "Very Low",
    "M-type": "Minimal"
}

# Define planet types by star type
PLANET_TYPES_BY_STAR = {
    "O-type": ["Barren", "Gas Giant"],
    "B-type": ["Barren", "Gas Giant", "Lava"],
    "A-type": ["Gas Giant", "Ice", "Lava"],
    "F-type": ["Terrestrial", "Oceanic", "Ice"],
    "G-type": ["Terrestrial", "Oceanic", "Toxic"],
    "K-type": ["Terrestrial", "Oceanic", "Barren"],
    "M-type": ["Ice", "Barren"]
}

# Define asteroid field characteristics by star type
ASTEROID_FIELDS_BY_STAR = {
    "O-type": {"density": "Sparse", "types": ["Metallic"]},
    "B-type": {"density": "Sparse", "types": ["Metallic", "Silicate"]},
    "A-type": {"density": "Moderate", "types": ["Carbonaceous", "Silicate"]},
    "F-type": {"density": "Moderate to Dense", "types": ["Carbonaceous", "Silicate", "Metallic"]},
    "G-type": {"density": "Dense", "types": ["Carbonaceous", "Silicate", "Metallic"]},
    "K-type": {"density": "Dense", "types": ["Carbonaceous", "Silicate"]},
    "M-type": {"density": "Moderate to Dense", "types": ["Silicate", "Metallic"]}
}

# Define resource availability based on planet types
RESOURCES_BY_PLANET_TYPE = {
    "Oceanic": ["Ore", "Water", "Food", "Metals", "Fuel"],
    "Barren": ["Ore", "Metals", "Electronics", "Fuel"],
    "Terrestrial": ["Ore", "Water", "Food", "Metals", "Electronics", "Fuel"],
    "Ice": ["Ore", "Water", "Metals"],
    "Gas Giant": ["Ore", "Metals", "Fuel"],
    "Lava": ["Ore", "Metals", "Fuel"],
    "Toxic": ["Ore", "Metals", "Fuel"]
}

# Define resource availability based on asteroid field types
RESOURCES_BY_ASTEROID_TYPE = {
    "Metallic": ["Metals", "Ore"],
    "Silicate": ["Ore", "Electronics"],
    "Carbonaceous": ["Ore", "Fuel"]
}

# Faction placement rules
FACTION_RULES = {
    "Noringian Hive": {"star_types": ["O-type", "B-type", "A-type"], "planet_types": None},
    "Mandate of God": {"star_types": ["A-type", "F-type", "G-type"], "planet_types": ["Terrestrial"]},
    "Shogunate 3072": {"star_types": ["G-type", "K-type", "M-type"], "planet_types": ["Terrestrial"]},
    "United Systems of Man": {"star_types": ["A-type", "F-type", "G-type"], "planet_types": ["Terrestrial"]},
    "People of the River": {"star_types": ["F-type", "G-type", "K-type"], "planet_types": ["Terrestrial"]}
}

def load_settings():
    """Loads settings from settings.json file."""
    try:
        with open('settings.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")
        return {
            "Universe Size": 16
        }

def load_station_names(filename='station_names.json'):
    """Loads station names from a JSON file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get('station_names', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        game_logger.error(f"Error loading station names: {e}")
        return []

def load_station_types(filename='station_types.json'):
    """Loads station types from a JSON file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get('station_types', {})
    except (FileNotFoundError, json.JSONDecodeError) as e:
        game_logger.error(f"Error loading station types: {e}")
        return {}

def generate_random_resources(resources):
    """Generates a dictionary of resources with random values between 1000 to 3000."""
    return {resource: random.randint(1000, 3000) for resource in resources}

def assign_planet_details(planet, star_type):
    """Assigns a type and resources to a planet based on the star type."""
    possible_planet_types = PLANET_TYPES_BY_STAR[star_type]
    planet_type = random.choice(possible_planet_types)
    planet["type"] = planet_type
    resources = RESOURCES_BY_PLANET_TYPE.get(planet_type, [])
    planet["resources"] = generate_random_resources(resources)
    planet["colonizable"] = "Yes" if planet_type in ["Oceanic", "Barren", "Terrestrial", "Ice"] else "No"

def generate_asteroid_fields(system_id, star_type):
    """Generates asteroid fields for a system based on the star type."""
    asteroid_field_info = ASTEROID_FIELDS_BY_STAR.get(star_type)
    if not asteroid_field_info:
        return []
    
    num_asteroid_fields = random.randint(1, 4)  # Random number of fields between 1 and 4
    asteroid_fields = []
    for i in range(num_asteroid_fields):
        field_id = f"{system_id}{string.ascii_uppercase[i]}"
        resource_type = random.choice(asteroid_field_info["types"])
        resources = RESOURCES_BY_ASTEROID_TYPE.get(resource_type, [])
        asteroid_field = {
            "id": field_id,
            "density": asteroid_field_info["density"],
            "resource_type": resource_type,
            "hazard_level": STAR_TYPES[star_type],
            "resources": generate_random_resources(resources)
        }
        asteroid_fields.append(asteroid_field)
    return asteroid_fields

def assign_star_type_and_hazards(system):
    """Assigns a random star type and hazard level to the system."""
    star_type = random.choice(list(STAR_TYPES.keys()))
    system["star_type"] = star_type
    system["hazard_level"] = STAR_TYPES[star_type]
    return star_type

def assign_faction_systems(systems_data, factions):
    """Assigns starting systems to each faction based on their rules."""
    assigned_systems = {}
    for faction, rules in factions.items():
        eligible_systems = [
            sys_id for sys_id, sys_info in systems_data.items()
            if sys_info["star_type"] in rules["star_types"] and 
            (rules["planet_types"] is None or any(
                planet["type"] in rules["planet_types"] for planet in sys_info["planets"]
            )) and sys_info["owned_by"] == "Unoccupied"
        ]

        if eligible_systems:
            selected_system = random.choice(eligible_systems)
            systems_data[selected_system]["owned_by"] = faction
            assigned_systems[faction] = selected_system
        else:
            game_logger.info(f"No eligible systems found for {faction}")
            print(f"No eligible systems found for {faction}")  # Debugging output

    return assigned_systems

def log_assigned_systems(assigned_systems):
    """Logs the assigned systems for factions."""
    if not assigned_systems:
        game_logger.warning("No systems were assigned to any faction.")
        print("No systems were assigned to any faction.")  # Debugging output if needed

def generate_connections_with_min_threshold(system_data, min_connections=2, max_connections=6, cluster_bias=0.3):
    """Generates connections ensuring each system has at least a minimum number of connections."""
    system_ids = list(system_data.keys())
    num_systems = len(system_ids)

    if num_systems > 1000:
        connections = generate_connections_parallel(system_ids, system_data, max_connections, cluster_bias)
    else:
        connections = generate_connections_sequential(system_ids, system_data, max_connections, cluster_bias)

    # Ensure each system meets the minimum connection threshold
    for system_id in system_ids:
        while len(connections[system_id]) < min_connections:
            potential_connections = [
                s for s in system_ids
                if s != system_id and len(connections[s]) < max_connections and s not in connections[system_id]
            ]
            if not potential_connections:
                break
            new_connection = random.choice(potential_connections)
            connections[system_id].add(new_connection)
            connections[new_connection].add(system_id)

    # Apply connections back to the systems data
    for system_id, conn in connections.items():
        system_data[system_id]['connections'] = list(conn)

    ensure_full_navigability(system_data, max_connections)

def generate_connections_sequential(system_ids, system_data, max_connections, cluster_bias):
    """Sequential connection generation for smaller universes."""
    connections = {system_id: set() for system_id in system_ids}

    for system_id in system_ids:
        if len(connections[system_id]) >= max_connections:
            continue

        possible_connections = [
            s for s in system_ids
            if s != system_id and
            len(connections[s]) < max_connections and
            s not in connections[system_id]
        ]

        if not possible_connections:
            continue

        if not connections[system_id]:
            connection = random.choice(possible_connections)
            connections[system_id].add(connection)
            connections[connection].add(system_id)

        additional_connections = random.randint(1, 2)
        weighted_connections = [
            s for s in possible_connections
            if has_similar_resources(system_data[system_id], system_data[s])
        ]

        if random.random() < cluster_bias and weighted_connections:
            new_connections = random.sample(weighted_connections, min(additional_connections, len(weighted_connections)))
        else:
            new_connections = random.sample(possible_connections, min(additional_connections, len(possible_connections)))

        for new_connection in new_connections:
            if len(connections[system_id]) < max_connections and len(connections[new_connection]) < max_connections:
                connections[system_id].add(new_connection)
                connections[new_connection].add(system_id)

    return connections

def generate_connections_parallel(system_ids, system_data, max_connections, cluster_bias):
    """Parallel connection generation for large universes using multiprocessing."""
    with Manager() as manager:
        connections = manager.dict({system_id: set() for system_id in system_ids})

        chunk_size = max(1, len(system_ids) // 10)
        system_chunks = [system_ids[i:i + chunk_size] for i in range(0, len(system_ids), chunk_size)]

        with Pool() as pool:
            results = pool.starmap(process_connections, [(chunk, system_ids, system_data, connections, max_connections, cluster_bias) for chunk in system_chunks])

        for result in results:
            for system_id, conn in result.items():
                connections[system_id].update(conn)

        return dict(connections)

def process_connections(subset, system_ids, system_data, connections, max_connections, cluster_bias):
    """Processes a subset of systems to generate connections."""
    local_connections = {system_id: set(connections[system_id]) for system_id in subset}
    for system_id in subset:
        if len(local_connections[system_id]) >= max_connections:
            continue

        possible_connections = [
            s for s in system_ids
            if s != system_id and
            s in local_connections and
            len(local_connections[s]) < max_connections and
            s not in local_connections[system_id]
        ]

        if not possible_connections:
            continue

        if not local_connections[system_id]:
            connection = random.choice(possible_connections)
            local_connections[system_id].add(connection)
            local_connections[connection].add(system_id)

        additional_connections = random.randint(1, 2)
        weighted_connections = [
            s for s in possible_connections
            if has_similar_resources(system_data[system_id], system_data[s])
        ]

        if random.random() < cluster_bias and weighted_connections:
            new_connections = random.sample(weighted_connections, min(additional_connections, len(weighted_connections)))
        else:
            new_connections = random.sample(possible_connections, min(additional_connections, len(possible_connections)))

        for new_connection in new_connections:
            if len(local_connections[system_id]) < max_connections and len(local_connections[new_connection]) < max_connections:
                local_connections[system_id].add(new_connection)
                local_connections[new_connection].add(system_id)

    return local_connections

def has_similar_resources(system_a, system_b):
    """Checks if two systems have similar resources."""
    resources_a = set(system_a.get("resources", []))
    resources_b = set(system_b.get("resources", []))
    return len(resources_a & resources_b) > 0

def ensure_full_navigability(system_data, max_connections):
    """Ensures all systems are reachable by connecting isolated clusters, respecting the connection limit."""
    system_ids = list(system_data.keys())
    visited = set()

    def dfs_iterative(start_id):
        """Iterative version of DFS to avoid recursion depth issues."""
        stack = [start_id]
        while stack:
            system_id = stack.pop()
            if system_id not in visited:
                visited.add(system_id)
                for connection in system_data[system_id]["connections"]:
                    if connection not in visited:
                        stack.append(connection)

    # Start DFS from the first system
    dfs_iterative(system_ids[0])

    # Handle isolated systems
    isolated_systems = [sys for sys in system_ids if sys not in visited]
    while isolated_systems:
        isolated_system = isolated_systems.pop()
        potential_connectors = [s for s in visited if len(system_data[s]["connections"]) < max_connections]
        if potential_connectors:
            connect_to = random.choice(potential_connectors)
            system_data[isolated_system]["connections"].append(connect_to)
            system_data[connect_to]["connections"].append(isolated_system)
            visited.add(isolated_system)
            dfs_iterative(isolated_system)

def update_system_with_details(system_id, system):
    """Updates a system with star type, planets, and asteroid fields."""
    star_type = assign_star_type_and_hazards(system)
    system['resources'] = []  # Initialize resources as an empty list
    
    for planet in system["planets"]:
        assign_planet_details(planet, star_type)
        system['resources'].extend(list(planet["resources"].keys()))

    system["asteroid_fields"] = generate_asteroid_fields(system_id, star_type)
    for asteroid in system["asteroid_fields"]:
        system['resources'].extend(list(asteroid["resources"].keys()))

    system["resources"] = list(set(system["resources"]))  # Ensure resources are unique
    system["owned_by"] = "Unoccupied"

def assign_additional_faction_systems(systems_data, factions, current_assigned):
    """Assigns starting systems to the remaining factions that do not have a starting system yet."""
    all_factions = set(factions.keys())
    already_assigned_factions = set(current_assigned.keys())
    factions_to_assign = list(all_factions - already_assigned_factions)
    additional_assigned_systems = {}

    for faction in factions_to_assign:
        rules = factions[faction]
        eligible_systems = [
            sys_id for sys_id, sys_info in systems_data.items()
            if sys_info["star_type"] in rules["star_types"] and 
            (rules["planet_types"] is None or any(
                planet["type"] in rules["planet_types"] for planet in sys_info["planets"]
            )) and sys_info["owned_by"] == "Unoccupied"
        ]

        if eligible_systems:
            selected_system = random.choice(eligible_systems)
            systems_data[selected_system]["owned_by"] = faction
            additional_assigned_systems[faction] = selected_system
        else:
            game_logger.warning(f"No eligible systems found for {faction}")
            print(f"No eligible systems found for {faction}")  # Debugging output

    return additional_assigned_systems

def assign_space_stations_to_systems(systems_data):
    """Randomly assigns space stations to systems based on loaded names and types."""
    station_names = load_station_names()
    station_types = load_station_types()
    station_count = len(systems_data) // 25  # Approximately one station per 25 systems
    
    for system_id in random.sample(list(systems_data.keys()), min(station_count, len(station_names))):
        if station_names and station_types:
            station_name = station_names.pop(0)  # Use names sequentially from the list
            station_type = random.choice(list(station_types.keys()))  # Randomly choose a station type
            systems_data[system_id]["space_station"] = {
                "name": station_name,
                "type": station_type,
                "description": station_types[station_type]["description"],
                "services": station_types[station_type]["services"]
            }
            game_logger.info(f"Assigned {station_name} ({station_type}) to system {system_id}.")

def create_systems(universe_size):
    """Creates systems based on the universe size setting."""
    systems_data = {}
    for i in range(1, universe_size + 1):
        system_id = str(i)
        systems_data[system_id] = {
            "description": f"System {system_id} with unique features.",
            "planets": [{"name": f"Planet {letter}"} for letter in string.ascii_uppercase[:random.randint(2, 4)]],
            "connections": [],
            "asteroid_fields": []
        }
        update_system_with_details(system_id, systems_data[system_id])
    
    generate_connections_with_min_threshold(systems_data)  # Use the enhanced connection generation with min threshold
    
    assigned_systems = assign_faction_systems(systems_data, FACTION_RULES)
    additional_assigned_systems = assign_additional_faction_systems(systems_data, FACTION_RULES, assigned_systems)
    all_assigned_systems = {**assigned_systems, **additional_assigned_systems}

    # Assign space stations to the systems
    assign_space_stations_to_systems(systems_data)

    return systems_data, all_assigned_systems

def load_systems_data(filename):
    """Loads the systems data from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

def save_systems_data(filename, systems_data):
    """Saves the updated systems data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(systems_data, file, indent=4)  

def log_owned_systems_from_json(json_file):
    """Reads the systems.json file, extracts owned systems, and logs them."""
    try:
        with open(json_file, 'r') as file:
            systems_data = json.load(file)
        
        owned_systems = {system_id: details for system_id, details in systems_data.items() if details.get('owned_by') and details['owned_by'] != 'Unoccupied'}
        
        if owned_systems:
            game_logger.info("Logging owned systems:")
            for system_id, details in owned_systems.items():
                game_logger.info(f"System ID {system_id} is owned by {details['owned_by']}")
        else:
            game_logger.info("No systems are owned by any faction.")
    
    except Exception as e:
        game_logger.error(f"Error reading or processing {json_file}: {e}")

def main():
    """Main function to update systems.json with new data."""
    game_logger.info("Starting the main function.")
    
    settings = load_settings()
    universe_size = settings.get("Universe Size", 16)  # Default to 16 if not found
    systems_data, assigned_systems = create_systems(universe_size)
    
    save_systems_data('systems.json', systems_data)
    game_logger.info(f"Universe with {universe_size} systems created and updated successfully.")
    
    log_assigned_systems(assigned_systems)  # Log assigned systems

    log_owned_systems_from_json('systems.json')  # Log owned systems from JSON file
    
    for handler in game_logger.handlers:
        handler.flush()

    # Trim the log file to keep it manageable
    trim_log_file('game_log.txt')

if __name__ == "__main__":
    main()
