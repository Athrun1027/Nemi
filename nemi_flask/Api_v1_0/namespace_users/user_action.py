from datetime import datetime


def user_disable(instance, db):
    for item in instance.file_mine:
        item.is_enable = False
        item.disable_time = datetime.now()
    db.session.commit()
    if instance.role == "admin":
        for item in instance.kids:
            user_disable(item, db)
    instance.is_enable = False
    instance.disable_time = datetime.now()
    db.session.commit()
    return True


def user_enable(instance, db):
    for item in instance.file_mine:
        item.is_enable = True
        item.disable_time = None
    db.session.commit()
    if instance.role == "admin":
        for item in instance.kids:
            user_enable(item, db)
    instance.is_enable = True
    instance.disable_time = None
    db.session.commit()
    return True


def user_delete(instance, db):
    for item in instance.file_mine:
        # TODO 根据文件和文件夹进行进一步操作
        db.session.delete(item)
    db.session.commit()
    if instance.role == "admin":
        for item in instance.kids:
            user_delete(item, db)
    for item in instance.space_mine[0].bucket_kids:
        db.session.delete(item)
    db.session.delete(instance.space_mine[0])
    db.session.delete(instance)
    db.session.commit()
    return True
