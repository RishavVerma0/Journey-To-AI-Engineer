def generate_parentheses(n):

    result = []

    def backtrack(current, opened, closed):

        # Valid complete combination
        if len(current) == 2 * n:
            result.append(current)
            return

        # Add '(' if we still have some available
        if opened < n:
            backtrack(
                current + "(",
                opened + 1,
                closed
            )

        # Add ')' only when it won't make the sequence invalid
        if closed < opened:
            backtrack(
                current + ")",
                opened,
                closed + 1
            )

    backtrack("", 0, 0)

    return result


n = 3

print(generate_parentheses(n))