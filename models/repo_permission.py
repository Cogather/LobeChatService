from models import db


class RepoPermission(db.Model):
    __tablename__ = 'repo_permission'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增主键
    repo_name = db.Column(db.String(255), nullable=False, unique=True)  # 仓库名称，唯一
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())  # 更新时间

    def __init__(self, repo_name):
        """初始化 RepoPermission 对象"""
        self.repo_name = repo_name

    def __repr__(self):
        """定义对象的字符串表示"""
        return f"<RepoPermission {self.repo_name}>"
