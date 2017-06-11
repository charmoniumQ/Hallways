import time
import sys
import multiprocessing as mp
from wifi_scanners import scanners

class Scanner(mp.Process):
    def __init__(self, interface, delay):
        super().__init__()
        self.interface = interface
        self.delay = delay
        self.your_pipe, self.my_pipe = mp.Pipe(False)
        self.stop_ev = mp.Event()

    def run(self):
        while not self.stop_ev.is_set():
            # while stop signal has not been issued
            network_list = scanners[sys.platform](self.interface)
            self.my_pipe.send(network_list)
            time.sleep(self.delay)
        self.my_pipe.close()

    def stop(self):
        self.stop_ev.set()
        self.your_pipe.close()
        self.join()

    def poll(self, timeout=0):
        return self.your_pipe.poll()

    def recv(self, timeout=0):
        if self.your_pipe.poll(timeout):
            return self.your_pipe.recv()
        else:
            return None

def test():
    s = Scanner('wlp3s0', 5)
    s.start()
    for i in range(3):
        print(s.recv(timeout=None))
    s.stop()

__all__ = ['Scanner']
