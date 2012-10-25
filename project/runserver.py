import socket
from mockups import app

try:
    app.run(debug=True)
except socket.error:
    print "The server is already running."
