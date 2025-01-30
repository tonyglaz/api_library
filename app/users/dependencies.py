from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from app.exceptions import *
from datetime import datetime, timezone
from app.users.auth import get_auth_data
from app.users.dao import UsersDAO
from app.users.models import User


# достать значение ключа users_access_token из куки.
def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNoFound
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        # декодер для получения из токена декодированной полезной нагрузки (payload) JWT-токена exp, user_id  и sub
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[
                             auth_data['algorithm']])
    except JWTError:
        raise NoJwtException

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException
    user_id = payload.get("sub")
    print(user_id)
    if not user_id:
        raise NoUserIdException
    user = await UsersDAO.find_one_or_none(int(user_id))
    if not user:
        raise NoUserException
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise ForbiddenException
