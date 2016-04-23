import xml.etree.ElementTree as ET
import sh
import re

if True:
    output = sh.command(r'/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport', '-s')
    BSSIDs = []
    ESSIDs = []
    RSSIs = []
    for line in output:
        match = re.search(r'\s*(.*) ([0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}) (-?\d{1,2})', line)
        if match:
            ESSIDs.append(match.group(1))
            BSSIDs.append(match.group(2))
            RSSIs.append(match.group(3))
    print(list(zip(BSSIDs, ESSIDs, RSSIs)))
            