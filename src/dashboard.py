from dashboardapp import create_app, socketio

print("Creating applicaiton...")
app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True, ssl_context='adhoc')
    # This application needs to be self signed to use HTTPS,
    # I was able to sniff the admin credentials when HTTP is being used.
    # ssl_context='adhoc'
