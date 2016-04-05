from socket_test import socketio
from socket_test import app
if __name__ == '__main__':
    # Create the application from views and run the application on port 5000
    # app.run(port=5000, debug=True)
    socketio.run(app)