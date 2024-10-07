import json

def load_character_data():
    """Loads character data from the character_data.json file."""
    with open('character_data.json', 'r') as file:
        return json.load(file)

def save_character_data(data):
    """Saves character data to the character_data.json file."""
    with open('character_data.json', 'w') as file:
        json.dump(data, file, indent=4)

def add_credits(amount):
    """Adds credits to the player's Current Credits."""
    character_data = load_character_data()
    current_credits = character_data.get('Current Credits', 0)
    character_data['Current Credits'] = current_credits + amount
    save_character_data(character_data)
    print(f"Added {amount} credits. Current Credits: {character_data['Current Credits']}")

def subtract_credits(amount):
    """Subtracts credits from the player's Current Credits."""
    character_data = load_character_data()
    current_credits = character_data.get('Current Credits', 0)
    
    if current_credits >= amount:
        character_data['Current Credits'] = current_credits - amount
        save_character_data(character_data)
        print(f"Subtracted {amount} credits. Current Credits: {character_data['Current Credits']}")
    else:
        print("Not enough credits for this transaction.")

