package com.github.jachan.hallways;

import java.util.List;

/**
 * Code that represents data of WiFi signal-strength for a single AP names. I haven't worked out
 * all of the details of this class. This needs to be filled with attributes that will be decided
 * later.
 */
public class Fingerprint {
    /**
     * Constructs a place-holder for the fingerprint of <code>BSSID</code>
     * @param BSSID name of the network
     */
    Fingerprint(String BSSID) {
        this.BSSID = BSSID;
    }

    /**
     * Stores <code>RSSI</code> to the current fingerprint
     */
    void update(double RSSI) {
        RSSIs.add(RSSI);
    }

    List<Double> RSSIs;
    String BSSID;
}
