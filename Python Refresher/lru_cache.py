class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

        self.left = Node()   # LRU
        self.right = Node()  # MRU

        self.left.next = self.right # type: ignore
        self.right.prev = self.left # type: ignore

    def remove(self, node):
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node

    def insert(self, node):
        prev_node = self.right.prev
        next_node = self.right

        prev_node.next = node # type: ignore
        node.prev = prev_node
        node.next = next_node
        next_node.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self.remove(node)
        self.insert(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.remove(self.cache[key])

        node = Node(key, value)
        self.cache[key] = node
        self.insert(node)

        if len(self.cache) > self.capacity:
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key] # type: ignore


def main():
    cache = LRUCache(2)

    cache.put(1, 10)
    cache.put(2, 20)

    print(cache.get(1))
    cache.put(3, 30)

    print(cache.get(2))
    print(cache.get(3))


if __name__ == "__main__":
    main()