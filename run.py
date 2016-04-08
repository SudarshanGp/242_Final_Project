from VOH import create_app, socketio

app = create_app(debug=True) # Create an application

if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0')  # Run app as a socketio instance