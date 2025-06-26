from models import db

class GroupApplication(db.Model):
    __tablename__ = 'group_permission_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100))
    modify_group = db.Column(db.Integer, nullable=False)
    requested_status = db.Column(db.String(20), nullable=False)
    reason_for_request = db.Column(db.Text, nullable=True)
    approved_by = db.Column(db.String(100), nullable=True)  # 审批管理员的 ID
    approved_at = db.Column(db.DateTime, nullable=True)
    approval_comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime)
    operate_type = db.Column(db.String(20))

    def __init__(self, user_name, modify_group,requested_status,operate_type, reason_for_request=None,
                 approved_by=None, approved_at=None, approval_comments=None, created_at=None):
        self.user_name = user_name
        self.modify_group = modify_group
        self.requested_status = requested_status
        self.reason_for_request = reason_for_request
        self.approved_by = approved_by
        self.approved_at = approved_at
        self.approval_comments = approval_comments
        self.created_at = created_at or db.func.now()
        self.operate_type = operate_type
    def __repr__(self):
        return f'<GroupApplication {self.request_id}>'