from users.models import UserModel
from fastapi.exceptions import HTTPException
from core.security import verify_password
from core.config import get_settings
from datetime import timedelta
from core.security import create_access_token, create_refresh_token, get_token_payload
from auth.responses import TokenResponse

settings = get_settings()

async def get_token(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered",
            headers={"WWW-Authenticator": "Bearer"},
        )
        
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid login credentials",
            headers={"WWW-Authenticator": "Bearer"},
        )
    
    _verify_user_access(user=user)
    
    return await _get_user_token(user=user)

async def get_refresh_token(token, db):
    payload = get_token_payload(token=token) 
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
            headers={"WWW-Authenticator": "Bearer"},
        )
        
    user_id = payload.get("id", None)
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
            headers={"WWW-Authenticator": "Bearer"},
        )
    return await _get_user_token(user=user, refresh_token=token)
        
    
def _verify_user_access(user: UserModel):
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Your account is inactive",
            headers={"WWW-Authenticator": "Bearer"},
        )
        
    if not user.is_verified:
        # Trigger user account verification email
        raise HTTPException(
            status_code=400,
            detail="Your account is unverified, Whe have the resend the account verification email.",
            headers={"WWW-Authenticator": "Bearer"},
        )

async def _get_user_token(user: UserModel, refresh_token = None):
    payload = {"id": user.id}

    access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expire_in=access_token_expiry.seconds # in sconds
    )
