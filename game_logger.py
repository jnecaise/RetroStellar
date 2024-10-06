# game_logger.py

import logging

def setup_logger(name="game_logger", log_file='game_log.txt', level=logging.DEBUG):
    """Sets up the logger with the specified name, log file, and level."""
    # Create a custom logger
    logger = logging.getLogger(name)
    
    # Check if the logger already has handlers (to avoid adding multiple handlers)
    if not logger.handlers:
        # Set the level of the logger
        logger.setLevel(level)

        # Create handlers
        file_handler = logging.FileHandler(log_file, mode='a')  # 'a' mode appends each run
        file_handler.setLevel(level)

        # Create formatters and add it to handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)

    return logger

def trim_log_file(log_file, max_lines=1000):
    """Trims the log file to keep only the last 'max_lines' lines."""
    try:
        with open(log_file, 'r') as file:
            lines = file.readlines()
        
        if len(lines) > max_lines:
            # Keep only the last 'max_lines' lines
            lines = lines[-max_lines:]
            with open(log_file, 'w') as file:
                file.writelines(lines)
                
    except Exception as e:
        print(f"Error trimming log file: {e}")

# Initialize the logger when this module is imported
game_logger = setup_logger()

# Test log entry to verify setup
game_logger.info("==============================================")
game_logger.info("Logger initialized. Ready to capture game data.")

# Example function to log character menu display
def log_character_menu(character_data):
    """Logs the details of the character menu for debugging purposes."""
    game_logger.info("Displaying character menu for character: %s", character_data["Character Name"])
    game_logger.info("Faction: %s", character_data["Faction"])
    game_logger.info("Ship Name: %s", character_data["Ship Name"])
    game_logger.info("Ship details: %s", character_data["Ship Type"])
    game_logger.info("Starting Credits: %s", character_data["Starting Credits"])

# Example function to log if old fields like "System Scanner" are displayed
def log_deprecated_fields_check():
    """Logs if deprecated fields like 'System Scanner' are still being used."""
    game_logger.info("Checking if deprecated fields (e.g., System Scanner, Planet Scanner) are being displayed.")
