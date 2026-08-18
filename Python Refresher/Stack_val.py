def is_valid(expression):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}

    for char in expression:
        if char in "([{":
            stack.append(char)

        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False

    return not stack


tests = ["{[()]}", "{[(])}", "((()))", "([{}])"]

for test in tests:
    print(test, "->", is_valid(test))