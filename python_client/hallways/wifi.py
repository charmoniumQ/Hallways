from __future__ import print_function
import sys
import time
import threading
import re
import sh
from .fingerprint import Fingerprint
from .exceptions import WiFiScannerException

class WiFiScanner(object):
    def __init__(self, interface, delay=2):
        '''Create a scanner for wireless interface that rescans every delay seconds'''
        self._interface = interface
        self._delay = delay

    def start_scanning(self, loc):
        '''Start collecting data, and remember that it was taken from location loc'''
        self._loc = loc
        self._stopped = False
        self._data = {}
        self._data_lock = threading.Lock()
        self._last = None
        self._thread = threading.Thread(target=self._update)
        self._thread.start()

    def _update(self):
        while not self._stopped:
            try:
                iwlist = scan(self._interface)
            except WiFiScannerException as e:
                print(str(e))
                pass
            else:
                t = time.time() - self._last if self._last else None
                print ('Updating',  '{:.2f}'.format(t) if t else '')
                self._last = time.time()
                with self._data_lock:
                    for BSSID, RSSI in iwlist:
                        if BSSID not in self._data:
                            self._data[BSSID] = Fingerprint(BSSID, self._loc)
                        self._data[BSSID].update(RSSI)
            time.sleep(self._delay)

    def stop_scanning(self):
        '''Stops scanning and returns data as a dict of fingerprints'''
        self._stopped = True
        with self._data_lock:
            return self._data.copy()

    def join(self):
        self._thread.join()

def scan(interface):
    '''Gets the a list if networks and signal strength using iwlist'''
    try:
        output = sh.iwlist(interface, 'scanning')
    except sh.ErrorReturnCode_255:
        raise WiFiScannerException('Interface is busy')
    BSSIDs = []
    RSSIs = []
    BSSID_line = re.compile(r'Address: ([0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2})')
    RSSI_line = re.compile(r'Signal level=(-\d+)')
    for line in output:
        m = re.search(BSSID_line, line)
        if m:
            BSSIDs.append(m.group(1))
        m = re.search(RSSI_line, line)
        if m:
            RSSIs.append(int(m.group(1)))
            if len(BSSIDs) != len(RSSIs):
                raise WiFiScannerException('Mismatch between BSSIDs and RSSIs')
    return zip(BSSIDs, RSSIs)

def continuous_scan(interface):
    '''Repeatedly calls and accumulates scan information to build a fingerprint'''

__all__ = ['WiFiScanner']
