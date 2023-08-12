import json
from typing import Any, Dict


# Custom errors
class JSONFileNotFoundError(Exception):
    """Raised when the configuration file is not found."""
    pass

class JSONParseError(Exception):
    """Raised when there's an error parsing the configuration file."""
    pass


def read_json(file: str) -> Dict[str, Any]:
    """Utility .json reader"""
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise JSONFileNotFoundError(f"The configuration file {file} was not found.")
    except json.JSONDecodeError as e:
        raise JSONParseError(f"Error parsing the JSON file: {str(e)}")


# # Usage example
# if __name__ == "__main__":
#     from ..app.config import ConfigFiles
#     json_data = read_json(file=ConfigFiles.SF2DB_MAPPINGS)
#     print(json_data)
