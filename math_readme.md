Maths behind the project
------------------------

##### Example #####
Lets say I collect a the signal strength of three different networks (a, b, and c) at 2 known locations (p1 and p2). Now I have another fingerprint of networks a, b, and c from an unknown location p3. How do I get the unknown location from the known signal strength at p1 and p2? If you simply develop a comparison of different signal strengh fingerprints, what if p3.a is similar to p1.a, but p3.b is similar to p2.b?

##### General case #####
You have a list of sources N\_1, N\_2, ... N\_m. You have a list of measurement vectors V\_1, V\_2, ..., V\_n where in each vector, the first component is the signal strength (always positive) from the first source, the second component is the signal strength from the second source, ..., the mth component is the signal strength from the mth source. You have a list of locations in R^3 P\_1, P\_2, ..., P\_n which is coordinated with the measurement vector. Each P\_i is the location at which V\_i was measured.

Given a new measurement vector, X, predict what location X was measured from.

##### First attempt #####

If you look at a single measurement of an arbitrary source V\_i at the current position, it should follow a [normal distribution](https://en.wikipedia.org/wiki/Normal_distribution). The probability that a new measurement, call it X\_i, is drawn from the same random variable that produced V\_i is proportional to exp(-(V\_i - X\_i)^2). And P(A and B) = P(A) P(B), so the probability that the entire measurement vector was drawn from the same distribution as a known measurement vector is the product of the probability that each measurement was drawn from the same distribution as each known measurement. P(X came from V) = product for 1 < i <= n {exp(-(V\_i - X\_i)^2)}.

Each source acts like a [scalar field](https://en.wikipedia.org/wiki/Scalar_field) which maps from location in R^3 to a signal strength value. In order to reconstruct this scalar field, do a polynomial regression on the known samples. Considering all of the scalar fields together, we have a vector field (call it Vp) which inputs location in R^3 and outputs measurement vectors of what we 'think' the measurement vector would be at that point.

We want to find the measurement vector V with the maximum probability that it was drawn from the same distribution as X. Therefore we need to use [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent) to find the location that maximizes the probability function: argmax L (where L in R^3) product 1 < i <= n {exp(-(Vp(L) - X\_i)^2)}.

##### Possible improvements #####
- Perhaps another type of field estimator could be used instead of a polynomial regression was used. Polynomials don't tend towards zero when x tends towards infinity, but WiFi strength does in fact tend towards zero.
- Perhaps a faster method could be used to analytically minimize the cost function (the P(X came form V))
- Perhaps standard deviation could be captured by the client and used to normalize the probability measurement to exp(-(V\_i - X\_i)^2 / (2 stddev)^2)
- Normalize measurements by the number of WiFi scans they used to sample

##### Second attempt #####
Do any of you want to take a shot?
