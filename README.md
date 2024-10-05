# Turing

A bunch of cells that can be manipulated. [I wrote an interpreter for this in Scratch.](https://scratch.mit.edu/projects/1074402996/)

# Syntax
| Basic Instructions | Description |
| ------------------ | ----------- |
| `>` | Shift the current cell one to the right
| `<` | Shift the current cell one to the left
| `+` | Increment the current cell
| `-` | Decrement the current cell
| `^` | Push the current cell to the stack (keeps value in current cell)
| `\|` | Pop from the stack to the current cell
| `,` | Pop from the stack to the current cell and subtract
| `.` | Pop from the stack to the current cell and add
| `%` | Jump to cell specified in stack
| `*` | Clear the stack
| `!` | Clear the current cell
| `$` | Output the current cell

## `@` Jump/Loop Flags
- Runs a comparison against the current cell
- Inputs are given on the stack
- Standalone (Compare then Jump)
    - Inputs required, `[flag, numerical label if true, numerical label if false]`
    - If the "if false" condition is -1, then this becomes an if not an if-else
- As part of a loop (Compare)
    - Inputs required, `[flag]`
    - Run before first iteration of the loop
- Flags

    | Number | Comparison |
    | ------ | ---------- |
    | 1 | Jump if equal zero
    | 2 | Jump if not equal zero
    | 3 | Jump if greater than zero
    | 4 | Jump if greater than or equal zero
    | 5 | Jump if less than zero
    | 6 | Jump if less than or equal zero

## `(n:...)` Labels
- This is a jump point for the jump instruction
- The name of the label is specified as `n`, where `n` is numerical

## `[...]` Loops
- Setup comparison on stack before loop is run
- The comp instruction doesn't require cell locations since it will jump back to the begininng of the loop
- The comparison is run before the body is executed (like a do while)
- **The ending cell will still be used for the comparison**


# Examples
| Code | Description |
| ---- | ----------- |
| `++++++++++>++^<[$-]` | Print all the numbers from 10 to 1