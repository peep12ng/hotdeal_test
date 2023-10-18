from flask_sqlalchemy.model import Model, DefaultMeta
from typing import Tuple
from sqlalchemy import orm

def my_declarative_constructor(self, **kwargs):
    cls_ =  type(self)
    for k in kwargs:
        if hasattr(cls_, k):
            setattr(self, k, kwargs[k])

class ModelObject(Model):

    serialize_only: Tuple[str, ...] = None
    serialize_rules: Tuple[str, ...] = None
    update_only: Tuple[str, ...] = None

    def serialize(self):

        result = {}

        _columns = self.__table__.columns.keys()
        columns = []

        if self.serialize_only!=None:
            columns = list(self.serialize_only)
        elif self.serialize_rules!=None:
            columns = list(set(_columns)-set(self.serialize_rules))
        else:
            columns = list(_columns)

        for c in columns:
            result[c] = getattr(self, c)
        
        return result

Base = orm.declarative_base(
    constructor=my_declarative_constructor, metaclass=DefaultMeta, cls=ModelObject
)