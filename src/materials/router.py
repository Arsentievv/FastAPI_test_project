from fastapi.routing import APIRouter
from src.materials import schemas
from src.materials.crud import MaterialCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.data_base.db_connect import get_db
from src.utils.http_response_schemas import (
    NotFound
)
from src.utils.http_exceptions import (
    NotFoundError,
)
from fastapi import status



router = APIRouter(prefix="/materials", tags=["materials"])


@router.post(
    "/create",
    response_model=schemas.MaterialSchemaGet,
    description="Добавить материал"
)
async def create_material(
        material: schemas.MaterialSchemaCreate,
        db: AsyncSession = Depends(get_db)
):
    result = await MaterialCRUD.create_material(material=material, db=db)
    return result


@router.get(
    "",
    response_model=list[schemas.MaterialSchemaGet],
    status_code=200,
    description="Получаем все материалы"
)
async def get_all_materials(db: AsyncSession = Depends(get_db)):
    result = MaterialCRUD.get_all_materials(db=db)
    return await result


@router.get(
    "/title/{material_title}",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.MaterialSchemaGet,
            "description": "Получение материала по названию"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFound,
            "description": "Материал с таким названием не найден"
        }
    },
    status_code=200,
    description="Получение материала по названию"
)
async def get_material_by_title(material_title: str, db: AsyncSession = Depends(get_db)):
    result = await MaterialCRUD.get_material_by_title(db=db, title=material_title)
    if not result:
        raise NotFoundError(
            detail="Материал с таким названием не найден",
            status_code=404
        )
    return result


@router.get(
    "/id/{material_id}",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.MaterialSchemaGet,
            "description": "Детальное представление материала"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFound,
            "description": "Материал с таким ID не найден"
        }
    },
    status_code=200,
    description="Получение материала по ID"
)
async def get_material_by_id(material_id: int, db: AsyncSession = Depends(get_db)):
    result = await MaterialCRUD.get_current_material(db=db, material_id=material_id)
    if not result:
        raise NotFoundError(
            detail="Материал с таким ID не найден",
            status_code=404
        )
    return result