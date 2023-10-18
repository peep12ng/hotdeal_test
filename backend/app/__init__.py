from flask import Flask

from . import config as Config
from .extensions import db, migrate, scheduler, api
from .apis import hotdeal_api, hotdeals_api

from .injector import AppModule
from injector import Injector
from flask_injector import FlaskInjector

from flask_restx import Namespace
from .tasks import task2

DEFAULT_APIS = [
    hotdeal_api,
    hotdeals_api,
]

def create_app(config=None, app_name=None) -> Flask:

    if app_name is None:
        app_name = Config.DefaultConfig.PROJECT

    app = Flask(__name__)
    
    configure_app(app, config)
    configure_extensions(app, DEFAULT_APIS)
    configure_injector(app)
    
    return app

def configure_app(app:Flask, config=None):
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(Config.DefaultConfig)
    app.config["JSON_AS_ASCII"] = False

def configure_extensions(app, apis: list[Namespace]):
    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)
    api.init_app(app)

    for a in apis:
        api.add_namespace(a)

    from . import tasks
    from . import models
    scheduler.add_job(
        func=task2,
        id="update_hotdeal",
        trigger="interval",
        seconds=30,
        max_instances=1,
        start_date="2000-01-01 12:19:00",
    )
    scheduler.start()

def configure_injector(app:Flask) -> FlaskInjector:
    
    injector = Injector([AppModule(app, db, migrate)])
    
    return FlaskInjector(app=app, injector=injector)