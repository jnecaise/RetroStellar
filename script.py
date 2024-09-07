# script.py

import json
import random
import string

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
        field_id = f"{system_id}{string.ascii_uppercase[i]}"  # Create a unique ID like "1A", "1B", etc.
        resource_type = random.choice(asteroid_field_info["types"])
        resources = RESOURCES_BY_ASTEROID_TYPE.get(resource_type, [])
        asteroid_field = {
            "id": field_id,
            "density": asteroid_field_info["density"],
            "resource_type": resource_type,
            "hazard_level": STAR_TYPES[star_type],  # Use star type hazard level for asteroid fields
            "resources": generate_random_resources(resources)  # Generate resources for the asteroid field
        }
        asteroid_fields.append(asteroid_field)
    return asteroid_fields

def assign_star_type_and_hazards(system):
    """Assigns a random star type and hazard level to the system."""
    star_type = random.choice(list(STAR_TYPES.keys()))
    system["star_type"] = star_type
    system["hazard_level"] = STAR_TYPES[star_type]
    return star_type

def update_system_with_details(system_id, system):
    """Updates a system with star type, planets, and asteroid fields."""
    star_type = assign_star_type_and_hazards(system)
    for planet in system["planets"]:
        assign_planet_details(planet, star_type)
    system["asteroid_fields"] = generate_asteroid_fields(system_id, star_type)
    system["owned_by"] = "Unoccupied"

def update_systems_data(systems_data):
    """Updates each system with star type, hazard level, planet types, asteroid fields, and ownership."""
    for system_id, system in systems_data.items():
        update_system_with_details(system_id, system)

def load_systems_data(filename):
    """Loads the systems data from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

def save_systems_data(filename, systems_data):
    """Saves the updated systems data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(systems_data, file, indent=4)

def main():
    """Main function to update systems.json with new data."""
    systems_data = load_systems_data('systems.json')
    update_systems_data(systems_data)
    save_systems_data('systems.json', systems_data)
    # print("Created planets...asteroids...stars...")

if __name__ == "__main__":
    main()
