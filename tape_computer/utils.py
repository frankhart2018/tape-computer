from .errors import DataTypeError


def is_numeric(value: str) -> bool:
    return all(x.isdigit() for x in value)


def range_check(value: int, min_bits: int, max_bits: int, dtype: str) -> None:
    low_expr = (-1 * (1 << min_bits)) if min_bits > 1 else min_bits

    if value < low_expr or value > (1 << max_bits) - 1:
        raise DataTypeError(f"Invalid {dtype} value: {value}")


def get_int_from_str(value: str, dtype: str) -> int:
    is_str = isinstance(value, str)
    if is_str and not is_numeric(value):
        raise DataTypeError(f"Invalid value for {dtype}: {value}")

    value = int(value) if is_str else value
    return value
