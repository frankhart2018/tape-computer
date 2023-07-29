import importlib

from .errors import DataTypeError, MemoryError


class Memory:
    def __init__(self) -> None:
        self.memory = []
        self.iterator = 0

    def __get_class_obj(self, dtype: str) -> any:
        module = importlib.import_module(f"tape_computer.unsigned_types")
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

    def load(self, dtype: str) -> int:
        if self.iterator >= len(self.memory):
            raise MemoryError("Illegal memory access")

        class_obj = self.__get_class_obj(dtype)
        bytes_requested = class_obj.request_bytes()
        obj, size = class_obj.load(
            b"".join(self.memory[self.iterator : self.iterator + bytes_requested])
        )

        # Tape pointer moves one byte at a time, deal with it :P
        for _ in range(size):
            self.iterator += 1
        value = obj.byte

        return value

    def move(self, loc: int) -> None:
        if loc >= len(self.memory):
            raise DataTypeError("Invalid memory location")

        # I could've just assigned the loc to self.iterator
        # but then how'd you get the feel of the tape pointer moving?
        diff = self.iterator - loc
        for _ in range(diff):
            self.iterator -= 1
