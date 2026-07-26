def second_largest(nums):
    if len(nums) < 2:
        return None

    first = second = float("-inf")

    for num in nums:
        if num > first:
            second = first
            first = num
        elif first > num > second:
            second = num

    return second if second != float("-inf") else None


def main():
    nums = list(map(int, input("Enter numbers separated by spaces: ").split()))
    result = second_largest(nums)

    if result is None:
        print("Second largest element not found.")
    else:
        print("Second largest:", result)


if __name__ == "__main__":
    main()