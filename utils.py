def is_numeric(value: str) -> bool:
    return all(x.isdigit() for x in value)
