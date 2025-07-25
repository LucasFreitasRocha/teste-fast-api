import inject
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from src.service.auth_service import AuthService

router = APIRouter()


@router.get("/api/auth/login/{provider}")
async def oauth_login(provider: str, request: Request, app_id: str = None):
    auth_service = inject.instance(AuthService)
    return await auth_service.oauth_login(provider, request, app_id)


@router.get("/api/auth/{provider}")
async def oauth_callback(provider: str, request: Request):
    auth_service = inject.instance(AuthService)
    return await auth_service.oauth_callback(provider, request)


@router.get("/api/auth/verify")
async def verify_session(request: Request):
    auth_service = inject.instance(AuthService)
    """Verify JWT token validity"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse({"valid": False})

    token = auth_header.split(" ")[1]
    payload = auth_service.verify_token(token)
    return JSONResponse({"valid": bool(payload)})


@router.get("/api/user")
async def get_user_data(request: Request):
    auth_service = inject.instance(AuthService)
    """Get user data from JWT token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token provided")

    token = auth_header.split(" ")[1]
    payload = auth_service.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return JSONResponse(payload["user"])
