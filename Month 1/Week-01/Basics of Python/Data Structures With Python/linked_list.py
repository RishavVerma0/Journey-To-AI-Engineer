class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None       

    def insert_at_begining(self,data):
        node = Node(data,self.head)
        self.head = node

    def print(self):
        if self.head is None:
            print("Linked List is Empty")
            return
        
        itr = self.head
        llstr = ''

        while itr:
            llstr += str(itr.data) + '-->'
            itr = itr.next

        print(llstr)

    def insert_at_end(self,data):
        if self.head is None:
            self.head = Node(data,None)
            return
        
        itr = self.head

        while itr.next:
            itr = itr.next

        itr.next = Node(data,None)


    def insert_values(self,data_list):
        self.head = None
        for data in data_list:
            self.insert_at_end(data)

    def get_length(self):
        count = 0
        itr = self.head

        while itr:
            count += 1
            itr = itr.next

        return count
    
    def remove_at(self, index):

        if index < 0 or index >= self.get_length():

            raise Exception("Invalid Index")

        if index == 0:

            self.head = self.head.next # type: ignore

            return

        count = 0

        itr = self.head

        while itr and count < index - 1:

            itr = itr.next

            count += 1

        if not itr or not itr.next:

            raise Exception("Invalid Index")

        itr.next = itr.next.next

    def insert_at(self, index, data):

        if index < 0 or index > self.get_length():

            raise Exception("Invalid Index")

        if index == 0:

            self.insert_at_begining(data)

            return

        count = 0

        itr = self.head

        while itr and count < index - 1:

            itr = itr.next

            count += 1

        if not itr:

            raise Exception("Invalid Index")

        node = Node(data, itr.next)

        itr.next = node 

if __name__ == '__main__':
    ll = LinkedList()
    ll.insert_values(["Apple", "Banana", "Cherry", "Date"])
    ll.insert_at_begining(5)
    ll.insert_at_begining(20)
    ll.insert_at_begining(15)
    ll.insert_at_end(30)
    ll.insert_at_end(35)
    print("Linked List:")
    ll.print()
    print("Length of Linked List:", ll.get_length())

    ll.remove_at(2)
    print("Linked List after removing element at index 2:")
    ll.print()

    ll.insert_at(2, "Kiwi")
    print("Linked List after inserting 'Kiwi' at index 2:")
    ll.print()