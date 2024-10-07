from .turing import Machine


class Compiler:
    def __init__(self):
        self._code = ""
        self._labels_idx = 0

    def _emit(self, x):
        self._code += x

    # Basic Instructions
    def right(self):
        self._emit(">")

    def left(self):
        self._emit("<")

    def inc(self):
        self._emit("+")

    def dec(self):
        self._emit("-")

    def push(self):
        self._emit("^")

    def pop(self):
        self._emit("|")

    def pop_s(self):
        self._emit(",")

    def pop_a(self):
        self._emit(".")

    # Jump to cell has arguments so it isn't a basic instruction
    def clear_s(self):
        self._emit("*")

    def clear_c(self):
        self._emit("!")

    def print_(self):
        self._emit("$")

    def push_loc(self):
        self._emit("#")

    # WARNING: Consumes current cell and jumps to cell[index]
    def jump_c(self, index):
        self.set(index)  # self.set is more optimized than self.add
        self.push()

        self._emit("%")

    def add(self, i):
        if i > 0:
            for j in range(i):
                self.inc()
        else:
            for j in range(abs(i)):
                self.dec()

    def sub(self, i):
        if i > 0:
            for j in range(i):
                self.dec()
        else:
            for j in range(abs(i)):
                self.inc()

    # Basic multiplication generating sub-optimal code
    def _simple_mul(self, a, b):
        for i in range(a):
            self.add(b)

    # Find optimal code
    def mul(self, a, b):
        # Multiply a and b - set helps to find the optimal ab+x
        self.set(a * b)

    # Prefixed with underscore because it doesn't emit code, and isn't part of Machine
    def _find_abx(self, target):
        # Find optimal ABX where ab + x = target
        # and a + |b| + |x| + 10 < |target|
        # The 10 signifies that overhead of characters for multiplication

        min_sum = abs(target)
        best = None

        for a in range(1, abs(target) + 1):  # All positive a values
            # Negative to positive B valueA
            for b in range(-abs(target) // a, abs(target) // a + 1):
                product = a * b
                x = target - product  # diff = x
                curr_sum = a + abs(b) + abs(x) + 10  # a + |b| + |x| + 10
                # Check if this sum is smaller
                if curr_sum < min_sum:
                    min_sum = curr_sum
                    best = (a, b, x)
        return best

    # set the current cell to a value
    def set(self, target):
        # Wipe the current cell

        self.clear_c()
        abx = self._find_abx(target)
        if abx is None:
            self.add(target)
        else:
            a, b, x = abx

            self.right()
            self.push()  # save
            self.clear_c()

            self.add(a)  # A

            # Internally, try to use definitions defined as class methods
            def inner(ctx):
                # Go to result cell
                ctx.left()
                # Add can handle negatives
                ctx.add(b)
                ctx.right()
                # Decrement A
                ctx.dec()

            self.loop(2, inner)
            self.add(x)  # a[b] + x

            self.pop()  # load
            self.left()

    def _code_from_fn(self, fn):
        c = Compiler()
        fn(c)
        return c._code

    def loop(self, flag, fn):
        self.right()
        self.push()  # save whatever was on the cell before flag
        self.set(flag)

        self.push()
        self.clear_c()

        self.left()
        self._emit("[" + self._code_from_fn(fn) + "]")

        # Load
        self.right()
        # Opening bracket consumes flag from stack
        self.pop()  # load
        self.left()

    def if_(self, flag, label_true_fn):
        self.if_else(flag, label_true_fn, None)

    def if_else(self, flag, label_true_fn, label_false_fn):
        # Flag is constructed 1 cell to the right
        self.right()

        # Push current cell to stack (save)
        self.push()
        # Construct flag
        self.clear_c()
        for i in range(flag):
            self.inc()
        self.push()

        # True Condition
        self.set(self._labels_idx)
        self.push()
        if label_false_fn is None:
            # False Condition (None)
            self.set(-1)
            self.push()
            # Go back to comparison cell
            self.left()

            self._emit(f"({self._labels_idx}:{self._code_from_fn(label_true_fn)})@")
            self._labels_idx += 1
        else:
            self._labels_idx += 1
            self.set(self._labels_idx)
            self.push()
            self.left()
            self._emit(
                f"({self._labels_idx-1}:{self._code_from_fn(label_true_fn)})({self._labels_idx}:{self._code_from_fn(label_false_fn)})@"
            )

        self.right()
        # Pop cell from stack (save)
        self.pop()
        self.left()