"""
Not using JIT compiler for linked lists
<function sum_list at 0x10c3f6f70>
Time elapsed: 0.13804074500000008

Using JIT compiler for linked lists
<function sum_list at 0x10da07f70>
Time elapsed: 0.669147938
"""

from numba import deferred_type, optional, int64
from numba.experimental import jitclass
from caching import time_decorator

node_type = deferred_type()

node_spec = [("next", optional(node_type)), ("value", int64)]


@jitclass(node_spec)
class Node:
    def __init__(self, value):
        self.next = None
        self.value = value


node_type.define(Node.class_type.instance_type)
ll_spec = [("head", optional(Node.class_type.instance_type))]


@jitclass(ll_spec)
class LinkedList:
    def __init__(self):
        self.head = None

    def push_front(self, value):
        if self.head is None:
            self.head = Node(value)
        else:
            new_head = Node(value)
            new_head.next = self.head
            self.head = new_head

    def show(self):
        node = self.head
        while node is not None:
            print(node.value)
            node = node.next


def sum_list(lst):
    res: int = 0
    node: LinkedList = lst.head
    while node is not None:
        res += node.value
        node = node.next

    return res


@time_decorator
def process():
    lst = LinkedList()
    [lst.push_front(x) for x in range(100000)]
    print("Using JIT compiler for linked lists")
    print(sum_list)


if __name__ == "__main__":
    process()
