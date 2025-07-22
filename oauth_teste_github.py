from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from dotenv import dotenv_values
from jose import jwt
import os
import secrets
import httpx
import json
from typing import Optional
from datetime import datetime, timedelta

# Load environment variables
config = dotenv_values(".env")

# Configuration
GITHUB_CLIENT_ID = config.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = config.get("GITHUB_CLIENT_SECRET")
GITHUB_CALLBACK_URL = "http://127.0.0.1:8000/auth/github"

# Chave secreta para JWT
JWT_SECRET = secrets.token_urlsafe(32)
JWT_ALGORITHM = "HS256"

print("client id: ", GITHUB_CLIENT_ID)
print("client secret: ", GITHUB_CLIENT_SECRET)

# FastAPI app setup
app = FastAPI(title="OAuth Demo")

# Adiciona SessionMiddleware para o OAuth
app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_urlsafe(32),
    session_cookie="oauth_session",
    max_age=3600,  # 1 hora
    same_site="lax",
    https_only=False,  # Mudar para True em produção
)

# OAuth setup
oauth = OAuth()
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


def create_token(data: dict):
    to_encode = data.copy()
    # Token expira em 1 hora
    to_encode.update({"exp": datetime.utcnow() + timedelta(hours=1)})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except:
        return None


# Routes
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <script>
                // Verifica se já está autenticado
                const token = localStorage.getItem('session_token');
                if (token) {
                    fetch('/verify-token', {
                        headers: {
                            'Authorization': 'Bearer ' + token
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.valid) {
                            window.location.href = '/profile';
                        } else {
                            localStorage.removeItem('session_token');
                        }
                    });
                }

                function openGitHubLogin() {
                    // Configurações do popup
                    const width = 600;
                    const height = 700;
                    const left = (window.innerWidth - width) / 2;
                    const top = (window.innerHeight - height) / 2;
                    
                    // Abre o popup
                    window.loginWindow = window.open(
                        '/login/github',
                        'GitHubLogin',
                        `width=${width},height=${height},top=${top},left=${left}`
                    );
                }
            </script>
        </head>
        <body>
            <h1>OAuth Demo</h1>
            <p><button onclick="openGitHubLogin()">Login with GitHub</button></p>
        </body>
    </html>
    """


@app.get("/login/{provider}")
async def login(provider: str, request: Request):
    if provider != "github":
        raise HTTPException(status_code=400, detail="Unsupported provider")

    # Usando a URL de callback fixa
    redirect_uri = GITHUB_CALLBACK_URL
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)


@app.get("/auth/github", name="auth_github")
async def auth_github(request: Request):
    try:
        token = await oauth.github.authorize_access_token(request)
        resp = await oauth.github.get("user", token=token)
        user = resp.json()
        if user:
            # Get user's email
            emails_resp = await oauth.github.get("user/emails", token=token)
            emails = emails_resp.json()
            primary_email = next(
                (email["email"] for email in emails if email["primary"]), None
            )
            user["email"] = primary_email

            # Criar JWT token
            session_token = create_token({"user": user})

            return HTMLResponse(
                f"""
                <script>
                    // Salvar token no localStorage
                    window.opener.localStorage.setItem('session_token', '{session_token}');
                    window.opener.location.href = '/profile';
                    window.close();
                </script>
            """
            )
    except Exception as e:
        print(f"Error during authentication: {str(e)}")
        return HTMLResponse(
            """
            <script>
                window.opener.location.href = '/?error=auth_failed';
                window.close();
            </script>
        """
        )
    return RedirectResponse(url="/")


@app.get("/verify-token")
async def verify_session(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse({"valid": False})

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    return JSONResponse({"valid": bool(payload)})


@app.get("/profile")
async def profile(request: Request):
    return HTMLResponse(
        """
    <html>
        <head>
            <script>
                // Verificar token ao carregar a página
                const token = localStorage.getItem('session_token');
                if (!token) {
                    window.location.href = '/';
                }

                // Carregar dados do usuário
                fetch('/user-data', {
                    headers: {
                        'Authorization': 'Bearer ' + token
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        localStorage.removeItem('session_token');
                        window.location.href = '/';
                        return;
                    }
                    document.getElementById('name').textContent = data.name || 'N/A';
                    document.getElementById('email').textContent = data.email || 'N/A';
                });

                function logout() {
                    localStorage.removeItem('session_token');
                    window.location.href = '/';
                }
            </script>
        </head>
        <body>
            <h1>Profile</h1>
            <p>Name: <span id="name">Loading...</span></p>
            <p>Email: <span id="email">Loading...</span></p>
            <p><button onclick="logout()">Logout</button></p>
        </body>
    </html>
    """
    )


@app.get("/user-data")
async def user_data(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse({"error": "No token provided"})

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        return JSONResponse({"error": "Invalid token"})

    return JSONResponse(payload["user"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
