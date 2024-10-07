from turing import Machine


if __name__ == "__main__":
    with open("examples/multiplication.txt") as f:
        code = f.read()
    m = Machine(code)
    m.run()
    print(m.cells[:10])
    print(m.output)
