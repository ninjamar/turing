# I adapted the inital version of this code from my scratch project (https://scratch.mit.edu/projects/1074402996/)
class Stack:
    def __init__(self):
        self.s = []

    def push(self, v):
        self.s.insert(0, v)

    def pop(self):
        return self.s.pop(0)

    def clear(self):
        self.s.clear()

    def __str__(self):
        return str(self.s)


class Machine:
    def __init__(self, code, memsize=10000):
        self.code = code

        self.stack = Stack()

        self.output = []
        self.loops = []
        self.labels = {}  # name: code

        self.cells = [0] * memsize

        self.curr_cell = 1

        self.pc = 1

    def replace_curr_cell(self, value):
        self.cells[self.curr_cell - 1] = value

    @property
    def v_curr_cell(self):
        return self.cells[self.curr_cell - 1]  # 0 indexed vs. 1 indexed

    @property
    def curr_instr(self):
        return self.code[self.pc - 1]

    def compare(self, flag, value):
        if flag == 1 and value == 0:
            return True
        elif flag == 2 and value != 0:
            return True
        elif flag == 3 and value > 0:
            return True
        elif flag == 4 and value >= 0:
            return True
        elif flag == 5 and value < 0:
            return True
        elif flag == 6 and value <= 0:
            return True
        return False

    def exec_instr(self, instr):
        if instr == "(":
            self.pc += 1
            label_name = ""
            while self.curr_instr != ":":
                label_name = label_name + self.curr_instr
                self.pc += 1

            label_code = ""
            while self.curr_instr != ")":
                label_code = label_code + self.curr_instr
                self.pc += 1

            self.labels[int(label_name)] = label_code
            self.pc += 1

        elif instr == "[":
            dist = 0
            end = False
            nested = 0
            while not end:
                dist += 1
                # Need shorthand for self.curr_instr
                if self.code[self.pc - 1 + dist] == "[":
                    nested += 1
                elif self.code[self.pc - 1 + dist] == "]" and nested > 0:
                    nested -= 1
                elif self.code[self.pc - 1 + dist] == "]" and nested == 0:
                    end = True

            flag = self.stack.pop()
            if self.compare(flag, self.v_curr_cell):
                self.loops.append(flag)
                self.loops.append(dist)

                self.pc += 1
            else:
                self.pc += dist + 1

        elif instr == "]":
            if self.compare(self.loops[-2], self.v_curr_cell):
                # This is the part I'm confused about - I do +1 in scratch, but why -1 here
                self.pc -= self.loops[-1] - 1
            else:
                del self.loops[-1]
                del self.loops[-1]
                self.pc += 1

        elif instr == "@":
            old_pc = self.pc + 1
            self.pc = 1
            false_cond = self.stack.pop()
            true_cond = self.stack.pop()
            flag = self.stack.pop()

            label_code = ""
            if self.compare(flag, self.v_curr_cell):
                label_code = self.labels[true_cond]
            else:
                # don't do false if cond = -1
                if false_cond != -1:
                    label_code = self.labels[false_cond]

            if label_code != "":
                while self.pc <= len(label_code):
                    # 0 indexed vs 1 indexed TODO: Maybe fix this
                    self.exec_instr(label_code[self.pc - 1])

            self.pc = old_pc

        else:
            if instr == ">":
                self.curr_cell += 1
            elif instr == "<":
                self.curr_cell -= 1
            elif instr == "%":
                self.curr_cell = self.stack.pop()
            elif instr == "+":
                self.replace_curr_cell(self.v_curr_cell + 1)
            elif instr == "-":
                self.replace_curr_cell(self.v_curr_cell - 1)
            elif instr == "^":
                self.stack.push(self.v_curr_cell)
            elif instr == "|":
                self.replace_curr_cell(self.stack.pop())
            elif instr == ",":
                self.replace_curr_cell(self.v_curr_cell - self.stack.pop())
            elif instr == ".":
                self.replace_curr_cell(self.v_curr_cell + self.stack.pop())
            elif instr == "*":
                self.stack.clear()
            elif instr == "!":
                self.replace_curr_cell(0)
            elif instr == "$":
                self.output.append(self.v_curr_cell)
            self.pc += 1  # Normal control flow of PC

    def run(self):
        while self.pc <= len(self.code):
            # print(self.code[self.pc - 1])
            self.exec_instr(self.curr_instr)
