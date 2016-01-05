Android app
-----------

##### Functionality #####

- There is a toggle switch between "Where am I?" (called download) and "I know my location" (called upload mode) ("toggle switch" means exactly one of them is active and the other is grayed out).
- When the app is in download mode:
    * if the data cache is out of date, download the pre-measured WiFi data from the server
    * When the accelerometer detects no motion:
        + measure WiFi signal strength
        + update the existing fingerprint with the new data (update the mean, update the standard deviation, etc.)
        + if there is enough data to locate the user, do so
            - render a marker on the map that moves with the map
            - center the map around that marker and zoom to a preset size
            - show the rooms for the floor in the building where the user is (if the user is in a building)
            - all other buildings just have their outline (not rooms) showing
            - the user can move the map with a finger-drag and zoom the map with a pinch
            - when the accelerometer detects motion, reset the accumulator
- When the app is in upload mode:
    * crosshairs are placed in the center of the map that do not move with the map
    * the user can move the map with a finger-drag and zoom the map with a pinch (as described above)
    * the user selects their building by moving that building under the crosshairs
    * the user selects their floor from a drop-down that changes based on the building or is grayed out if the user has not selected a building
    * their is a toggle switch between "start collecting" and "stop collecting"
    * if "start collecting":
        + start an accumulator, if none exists
        + measure WiFi signal strength, and accumulate it (as described above)
        + decide if the data is good enough to send to the server. If so, render a "good enough" thing to the user
    * if "stop collecting":
        + if data is good enough to send to the server, do so

##### Code #####

The following classes are located in [Hallways/android/app/src/main/java/com/github/jachan/hallways](https://github.com/jachan/Hallways/tree/master/android/app/src/main/java/com/github/jachan/hallways) (the crazy path is default for android projects built with AndroidStudio)
- [Field](https://github.com/jachan/Hallways/blob/master/android/app/src/main/java/com/github/jachan/hallways/Field.java): Code that represents a scalar field of estimated measurements of signal strength emanating from a single source.
- [Fingerprint](https://github.com/jachan/Hallways/blob/master/android/app/src/main/java/com/github/jachan/hallways/Fingerprint.java): Code that represents data of WiFi signal-strength for a single AP names.
- [Location](https://github.com/jachan/Hallways/blob/master/android/app/src/main/java/com/github/jachan/hallways/Location.java): Code that represents a place on in coordinate space
- [Locator](https://github.com/jachan/Hallways/blob/master/android/app/src/main/java/com/github/jachan/hallways/Locator.java): Code that actually locates you based on data
- [MainActivity](https://github.com/jachan/Hallways/blob/master/android/app/src/main/java/com/github/jachan/hallways/MainActivity.java): GUI code
- [ServerUtility](https://github.com/jachan/Hallways/blob/master/android/app/src/main/java/com/github/jachan/hallways/ServerUtility.java): Code that talks to the server
- [VisualMap](https://github.com/jachan/Hallways/blob/master/android/app/src/main/java/com/github/jachan/hallways/VisualMap.java): Code for representing a map of a building
- [WiFiUtility](https://github.com/jachan/Hallways/blob/master/android/app/src/main/java/com/github/jachan/hallways/WiFiUtility.java): Code for getting WiFi signal strengths

Javadocs are offered for readability. They are periodically built.

The Python client should always be one step ahead of the android client since it acts as a prototype
