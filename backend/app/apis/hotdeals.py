from ..services import HotdealService

from flask_restx import Resource, Namespace, reqparse

from flask import make_response
import json

from injector import inject

ns = Namespace("hotdeals", description="핫딜 정보 리스트 API", path="/hotdeals")

parser = reqparse.RequestParser()
parser.add_argument("page", type=int, default=1, help="페이지")

@ns.route("/")
class Hotdeals(Resource):

    @inject
    def __init__(self, api, svc: HotdealService, *args, **kwargs):
        self.svc = svc
        super().__init__(api, *args, **kwargs)
    
    @ns.expect(parser)
    def get(self):
        page = parser.parse_args().get("page")
        hotdeals = self.svc.get_hotdeals(page)

        return make_response(json.dumps({
            "success": True,
            "page": page,
            "data": hotdeals
        }, ensure_ascii=False, indent=4).encode("utf-8"))