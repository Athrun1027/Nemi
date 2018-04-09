from flask import request, current_app, g
from flask_restplus import Resource
from sqlalchemy import or_
import jwt

from datetime import datetime, timedelta

from .api_init import api, come_in_login, come_out_token_success, come_out_user_login

from models import db, User

# from ..namespace_users.api_init import come_out_user_item_success

from ..utills.response_init import ProfileError, success_response
from ..utills.wraps_define import login_require
from ..utills.size_count import user_space_count


@api.route('/login/')
@api.response(400, '参数形式有误')
@api.response(404, '用户不存在')
class UserLogin(Resource):

    @api.marshal_with(come_out_user_login, code=200, description="成功返回当前登录用户!")
    @login_require
    def get(self):
        """当前登录用户"""
        user = g.login_user
        (buckets_count, files_count, files_size, files_types) = user_space_count(user)
        user.buckets_count = buckets_count
        user.files_count = files_count
        user.files_size = files_size
        user.files_types = files_types
        return success_response(data=user)

    @api.marshal_with(come_out_token_success, code=200, description="用户登录成功!")
    @api.expect(come_in_login)
    def post(self):
        """用户登录"""
        body_data = request.get_json()
        # 根据邮箱或用户名得到用户
        user = db.session.query(User).filter(or_(User.email == body_data["username"],
                                                 User.username == body_data["username"])).first()
        if user is None:
            # 用户不存在
            raise ProfileError(code=404, message={
                "username": "No enable user's username or email is {0}!".format(body_data["username"])})
        if not user.check_password(body_data["password"]):
            # 用户密码错误
            raise ProfileError(code=400, message={
                "password": "Your password is wrong!"})
        # 此刻的时间加上30分钟为过期时间
        expire_time = datetime.now() + timedelta(minutes=30)
        # 将用户ID、过期时间 通过当前工程的密钥 加密为令牌
        token = jwt.encode(
            {"user_id": user.id, "expire": expire_time.timestamp()}, key=current_app.config["SECRET_KEY"])
        # 设置最后一次登录的时间和IP地址
        user.last_login_time = datetime.now()
        user.last_login_ip = request.remote_addr
        db.session.commit()
        return success_response(data={"token": token.decode("UTF-8")})
