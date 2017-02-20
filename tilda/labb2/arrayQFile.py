class ArrayQ(object):

    def __init__(self, queue = None):
        if queue == None:
            self.queue = []
        else:
            self.queue = list(queue)

    def enqueue(self, x):
        self.queue.append(x)

    def dequeue(self):
        x = self.queue.pop(0)
        return x

    def isEmpty(self):
        if self.queue == []:
            return True
        else:
            return False
