from typing import Dict
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi import FastAPI

config = Config(".env")

# Configurações do OAuth
oauth = OAuth()

# Configuração do Google OAuth
oauth.register(
    name="google",
    client_id=config("GOOGLE_CLIENT_ID", default=None),
    client_secret=config("GOOGLE_CLIENT_SECRET", default=None),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Configuração do GitHub OAuth
oauth.register(
    name="github",
    client_id=config("GITHUB_CLIENT_ID", default=None),
    client_secret=config("GITHUB_CLIENT_SECRET", default=None),
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)
