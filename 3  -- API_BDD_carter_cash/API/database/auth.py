from models import User, UserCreate , PasswordChange

from .db_connection import create_conn
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from jose import jwt
from fastapi import HTTPException, Depends ,status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Pour hacher et vérifier le mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "YOUR_SECRET_KEY"  # Remplacez par votre propre clé secrète
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username: str):
    cursor = create_conn()
    query = f"SELECT * FROM USER_API WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()
    return user

def create_user(user: UserCreate):
    cursor = create_conn()
    hashed_password = get_password_hash(user.password)
    current_date = datetime.now().strftime('%Y-%m-%d')  # Obtenez la date actuelle
    query = f"""
    INSERT INTO USER_API (username, email, full_name, hashed_password, Date_Création)
    VALUES ('{user.username}', '{user.email}', '{user.full_name}', '{hashed_password}', '{current_date}')
    """
    cursor.execute(query)
    cursor.commit()
    return user


def update_user(user: UserCreate, current_user: str):
    if user.username != current_user:
        return {"detail": "Not authorized to update this user"}
    cursor = create_conn()
    hashed_password = get_password_hash(user.password)
    query = f"""
    UPDATE USER_API
    SET email = '{user.email}', full_name = '{user.full_name}', hashed_password = '{hashed_password}'
    WHERE username = '{user.username}'
    """
    cursor.execute(query)
    cursor.commit()
    return user

def delete_user(username: str, current_user: str):
    if username != current_user:
        return {"detail": "Not authorized to delete this user"}
    cursor = create_conn()
    query = f"DELETE FROM USER_API WHERE username = '{username}'"
    cursor.execute(query)
    cursor.commit()
    return {"detail": "User deleted"}


def get_current_username(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username



def change_password(username: str, password_change: PasswordChange):
    user = get_user(username)
    if not user or not verify_password(password_change.current_password, user.hashed_password):
        return {"detail": "Incorrect current password"}
    if password_change.new_password != password_change.confirm_password:
        return {"detail": "New password and confirm password do not match"}
    hashed_password = get_password_hash(password_change.new_password)
    cursor = create_conn()
    query = f"""
    UPDATE USER_API
    SET hashed_password = '{hashed_password}'
    WHERE username = '{username}'
    """
    cursor.execute(query)
    cursor.commit()
    return {"detail": "Password updated successfully"}


def record_last_login(username: str):
    cursor = create_conn()
    current_datetime = datetime.now().isoformat()  # Obtenez la date et l'heure actuelles au format ISO
    query = f"""
    UPDATE USER_API
    SET Date_Derniere_Connexion = '{current_datetime}'
    WHERE username = '{username}'
    """
    cursor.execute(query)
    cursor.commit()
    return {"detail": "Last login recorded"}

