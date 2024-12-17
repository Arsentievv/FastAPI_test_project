from sqlalchemy.ext.asyncio import AsyncSession
from src.collections.schemas import CollectionSchemaCreate
from src.collections.models import Collection
from sqlalchemy import select


class CollectionCRUD:
    @staticmethod
    async def create_collection(
            collection: CollectionSchemaCreate,
            db: AsyncSession
    ):
        result = Collection(
            title=collection.title,
            description=collection.description,
            photo=collection.photo
        )
        db.add(result)
        await db.commit()
        return result

    @staticmethod
    async def get_collection_by_id(collection_id: int, db: AsyncSession):
        query = select(Collection).filter(Collection.id == collection_id)
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()

    @staticmethod
    async def get_collection_by_title(collection_title: str, db: AsyncSession):
        query = select(Collection).filter(Collection.title == collection_title)
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()

    @staticmethod
    async def get_all_collections(db: AsyncSession):
        query = select(Collection)
        result = await db.execute(query)
        return result.scalars().all()