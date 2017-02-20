class Node(object):
    def __init__(self, v, n=None):
        self.__v = v
        self.__n = n

class LinkedQ:
    def __init__(self, first=None, last=None):
        self.first = None
        self.last = None

    def enqueue(self, v):
        newNode = Node(v)
        if self.first == None:
            self.last = newNode
            self.first = newNode
        else:
            self.last._Node__n = newNode
            self.last = self.last._Node__n

    def dequeue(self):
        removed_node = self.first._Node__v
        self.first = self.first._Node__n
        return removed_node

    def isEmpty(self):
        if self.first == None:
            return True
        else:
            return False
