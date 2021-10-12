# Queue to hold frings
from fringe_node import Fringe_Node
import heapq

class Priority_Queue:
    def __init__(self):
        self.queue = []
        self.fringe_set = {}
        self.counter = 0
    
    # checks if it is empty
    def is_empty(self):
        return True if len(self.queue) == 0 else False
    
    # adds a fringe node to the queue
    def enqueue(self, node):

        # check if the node exists in the queue
        if node.curr_block in self.fringe_set:
            if node.distance < self.fringe_set[node.curr_block]:
                self.remove_fringe_node(node.curr_block)
            else:
                return

        # add the new node into the queue
        heapq.heappush(self.queue, (node.distance, self.counter, node))
        self.counter += 1
        self.fringe_set[node.curr_block] = node.distance
    
    # removes the fringe node from list
    def remove_fringe_node(self, coord):
        for index, node in enumerate(self.queue):
            if node[2].curr_block == coord:
                # if node is in last index, just pop it
                if index == len(self.queue) - 1:
                    self.queue.pop()
                    return
                # replace the node to remove with the last node and heapify
                last_node = self.queue.pop()
                self.queue[index] = last_node
                heapq.heapify(self.queue)

    # pops the lowest distance node from the queue
    def de_queue(self):
        node = heapq.heappop(self.queue)
        self.fringe_set.pop(node[2].curr_block)
        return node[2]