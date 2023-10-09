class Stack:
    def __init__(self):
        self.stack = []

    def add(self, dataval):
        # Use list append method to add element
        if dataval not in self.stack:
            self.stack.append(dataval)
            return True
        else:
            return False

    # Use peek to look at the top of the stack
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            return None

    def is_empty(self):
        return len(self.stack) == 0

AStack = Stack()
AStack.add("Mon")
AStack.add("Tue")
print(AStack.peek())  # Should print "Tue"
AStack.add("Wed")
AStack.add("Thu")
print(AStack.peek())  # Should print "Thu"
