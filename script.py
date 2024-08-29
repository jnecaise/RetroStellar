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

def assign_star_type_hazard_planets_and_asteroids(system_data):
    for system_id, system in system_data.items():
        # Randomly select a star type
        star_type = random.choice(list(STAR_TYPES.keys()))

        # Assign star type and corresponding hazard level
        system["star_type"] = star_type
        system["hazard_level"] = STAR_TYPES[star_type]

        # Determine possible planet types based on star type
        possible_planet_types = PLANET_TYPES_BY_STAR[star_type]

        # Assign a type to each planet in the system
        for planet in system["planets"]:
            planet["type"] = random.choice(possible_planet_types)

        # Generate asteroid fields for the system
        asteroid_field_info = ASTEROID_FIELDS_BY_STAR.get(star_type)
        if asteroid_field_info:
            num_asteroid_fields = random.randint(1, 4)  # Random number of fields between 1 and 4
            asteroid_fields = []
            for i in range(num_asteroid_fields):
                field_id = f"{system_id}{string.ascii_uppercase[i]}"  # Create a unique ID like "1A", "1B", etc.
                asteroid_field = {
                    "id": field_id,
                    "density": asteroid_field_info["density"],
                    "resource_type": random.choice(asteroid_field_info["types"]),
                    "hazard_level": STAR_TYPES[star_type]  # Use star type hazard level for asteroid fields
                }
                asteroid_fields.append(asteroid_field)

            # Consolidate all asteroid fields under one key
            system["asteroid_fields"] = asteroid_fields

# Load existing systems data from systems.json
with open('systems.json', 'r') as file:
    systems_data = json.load(file)

# Update each system with star type, hazard level, planet types, and asteroid fields
assign_star_type_hazard_planets_and_asteroids(systems_data)

# Save the updated data back to systems.json
with open('systems.json', 'w') as file:
    json.dump(systems_data, file, indent=4)

print("Updated systems.json with star types, hazard levels, planet types, and consolidated asteroid fields.")
