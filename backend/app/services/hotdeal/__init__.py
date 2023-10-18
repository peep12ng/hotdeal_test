from injector import inject
from .quasarzone import QuasarzoneService
from ...repositories import HotdealRepository
from flask_paginate import Pagination, get_page_args

class HotdealService:

    @inject
    def __init__(self,
                quasarzone_service: QuasarzoneService,
                hotdeal_repo: HotdealRepository):
        self._services = [quasarzone_service]
        self._hotdeal_repo = hotdeal_repo
    
    def update(self):

        for svc in self._services:
            svc.update(self._hotdeal_repo)
            self._hotdeal_repo.commit()
            self._hotdeal_repo.close()
    
    def get_hotdeals(self, page=1):
        per_page = 10

        offset = 10*(page-1)

        # page, _, offset = get_page_args(per_page=per_page) # 10개씩 페이지네이션
        # page - 현재 위치한 page, 기본 1
        # offset - page에 따라 보여줄 포스트의 번호

        # total = len(self._hotdeal_repo.list(is_blind=False, is_done=False))

        _hotdeals = self._hotdeal_repo.list(per_page, offset, is_blind=False, is_done=False)

        hotdeals = {h.id:h.serialize() for h in _hotdeals}

        return hotdeals
    
    def get_hotdeal(self, id: str):

        _hotdeal = self._hotdeal_repo.get_by_id(id)

        hotdeal = _hotdeal.serialize()

        return hotdeal