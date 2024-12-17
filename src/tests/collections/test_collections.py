import pytest
from src.main import app
from fastapi import status


@pytest.mark.anyio
async def test_create_collection(async_client, session):
    test_collection_data = {
        "title": "Collection 1",
        "description": "Test description",
        "photo": "Test photo url"
    }
    response = await async_client.post(url="/collections/create", json=test_collection_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_data = response.json()
    assert created_data["title"] == "Collection 1"
    assert created_data["description"] == "Test description"
    assert created_data["photo"] == "Test photo url"


@pytest.mark.anyio
async def test_same_name_collection_create(async_client, session):
    test_collection_data = {
        "title": "Collection 1",
        "description": "Test description",
        "photo": "Test photo url"
    }
    response = await async_client.post(url="/collections/create", json=test_collection_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Объект с таким именем существует"


@pytest.mark.anyio
async def test_get_all_collections(async_client, session):
    response = await async_client.get("/collections/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_collection_by_id(async_client, session):
    test_collection_data = {
        "title": "Collection 2",
        "description": "Test description 2",
        "photo": "Test photo url 2"
    }
    response = await async_client.post("/collections/create", json=test_collection_data)

    collection_id = response.json()["id"]

    response = await async_client.get(f"/collections/{collection_id}")
    got_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert got_data["id"] == collection_id


@pytest.mark.anyio
async def test_get_collection_by_title(async_client, session):
    test_collection_data = {
        "title": "Collection 3",
        "description": "Test description 3",
        "photo": "Test photo url 3"
    }
    response = await async_client.post("/collections/create", json=test_collection_data)
    collection_title = response.json()["title"]

    response = await async_client.get(f"/collections/title/{collection_title}")
    got_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert got_data["title"] == collection_title


@pytest.mark.anyio
async def test_collection_id_not_found(async_client, session):
    test_id = 10000000
    response = await async_client.get(f"/collections/{test_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Коллекции с таким ID не найдено"


@pytest.mark.anyio
async def test_collection_title_not_found(async_client, session):
    test_title = "test_not_found_title"
    response = await async_client.get(f"/collections/title/{test_title}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "коллекции с таким названием не существует"
