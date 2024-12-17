from src.materials.schemas import MaterialSchemaCreate
from sqlalchemy.ext.asyncio import AsyncSession
from src.materials.models import Material
from sqlalchemy import select
from fastapi import HTTPException, status


class MaterialCRUD:
    @staticmethod
    async def create_material(
        material: MaterialSchemaCreate, db: AsyncSession
    ):
        result = Material(
            title=material.title,
            description=material.description,
            materials_type=material.materials_type,
            photo=material.photo
        )

        db.add(result)
        await db.commit()
        return result

    @staticmethod
    async def get_current_material(material_id: int, db: AsyncSession):
        query = select(Material).filter(Material.id == material_id)
        current_material = await db.execute(query)
        return current_material.unique().scalar_one_or_none()

    @staticmethod
    async def get_all_materials(db: AsyncSession):
        query = select(Material)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_material_by_title(db: AsyncSession, title: str):
        query = select(Material).filter(Material.title == title)
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()