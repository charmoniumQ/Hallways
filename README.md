# Hallways

Hallways is a project to help people navigate the littered layout of the UT Dallas campus. By using WiFi network signals, Hallways aims to help the user find their location indoors. There's no need for battery draining GPS (which doesn't work well indoors anyway). Users will be able to open up an app and easily get to their classes.

## Specifications:
- Empirically measure the signal strength of existing semi-permanent access points.
- Consult a database containing the signal strength of various access points with respect to the location.
- Locate self on client with room-to-room accuracy.
- Display location on a map.
- Either (based on user option) continuously update location or update location upon request.
- Passively acquire user data (without sacrificing privacy) to improve results.
- Allow users to write their location in a link and send it to other users who can open that location on a map.

## Roadmap:
### Design/research:
- Understand the state-of-the-art indoor tracking systems.
    * Understand the variance of 'signal strength' across different platforms.
    * Understand what environmental factors change signal strength.
    * Understand the algorithms for matching signal strength to location.
- Choose/design an algorithm for matching signal strength to location (psuedocode).
- Choose/design an algorithm for updating the database based on passive user input.

### Getting the data:
- Design the UI for collecting data.
- Create database structure for storing signal strength to location data.
- Write database setting methods for collecting data.
- Take data!
- Find out error-tolerance (eg. how much does the signal change? how accurate is our reading?).

### Implementation of client:
- Write code that embeds maps (with labeled room numbers) of UTD buildings into the database
- Design an UI for displaying maps from the database.
- Write the methods that implement our algorithm for matching signal strength to location
- Write the methods that implement our algorithm for updating the database.
- Write the methods that allow users to open a certain type of location-link in our app.

### Maintenance and further improvement:
- Write a user feedback form to improve our project.
- Port to multiple platforms.

## Similar projects and related research:
- [Navizon](https://www.navizon.com/), now called [Accuware](http://www.accuware.com/)
- [Redpin](http://redpin.org/)
- [Duke's UnLoc](http://today.duke.edu/2012/06/unloc)
- [Google Scholar](https://scholar.google.com/scholar?q=indoor+positioning+wifi&hl=en&as_sdt=0&as_vis=1&oi=scholart&sa=X&ved=0CC8QgQMwAGoVChMI5dn4-_acyAIVyJINCh14BAU1)
- [SO post 1](http://stackoverflow.com/questions/9726666/pinpointing-indoor-location-with-android-not-accurate-enough), [SO post 2](http://stackoverflow.com/questions/12098122/how-to-improve-accuracy-of-indoor-positioning) (take with grain of salt)

Contact us if you would like to join.
