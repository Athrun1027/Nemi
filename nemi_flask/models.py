from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'nemi_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(40), unique=True)
    username = db.Column(db.String(40), unique=True, default=email)
    is_enable = db.Column(db.Boolean, default=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(10))
    creator_id = db.Column(db.Integer, db.ForeignKey('nemi_user.id'), nullable=True)

    nickname = db.Column(db.String(60), default=username)
    student_num = db.Column(db.String(13), nullable=True)
    school_in = db.Column(db.String(60), nullable=True)
    college_in = db.Column(db.String(60), nullable=True)
    class_in = db.Column(db.String(60), nullable=True)
    nick_call = db.Column(db.String(60), nullable=True)
    img_url = db.Column(db.String(200), nullable=True)

    permission = db.Column(db.Integer, default=0)
    is_changed = db.Column(db.Boolean, default=False)

    join_time = db.Column(db.DateTime(), default=datetime.now)
    last_login_time = db.Column(db.DateTime(), default=None, nullable=True)
    last_login_ip = db.Column(db.String(60), default=None, nullable=True)
    disable_time = db.Column(db.DateTime(), default=None, nullable=True)

    creator = db.relationship('User', remote_side=[id], backref="kids")
    # kids 创建的子用户
    # file_mine 属于该用户的资源
    # space_mine 该用户的个人空间
    # groups_mine 该用户创建的群组
    # groups 该用户加入的群组
    pass

    def check_password(self, pass_word):
        if check_password_hash(self.password, pass_word):
            return True
        return False

    def change_password(self, pass_word):
        password = generate_password_hash(pass_word, method="pbkdf2:sha256")
        self.password = password
        return True

    def __repr__(self):
        return "<Model User `{0}`>".format(self.username)


user_group = db.Table('nemi_user_group', db.Model.metadata,
                      db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                      db.Column('user_id', db.Integer, db.ForeignKey('nemi_user.id')),
                      db.Column('group_id', db.Integer, db.ForeignKey('nemi_group.id')))


class Group(db.Model):
    __tablename__ = 'nemi_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), unique=True)
    is_enable = db.Column(db.Boolean, default=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('nemi_user.id'), nullable=True)

    nickname = db.Column(db.String(60), default=name)

    join_time = db.Column(db.DateTime(), default=datetime.now)
    edit_time = db.Column(db.DateTime(), default=datetime.now)
    disable_time = db.Column(db.DateTime(), default=None, nullable=True)

    creator = db.relationship('User', foreign_keys=[creator_id], backref="groups_mine")
    users = db.relationship(
        'User',
        secondary=user_group,
        backref=db.backref('groups'))
    # space_mine 该群组的空间
    pass

    def __repr__(self):
        return "<Model Group `{0}`>".format(self.name)


class File(db.Model):
    __tablename__ = 'nemi_file'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    object_name = db.Column(db.String(60))
    object_type = db.Column(db.String(20), default="folder")
    object_size = db.Column(db.Integer, default=0)
    object_uuid = db.Column(db.String(100), nullable=True)
    is_enable = db.Column(db.Boolean, default=True)

    creator_id = db.Column(db.Integer, db.ForeignKey('nemi_user.id'))
    folder_id = db.Column(db.Integer, db.ForeignKey('nemi_file.id'), nullable=True)
    bucket_id = db.Column(db.Integer, db.ForeignKey('nemi_bucket.id'), nullable=True)

    join_time = db.Column(db.DateTime(), default=datetime.now)
    open_time = db.Column(db.DateTime(), default=None, nullable=True)
    edit_time = db.Column(db.DateTime(), default=datetime.now)
    disable_time = db.Column(db.DateTime(), default=None, nullable=True)

    folder = db.relationship('File', remote_side=[id], backref="kids")
    creator = db.relationship('User', backref="file_mine")
    bucket = db.relationship('Bucket', backref="file_in")
    # kids 属于该文件夹的资源
    # space_root 如果该资源为根目录，则此字段指向所在空间，目前无用处

    pass

    def __repr__(self):
        return "<Model FileOrFolder `{0}`>".format(self.object_name)


