from pydantic import BaseModel


class BaseErrorModel(BaseModel):
    detail: str


class UniqueConstraint(BaseErrorModel):
    class ConfigDict:
        json_schema_extra = {
            "example": {
                "detail": "Ошибка при проверка на уникальность"
            }
        }


class NotFound(BaseErrorModel):
    class ConfigDict:
        json_schema_extra = {"example": {
            "detail": "Объект не найден"
        }
    }
