from dataclasses import dataclass
import json


@dataclass
class DumpData:
    memory: list[int]
    instruction: str
    pointer: int

    def to_json(self) -> dict:
        return {
            "memory": [str(val) for val in self.memory],
            "instruction": self.instruction,
            "pointer": self.pointer,
        }


class Dumper:
    def __init__(self) -> None:
        self.__value = {}
        self.__current_dump = DumpData([], "", 0)

    def register_memory(self, memory: list[int]) -> None:
        self.__current_dump.memory = memory

    def register_instruction(self, instruction: str) -> None:
        self.__current_dump.instruction = instruction

    def register_pointer(self, pointer: int) -> None:
        self.__current_dump.pointer = pointer

    def commit(self) -> None:
        self.__value[len(self.__value)] = self.__current_dump.to_json()
        self.__current_dump = DumpData([], "", 0)

    def dump(self, file_path: str) -> None:
        with open(file_path, "w") as f:
            json.dump(self.__value, f, indent=4)
