Python app
-----------

##### Part 1 #####

- There is a map of campus
- The user clicks on where he/she is
- When the user clicks "Record Data"
    * WiFi measurements are periodically taken
    * When the user clicks "Record Data"
        + The WiFi data collection stops
        + If the user clicks "Send data", the data is sent to the server
		+ If the user clicks "Where am I"
            - All the WiFi data is downloaded from the server to the client
			- The client attempts to locate itself on the map


##### Running #####

    cd project_root/python_client       # enter the directory
    python -m unittest tests.wifi_test  # run a unit test
	python -m hallways.gui.main         # run the main program

##### Code #####

The code is divided into packages:

- `hallways/`
    * `wifi.py`: actually gets wifi signal strength from hardware
	* `fingerprint.py`: stores the data from a particular location
	* `field.py`: mathematical representation of the predicted signal field
	* `connection.py`: talks to Ruby on Rails server
	* `location.py`: represents a single location
	* `locator.py`: the actual algorithm for locating the client
	* `exceptions.py`: exceptions the software might throw
	* `gui/`
	    + `main.py`: the main program
		+ `skeleton.py`: the skeleton/wireframe of the main program
		+ `visual_map.py`: a widget that makes a picture into a clickable map
- tests/
    * `<name>_test.py`: unittest for <name>

