# -*- coding: utf-8 -*-


import click


@click.group()
def cli():
    """
    Group for commands
    """
    pass


@cli.command()
@click.option('--host', '-h', default='0.0.0.0', help='runserver with specific host', show_default=True)
@click.option('--port', '-p', default=8001, help='runserver with specific port', show_default=True)
@click.option('--debug', '-d', is_flag=True, help='runserver with debug mode', default=False, show_default=True)
def runserver(host, port, debug):
    """
    Run server using flask
    """
    try:
        from yayp import app
        app.run(host=str(host),
                port=int(port),
                debug=bool(debug))
    except Exception as msg:
        print 'Failed to run server:'
        print '====================='
        print msg


@cli.command()
def init_db():
    """
    Initialize tables you defined via models
    """
    print 'Initialize DB'
    from yayp.app import db, engine
    from yayp.models import Base, __all__ as model_files
    from importlib import import_module
    for model_file in model_files:
        import_module('yayp.models.' + model_file, __name__)
        print '* Model "%s" loaded.' % model_file
    Base.metadata.create_all(bind=engine)
    db.commit()
    print '... All tables created!'
    raise SystemExit


@cli.command()
def drop_db():
    """
    Drop all of tables you defined via models
    """
    print 'Drop DB'
    from yayp.app import db, engine
    from yayp.models import Base, __all__ as model_files
    from importlib import import_module
    for model_file in model_files:
        import_module('yayp.models.' + model_file, __name__)
        print '* Model "%s" loaded.' % model_file
    Base.metadata.drop_all(bind=engine)
    db.commit()
    print '... All tables deleted!'
    raise SystemExit


if __name__ == '__main__':
    cli()