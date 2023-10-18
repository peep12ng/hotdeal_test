from typing import Generic, TypeVar, Optional, List, Type
from abc import ABC, abstractmethod

from flask_sqlalchemy.session import Session
from flask_sqlalchemy.model import Model
from flask_sqlalchemy.query import Query

T = TypeVar("T", bound=Model)

class GenericRepository(Generic[T], ABC):

    @abstractmethod
    def get_by_id(self, id:str) -> Optional[T]:
        raise NotImplementedError()
    
    @abstractmethod
    def new(self, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    def list(self, **filters) -> List[T]:
        raise NotImplementedError()
    
    @abstractmethod
    def add(self, record: T) -> T:
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, record: T) -> T:
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def commit(self):
        raise NotImplementedError()
    
    @abstractmethod
    def close(self):
        raise NotImplementedError()
    
    @abstractmethod
    def rollback(self):
        raise NotImplementedError()

class GenericSQLRepository(GenericRepository[T], ABC):
    def __init__(self, session: Session, model_cls: Type[T]) -> None:
        self._session = session
        self._model_cls = model_cls
    
    def _construct_get_query(self, id: str) -> Query:
        query = self._model_cls.query.filter(self._model_cls.id==id)
        return query

    def get_by_id(self, id: str) -> Optional[T]:
        query = self._construct_get_query(id)
        return query.first()
    
    def _construct_list_query(self, **filters) -> Query:
        query = self._model_cls.query
        where_clauses = []
        for c, v in filters.items():
            if not hasattr(self._model_cls, c):
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self._model_cls, c)==v)
        
        print(*where_clauses)
        
        if len(where_clauses)==1:
            query = query.filter(where_clauses[0])
        elif len(where_clauses) > 1:
            query = query.filter_by(**filters)

        return query

    def new(self, **kwargs) -> T:
        return self._model_cls(**kwargs)
    
    def list(self, limit=None, offset=None, **filters) -> List[T]:
        query = self._construct_list_query(**filters)
        
        if offset is not None:
            query = query.offset(offset)
        
        if limit is not None:
            query = query.limit(limit)

        return query.all()
    
    def add(self, record: T) -> T:
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record
    
    def update(self, record: T, columns) -> T:

        _record = self.get_by_id(record.id)

        for c in columns:
            setattr(_record, c, getattr(record, c))

        self._session.flush()
        self._session.refresh(_record)
        return _record
    
    def delete(self, id: str) -> None:
        record = self.get_by_id(id)
        if record is not None:
            self._session.delete(record)
            self._session.flush()
    
    def exists(self, id: str) -> bool:
        return bool(self.get_by_id(id))
    
    def commit(self) -> None:
        self._session.commit()
    
    def rollback(self) -> None:
        self._session.rollback()
    
    def close(self) -> None:
        self._session.close()