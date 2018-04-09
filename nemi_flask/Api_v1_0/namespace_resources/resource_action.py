from datetime import datetime


def resource_disable(instance, db):
    for item in instance.kids:
        resource_disable(item, db)
    instance.is_enable = False
    instance.disable_time = datetime.now()
    db.session.commit()
    return True


def get_folder_size(instance):
    folder_size = 0
    if instance.object_type != "folder":
        return instance.object_size
    for item in instance.kids:
        folder_size += get_folder_size(item)
    return folder_size


def resource_enable(instance, db):
    for item in instance.kids:
        resource_enable(item, db)
    for item in instance.share_files:
        db.session.delete(item)
    instance.is_enable = True
    instance.disable_time = None
    db.session.commit()
    return True


def resource_delete(instance, db):
    for item in instance.kids:
        resource_delete(item, db)
    if instance.object_uuid:
        # TODO 删除实体文件（或不删除，统一时间删除没有对应的文件）
        pass
    db.session.delete(instance)
    db.session.commit()
    return True
