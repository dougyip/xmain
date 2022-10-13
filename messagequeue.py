import queue
import time
from threading import Thread


class MicroTerminal:
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        i = 0
        while True:
            if not self.queue.full():
                self.queue.put([self, f"M-{i}"])
                print(f"Microterminal enqueues M-{i}")
                i = i + 1

    def process_result(self, result_code):
        print(f"Microterminal {result_code}")

class Ethernet:
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        i = 0
        while True:
            if not self.queue.full():
                self.queue.put([self, f"E-{i}"])
                print(f"Ethernet enqueues E-{i}")
                i = i + 1

    def process_result(self, result_code):
        print(f"Ethernet {result_code}")

if __name__ == "__main__":

 # Create command queue object
    q = queue.Queue(1)

# Create microterminal object and run in separate thread
    mt = MicroTerminal(q)
    t1 = Thread(target=mt.run)
    t1.start()

# Create ethernet object and run in separate thread
    e = Ethernet(q)
    t2 = Thread(target=e.run)
    t2.start()

# Loop to get commands and return results to calling objects
# queue entries are in the form [calling_object, command]
    while True:
        command = q.get()
        print(f"Controller dequeues {command[1]} from {command[0]}")
        command[0].process_result("success!")
        time.sleep(.01)


