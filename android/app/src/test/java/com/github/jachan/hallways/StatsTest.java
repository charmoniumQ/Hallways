package com.github.jachan.hallways;

import java.util.ArrayList;
import java.util.List;
import static java.lang.Math.*;
import org.junit.Test;
import static org.junit.Assert.*;
import com.github.jachan.hallways.math.ContinuousStats;

public class StatsTest {
    final int NUM_TESTS = 100;
    final int MAX_DATA_COUNT = 1000;
    final int MAX_ELEM = 1000;
    final int MIN_ELEM = -1000;

    @Test
    public void mean_isCorrect() {
        for (int i = 0; i < NUM_TESTS; ++i) {
            List<Double> data = randomData();
            ContinuousStats c = new ContinuousStats();
            for (double x : data) {
                c.update(x);
            }
            assertEquals(realAvg(data), c.avg(), 0.01d);
        }
    }

    @Test
    public void stddev_isCorrect() {
        for (int i = 0; i < NUM_TESTS; ++i) {
            List<Double> data = randomData();
            ContinuousStats c = new ContinuousStats();
            for (double x : data) {
                c.update(x);
            }
            assertEquals(realStddev(data), c.stddev(), 0.01d);
        }
    }

    double realAvg(List<Double> data) {
        double sum = 0;
        for (double x : data) {
            sum += x;
        }
        return sum / data.size();
    }

    double realStddev(List<Double> data) {
        double avg = realAvg(data);
        double sumVariance = 0;
        for (double x : data) {
            sumVariance += pow(x - avg, 2);
        }
        return sqrt(sumVariance / data.size());
    }

    List<Double> randomData() {
        int n = (int) (random() * MAX_DATA_COUNT + 1);
        List<Double> data = new ArrayList<>();
        for (int i = 0; i < n; ++i) {
            data.add(random() * (MAX_ELEM - MIN_ELEM) + MIN_ELEM);
        }
        return data;
    }
}