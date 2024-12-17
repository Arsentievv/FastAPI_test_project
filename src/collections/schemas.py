from pydantic import BaseModel, Field
from datetime import datetime


class CollectionSchemaBase(BaseModel):
    title: str = Field(description="Название", max_length=50)
    description: str | None = Field(
        default=None, max_length=500, description="Описание"
    )
    photo: str | None = Field(default=None, description="Фото")

    class ConfigDict:
        orm_mode = True


class CollectionSchemaCreate(CollectionSchemaBase):
    pass


class CollectionSchemaGet(CollectionSchemaBase):
    id: int = Field(gt=0, description="ID")
    created_at: datetime
    updated_at: datetime

