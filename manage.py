# -*- coding: utf-8 -*-


import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', default='0.0.0.0', help='host (default: 0.0.0.0)')
@click.option('--port', '-p', default=8001, help='port (default: 8001)')
@click.option('--debug', '-d', default=True, help='debug (default: True)')
def runserver(host, port, debug):
    from yayp.app import app
    app.run(host=str(host),
            port=int(port),
            debug=not bool(debug))


@cli.command()
def init_db():
    pass


@cli.command()
def drop_db():
    pass


if __name__ == '__main__':
    cli()