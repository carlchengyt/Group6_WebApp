# Copied from Lecture 6 of COMP0034 and edited by Group 6

from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)