import secrets
import traceback
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from jose import jwt
from src.config.oauth_config import FRONTEND_CALLBACK_URL, FRONTEND_URL, GITHUB_CALLBACK_URL, oauth
from src.service.domain.user_app.user_app_request import UserAppRequest
from src.service.user_app_service import UserAppService
from datetime import datetime, timedelta



JWT_SECRET = secrets.token_urlsafe(32)
JWT_ALGORITHM = "HS256"

class AuthService:
    def __init__(self, user_app_service: UserAppService):
        self.user_app_service = user_app_service

    def create_token(self, data: dict):
        """Create a JWT token with expiration"""
        to_encode = data.copy()
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=1)})
        return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

    def verify_token(self, token: str):
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except:
            return None

    async def oauth_login(self, provider: str, request: Request, app_id: str = None):
        if not app_id:
            raise HTTPException(status_code=400, detail="app_id query parameter is required")

        if provider not in ["github"]:
            raise HTTPException(
            status_code=400, detail=f"Unsupported provider: {provider}"
        )

        redirect_uri = None
        if provider == "github":
            redirect_uri = GITHUB_CALLBACK_URL

        request.session["app_id"] = app_id
        request.session["provider"] = provider

        oauth_client = getattr(oauth, provider)
        return await oauth_client.authorize_redirect(request, redirect_uri)

    async def oauth_callback(self, provider: str, request: Request):
        if provider not in ["github"]:  # Add other providers aqui no futuro
            raise HTTPException(
                status_code=400, detail=f"Unsupported provider: {provider}"
            )
        try:
            oauth_client = getattr(oauth, provider)
            token = await oauth_client.authorize_access_token(request)
            user_info = {}
            if provider == "github":
                resp = await oauth_client.get("user", token=token)
                user_data = resp.json()
                emails_resp = await oauth_client.get("user/emails", token=token)
                emails = emails_resp.json()
                primary_email = next(
                    (email["email"] for email in emails if email["primary"]), None
                )

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
            app_id = request.session.get("app_id")
            stored_provider = request.session.get("provider")
            if stored_provider != provider:
                print(
                    f"WARNING: Provider mismatch! Expected {stored_provider}, got {provider}"
                )

            user_info["app_id"] = app_id
            # Save to database
            user_app_domain = UserAppRequest(
                email=user_info["email"],
                name=user_info["name"],
                app_id=app_id,
            )
            self.user_app_service.create_user_app(user_app_domain)
            # Create JWT token with minimal user data
            session_token = self.create_token({"user": user_info})

            redirect_url = f"{FRONTEND_CALLBACK_URL}?token={session_token}"
            print(f"=== REDIRECTING TO FRONTEND ===")
            print(f"Redirect URL: {redirect_url}")
            print(f"Frontend callback URL: {FRONTEND_CALLBACK_URL}")
            return RedirectResponse(url=redirect_url)
        except Exception as e:
            print(f"Error during authentication: {str(e)}")
            traceback.print_exc()
            return RedirectResponse(url=f"{FRONTEND_URL}?error=auth_failed")
