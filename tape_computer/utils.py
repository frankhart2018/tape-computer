from .errors import DataTypeError


def is_numeric(value: str) -> bool:
    return all(x.isdigit() for x in value)


def _range_check(value: int, low: int, max_bits: int, dtype: str) -> None:
    if value < low or value > (1 << max_bits) - 1:
        raise DataTypeError(f"Invalid {dtype} value: {value}")
