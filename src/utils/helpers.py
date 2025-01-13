from typing import Dict


def camel_to_snake(name: str) -> str:
    """
    Convert a CamelCase string to snake_case.

    Args:
        name (str): CamelCase string.

    Returns:
        str: snake_case string.
    """
    import re
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def merge_dicts(base: Dict, update: Dict) -> Dict:
    """
    Merge two dictionaries, updating the base dictionary with the new data.

    Args:
        base (Dict): Base dictionary.
        update (Dict): Dictionary with updates.

    Returns:
        Dict: Merged dictionary.
    """
    merged = base.copy()
    merged.update(update)
    return merged