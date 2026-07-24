def is_isomorphic(s, t):
    if len(s) != len(t):
        return False

    map_st = {}
    map_ts = {}

    for c1, c2 in zip(s, t):
        if c1 in map_st and map_st[c1] != c2:
            return False

        if c2 in map_ts and map_ts[c2] != c1:
            return False

        map_st[c1] = c2
        map_ts[c2] = c1

    return True


def main():
    s = input("Enter first string: ")
    t = input("Enter second string: ")

    print("Isomorphic:", is_isomorphic(s, t))


if __name__ == "__main__":
    main()