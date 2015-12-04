Ruby on Rails server
--------------------

Ruby on Rails uses Model-View-Controller framework. Almost all of the code is in the controller [Hallways/server/app/controllers/api/v1/main_controller.rb](https://github.com/jachan/Hallways/blob/master/server/app/controllers/api/v1/main_controller.rb).

The controller has two actions. One action is for when users upload their WiFi fingerprint to the server. It writes the fingerprint to the database verbatim, and it updates the server's mathematical conception of WiFI points (accumulates into the field). The download sends over the mathematical conception to the client so the client can locate himself. All location is done on the client because: the client doesn't want the server to know its location for privacy reasons, and it is less load on the server.

There is a model for reperesenting the verbatim WiFi fingerprint collected by the client, and there will be a model for representing the mathematical conception as well.
