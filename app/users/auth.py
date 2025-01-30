from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from pydantic import EmailStr
from app.config import get_auth_data
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(
        to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str):
    # Тут мы попытались получить данные о пользователе по email.
    # Затем, если пользователь с таким email получен, мы проверяем
    # соответствует ли тот пароль что передал пользователь — hash-строке.
    user = await UsersDAO.find_one_or_none_by_email(email)
    if not user or verify_password(password, user.password) is False:
        return None
    return user


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
