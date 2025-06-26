from flask import Blueprint, request, jsonify
from models.session import db, Session

sessions_bp = Blueprint('sessions', __name__)

from datetime import datetime

@sessions_bp.route('', methods=['POST'])
def create_session():
    try:
        data = request.get_json()
        
        # 验证必需字段
        if not data.get('session_id'):
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: session_id'
            }), 400
            
        if not data.get('session_name'):
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: session_name'
            }), 400

        # 如果 'creation_time' 字段存在，则使用它；否则使用当前时间
        creation_time_str = data.get('creation_time')

        if creation_time_str:
            # 如果传递了 creation_time，则转换为 datetime 对象
            creation_time = datetime.fromisoformat(creation_time_str)  # 或使用其他格式的解析方式
        else:
            # 如果没有传递 creation_time，使用当前时间
            creation_time = datetime.utcnow()

        new_session = Session(
            session_id=data['session_id'],
            creation_time=creation_time,
            initial_persona=data.get('initial_persona'),
            session_name=data['session_name'],
            topics=data.get('topics', ''),
            domain_account=data.get('domain_account')
        )

        db.session.add(new_session)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Session created successfully',
            'data': {
                'session_id': new_session.session_id,
                'session_name': new_session.session_name
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@sessions_bp.route('/<session_id>', methods=['PUT'])
def update_session(session_id):
    data = request.get_json()
    session = Session.query.get_or_404(session_id)
    session.initial_persona = data.get('initial_persona', session.initial_persona)
    session.session_name = data.get('session_name', session.session_name)
    session.topics = data.get('topics', session.topics)

    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Session updated successfully',
        'data': {
            'session_id': session.session_id,
            'session_name': session.session_name
        }
    })
