package com.github.jachan.hallways;

import java.util.List;
import com.github.jachan.hallways.math.ContinuousStats;

/**
 * A fingerprint is a measurement over time of the WiFi signal-strength for a single WiFi access
 * point and the location from which the signal-strength is measured. In order to maximize the
 * information we have to work with, we will record the average and standard-deviation for
 * future use.
 */
public class Fingerprint {
    /**
     * @param bssid name of the network whose strength is being recorded
     * @param loc the location from which the strength is being recorded (if the location is
     *            unknown, set this to zero and set <code>known</code> to true)
     * @param known whether or not the location from which the strength is being recorded is known
     */
    Fingerprint(String bssid, Location loc, boolean known) {
        this.bssid = bssid;
        this.loc = loc;
        this.known = known;
    }

    /**
     * Stores <code>strength</code> to the current fingerprint
     */
    void update(double strength) {
        c.update(strength);
    }

    public double getAvg() {
        return c.avg();
    }

    public double getStddev() {
        return c.stddev();
    }

    public String getBssid() {
        return bssid;
    }

    public int getN() {
        return c.n();
    }

    public double getX() {
        return loc.getX();
    }

    public double getY() {
        return loc.getY();
    }

    public double getZ() {
        return loc.getZ();
    }

    public boolean isKnown() {
        return known;
    }

    ContinuousStats c;
    String bssid;
    Location loc;
    boolean known;
}
