# Tape Computer

A fun project with a simple opcode processor and a tape memory.

## Usage

1. Write a tape program into any file, let's call it `program.tape`:

```
STORE 12:u8
STORE 200:u8
MOVE 0
SHOW u8
SHOW u8
MOVE 1
STORE 34:u8
MOVE 1
SHOW u8
STORE 257:u16
MOVE 2
SHOW u16
STORE 25:u32
MOVE 4
SHOW u32
STORE 65536:u64
MOVE 8
SHOW u64
```

2. Run it:

```bash
user@programmer~:$ python . program.tape
```