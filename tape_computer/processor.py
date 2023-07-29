import re

from .errors import ParseError
from .memory import Memory


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

    def exec_instruction(self, instruction: str) -> bool:
        opcode, args = instruction.split(" ", 1)
        opcode = opcode.upper()

        return_val = True

        if opcode == "STORE":
            store_regex = r"^STORE [-]?[0-9]+:[ui](?:8|16|32|64)"
            if not re.match(store_regex, instruction):
                raise ParseError(f"Invalid STORE instruction: {instruction}")

            value, dtype = args.split(":")
            self.memory.register(int(value), dtype)
        elif opcode == "SHOW":
            show_regex = r"^SHOW [ui](?:8|16|32|64)"
            if not re.match(show_regex, instruction):
                raise ParseError(f"Invalid SHOW instruction: {instruction}")

            dtype = args
            value = self.memory.load(dtype)
            print(value)
        elif opcode == "MOVE":
            move_regex = r"^MOVE [0-9]+"
            if not re.match(move_regex, instruction):
                raise ParseError(f"Invalid MOVE instruction: {instruction}")

            loc = int(args)
            self.memory.move(loc)

        return return_val
