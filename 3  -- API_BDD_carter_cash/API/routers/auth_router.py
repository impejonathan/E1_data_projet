from models import User, UserCreate ,Token,  PasswordChange

from datetime import datetime, timedelta  # Ajouter cette ligne


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database.auth import verify_password, create_user, get_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES , delete_user , update_user, get_current_username , change_password, record_last_login
from models import UserCreate, Token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    record_last_login(form_data.username)  # Enregistrez la dernière connexion
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




@router.post("/register", response_model=UserCreate)
def register_new_user(user: UserCreate):
    db_user = get_user(user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Nom d'utilisateur déjà enregistré"
        )
    return create_user(user)





@router.put("/users/me", response_model=UserCreate)
def update_current_user(user: UserCreate, current_user: str = Depends(get_current_username)):
    return update_user(user, current_user)

@router.delete("/users/me")
def delete_current_user(user: UserCreate, current_user: str = Depends(get_current_username)):
    return delete_user(user.username, current_user)



from models import PasswordChange

@router.put("/users/me/password", response_model=PasswordChange)
def change_current_user_password(password_change: PasswordChange, current_user: str = Depends(get_current_username)):
    return change_password(current_user, password_change)