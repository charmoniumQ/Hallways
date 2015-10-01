## Project motivations:
- Indoor localization could help people navigate large buildings by showing users their location.
- Indoor localization could be used to streamline events by showing users' location to venue administrators.
- Indoor localization could let users share their location in a unambiguous way.
- Indoor localization could open the door for location-aware services (eg. a supermaket that makes suggestions based on the products near you)

## Signal information:
- RSSI is a measure of how much power is going through the antenna from a certain network [1][1].
- Different manufacturers of network cards can make RSSI mean different things, not just a linear measure of dBm. Not even the bounds are consistent across all devices [2][2]. Note that the android developer documentation erroneously refers to the RSSI as the signal strength in dBm.
- RCPI could be a better more consistent measure of signal strength, but the Android OS doesn't currently report this value in an API. ([Android Developer Site](http://developer.android.com/reference/android/net/wifi/ScanResult.html))
- The iPhone API doesn't let you get any information about networks in the area without the use of private libraries ([Stack Overflow post I](http://stackoverflow.com/questions/9684341/iphone-get-a-list-of-all-ssids-without-private-library), [Stack Overflow post II](http://stackoverflow.com/questions/10317028/find-available-wi-fi-networks)). On the other hand, the private library [Apple80211Functions](https://code.google.com/p/iphone-wireless/wiki/Apple80211Functions) exposes the access of RSSI, but not RCPI. Apps developed with private libraries are not permitted to be put on the app store.
- Physical events can change signal strength with time such as [3][3]:
   * other moving things in the environment causing multipath
   * time variations in other radio networks affect interference patterns
   * other users of the network can cause interference patterns
- WiFi receivers can take time-of-travel into account making the result more accurate, but this requires synchronized clocks, modifying the access-points, and line-of-sight [3][3] (additional research needed, I think this citation is misleading).
- RSSI varies if the user is standing between the phone and the AP (access point) [4][4]. This could be very bad.
- It is too difficult to estimate the RSSI based on the location of the APs. Instead, this has to be found empirically [4][4] because
   * Diffraction around barriers is hard to predict
   * Attenuation through walls is hard to predict since all walls are different
   * Attenuation caused by movable objects (like bookshelves and desks)
   * Scattering by a rough surface
   * Multipath when there are reflectors that let you get to an object in multiple ways
   * Fading due to interferance patterns
- The RSSI is less noisy at 5GHz than at 2.4GHz probably because less other appliances take up the 5GHz band [1][1].
- Most WiFi antennae are not isotropic, so the orientation that you hold your phone affects the RSSI [1][1].
- Some WiFI devices report an RSSI that simply has too much noise to locate [1][1].



