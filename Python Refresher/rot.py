def rotate_list(nums, k):
    if len(nums) == 0:
        return nums

    k = k % len(nums)
    return nums[-k:] + nums[:-k]


def main():
    numbers = list(map(int, input("Enter numbers separated by space: ").split()))
    k = int(input("Enter rotation value: "))

    result = rotate_list(numbers, k)

    print("Rotated List:", result)


if __name__ == "__main__":
    main()