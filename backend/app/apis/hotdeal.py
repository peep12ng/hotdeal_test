from ..services import HotdealService

from flask_restx import Resource, Namespace, reqparse

from flask import make_response
import json

from injector import inject

ns = Namespace("hotdeal", description="핫딜 정보를 조회, 갱신하기 위해 사용하는 API", path="/hotdeal")

parser = reqparse.RequestParser()
parser.add_argument("page", type=int, default=1, help="페이지")

@ns.route("/<string:id>")
class Hotdeal(Resource):

    @inject
    def __init__(self, api, svc: HotdealService, *args, **kwrags):
        self.svc = svc
        super().__init__(api, *args, **kwrags)
    
    @ns.response(200, "Success")
    @ns.response(500, "Failed")
    def get(self, id):
        """id에 해당하는 Hotdeal 반환"""
        hotdeal = self.svc.get_hotdeal(id)

        return make_response(json.dumps({
            "success": True,
            "id":id,
            "data": hotdeal
            }, ensure_ascii=False).encode("utf-8"))

@ns.route("/update")
class HotdealUpdate(Resource):

    @inject
    def __init__(self, api, svc: HotdealService, *args, **kwargs):
        self.svc = svc
        super().__init__(api, *args, **kwargs)
    
    def get(self):
        self.svc.update()
        return "update"
