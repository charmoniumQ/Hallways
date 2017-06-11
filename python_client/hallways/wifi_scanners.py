import re
import collections
import subprocess

hex_digit = '[0-9a-fA-F]'
sep = '[:.-]'
mac_address = sep.join(hex_digit + hex_digit for _ in range(6))

class WiFiScannerException(Exception):
    pass

def scan_linux(interface):
    stdout, _ = run(['iwlist', interface, 'scanning'])
    BSSID_line = re.compile(r'^.*?Address: ({mac_address})'.format(**globals()), flags=re.MULTILINE)
    RSSI_line = re.compile(r'^.*?Signal level=(-\d+)', flags=re.MULTILINE)
    ESSID_line = re.compile(r'^\s*ESSID:"(.*?)"', flags=re.MULTILINE)
    BSSIDs = []
    ESSIDs = []
    RSSIs = []
    for line in stdout.decode().split('\n'):
        m = BSSID_line.search(line)
        if m:
            BSSIDs.append(mac_to_bytes(m.group(1)))
            continue
        m = RSSI_line.search(line)
        if m:
            RSSIs.append(int(m.group(1)))
            continue
        m = ESSID_line.search(line)
        if m:
            ESSIDs.append(m.group(1))
            if len(BSSIDs) != len(RSSIs) or len(BSSIDs) != len(ESSIDs):
                print(BSSIDs, RSSIs, ESSIDs, stdout, sep='\n')
                raise WiFiScannerException('Mismatch between BSSIDs and RSSIs')
    return zip(BSSIDs, RSSIs, ESSIDs)

def scan_mac(interface):
    airport = r'/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport'
    stdout, stderr = run([airport, '-s'])
    BSSIDs = []
    ESSIDs = []
    RSSIs = []
    for line in output:
        match = re.search(r'\s*(.*?) ({mac_address}) (-?\d+)', line)
        if match:
            ESSIDs.append(match.group(1))
            BSSIDs.append(mac_to_bytes(match.group(2)))
            RSSIs.append(int(match.group(3)))
    return (zip(BSSIDs, ESSIDs, RSSIs)

def scan_windows(interface):
    raise NotImplementedError('Windows is not yet supported')

def scan_other(interface):
    raise NotImplementedError('Your OS is not yet supported')

# TODO: implement MAC address as 6 bytes instead of string
# it is more compact
# TODO: use custom JSON decoder object hooks to make a string MAC address serialize to 6 bytes
def mac_to_bytes(MAC_):
    '''Accepts any delimiter in the second index (usually a colon or dash) and returns bytes

For example, mac_to_bytes('00:11:22:33:44:55') == [0, 17, 34, 51, 68, 85}'''
    MAC = re.sub('[^0-9a-fA-F]', '', MAC_)
    if len(MAC) != 12:
        raise RuntimeError('Invalid MAC address ' + repr(MAC_))
    return bytes.fromhex(MAC)

def run(cmd):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        print(proc.stdout, proc.stderr, sep='\n')
        raise RuntimeError('Listing wifi beacons failed with return code {proc.returncode}'.format(**locals()))
    return proc.stdout, proc.stderr

scanners = collections.defaultdict(lambda: scan_other, {
    'linux': scan_linux,
    'linux2': scan_linux,
    'darwin': scan_mac,
    'win32': scan_windows
})

# TODO: write a interfaces[sys.platform]()

def test_scanner():
    import pytest
    with pytest.raises(NotImplementedError):
        scanners['bsd']('wlp3s0')
    scan_linux('wlp3s0')

__all__ = ['scanners']
