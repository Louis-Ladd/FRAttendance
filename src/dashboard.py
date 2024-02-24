from dashboardapp import create_app, socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)
    # This application needs to be self signed to use HTTPS,
    # I was able to sniff the admin credentials when HTTP is being used.
    # ssl_context='adhoc'
