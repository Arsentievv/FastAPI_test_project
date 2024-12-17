from pydantic import BaseModel, Field
from datetime import datetime
from src.materials.enums import MaterialType


class MaterialSchemaBase(BaseModel):
    title: str = Field(
        max_length=40, description="Название"
    )
    description: str | None = Field(
        default=None, max_length=500, description="Описание"
    )
    materials_type: MaterialType = Field(
        default=MaterialType.other, description="Тип"
    )
    photo: str | None = Field(
        default=None, description="Изображение"
    )

    class ConfigDict:
        orm_mode = True


class MaterialSchemaCreate(MaterialSchemaBase):
    pass


class MaterialSchemaGet(MaterialSchemaBase):
    id: int = Field(
        gt=0, description="ID"
    )
    created_at: datetime = Field(
        description="Дата создания"
    )
    updated_at: datetime = Field(
        description="Дата обновления"
    )

