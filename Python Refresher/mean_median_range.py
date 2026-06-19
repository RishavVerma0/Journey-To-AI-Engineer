def calculate_stats(nums):

    #printing the mean of the above array
    mean = sum(nums) / len(nums)
    print("Mean of nums is : ", mean)

    #printing the median of the above array
    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    if n % 2 == 0:
        median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else: 
        median = sorted_nums[n//2]
    print("Median of nums is : ", median)

    #printing the range of the nums 
    range = max(nums) - min(nums)

    print("Range of nums is : " , range)


def main():
    calculate_stats([23, 87, 42, 12, 65, 91, 5, 54, 78, 33])
main()
