

from typing import Any, Callable, Dict

import yaml

YAMLData = Callable[[str], Dict[str, Any]]

# Custom errors
class YAMLFileNotFoundError(Exception):
    """Raised when the configuration file is not found."""
    pass

class YAMLParseError(Exception):
    """Raised when there's an error parsing the configuration file."""
    pass


def read_yaml(file: str) -> YAMLData:
    """Utility .yaml reader"""
    try:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
        return data
    except FileNotFoundError:
        raise YAMLFileNotFoundError(f"The configuration file {file} was not found.")
    except yaml.YAMLError as e:
        raise YAMLParseError(f"Error parsing the YAML file: {str(e)}")


# Usage example
if __name__ == "__main__":
    from .config import ConfigFiles
    yaml_data = read_yaml(file = ConfigFiles.CREDENTIALS)
    print(yaml_data)