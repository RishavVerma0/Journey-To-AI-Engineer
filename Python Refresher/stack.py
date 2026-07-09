class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        "Insertion at the top"
        self._items.append(item)

    def pop(self):
        "Deletion from the top"
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()
    
    def peek(self):
        "Looking for the top index"
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items[-1]
    
    def is_empty(self):
        """Return True if the stack is empty, otherwise False."""
        return len(self._items) == 0

    def size(self):

        """Return the number of items in the stack."""

        return len(self._items)

    
stack = Stack()

stack.push(10)

stack.push(20)

stack.push(30)

print(stack.peek())   # 30

print(stack.pop())    # 30

print(stack.pop())    # 20

print(stack.size())   # 1

print(stack.is_empty()) 