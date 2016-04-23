from __future__ import print_function
import sys
import time
import threading
import re
import sh
from sys import platform as _platform
#from wifi import Cell
from .fingerprint import Fingerprint, WriteableFingerprint
from .exceptions import WiFiScannerException

# TODO: implement MAC address as 6 bytes instead of string
# it is more compact
# TODO: use custom JSON decoder object hooks to make a string MAC address serialize to 6 bytes
def mac_to_bytes(MAC):
    MAC = MAC.replace(MAC[2], '')
    if len(MAC) != 12:
        # TODO: make this an exception from the exceptions module?
        raise RuntimeError('Invalid MAC address')
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
                # TODO: remove print statements maybe? communicate status some other way
                print('Updating',  't = {:.2f}'.format(t) if t else 't = NaN', 'len(networks) = {}'.format(len(self._fingerprint)))
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
    if _platform == "linux" or _platform == "linux2":
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
    elif _platform == "darwin":
        output = sh.command(r'/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport', '-s')
        BSSIDs = []
        ESSIDs = []
        RSSIs = []
        for line in output:
            match = re.search(r'\s*(.*) ([0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}) (-?\d{1,2})', line)
            if match:
                ESSIDs.append(match.group(1))
                BSSIDs.append(match.group(2))
                RSSIs.append(int(match.group(3)))
        return zip(BSSIDs, ESSIDs, RSSIs)
    elif _platform == "win32":
        # Windows...
        pass

mock_scan_data = [
    Fingerprint(
        x=3.0, y=2.0, z=6.0,
        n=20,
        networks={
            "what is a mac address": {"m": 19, "avg": 20, "stddev": 2}
        }
    ),
]

__all__ = ['WiFiScanner']