## Tracking considerations:
- The position can be gathered by taking a double time integral of the accelerometer. This can help improve location results [4][4].
- Although accelerometers have good accuracy for a single datapoint, integrating multiple datapoints accumulates too much error to find position accurately [StackOverflow post](http://stackoverflow.com/questions/7499959/indoor-positioning-system-based-on-gyroscope-and-accelerometer) [4][4].
- Angle-of-Arrival could give more information to track users on.
- Linear interpolation could be used in between points of measurement.
- Algorithm could use gradient descent to minimize the euclidean distance of the current measurement vector to previously observed measurements vectors. But if we are using linear interpolation to guess what the measurements are like in between measurements, the measurement vector won't be a smooth function with respect to position, therefore gradient descent might fail.
- [4][4] used Euclidean Distance as a metric to see how observed measurement vector was differnt from the known measurement vector.
- [4][4] identifies the signal strength variations during the measurement taking as a potential weakness. [5][5] partially mitigates this by continously taking measurements while stationary. It still however takes time to integrate enough 
- [4][4] identifies the changing environment as a potential weakness. [5][5] lets users update the database over time, partially mitigating that. However, it still takes time and frequency of visitors to correct.
- On the other hand, [4][4] was successfully able to use a combination of multiple sensors to get more accurate results than [5][5].
- [4][4] suggests using a Kalman filter to combine the acceleration data with the WiFi position data.

## Other research:
- [1][1] is comparing the RSSI from different WiFi devices. There are huge differences between manufacturers and even among a single manufacturer.
- [2][2] is looking for a solution to track people in a mine. The researchers are assuming the two-dimensional case and using previous location to help coordinate future results. There is good information on the error distribution of RSSI.
- [3][3] the researchers are modifying Sofware-Defined Networks to implement time-of-arrival based tracking.
- [4][4] is all about combining multiple sensor streams to deduce location (including WiFi, GPS, Bluetooth, and inertial sensors). It offers many routines for cleaning up accelerometer data. It also offers information about the data-collection of RSSI networks. This is a complete system with good results. Very important to read.
- [5][5] is a complete system for tracking based on location fingerprinting. This means instead of putting WiFi measurement vectors on a continuum, it puts them in discrete locations and looks to see which one you are closest to. This simplifies the problem, however it is less accurate for large rooms like lecture halls or corridors.

[1]: http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=5955283 "[1] Differences in RSSI readings made by different Wi-Fi chipsets: A limitation of WLAN localization"
[2]: http://www.cdc.gov/niosh/mining/UserFiles/workshops/commtrack2009/NodeBasedTracking-Dubaniewicz.pdf "[2] Node-Based Tracking Using Received Signal Strength Indication"
[3]: https://www.wpi.edu/Pubs/E-project/Available/E-project-042811-163711/unrestricted/NRL_MQP_Final_Report.pdf "[3] Software Defined Radio Localization Using 802.11-style Communications"
[4]: http://hkr.diva-portal.org/smash/get/diva2:475619/FULLTEXT02.pdf "[4] Indoor Positioning using Sensor-fusion in Android Devices"
[5]: http://www.vs.inf.ethz.ch/publ/papers/bolliger-loca09.pdf "[5] Improving Location Fingerprinting through Motion Detection and Asynchronous Interval Labeling"
[6]: http://research.microsoft.com/en-us/groups/sn-res/infocom2000.pdf "RADAR: An In-Building RF-based User Location and Tracking System"

http://www.csd.uoc.gr/~hy539/Assignments/presentations/practical_robust_localization.pdf
http://www.cis.upenn.edu/~ahae/papers/mobicom2004.pdf
http://ieeexplore.ieee.org.libproxy.utdallas.edu/xpls/icp.jsp?arnumber=5646681&tag=1
http://pi4.informatik.uni-mannheim.de/~kopf/publications/2006/King_2006c.pdf
http://www.cis.upenn.edu/~ahae/papers/mobicom2004.pdf
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.3.6233&rep=rep1&type=pdf
http://ieeexplore.ieee.org.libproxy.utdallas.edu/xpls/icp.jsp?arnumber=6963028
http://ieeexplore.ieee.org.libproxy.utdallas.edu/xpls/icp.jsp?arnumber=6805651
http://ieeexplore.ieee.org.libproxy.utdallas.edu/xpls/icp.jsp?arnumber=7127744
http://ieeexplore.ieee.org.libproxy.utdallas.edu/xpls/icp.jsp?arnumber=7164524
http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=1613734&url=http%3A%2F%2Fieeexplore.ieee.org%2Fiel5%2F4234%2F33873%2F01613734.pdf%3Farnumber%3D1613734
http://www.vs.inf.ethz.ch/publ/papers/bolligph-redpin2008.pdf

http://stackoverflow.com/questions/12098122/how-to-improve-accuracy-of-indoor-positioning
http://www.gizmag.com/unloc-indoor-navigation-app/23106/
https://github.com/COMSYS/FootPath
http://today.duke.edu/2012/06/unloc
https://www.google.com/search?sourceid=chrome-psyapi2&ion=1&espv=2&ie=UTF-8&q=google%20indoor%20mapping&oq=google%20indoor%20mapping&aqs=chrome..69i57j0l4j69i64.3424j0j7
