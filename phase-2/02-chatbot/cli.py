import logging

from config import MAX_INPUT_LENGTH

logger = logging.getLogger(__name__)


def get_input() -> str:
    try:
        return input(">").strip()
    except KeyboardInterrupt:
        logger.critical("Keyboard Interrupt terminating program")
        raise KeyboardInterrupt


def validate_input(user_input: str) -> bool:
    if len(user_input) < 2:
        print("Message too short.")
        return False
    if len(user_input) > MAX_INPUT_LENGTH:
        print(f"Message too long ({len(user_input)} chars). {MAX_INPUT_LENGTH} maximum")
        return False
    return True


def formatted_print(output_str: str) -> None:
    print(output_str)


def print_welcome() -> None:
    print("""Welcome! Type your message to start chatting.
Use /help to see available commands.""")


def print_help() -> None:
    print("""
/help - prints this help message
/quit - exits the program
/clear - clears chat history
/save file_name - saves conversation history as a JSON file with the file name specified, don't include file type extension
/load file_name - loads file into conversation history, don't include file type extension""")
