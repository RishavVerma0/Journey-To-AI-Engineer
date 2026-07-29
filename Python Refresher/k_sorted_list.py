import heapq


class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next


def merge_k_lists(lists):
    heap = []

    for index, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.value, index, node))

    dummy = ListNode()
    current = dummy

    while heap:
        value, index, node = heapq.heappop(heap)

        current.next = node
        current = current.next

        if node.next:
            heapq.heappush(heap, (node.next.value, index, node.next))

    return dummy.next


def build_list(values):
    dummy = ListNode()
    current = dummy

    for value in values:
        current.next = ListNode(value)
        current = current.next

    return dummy.next


def print_list(head):
    while head:
        print(head.value, end=" ")
        head = head.next
    print()


def main():
    list1 = build_list([1, 4, 5])
    list2 = build_list([1, 3, 4])
    list3 = build_list([2, 6])

    merged = merge_k_lists([list1, list2, list3])

    print("Merged List:")
    print_list(merged)


if __name__ == "__main__":
    main()