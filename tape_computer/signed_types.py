from typing import Union

from .utils import get_int_from_str, range_check


class SignedType:
    def __init__(self, value: str, min_bits: int,  max_bits: int, dtype: str) -> None:
        value = get_int_from_str(value, dtype)
        range_check(value, min_bits, max_bits, dtype)
        self.value = value
        self.min_bits = min_bits
        self.max_bits = max_bits

    def to_be_bytes(self) -> bytes:
        return self.value.to_bytes(self.max_bits // 8, "big", signed=True)

    @property
    def byte(self) -> int:
        return self.value


class I8(SignedType):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__(value, 8, 8, "i8")

    @classmethod
    def load(cls, value: bytes) -> "I8":
        return cls(int.from_bytes(value, "big", signed=True))

    @classmethod
    def request_bytes(cls) -> int:
        return 1


class I16(SignedType):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__(value, 16, 16, "i16")

    @classmethod
    def load(cls, value: bytes) -> "I16":
        return cls(int.from_bytes(value, "big", signed=True))

    @classmethod
    def request_bytes(cls) -> int:
        return 2


class I32(SignedType):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__(value, 32, 32, "i32")

    @classmethod
    def load(cls, value: bytes) -> "I32":
        return cls(int.from_bytes(value, "big", signed=True))

    @classmethod
    def request_bytes(cls) -> int:
        return 4


class I64(SignedType):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__(value, 64, 64, "i64")

    @classmethod
    def load(cls, value: bytes) -> "I64":
        return cls(int.from_bytes(value, "big", signed=True))

    @classmethod
    def request_bytes(cls) -> int:
        return 8