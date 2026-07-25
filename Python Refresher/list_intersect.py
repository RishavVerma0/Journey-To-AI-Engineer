def find_intersection(list1, list2):
    return list(set(list1) & set(list2))


def main():
    list1 = list(map(int, input("Enter first list: ").split()))
    list2 = list(map(int, input("Enter second list: ").split()))

    result = find_intersection(list1, list2)

    if result:
        print("Common elements:", sorted(result))
    else:
        print("No common elements found.")


if __name__ == "__main__":
    main()