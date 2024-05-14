import click
from aiohttp import web
from myapp import app

@click.command()
@click.option('--host', default='0.0.0.0', help='Host to bind.')
@click.option('--port', default=8080, help='Port to bind.')
def run_server(host, port):
    """Запускает сервер aiohttp"""
    web.run_app(app, host=host, port=port)

if __name__ == '__main__':
    run_server()