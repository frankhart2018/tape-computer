import argparse

from .processor import Processor
from .memory import Memory
from .dumper import Dumper


def main():
    parser = argparse.ArgumentParser(description="Tape computer")
    parser.add_argument("file", help="file to run")
    parser.add_argument(
        "--dump",
        action="store_true",
        default=False,
        help="Dump memory and instruction for debugging",
    )

    args = parser.parse_args()

    with open(args.file) as f:
        program_lines = f.read().splitlines()

    dumper = None
    if args.dump:
        dumper = Dumper()

    memory = Memory(dumper)
    processor = Processor(memory, program_lines, dumper)

    while val := processor.execnext():
        if not val:
            break

        dumper is not None and dumper.commit()

    if args.dump:
        file_name = ".".join(args.file.split(".")[:-1]) + "-dump.json"
        dumper.dump(file_name)
