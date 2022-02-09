from requests_oauthlib import OAuth2Session

from .config import auto_config as ac
from .auth import open_login, generate_pkse

class NeuroStore():
    def __init__(self):
        self.oauth = OAuth2Session(ac.AUTH0_CLIENT_ID, redirect_uri=ac.REDIRECT_URI,
                            scope=ac.SCOPE)
        
    def login(self):
        # Generate a PKSE verifier and challenge
        verifier, challenge = generate_pkse()
        authorization_url, state = self.oauth.authorization_url(
            f'{ac.AUTH0_BASE_URL}/authorize', 
            audience=ac.AUTH0_AUDIENCE, code_challenge=challenge.replace('=', ''), 
            code_challenge_method='S256')

        authorization_code = open_login(authorization_url, state)

        # Fetch code
        _ = self.oauth.fetch_token(
            f'{ac.AUTH0_BASE_URL}/oauth/token',
            audience=ac.AUTH0_CLIENT_ID,
            code_verifier=verifier,
            code=authorization_code,
            include_client_id=True)