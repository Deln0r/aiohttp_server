import pytest
import hashlib
from aiohttp import web
from ..myapp import healthcheck, hash_string

# Фикстура для создания клиента aiohttp и запуска приложения
@pytest.fixture
async def aiohttp_client_fixture(aiohttp_client, event_loop):
    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    app.router.add_post('/hash', hash_string)
    client = await aiohttp_client(app)
    return client

# Тест для /healthcheck
@pytest.mark.asyncio
async def test_healthcheck(aiohttp_client_fixture):
    client = await aiohttp_client_fixture
    resp = await client.get('/healthcheck')
    assert resp.status == 200
    data = await resp.text()
    assert data == '{}'

# Тесты для /hash
@pytest.mark.asyncio
async def test_hash_string_missing_string_field(aiohttp_client_fixture):
    client = await aiohttp_client_fixture
    resp = await client.post('/hash', json={})
    assert resp.status == 400
    data = await resp.json()
    assert data == {'validation_errors': 'Missing "string" field'}

@pytest.mark.asyncio
async def test_hash_string_correct_input(aiohttp_client_fixture):
    client = await aiohttp_client_fixture
    data = {'string': 'test_string'}
    resp = await client.post('/hash', json=data)
    assert resp.status == 200
    data = await resp.json()
    hashed_string = data['hash_string']
    assert hashed_string is not None

@pytest.mark.asyncio
async def test_hash_string_correct_hashing(aiohttp_client_fixture):
    client = await aiohttp_client_fixture
    data = {'string': 'test_string'}
    resp = await client.post('/hash', json=data)
    assert resp.status == 200
    response_data = await resp.json()
    hashed_string = hashlib.sha256(data['string'].encode()).hexdigest()
    assert response_data['hash_string'] == hashed_string
