import re

from .errors import ParseError
from .memory import Memory
from .utils import get_int_from_str


class Processor:
    def __init__(self, memory: Memory, prog: list[str]) -> None:
        self.memory = memory
        self.prog = prog
        self.prog_iterator = -1

    def execnext(self) -> bool:
        if self.prog_iterator + 1 >= len(self.prog):
            return False

        self.prog_iterator += 1
        instruction = self.prog[self.prog_iterator]

        return self.exec_instruction(instruction)

    def __verify_instruction(self, instruction: str, opcode: str, regex: str):
        if not re.match(regex, instruction):
            raise ParseError(f"Invalid {opcode} instruction: {instruction}")

    def exec_instruction(self, instruction: str) -> bool:
        opcode, args = instruction.split(" ", 1)
        opcode = opcode.upper()

        return_val = True

        if opcode == "STORE":
            store_regex = r"^STORE [-]?[0-9]+:[ui](?:8|16|32|64)"
            self.__verify_instruction(instruction, opcode, store_regex)

            value, dtype = args.split(":")
            self.memory.register(get_int_from_str(value), dtype)
        elif opcode == "SHOW":
            show_regex = r"^SHOW [ui](?:8|16|32|64)"
            self.__verify_instruction(instruction, opcode, show_regex)

            dtype = args
            value = self.memory.load(dtype)
            print(value)
        elif opcode == "MOVE":
            move_regex = r"^MOVE [0-9]+"
            self.__verify_instruction(instruction, opcode, move_regex)

            loc = int(args)
            self.memory.move_ptr(loc)
        else:
            raise ParseError(f"Unknown instruction: {instruction}")

        return return_val
