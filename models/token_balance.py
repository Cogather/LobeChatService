
from models import db


class TokenBalance(db.Model):
    __tablename__ = 't_lobechat_token_balances'

    # 将 domain_account 设置为主键，去掉 token_id
    domain_account = db.Column(db.String(100), primary_key=True)
    token_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __init__(self, domain_account, token_count=0):
        self.domain_account = domain_account
        self.token_count = token_count
