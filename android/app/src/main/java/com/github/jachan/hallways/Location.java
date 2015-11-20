package com.github.jachan.hallways;

/**
 * Code that represents a place on in coordinate space
 */
public class Location {
    Location(double x, double y) {
        this.x = x;
        this.y = y;
    }

    double getX() {
        return x;
    }

    double getY() {
        return y;
    }

    double x, y;
}
