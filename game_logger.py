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
        file_handler = logging.FileHandler(log_file, mode='w')  # 'w' mode clears the file each run
        file_handler.setLevel(level)

        # Create formatters and add it to handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)

    return logger

# Initialize the logger when this module is imported
game_logger = setup_logger()
