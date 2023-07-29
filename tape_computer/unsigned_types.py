from typing import Union

from .errors import DataTypeError
from .utils import is_numeric, _range_check


def _get_int_from_str(value: str, dtype: str) -> int:
    is_str = isinstance(value, str)
    if is_str and not is_numeric(value):
        raise DataTypeError(f"Invalid value for {dtype}: {value}")

    value = int(value) if is_str else value
    return value


class UnsignedType:
    def __init__(self, value: str, max_bits: int, dtype: str) -> None:
        value = _get_int_from_str(value, dtype)
        _range_check(value, 0, max_bits, dtype)
        self.value = value
        self.max_bits = max_bits

    def to_be_bytes(self) -> bytes:
        return self.value.to_bytes(self.max_bits // 8, "big")

    @property
    def byte(self) -> int:
        return self.value


class U8(UnsignedType):
    def __init__(self, value: Union[str, int]):
        super().__init__(value, 8, "u8")

    @classmethod
    def load(cls, value: bytes) -> tuple["U8", int]:
        return (cls(int.from_bytes(value, "big")), 1)

    @classmethod
    def request_bytes(cls) -> int:
        return 1


class U16(UnsignedType):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__(value, 16, "u16")

    @classmethod
    def load(cls, value: bytes) -> tuple["U16", int]:
        return (cls(int.from_bytes(value, "big")), 2)

    @classmethod
    def request_bytes(cls) -> int:
        return 2


class U32(UnsignedType):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__(value, 32, "u32")

    @classmethod
    def load(cls, value: bytes) -> tuple["U32", int]:
        return (cls(int.from_bytes(value, "big")), 4)

    @classmethod
    def request_bytes(cls) -> int:
        return 4


class U64(UnsignedType):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__(value, 64, "u64")

    @classmethod
    def load(cls, value: bytes) -> tuple["U64", int]:
        return (cls(int.from_bytes(value, "big")), 8)

    @classmethod
    def request_bytes(cls) -> int:
        return 8
