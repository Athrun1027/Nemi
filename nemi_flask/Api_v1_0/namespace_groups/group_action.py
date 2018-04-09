from datetime import datetime


def group_disable(instance, db):
    instance.is_enable = False
    instance.disable_time = datetime.now()
    db.session.commit()
    return True


def group_enable(instance, db):
    instance.is_enable = True
    instance.disable_time = None
    db.session.commit()
    return True


def group_delete(instance, db):

    for item in instance.space_mine[0].bucket_kids:
        for item_file in item.file_in:
            db.session.delete(item_file)
        db.session.delete(item)
    db.session.delete(instance.space_mine[0])
    db.session.delete(instance)
    db.session.commit()
    return True
