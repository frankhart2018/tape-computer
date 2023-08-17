import importlib
from typing import Optional

from .errors import DataTypeError, MemoryError
from .dumper import Dumper


class Memory:
    def __init__(self, dumper: Optional[Dumper] = None) -> None:
        self.memory = []
        self.iterator = 0
        self.dumper = dumper

    def __get_class_obj(self, dtype: str) -> any:
        if dtype.startswith("u"):
            module_name = "unsigned_types"
        elif dtype.startswith("i"):
            module_name = "signed_types"

        module = importlib.import_module(f"tape_computer.{module_name}")
        class_obj = getattr(module, dtype.upper())

        return class_obj

    def register(self, value: int, dtype: str) -> None:
        class_obj = self.__get_class_obj(dtype)(value)
        bytes_val = class_obj.to_be_bytes()

        for byte_val in bytes_val:
            self.iterator += 1
            byte_val = bytes([byte_val])
            if self.iterator > len(self.memory):
                self.memory.append(byte_val)
            else:
                self.memory[self.iterator - 1] = byte_val

        self.dumper is not None and self.dumper.register_memory(self.memory)
        self.dumper is not None and self.dumper.register_pointer(self.iterator)

    def load(self, dtype: str) -> int:
        if self.iterator >= len(self.memory):
            raise MemoryError("Illegal memory access")

        class_obj = self.__get_class_obj(dtype)
        bytes_requested = class_obj.request_bytes()
        obj = class_obj.load(
            b"".join(self.memory[self.iterator : self.iterator + bytes_requested])
        )

        # Tape pointer moves one byte at a time, deal with it :P
        for _ in range(bytes_requested):
            self.iterator += 1
        value = obj.byte

        self.dumper is not None and self.dumper.register_pointer(self.iterator)

        return value

    def move_ptr(self, loc: int, force_fill: bool = False) -> None:
        if loc >= len(self.memory) and not force_fill:
            raise DataTypeError("Invalid memory location")
        elif loc >= len(self.memory) and force_fill:
            self.memory.extend([bytes([0]) for _ in range(loc - len(self.memory) + 1)])

        # I could've just assigned the loc to self.iterator
        # but then how'd you get the feel of the tape pointer moving?
        diff = self.iterator - loc if self.iterator > loc else loc - self.iterator
        sign = 1 if self.iterator > loc else -1
        for _ in range(diff):
            self.iterator -= 1 * sign

        self.dumper is not None and self.dumper.register_pointer(self.iterator)
