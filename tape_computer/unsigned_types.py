from typing import Union

from .utils import range_check, get_int_from_str

class UnsignedType:
    def __init__(self, value: str, max_bits: int, dtype: str) -> None:
        value = get_int_from_str(value, dtype)
        range_check(value, 0, max_bits, dtype)
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
    def load(cls, value: bytes) -> "U8":
        return cls(int.from_bytes(value, "big"))

    @classmethod
    def request_bytes(cls) -> int:
        return 1


class U16(UnsignedType):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__(value, 16, "u16")

    @classmethod
    def load(cls, value: bytes) -> "U16":
        return cls(int.from_bytes(value, "big"))

    @classmethod
    def request_bytes(cls) -> int:
        return 2


class U32(UnsignedType):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__(value, 32, "u32")

    @classmethod
    def load(cls, value: bytes) -> "U32":
        return cls(int.from_bytes(value, "big"))

    @classmethod
    def request_bytes(cls) -> int:
        return 4


class U64(UnsignedType):
    def __init__(self, value: Union[str, int]) -> None:
        super().__init__(value, 64, "u64")

    @classmethod
    def load(cls, value: bytes) -> "U64":
        return cls(int.from_bytes(value, "big"))

    @classmethod
    def request_bytes(cls) -> int:
        return 8
