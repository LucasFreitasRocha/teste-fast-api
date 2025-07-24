from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from src.config.oauth_config import (
    FRONTEND_CALLBACK_URL,
    FRONTEND_URL,
    GITHUB_CALLBACK_URL,
    oauth,
)
from jose import jwt
from datetime import datetime, timedelta
import secrets
import traceback

router = APIRouter()

# JWT Configuration
JWT_SECRET = secrets.token_urlsafe(32)
JWT_ALGORITHM = "HS256"


def create_token(data: dict):
    """Create a JWT token with expiration"""
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(hours=1)})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except:
        return None


def save_user_to_database(user_info: dict):
    """
    Função para salvar usuário no banco de dados.
    Adapte esta função para seu banco de dados específico.
    """
    print(f"===  USER DATA ===")
    print(f"Name: {user_info['name']}")
    print(f"Email: {user_info['email']}")
    print(f"GitHub ID: {user_info['github_id']}")
    print(f"GitHub Login: {user_info['github_login']}")
    print(f"router ID: {user_info.get('router_id', 'N/A')}")

    # TODO: Implementar a lógica do seu banco aqui
    # Exemplo com SQLite/SQLAlchemy:
    # user = User(
    #     name=user_info['name'],
    #     email=user_info['email'],
    #     github_id=user_info['github_id'],
    #     github_login=user_info['github_login']
    # )
    # db.session.add(user)
    # db.session.commit()

    print("User would be saved to database here!")
    print("===============================")
    return True


@router.get("/api/auth/login/{provider}")
async def oauth_login(provider: str, request: Request):
    """Initiate OAuth login for specified provider"""
    # DEBUG: Inspecionar o request inicial de login
    print(f"=== DEBUG LOGIN REQUEST ({provider.upper()}) ===")
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Query params: {dict(request.query_params)}")
    print(f"Referer: {request.headers.get('referer', 'N/A')}")
    print("===========================")

    # Validate provider
    if provider not in ["github"]:  # Add other providers here in the future
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")

    # Get the OAuth client for the provider
    oauth_client = getattr(oauth, provider)

    # Configure callback URL based on provider
    if provider == "github":
        redirect_uri = GITHUB_CALLBACK_URL
    # Add other providers here:
    # elif provider == "google":
    #     redirect_uri = GOOGLE_CALLBACK_URL

    print(f"Redirect URI for {provider}: {redirect_uri}")
    return await oauth_client.authorize_redirect(request, redirect_uri)


@router.get("/api/auth/{provider}")
async def oauth_callback(provider: str, request: Request):
    """Handle OAuth callback for specified provider"""
    # DEBUG: Inspecionar o request que chega
    print(f"=== DEBUG REQUEST ({provider.upper()}) ===")
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Query params: {dict(request.query_params)}")
    print(f"Path params: {request.path_params}")
    print(f"Client: {request.client}")
    print("====================")

    # Validate provider
    if provider not in ["github"]:  # Add other providers here in the future
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")

    try:
        print(f"=== {provider.upper()} CALLBACK START ===")

        # Get the OAuth client for the provider
        oauth_client = getattr(oauth, provider)
        token = await oauth_client.authorize_access_token(request)
        print(f"OAuth Token received: {token}")

        print("=== FETCHING USER DATA ===")
        # Handle different provider APIs
        if provider == "github":
            resp = await oauth_client.get("user", token=token)
            user_data = resp.json()
            print(f"GitHub user data: {user_data}")

            # Get user's email
            print("=== FETCHING USER EMAILS ===")
            emails_resp = await oauth_client.get("user/emails", token=token)
            emails = emails_resp.json()
            print(f"GitHub emails: {emails}")

            primary_email = next(
                (email["email"] for email in emails if email["primary"]), None
            )
            print(f"Primary email found: {primary_email}")

            # Extract GitHub-specific data
            user_info = {
                "name": user_data.get("name") or user_data.get("login"),
                "email": primary_email,
                "provider": provider,
                "provider_id": user_data.get("id"),
                "provider_username": user_data.get("login"),
                # Legacy fields for backward compatibility
                "github_id": user_data.get("id"),
                "github_login": user_data.get("login"),
            }

        # Add support for other providers here:
        # elif provider == "google":
        #     user_info = {
        #         "name": user_data.get("name"),
        #         "email": user_data.get("email"),
        #         "provider": provider,
        #         "provider_id": user_data.get("sub"),
        #         "provider_username": user_data.get("email"),
        #     }

        # Add common fields
        router_id = request.session.get("router_id")
        user_info["router_id"] = router_id
        print(f"router ID recuperado da sessão: {router_id}")
        print(f"=== USER INFO EXTRACTED ===")
        print(f"User info: {user_info}")

        # Save to database
        save_user_to_database(user_info)

        # Create JWT token with minimal user data
        session_token = create_token({"user": user_info})
        print(f"=== JWT TOKEN CREATED ===")
        print(f"JWT Token: {session_token[:50]}...")

        # Redirect to frontend with token
        redirect_url = f"{FRONTEND_CALLBACK_URL}?token={session_token}"
        print(f"=== REDIRECTING TO FRONTEND ===")
        print(f"Redirect URL: {redirect_url}")
        print(f"Frontend callback URL: {FRONTEND_CALLBACK_URL}")
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        print(f"Error during authentication: {str(e)}")
        traceback.print_exc()
        return RedirectResponse(url=f"{FRONTEND_URL}?error=auth_failed")


@router.get("/api/auth/verify")
async def verify_session(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse({"valid": False})

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    return JSONResponse({"valid": bool(payload)})


@router.get("/api/user")
async def get_user_data(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token provided")

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return JSONResponse(payload["user"])
