William (Bill) Fahle points system web service (RESTful)

1. Install python3 on your system (assumes Windows, other OSes may vary)
2. Make sure it's the default python
3. Make sure you have the needed libraries
	pip3 install flask
	pip3 install json
	pip3 install urllib
	pip3 install requests
	pip3 install datetime
(note: if install gives error WinError 2 ... deleteme, just run the pip3 command again)
4. In a CMD command prompt, run the REST server (app.py):
	python app.py
5. In another fresh CMD prompt, run the test application client (testapp.py):
	python testapp.py

This process simulates a client and server running the assignment. The assumption is that the data is properly formatted
by the client; there is not a lot of error checking on the inputs. To exit the server, strike ctrl-c on the command line
running it. The client test app exits naturally. It performs the examples written in the requirements document, but obviously
other inputs are possible and would work against the server.