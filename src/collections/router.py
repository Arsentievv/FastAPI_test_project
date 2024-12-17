from fastapi import APIRouter, Depends, status
from src.collections import schemas
from src.utils.http_response_schemas import NotFound, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession
from src.data_base.db_connect import get_db
from src.collections.crud import CollectionCRUD
from src.utils.http_exceptions import NotFoundError, UniqueConstraintError


router = APIRouter(prefix="/collections", tags=["collections"])


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "model": list[schemas.CollectionSchemaGet],
            "description": "Получение всех коллекций"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFound,
            "description": "Нет созданных коллекций"
        }
    },
    description="Получить все коллекции",
    status_code=status.HTTP_200_OK
)
async def get_all_collections(db: AsyncSession = Depends(get_db)):
    result = await CollectionCRUD.get_all_collections(db=db)
    if not result:
        raise NotFoundError(detail="Объекты не найдены", status_code=status.HTTP_404_NOT_FOUND)
    return result


@router.post(
    "/create",
    responses={
        status.HTTP_201_CREATED: {
            "model": schemas.CollectionSchemaGet,
            "description": "создание коллекции"
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": UniqueConstraint,
            "description": "ошибка уникальности"
        }
    },
    status_code=status.HTTP_201_CREATED,
    description="создание коллекции"
)
async def create_collection(
        collection: schemas.CollectionSchemaCreate, db: AsyncSession = Depends(get_db)
):
    name_exits = await CollectionCRUD.get_collection_by_title(
        db=db, collection_title=collection.title
    )
    if name_exits:
        raise UniqueConstraintError(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Объект с таким именем существует"
        )
    new_collection = await CollectionCRUD.create_collection(collection=collection, db=db)
    return new_collection


@router.get(
    "/{collection_id}",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.CollectionSchemaGet,
            "description": "get collection by ID"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFound,
            "description": "Коллекция не существует"
        }
    },
    status_code=status.HTTP_200_OK,
    description="Получить коллекцию по ID"
)
async def get_collection_by_id(
        collection_id: int, db: AsyncSession = Depends(get_db)
):
    result = await CollectionCRUD.get_collection_by_id(
        collection_id=collection_id, db=db
    )
    if not result:
        raise NotFoundError(
            status_code=status.HTTP_404_NOT_FOUND, detail="Коллекции с таким ID не найдено"
        )
    return result


@router.get(
    "/title/{collection_title}",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.CollectionSchemaGet,
            "description": "получить коллекцию по имени"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFound,
            "description": "получить коллекцию по названию"
        }
    },
    status_code=status.HTTP_200_OK,
    description="получить коллекцию по названию"
)
async def get_collection_by_title(
        collection_title: str, db: AsyncSession = Depends(get_db)
):
    result = await CollectionCRUD.get_collection_by_title(
        collection_title=collection_title, db=db
    )
    if not result:
        raise NotFoundError(
            status_code=status.HTTP_404_NOT_FOUND, detail="коллекции с таким названием не существует"
        )
    return result
