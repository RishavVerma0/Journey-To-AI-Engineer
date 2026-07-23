class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {
            ')': '(',
            '}': '{',
            ']': '['
        }

        for char in s:
            if char in mapping:
                if not stack or stack.pop() != mapping[char]:
                    return False
            else:
                stack.append(char)

        return len(stack) == 0


def main():
    s = input("Enter parentheses string: ")

    solution = Solution()

    if solution.isValid(s):
        print("Valid")
    else:
        print("Invalid")


if __name__ == "__main__":
    main()