from __future__ import print_function
import sys
import time
import threading
import re
import sh
import numpy
#from wifi import Cell
from .fingerprint import Fingerprint, WriteableFingerprint
from .exceptions import WiFiScannerException

# TODO: implement MAC address as 6 bytes instead of string
# it is more compact
# TODO: use custom JSON decoder object hooks to make a string MAC address serialize to 6 bytes
def mac_to_bytes(MAC):
    '''Accepts any delimiter in the second index (usually a colon or dash) and returns a dict of index to bytes

For example, mac_to_bytes('00:11:22:33:44:55') == {0: 0, 1: 17, 2: 34, 3: 51, 4: 68, 5: 85}'''
    if re.match(MAC, '([0-9a-fA-F]{2}.){5}[0-9a-fA-F]{2}'):
        MAC = MAC.replace(MAC[2], '')
    elif re.match(MAC, '[0-9a-fA-F]{12}'):
        pass
    else:
        raise RuntimeError('Invalid MAC address ' + repr(MAC))
    return dict(enumerate((bytes.fromhex(MAC))))

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
        # TODO: use pipe objects to transfer data instead of locks + primitive objects
        self._stopped = False
        self._data = {}
        self._data_lock = threading.Lock()
        self._last_time = None
        self._fingerprint = WriteableFingerprint(loc=loc)
        self._thread = threading.Thread(target=self._update)
        self._thread.start()

    def _update(self):
        while not self._stopped:
            try:
                iwlist = list(scan(self._interface))
            except WiFiScannerException as e:
                # TODO: do something more sensible here
                print(str(e), file=sys.stderr)
                pass
            else:
                with self._data_lock:
                    data = []
                    for BSSID, ESSID, strength in iwlist:
                        if self._network_names and ESSID not in self._network_names:
                            # network_names is set to the names you want to capture
                            # this is not one of them, so ignore
                            continue
                        else:
                            data.append((BSSID, strength))
                    self._fingerprint.update(data)
                # TODO: this should be timedelta and datetime
                t = time.time() - self._last_time if self._last_time else None
                self._last_time = time.time()
                # TODO: remove print statements, and pass status through interprocess pipe instead
                print('Updating',  't = {:.2f}'.format(t) if t else 't = NaN', 'n = {}'.format(len(self._fingerprint)))
            time.sleep(self._delay)

    def stop_scanning(self):
        '''Stops scanning and returns data as a dict of fingerprints'''
        if self.mock:
            return mock_scan_data
        self._stopped = True
        with self._data_lock:
            return self._fingerprint.finalize()

    def join(self):
        if self.mock:
            return
        self._thread.join()

def scan_old(interface):
    out = []
    for net in Cell.all(interface):
        out.append((net.address, net.ssid, net.signal))
    return out

# TODO: this is the level mocks should be implemented at,
# not WiFiScanner
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
    ESSID_line = re.compile(r'ESSID:"(.*)"')
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
                print(BSSIDs)
                print(RSSIs)
                print(ESSIDs)
                raise WiFiScannerException('Mismatch between BSSIDs and RSSIs')
            continue
    return zip(BSSIDs, ESSIDs, RSSIs)

mock_scan_data = [
    Fingerprint(
        x=numpy.int32(3), y=numpy.int32(2), z=numpy.int32(6),
        n=20,
        networks={
            "what is a mac address": {"m": 19, "avg": 20, "stddev": 2}
        }
    ),
]
mock_scan_data2 = {
    "34:A8:4E:3B:B4:90": {
        "m": 2,
        "strength_stddev": 0.0,
        "strength_avg": -62.0
    },
    "34:A8:4E:D2:AE:01": {
        "m": 2,
        "strength_stddev": 0.0,
        "strength_avg": -63.0
    },
    "34:A8:4E:1E:73:B1": {
        "m": 2,
        "strength_stddev": 0.0,
        "strength_avg": -59.0
    },
    "34:A8:4E:D2:A1:F1": {
        "m": 2,
        "strength_stddev": 0.0,
        "strength_avg": -64.0
    },
}

__all__ = ['WiFiScanner']
