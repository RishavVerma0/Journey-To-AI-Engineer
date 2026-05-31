from functools import wraps
from time import perf_counter

def timer(func):
    """Decorater that measures and prints 
       the execution time of the decorated function.
       """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()

        result = func(*args, **kwargs)

        end = perf_counter()
        print(f"{func.__name__} executed in {end - start: 6f} seconds")

        return result
    return wrapper


@timer
def calculate_squares(n):
    """Function that Calculates the squares of numbers from 0 to n-1."""
    return [i**2 for i in range(n)]


@timer
def calculate_sum(n):

    """Returns the sum of numbers from 1 to n."""

    return sum(range(1, n + 1))

if __name__ == "__main__":

    tot_sum = calculate_sum(100)

    tot_sq = calculate_squares(16)

    print("Result:", tot_sum)

    print("Result:", tot_sq)


