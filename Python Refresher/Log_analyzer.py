from collections import defaultdict


def analyze_log(filename):
    status_count = defaultdict(int)
    ip_count = defaultdict(int)

    try:
        with open(filename, "r") as file:

            for line in file:
                parts = line.strip().split()

                if len(parts) != 3:
                    continue

                ip, endpoint, status = parts

                ip_count[ip] += 1
                status_count[status] += 1

        print("\nStatus Code Summary")
        print("-------------------")

        for status, count in sorted(status_count.items()):
            print(f"{status}: {count}")

        print("\nTop IP Addresses")
        print("----------------")

        top_ips = sorted(
            ip_count.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for ip, count in top_ips:
            print(f"{ip}: {count}")

    except FileNotFoundError:
        print("Log file not found.")


def main():
    filename = input("Enter log filename: ")
    analyze_log(filename)


if __name__ == "__main__":
    main()