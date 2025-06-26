from models import db


class Message(db.Model):
    __tablename__ = 't_lobechat_messages_flask'

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100))
    model_version = db.Column(db.String(100))
    tool_version = db.Column(db.String(100))
    user_input = db.Column(db.Text)
    model_output = db.Column(db.Text)
    sequence = db.Column(db.Integer)
    access_time = db.Column(db.DateTime)
    persona = db.Column(db.Text)
    api_request_content = db.Column(db.Text, nullable=True)
    api_response_content = db.Column(db.Text, nullable=True)
    session_id = db.Column(db.String(100))
    domain_account = db.Column(db.String(100))

    def __init__(self, model_name, model_version, tool_version, user_input, model_output, sequence, access_time,
                 persona, session_id, domain_account, api_request_content=None, api_response_content=None):
        self.model_name = model_name
        self.model_version = model_version
        self.tool_version = tool_version
        self.user_input = user_input
        self.model_output = model_output
        self.sequence = sequence
        self.access_time = access_time
        self.persona = persona
        self.session_id = session_id
        self.domain_account = domain_account
        self.api_request_content = api_request_content  # 可以为空，默认是 None
        self.api_response_content = api_response_content  # 可以为空，默认是 None
