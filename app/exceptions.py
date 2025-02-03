from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')

IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Неверная почта или пароль')

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='Токен истек')

TokenNoFound = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Токен не найден')

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен не валидный!')

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Не найден ID пользователя')
NoUserException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Не найден пользователь')

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')

NoBookException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Книга не найдена')
NoBookCopiesAvailableException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Нет доступных экземпляров книги")

MaximumBooksException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail=" Читатель уже имеет максимальное количество книг")
