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
- Implement server logs.
- Design the UI for collecting data.
- Create database structure for storing signal strength to location data.
- Create webserver for serving database.
- Write database setting methods for collecting data.
- Take data!
- Find out error-tolerance (eg. how much does the signal change? how accurate is our reading?).
- Write code that embeds maps (with labeled room numbers) of UTD buildings into the database

### Implementation of client:
- Design an UI
    * Design UI for displaying maps
    * Design UI for searching for places
    * Design UI for reporting incorrect identifications
- Write code that talks to the server.
- Write the methods that implement our algorithm for matching signal strength to location.
- Write the methods that implement our algorithm for updating the database.
- Write the methods that allow users to open a certain type of location-link in our app.
- Implement client logs and send crash-statistics to server.

### Maintenance and further improvement:
- Write a user feedback form to improve our project.
- Port to multiple platforms.

## Similar projects and related research:
- [Navizon](https://www.navizon.com/), now called [Accuware](http://www.accuware.com/)
- [Redpin](http://redpin.org/)
- [Duke's UnLoc](http://today.duke.edu/2012/06/unloc)
- [PlaceLab](http://ntrg.cs.tcd.ie/undergrad/4ba2.05/group1/) is similar, but wants much wider coverage (being able to locate yourself anywhere) and less accuracy (10m - 30m).

Contact us if you would like to join.
