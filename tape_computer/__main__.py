import argparse

from .processor import Processor
from .memory import Memory


def main():
    parser = argparse.ArgumentParser(description="Tape computer")
    parser.add_argument("file", help="file to run")

    args = parser.parse_args()

    with open(args.file) as f:
        program_lines = f.read().splitlines()

    memory = Memory()
    processor = Processor(memory, program_lines)

    while val := processor.execnext():
        if not val:
            break
