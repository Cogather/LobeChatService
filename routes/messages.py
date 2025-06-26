from flask import Blueprint, request, jsonify
from models.message import db, Message

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('', methods=['POST'])
def add_message():
    data = request.get_json()
    message = Message(**data)
    db.session.add(message)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Message added successfully',
        'data': {
            'message_id': message.message_id
        }
    })
