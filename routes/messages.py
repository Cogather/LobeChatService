from flask import Blueprint, request, jsonify
from models.message import db, Message
from datetime import datetime

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('', methods=['POST'])
def add_message():
    try:
        data = request.get_json()
        
        # 处理时间格式转换
        if 'access_time' in data and isinstance(data['access_time'], str):
            try:
                data['access_time'] = datetime.fromisoformat(data['access_time'].replace('Z', '+00:00'))
            except:
                data['access_time'] = datetime.strptime(data['access_time'], '%Y-%m-%d %H:%M:%S')
        
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
    except KeyError as e:
        return jsonify({
            'status': 'error',
            'message': f'Missing required field: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
