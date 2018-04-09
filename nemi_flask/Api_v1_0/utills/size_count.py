from models import db, Bucket, File

types_color = {
    "pdf": "#ff4343",
    "markdown": "#f69846",
    "ppt": "#f6d54a",
    "jpg": "#45dbf7",
    "excel": "#44aff0",
    "word": "#4777f5",
}


def user_space_count(user):
    buckets = db.session.query(Bucket).filter_by(space_id=user.space_mine[0].id).all()
    files = []
    for bucket_item in buckets:
        files += db.session.query(File).filter(File.bucket_id == bucket_item.id, File.object_type != "folder").all()
    files_size = 0
    files_types = {}
    files_types_list = []
    for item in files:
        files_size += int(item.object_size)
        if item.object_type in files_types:
            files_types[item.object_type]["value"] += 1
        else:
            if item.object_type in types_color:
                color = types_color[item.object_type]
            else:
                color = "#ad46f3"
            files_types[item.object_type] = {
                "value": 1,
                "name": item.object_type,
                "itemStyle": {
                    "normal": {
                        "color": color
                    }
                }
            }
    types_none = {
        "value": 0,
        "name": "",
        "itemStyle": {
            "normal": {
                "label": {
                    "show": False
                },
                "labelLine": {
                    "show": False
                }
            }
        }
    }
    for types_item in files_types:
        files_types_list.append(files_types[types_item])
    for x in range(0,len(files_types_list)):
        files_types_list.append(types_none)
    files_count = len(files)
    buckets_count = len(buckets)
    return buckets_count, files_count, files_size, files_types_list