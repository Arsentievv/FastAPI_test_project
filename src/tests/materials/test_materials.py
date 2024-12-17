import pytest


@pytest.mark.anyio
async def test_create_material(async_client, session):
    material_data = {
        "title": "Material 1",
        "description": "A description of Material 1",
        "materials_type": "Прочее",
        "photo": "string"
    }

    response = await async_client.post("/materials/create", json=material_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Material 1"
    assert response.json()["description"] == "A description of Material 1"


@pytest.mark.anyio
async def test_get_all_materials(async_client, session):
    response = await async_client.get("/materials")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_material_by_title(async_client, session):
    material_data = {
        "title": "Material 2",
        "description": "A description of Material 2",
        "materials_type": "Прочее",
        "photo": "image_url_2"
    }

    await async_client.post("/materials/create", json=material_data)

    response = await async_client.get("/materials/title/Material 2")
    assert response.status_code == 200
    assert response.json()["title"] == "Material 2"


@pytest.mark.anyio
async def test_get_material_by_id(async_client, session):
    material_data = {
        "title": "Material 3",
        "description": "A description of Material 3",
        "materials_type": "Прочее",
        "photo": "image_url_3"
    }

    response = await async_client.post("/materials/create", json=material_data)
    material_id = response.json()["id"]

    response = await async_client.get(f"/materials/id/{material_id}")
    assert response.status_code == 200
    assert response.json()["id"] == material_id


# Test getting a material by title that does not exist
@pytest.mark.anyio
async def test_get_material_by_title_not_found(async_client, session):
    response = await async_client.get("/materials/title/Nonexistent Material")
    assert response.status_code == 404
    assert response.json()["detail"] == "Материал с таким названием не найден"


# Test getting a material by ID that does not exist
@pytest.mark.anyio
async def test_get_material_by_id_not_found(async_client, session):
    response = await async_client.get("/materials/id/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Материал с таким ID не найден"