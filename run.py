# from VOH import app
# if __name__ == '__main__':
#     # Create the application from views and run the application on port 5000
#     app.run(port=5000, debug=True)

from VOH import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)