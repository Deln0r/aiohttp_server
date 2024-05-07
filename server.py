from aiohttp import web
import json
import hashlib
import click

async def healthcheck(request):
    """Обработчик для GET /healthcheck - возвращает пустой JSON и статус 200"""
    return web.json_response({}, status=200)

async def hash_string(request):
    """Обработчик для POST /hash - вычисляет SHA256 хэш строки"""
    try:
        data = await request.json()
        string_to_hash = data['string']
    except (json.JSONDecodeError, KeyError):
        return web.json_response({'validation_errors': 'Missing "string" field'}, status=400)

    hashed_string = hashlib.sha256(string_to_hash.encode()).hexdigest()
    return web.json_response({'hash_string': hashed_string})

app = web.Application()
app.add_routes([web.get('/healthcheck', healthcheck),
                web.post('/hash', hash_string)])

@click.command()
@click.option('--host', default='localhost', help='Host to bind.')
@click.option('--port', default=8080, help='Port to bind.')
def run_server(host, port):
    """Запускает сервер aiohttp"""
    web.run_app(app, host=host, port=port)

if __name__ == '__main__':
    run_server()