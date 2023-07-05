class qqueue:

    def __init__(self,size):
        self.stack = []
        for i in range(size):
            self.stack.append(0)
        self.pointer = 0
        self.size = size-1

    def push(self,value):
        self.pointer += 1
        if self.pointer > self.size:
            self.pointer = 0
        self.stack[self.pointer] = value

    def get_stack(self):
        stack0 = self.stack[:self.pointer+1]
        stack1 = self.stack[self.pointer+1:]
        return stack1+stack0

