from models import db


class TokenUsageRecord(db.Model):
    __tablename__ = 't_lobechat_token_usage_records'

    usage_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_account = db.Column(db.String(100))
    model_name = db.Column(db.String(255), nullable=False)
    model_version = db.Column(db.String(50), nullable=False)
    used_tokens = db.Column(db.Integer, default=0)
    used_type = db.Column(db.Enum('input', 'output'), nullable=False)
    message_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime)


    def __init__(self, domain_account, model_name, model_version, used_tokens, used_type, message_id=None,
                 created_at=None):
        self.domain_account = domain_account
        self.model_name = model_name
        self.model_version = model_version
        self.used_tokens = used_tokens
        self.used_type = used_type
        self.message_id = message_id
        self.created_at = created_at or db.func.now()

    def __repr__(self):
        return f'<TokenUsageRecord {self.usage_id}>'
