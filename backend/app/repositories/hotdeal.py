from abc import ABC, abstractmethod

from .generic import GenericRepository, GenericSQLRepository
from flask_sqlalchemy.session import Session
from injector import inject
from typing import List

from ..models import HotdealModel

from datetime import datetime, timedelta

class HotdealRepositoryBase(GenericRepository[HotdealModel], ABC):
    @abstractmethod
    def list_by_scrape_at(self) -> List[HotdealModel]:
        pass
    

class HotdealRepository(GenericSQLRepository[HotdealModel], HotdealRepositoryBase):
    @inject
    def __init__(self, session: Session) -> None:
        super().__init__(session, HotdealModel)
        print(session)
    
    def list_by_scrape_at(self, **filters) -> List[HotdealModel]:
        now = datetime.now()
        at = now - timedelta.day(5)
        query = self._construct_list_query(**filters)
        query = query.filter(getattr(self._model_cls, "scrape_at") > at)
        return query.all()