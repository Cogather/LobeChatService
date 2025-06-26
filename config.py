import base64

class Config:
    # 数据库配置 - 加密后的 URI
    URI = ("")

    # 连接池配置
    SQLALCHEMY_POOL_SIZE = 500  # 连接池大小
    SQLALCHEMY_MAX_OVERFLOW = 10  # 允许的最大溢出连接数
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def decrypt(encoded_text):
        """ 使用 base64 解密 """
        decoded_bytes = base64.b64decode(encoded_text)
        return decoded_bytes.decode('utf-8')

    @classmethod
    def init_app(cls, app):
        """ 用于在应用初始化时设置 SQLALCHEMY_DATABASE_URI """
        app.config['SQLALCHEMY_DATABASE_URI'] = cls.decrypt(cls.URI)

        # 将连接池参数传递到应用配置中
        app.config['SQLALCHEMY_POOL_SIZE'] = cls.SQLALCHEMY_POOL_SIZE
        app.config['SQLALCHEMY_MAX_OVERFLOW'] = cls.SQLALCHEMY_MAX_OVERFLOW

class Test_Config:
    # 数据库配置 - 加密后的 URI
    URI = "sqlite:///:memory:"
    TESTING = True
    # 连接池配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app):
        """ 用于在应用初始化时设置 SQLALCHEMY_DATABASE_URI """
        app.config['SQLALCHEMY_DATABASE_URI'] = cls.URI
        app.config['TESTING'] = cls.TESTING
        # 将连接池参数传递到应用配置中
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = cls.SQLALCHEMY_TRACK_MODIFICATIONS

