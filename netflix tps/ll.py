class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


a = Node(1)
b = Node(2)
a.next = b

c = Node(3)
b.next = c

def print_linked_list(head):
    cur = head
    while cur:
        print(cur.data, end=" -> ")
        cur = cur.next
    print("None\n")
print_linked_list(a)

def insert_at_end(head, data):
    new_node = Node(data)
    cur = head
    while cur.next:
        cur = cur.next
    cur.next = new_node

def insert_at_beginning(head, data):
    new_node = Node(data)
    new_node.next = head
    return new_node

insert_at_end(a, 4)
print_linked_list(a)

aa = insert_at_beginning(a, 0)
print_linked_list(aa)