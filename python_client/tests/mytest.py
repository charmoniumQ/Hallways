from __future__ import print_function
import time
from multiprocessing import Manager, Process

class MyProcess(object):
    def __init__(self):
        self._manager = Manager()
    def start_running(self):
        self._data = self._manager.dict()
        self._stop = self._manager.Value('b', False)
        self._process = Process(target=self._do_stuff)
        self._process.start()
    def _do_stuff(self):
        for i in range(10):
            self._data[i] = i
            if self._stop.value:
                return
            print('Subprocess', self._data)
            time.sleep(1)
    def stop_process(self):
        self._stop.value = True

a = MyProcess()
a.start_running()
time.sleep(0.2)
for j in range(5):
    print('Main process', a._data)
    time.sleep(1)
a.stop_process()
print('Final', a._data)
a._process.join()
