from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from supabase import create_client, Client
from pydantic import BaseModel

from app.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Initialize Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

class SupabaseUser(BaseModel):
    id: str
    email: str

def get_current_user(token: str = Depends(oauth2_scheme)) -> SupabaseUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        response = supabase.auth.get_user(token)
        if not response.user:
            raise credentials_exception
        
        return SupabaseUser(id=response.user.id, email=response.user.email)
    except Exception as e:
        raise credentials_exception
