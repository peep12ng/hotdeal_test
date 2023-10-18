from injector import Module, singleton
from flask_sqlalchemy.session import Session

class AppModule(Module):
    def __init__(self, app, db, migrate):
        self.app = app
        self.db = db
        self.migrate = migrate
    
    def configure(self, binder):
        binder.bind(Session, to=self.db.session, scope=singleton)