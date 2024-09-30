# Turing

A bunch of cells that can be manipulated. [I wrote an interpreter for this in Scratch.](https://scratch.mit.edu/projects/1074402996/)

# Syntax
| Basic Instructions | Description |
| ------------------ | ----------- |
| `>` | Shift the current cell one to the right
| `<` | Shift the current cell one to the left
| `+` | Increment the current cell
| `-` | Decrement the current cell
| `^` | Push the current cell to the stack
| `\|` | Pop from the stack to the current cell
| `,` | Pop from the stack to the current cell and subtract
| `.` | Pop from the stack to the current cell and add
| `*` | Clear the stack
| `!` | Clear the current cell
| `$` | Output the current cell

## `@` Jump
- Runs a comparison against the current cell
- Inputs are given on the stack
- Standalone
    - Inputs required, `[flag, cell location if true, cell location if false]`
    - With the true and false conditions, this is an if-else
    - With only the true condition, this is an if
- As part of a loop
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

## `[...]` Loops
- Setup comparison on stack before loop is run
- The jump instruction doesn't require cell locations since it will jump back to the begininng of the loop
- The comparison is run before the body is executed (like a do while)
- **The ending cell will still be used for the comparison**


# Examples
| Code | Description |
| ---- | ----------- |
| `++++++++++>++^<[$-]` | Print all the numbers from 10 to 1