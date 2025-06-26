from models import db

class Session(db.Model):
    __tablename__ = 't_lobechat_sessions_flask'

    session_id = db.Column(db.String(100), primary_key=True)
    creation_time = db.Column(db.DateTime)
    initial_persona = db.Column(db.Text)
    session_name = db.Column(db.String(100))
    topics = db.Column(db.Text)
    domain_account = db.Column(db.String(100))


    def __init__(self, session_id, creation_time, session_name, topics, domain_account, initial_persona=None):
        self.session_id = session_id
        self.creation_time = creation_time
        self.session_name = session_name
        self.topics = topics
        self.domain_account = domain_account
        self.initial_persona = initial_persona
