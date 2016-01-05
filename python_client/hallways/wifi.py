import re
import sh
from .exceptions import WiFiScannerException

class WiFiScanner(object):
    def __init__(self, interface):
        self._interface = interface

    def scan(self):
        output = sh.iwlist(self._interface, 'scanning')
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

__all__ = ['WiFiScanner']
