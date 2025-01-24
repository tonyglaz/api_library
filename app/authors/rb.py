# Классы, описывающие тело запроса
from datetime import date


class RBAuthor:
    def __init__(self, author_id: int | None = None,
                 name: str | None = None,
                 biography: str | None = None,
                 birthday: date | None = None):
        self.id = author_id
        self.name = name
        self.biography = biography
        self.birthday = birthday

    def to_dict(self) -> dict:
        data = {
            'id': self.id,
            'name': self.name,
            'biography': self.biography,
            'birthday': self.birthday
        }
        filtred_data = {key: value for key,
                        value in data.items() if value is not None}
        return filtred_data
