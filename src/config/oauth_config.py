import os
from typing import Dict
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi import FastAPI

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_CALLBACK_URL = "http://127.0.0.1:8000/api/auth/github"
FRONTEND_URL = "http://localhost:3000"
FRONTEND_CALLBACK_URL = f"{FRONTEND_URL}/auth/callback"


print("GITHUB_CLIENT_ID", GITHUB_CLIENT_ID)
print("GITHUB_CLIENT_SECRET", GITHUB_CLIENT_SECRET)

# Configurações do OAuth
oauth = OAuth()


# Configuração do GitHub OAuth
oauth.register(
    name="github",
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)