class ShareFile(db.Model):
    __tablename__ = 'nemi_share_file'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    object_name = db.Column(db.String(60))
    object_type = db.Column(db.String(20), default="folder")
    object_size = db.Column(db.Integer, default=0)
    object_uuid = db.Column(db.String(100), nullable=True)
    is_enable = db.Column(db.Boolean, default=True)

    creator_id = db.Column(db.Integer, db.ForeignKey('nemi_user.id'))
    own_id = db.Column(db.Integer, db.ForeignKey('nemi_user.id'))
    original_id = db.Column(db.Integer, db.ForeignKey('nemi_file.id'))

    join_time = db.Column(db.DateTime(), default=datetime.now)

    creator = db.relationship('User', foreign_keys=[creator_id], backref="share_from")
    own = db.relationship('User', foreign_keys=[own_id], backref="share_to")
    original = db.relationship('File', foreign_keys=[original_id], backref="share_files")

    pass

    def __repr__(self):
        return "<Model ShareFile `{0}`>".format(self.object_name)


class Space(db.Model):
    __tablename__ = 'nemi_space'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    space_type = db.Column(db.String(40))
    own_user_id = db.Column(db.Integer, db.ForeignKey('nemi_user.id'), nullable=True)
    own_group_id = db.Column(db.Integer, db.ForeignKey('nemi_group.id'), nullable=True)
    root_folder_id = db.Column(db.Integer, db.ForeignKey('nemi_file.id'), nullable=True)

    join_time = db.Column(db.DateTime(), default=datetime.now)

    root_folder = db.relationship('File', backref="space_root", uselist=False)
    own_user = db.relationship('User', backref="space_mine", uselist=False)
    own_group = db.relationship('Group', backref="space_mine", uselist=False)
    # bucket_kids 该空间内的桶
    pass

    def __repr__(self):
        return "<Model Space `{0}`>".format(self.name)


class Bucket(db.Model):
    __tablename__ = 'nemi_bucket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60))
    space_id = db.Column(db.Integer, db.ForeignKey('nemi_space.id'))
    s3_access_key = db.Column(db.String(100), nullable=True)
    s3_secret_key = db.Column(db.String(200), nullable=True)
    join_time = db.Column(db.DateTime(), default=datetime.now)

    space = db.relationship('Space', backref="bucket_kids")
    # file_in 在该桶内部的文件(无文件夹)
    pass

    def __repr__(self):
        return "<Model Bucket `{0}`>".format(self.name)


tag_file = db.Table('nemi_tag_file', db.Model.metadata,
                    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                    db.Column('tag_id', db.Integer, db.ForeignKey('nemi_tag.id')),
                    db.Column('file_id', db.Integer, db.ForeignKey('nemi_file.id')))


class Tag(db.Model):
    __tablename__ = 'nemi_tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    join_time = db.Column(db.DateTime(), default=datetime.now)

    files = db.relationship(
        'File',
        secondary=tag_file,
        backref=db.backref('tags'))
    pass

    def __repr__(self):
        return "<Model Tag `{0}`>".format(self.name)


class Message(db.Model):
    __tablename__ = 'nemi_message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_from_id = db.Column(db.Integer, db.ForeignKey('nemi_user.id'), nullable=True)
    user_to_id = db.Column(db.Integer, db.ForeignKey('nemi_user.id'), nullable=True)
    contant = db.Column(db.String(100), nullable=True)
    checked = db.Column(db.Boolean, default=False)
    last_login_time = db.Column(db.DateTime(), default=None, nullable=True)

    user_from = db.relationship('User', foreign_keys=[user_from_id], backref="message_sent")
    user_to = db.relationship('User', foreign_keys=[user_to_id], backref="message_received")

    pass

    def __repr__(self):
        return "<Model Message `{0}`>".format(self.last_login_time)


class Logging(db.Model):
    __tablename__ = 'nemi_logging'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    join_time = db.Column(db.DateTime(), default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('nemi_user.id'))
    action = db.Column(db.String(100))
    target = db.Column(db.String(300))
    result = db.Column(db.String(100))

    user = db.relationship('User', foreign_keys=[user_id], backref="all_logging")

    pass

    def __repr__(self):
        return "<Model Logging `{0}`>".format(self.join_time)
