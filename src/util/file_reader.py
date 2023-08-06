

from typing import Any, Dict

import yaml

from src.util.config import ConfigFiles


# Custom errors
class YAMLFileNotFoundError(Exception):
    """Raised when the configuration file is not found."""
    pass

class YAMLParseError(Exception):
    """Raised when there's an error parsing the configuration file."""
    pass


def read_yaml(file: str) -> Dict[str, Any]:
    """Utility .yaml reader"""
    try:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
        return data
    except FileNotFoundError:
        raise YAMLFileNotFoundError(f"The configuration file {file} was not found.")
    except yaml.YAMLError as e:
        raise YAMLParseError(f"Error parsing the YAML file: {str(e)}")


if __name__ == "__main__":
    yaml_data = read_yaml(file = ConfigFiles.CREDENTIALS)
    print(yaml_data)