package com.github.jachan.hallways;

/**
 * Code that represents a place on in coordinate space
 */
public class Location {
    Location(double x, double y, double z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    double getX() {
        return x;
    }

    double getY() {
        return y;
    }

    double getZ() {
        return z;
    }

    double x, y, z;
}
