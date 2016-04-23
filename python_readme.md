Python app
-----------

##### Part 1 #####

- There is a map of a building
- If the location is known, the user selects their location
- When the user clicks "Record Data"
    * WiFi measurements are periodically taken
    * When the user clicks "Record Data"
        + The WiFi data collection stops
        + If the location is selected, the data is uploaded to the client authoritatively
		+ If the location is not selected, the data is used to locate the user


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

