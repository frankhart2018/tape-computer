# Tape Computer

A fun project with a näive opcode processor and a tape memory.

## Usage

1. Install the package:

```bash
user@programmer~:$ pip install git+https://github.com/frankhart2018/tape-computer.git
```

2. Write a tape program into any file, let's call it `program.tape`:

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

3. Run it:

```bash
user@programmer~:$ tapec program.tape
```

## Opcode Reference

- `STORE <value>:<type>`: Stores a value of a given type into the tape memory (supported types: `u8`, `u16`, `u32`, `u64`, `i8`, `i16`, `i32`, `i64`). The value is stored at the current tape position.

- `MOVE <index>`: Moves the tape position to the given index (0-based).

- `SHOW <type>`: Shows the value at the current tape position of the given type (the type is used to determine the number of bytes to read).

- `ADD <operand_1_type> <operand_2_type> <result_type> [<index>]`: Adds the values at the current tape position of the given types and stores the result at the current tape position of the given result type if index is not given. If index is given, the result is stored at the given index.

## License

This project is licensed under the [MIT License](https://github.com/frankhart2018/tape-computer/blob/master/LICENSE.md)