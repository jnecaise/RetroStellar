import json

def load_character_data():
    """Loads character data from the character_data.json file."""
    with open('character_data.json', 'r') as file:
        return json.load(file)

def save_character_data(data):
    """Saves character data to the character_data.json file."""
    with open('character_data.json', 'w') as file:
        json.dump(data, file, indent=4)

def calculate_used_cargo_space(inventory):
    """Calculates the total used cargo space."""
    return sum(item['cargo_space_amount'] for item in inventory)

def add_item_to_inventory(item_name, cargo_space_amount=1):
    """Adds an item to the ship's inventory if there is enough space."""
    character_data = load_character_data()
    ship = character_data['Ship Type']
    max_cargo = ship.get('max_cargo', 0)
    inventory = character_data.get('inventory', [])
    
    # Calculate the total used cargo space
    used_space = calculate_used_cargo_space(inventory)

    # Check if there is enough space for the new item
    if used_space + cargo_space_amount > max_cargo:
        print("You've run out of cargo space.")
        return False

    # Add the item to the inventory
    inventory.append({"item_name": item_name, "cargo_space_amount": cargo_space_amount})
    character_data['inventory'] = inventory
    save_character_data(character_data)
    print(f"Added {item_name} to your inventory. Current cargo space used: {used_space + cargo_space_amount}/{max_cargo}.")
    return True

def remove_item_from_inventory(item_name):
    """Removes an item from the ship's inventory."""
    character_data = load_character_data()
    inventory = character_data.get('inventory', [])
    
    # Find the item and remove it
    updated_inventory = [item for item in inventory if item['item_name'] != item_name]
    
    # Save the updated inventory
    character_data['inventory'] = updated_inventory
    save_character_data(character_data)
    print(f"Removed {item_name} from your inventory.")
