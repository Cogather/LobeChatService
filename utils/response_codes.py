class ResponseCodes:
    # 成功相关
    SUCCESS = 200  # 成功
    SUCCESS_VALID = 201  # 用户为授权用户

    # 4xx 客户端错误
    BAD_REQUEST = 400  # 错误的请求
    USER_INVALID = 401  # 用户为非授权用户

    # 5xx 服务端错误
    INTERNAL_SERVER_ERROR = 500  # 服务器内部错误

    # 消息映射
    MESSAGE = {
        SUCCESS: "Success",
    }

    @classmethod
    def get_message(cls, code):
        """根据状态码获取对应的消息"""
        return cls.MESSAGE.get(code, "Unknown error")
