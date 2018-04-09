import os


class Config(object):
    """基础配置"""
    SECRET_KEY = str(os.urandom(24))
    # 使得处理api_model会返回校验结果
    RESTPLUS_VALIDATE = True
    # 使得处理api_parser会返回校验结果
    BUNDLE_ERRORS = False
    # 默认打开API页展开所有的接口
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://athrun:packet@192.168.72.11/Nemi'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    NFS_ADDR = "/mnt/mfs"
    pass

