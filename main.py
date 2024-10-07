from turing import Machine, Compiler


def a():
    with open("examples/multiplication.txt") as f:
        code = f.read()
    m = Machine(code, debug=True)
    m.run()
    print(m.cells[:10])
    print(m.output)


class Program(Compiler):
    def _a(self):
        self.right()
        self.inc()
        self.left()
        self.set(100)

    def _b(self):
        def t(ctx):
            ctx.set(1290)
            ctx.print_()

        self.right()
        self.add(10)
        self.left()

        self.inc()
        self.if_(2, t)
    
    def _c(self):
        def t(ctx):
            ctx.set(100)
            ctx.print_()

        def f(ctx):
            ctx.set(50)
            ctx.print_()

        self.right()
        self.add(10)
        self.left()

        self.inc()
        self.if_else(2, t, f)

def b():
    p = Program()
    p._c()

    m = Machine(p._code)
    print(p._code)
    m.run()
    print(m.cells[:10])
    print(m.output)


if __name__ == "__main__":
    b()
