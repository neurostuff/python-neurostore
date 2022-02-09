import threading
import base64
import hashlib
import webbrowser
import secrets
from time import sleep
from werkzeug.serving import make_server
from flask import Flask, request


global_dict = {
    'received_callback': False,
    'received_state': None,
    'authorization_code': None,
    'error_message': None
    }

app = Flask(__name__)

@app.route("/callback")
def callback():
    """
    The callback is invoked after a completed login attempt (succesful or otherwise).
    It sets global variables with the auth code or error messages, then sets the
    polling flag received_callback.
    :return:
    """
    if 'error' in request.args:
        global_dict['error_message'] = request.args['error'] + ': ' + request.args['error_description']
    else:
        global_dict['authorization_code'] = request.args['code']
    global_dict['received_state'] = request.args['state']
    global_dict['received_callback'] = True
    return "Please close this window and return to python-neurostore."


class ServerThread(threading.Thread):
    """
    The Flask server is done this way to allow shutting down after a single request has been received.
    """

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def open_login(authorization_url, state):
    # Open the browser window to the login url
    # Start the server
    # Poll til the callback has been invoked
    
    global_dict['received_callback'] = False
    webbrowser.open_new(authorization_url)
    server = ServerThread(app)
    server.start()
    while not global_dict['received_callback']:
        sleep(1)
    server.shutdown()

    if state != global_dict['received_state']:
        print("Error: session replay or similar attack in progress. Please log out of all connections.")
        exit(-1)

    if global_dict['error_message']:
        print("An error occurred:")
        print(global_dict['error_message'])
        exit(-1)

    return global_dict['authorization_code']

def auth0_url_encode(byte_data):
    """
    Safe encoding handles + and /, and also replace = with nothing
    :param byte_data:
    :return:
    """
    return base64.urlsafe_b64encode(byte_data).decode('utf-8').replace('=', '')

def generate_challenge(a_verifier):
    return auth0_url_encode(hashlib.sha256(a_verifier.encode()).digest())

def generate_pkse():
        verifier = auth0_url_encode(secrets.token_bytes(32))
        challenge = generate_challenge(verifier)
        return verifier, challenge