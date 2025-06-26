from models import db


class TokenApplication(db.Model):
    __tablename__ = 't_lobechat_token_applications'

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_account = db.Column(db.String(100))
    requested_tokens = db.Column(db.Integer, nullable=False)
    application_status = db.Column(db.Enum('pending', 'approved', 'rejected'), nullable=False)
    reason_for_request = db.Column(db.Text, nullable=True)
    approved_by = db.Column(db.String(100), nullable=True)  # 审批管理员的 ID
    approved_at = db.Column(db.DateTime, nullable=True)
    approval_comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


    def __init__(self, domain_account, requested_tokens, application_status, reason_for_request=None,
                 approved_by=None, approved_at=None, approval_comments=None, created_at=None, updated_at=None):
        self.domain_account = domain_account
        self.requested_tokens = requested_tokens
        self.application_status = application_status
        self.reason_for_request = reason_for_request
        self.approved_by = approved_by
        self.approved_at = approved_at
        self.approval_comments = approval_comments
        self.created_at = created_at or db.func.now()
        self.updated_at = updated_at or db.func.now()

    def __repr__(self):
        return f'<TokenApplication {self.request_id}>'
