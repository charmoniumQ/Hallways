package com.github.jachan.hallways.math;

import static java.lang.Math.pow;
import static java.lang.Math.sqrt;

/**
 * Instead of recalculating the mean and standard devation based on all of the data, it is possible to continuously update those values.
 * Code to do so has been written here.
 * It follows http://www.jstor.org/stable/1266577
 * http://www.jstor.org.libproxy.utdallas.edu/stable/1266577
 */
public class ContinuousStats {
    public ContinuousStats() {
        M = 0.0d;
        S = 0.0d;
        ni = 0;
    }

    public void update(double xn) {
        ni++;
        double n = ni;
        S = S + (n - 1) / n  * pow(xn - M, 2.0d); // here M refers to m_(i - 1)
        M = (n - 1) / n * M + xn / n;
    }

    public double avg() {
        return M;
    }

    public double stddev() {
        double n = ni;
        return sqrt(S / n);
    }

    public int n() {
        return ni;
    }

    double M, S;
    int ni;
}
