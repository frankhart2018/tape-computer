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
            self.memory.register(get_int_from_str(value, dtype), dtype)
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
        elif opcode == "ADD":
            add_regex = r"^ADD [ui](?:8|16|32|64) [ui](?:8|16|32|64) [ui](?:8|16|32|64)[ ]?[0-9]*"
            self.__verify_instruction(instruction, opcode, add_regex)

            # Remove trailing spaces as 'ADD u8 u8 ' is also valid according to above regex
            instruction = instruction.rstrip()
            arg_split = args.split(" ")

            # If ADD u8 u8 u8 without the index, result will be stored starting
            # from the next tape location and a single byte (expected result) will be stored,
            # If there is a location specified, then the result will be stored there
            dtype1, dtype2, res_dtype = arg_split[:3]
            loc = None
            if len(arg_split) == 4:
                loc = arg_split[3]

            val1 = self.memory.load(dtype1)
            val2 = self.memory.load(dtype2)
            res = val1 + val2
            if loc is not None:
                self.memory.move_ptr(int(loc), force_fill=True)
            self.memory.register(get_int_from_str(res, res_dtype), res_dtype)
        elif opcode == "COPY":
            copy_regex = r"^COPY [ui](?:8|16|32|64) [0-9]+"
            self.__verify_instruction(instruction, opcode, copy_regex)

            dtype, loc = args.split(" ")
            value = self.memory.load(dtype)
            self.memory.move_ptr(int(loc), force_fill=True)
            self.memory.register(value, dtype)
        else:
            raise ParseError(f"Unknown instruction: {instruction}")

        return return_val
