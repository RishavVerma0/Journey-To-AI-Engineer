from typing import Optional

def calculate_average(numbers: list[float]) -> Optional[float]:
    """
    Returns the average of a list of numbers.
    Returns None if the list is empty.
    """

    if not numbers:
        return None
    return sum(numbers) / len(numbers)

def format_result(name: str, average: float) -> str:
    """
    Formats the Output message
    """
    return f"{name}'s average score is {average:.2f}"


if __name__ == "__main__":

    scores : list[float] = [99.9, 90.0, 94.5, 34.5]

    avg = calculate_average(scores)

    if avg is not None:
        message = format_result("Alice", avg)

        print(message)