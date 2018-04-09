from flask import g
from flask_restplus import Resource

from models import User, db, Logging

from ..utills.wraps_define import login_require


from .api_init import api

from ..utills.response_init import success_response


@api.route('/')
@api.response(400, '参数形式有误')
class LoggingList(Resource):

    @login_require
    def get(self):
        """列出搜索结果"""
        instances = db.session.query(Logging).filter_by(user_id=g.login_user.id).order_by(Logging.join_time.desc()).all()[:200]
        data = []
        for item in instances:
            data.append({
                "key": item.id,
                "join_time": str(item.join_time),
                "user": {
                    "username": item.user.username,
                    "nickname": item.user.nickname
                },
                "action": item.action,
                "target": item.target,
                "result": item.result
            })
        return success_response(data=data)
