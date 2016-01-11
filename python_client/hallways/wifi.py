from __future__ import print_function
import sys
import time
import threading
import re
import sh
from .fingerprint import Fingerprint
from .exceptions import WiFiScannerException

class WiFiScanner(object):
    def __init__(self, interface, delay=2, network_names=None, mock=False):
        '''Create a scanner for wireless interface that rescans every delay seconds'''
        self.mock = mock
        if self.mock:
            return
        self._network_names = network_names
        self._interface = interface
        self._delay = delay

    def start_scanning(self, loc):
        '''Start collecting data, and remember that it was taken from location loc'''
        if self.mock:
            return
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
                with self._data_lock:
                    for BSSID, ESSID, RSSI in iwlist:
                        if self._network_names and ESSID not in self._network_names:
                            # network_names is set to the names you want to capture
                            # this is not one of them, so ignore
                            continue
                        if BSSID not in self._data:
                            self._data[BSSID] = Fingerprint(BSSID, self._loc)
                        self._data[BSSID].update(RSSI)
                t = time.time() - self._last if self._last else None
                self._last = time.time()
                print ('Updating',  '{:.2f}'.format(t) if t else '', str(len(self._data)))
            time.sleep(self._delay)

    def stop_scanning(self):
        '''Stops scanning and returns data as a dict of fingerprints'''
        if self.mock:
            return []
        self._stopped = True
        with self._data_lock:
            return [fingerprint.readonly_copy() for fingerprint in self._data.values()]

    def join(self):
        if self.mock:
            return
        self._thread.join()

def scan(interface):
    '''Gets the a list if networks and signal strength using iwlist'''
    try:
        output = sh.iwlist(interface, 'scanning')
    except sh.ErrorReturnCode_255:
        raise WiFiScannerException('Interface is busy')
    BSSIDs = []
    ESSIDs = []
    RSSIs = []
    BSSID_line = re.compile(r'Address: ([0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2})')
    ESSID_line = re.compile(r'ESSID:"(.+)"')
    RSSI_line = re.compile(r'Signal level=(-\d+)')
    for line in output:
        m = re.search(BSSID_line, line)
        if m:
            BSSIDs.append(m.group(1))
            continue
        m = re.search(RSSI_line, line)
        if m:
            RSSIs.append(int(m.group(1)))
            continue
        m = re.search(ESSID_line, line)
        if m:
            ESSIDs.append(m.group(1))
            if len(BSSIDs) != len(RSSIs) or len(BSSIDs) != len(ESSIDs):
                raise WiFiScannerException('Mismatch between BSSIDs and RSSIs')
            continue
    return zip(BSSIDs, ESSIDs, RSSIs)

__all__ = ['WiFiScanner']
