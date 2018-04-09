from flask import g, request, stream_with_context, Response
from flask_restplus import Resource
from models import db, File, ShareFile, User
import uuid

from ..utills.nemi_framework import ResourceCreate, ResourceList

from ..utills.wraps_define import login_require
from ..utills.response_init import success_response

from .api_init import api


@api.route('/')
@api.response(400, '参数形式有误')
class ShareCreate(ResourceCreate, ResourceList):
    model = ShareFile
    db = db

    @login_require
    def post(self):
        """创建分享文件"""
        original_id = request.json.get("original_id")
        own_id_list = request.json.get("own_id_list")
        original = self.db.session.query(File).filter_by(id=original_id).first()
        for own_id in own_id_list:
            create_data = {
                "object_name": original.object_name,
                "object_type": original.object_type,
                "object_size": original.object_size,
                "object_uuid": original.object_uuid,
                "creator_id": g.login_user.id,
                "own_id": own_id,
                "original_id": original_id,
            }
            instance = ShareFile(**create_data)
            db.session.add(instance)
            db.session.commit()
        return {"status": "success"}

    @login_require
    def get(self):
        """列出分享文件"""
        user = self.db.session.query(User).filter_by(id=g.login_user.id).first()
        share_from = user.share_from
        share_to = user.share_to
        share_from_data = []
        share_to_data = []

        for item in share_from:
            share_from_data.append({
                "id": item.id,
                "object_name": item.object_name,
                "object_type": item.object_type,
                "object_size": item.object_size,
                "original_id": item.original_id,
                "join_time": str(item.join_time),
                "creator": {
                    "creator_id": item.creator_id,
                    "creator_username": item.creator.username,
                    "creator_nickname": item.creator.nickname,
                },
                "own": {
                    "own_id": item.own_id,
                    "own_username": item.own.username,
                    "own_nickname": item.own.nickname,
                }
            })
        for item in share_to:
            share_to_data.append({
                "id": item.id,
                "object_name": item.object_name,
                "object_type": item.object_type,
                "object_size": item.object_size,
                "original_id": item.original_id,
                "join_time": str(item.join_time),
                "creator": {
                    "creator_id": item.creator_id,
                    "creator_username": item.creator.username,
                    "creator_nickname": item.creator.nickname,
                },
                "own": {
                    "own_id": item.own_id,
                    "own_username": item.own.username,
                    "own_nickname": item.own.nickname,
                }
            })
        return {"share_from": share_from_data, "share_to": share_to_data}
