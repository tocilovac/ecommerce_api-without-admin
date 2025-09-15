from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt, ExpiredSignatureError
from app.models import User

# Use HTTPBearer for simple token-based auth
http_bearer = HTTPBearer()

# Your JWT config
SECRET_KEY = "arian"
ALGORITHM = "HS256"

# Extract and validate the current user from token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> User:
    token = credentials.credentials
    print("🔐 Token received:", token)  # Debug: show raw token

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("📦 Decoded payload:", payload)  # Debug: show decoded payload

        user_id = payload.get("sub")
        username = payload.get("username")
        role = payload.get("role")

        if user_id is None or username is None or role is None:
            print("⚠️ Missing fields in payload")  # Debug: show missing field issue
            raise HTTPException(status_code=401, detail="Invalid token payload")

        return User(id=user_id, username=username, role=role)

    except ExpiredSignatureError:
        print("⏰ Token expired")  # Debug: show expiration issue
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError as e:
        print("❌ JWT decoding error:", str(e))  # Debug: show decoding error
        raise HTTPException(status_code=401, detail="Token verification failed")

# Restrict access to admins only
def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        print("🚫 Access denied: non-admin role")  # Debug: show role issue
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
