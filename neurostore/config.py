import os
from pathlib import Path

class Common():
    KEY_DIR=Path('~/.neurostore').expanduser()
    KEY_DIR.mkdir(exist_ok=True)
    REDIRECT_URI='http://127.0.0.1:5000/callback'
    SCOPE=['profile', 'openid', 'email', 'offline_access']

class Staging(Common):
    AUTH0_CLIENT_ID="qwYFu72aLngXIwSDpIoIRyw8fVl3yQVy"
    AUTH0_TENANT="neurosynth-staging"
    AUTH0_BASE_URL=f"https://{AUTH0_TENANT}.us.auth0.com"
    AUTH0_AUDIENCE="https://neurostore.xyz/api/"

config_space = os.getenv('API_TARGET', 'STAGING')

if config_space == 'STAGING':
    auto_config = Staging
    
