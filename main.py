from Website import Setup, config

# MAINLINE
if __name__ == "__main__":  # start the web server
    Setup.socketio.run(Setup.app, debug=True) 
    ## host=str(config.Config.SERVER)
    ## ^ Use this to go online
