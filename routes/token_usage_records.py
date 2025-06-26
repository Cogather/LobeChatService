from flask import Blueprint, jsonify, request
from models import db
from models.token_balance import TokenBalance
from models.token_usage_record import TokenUsageRecord

token_usage_records_bp = Blueprint('token_usage_records', __name__)

# 记录 token 消耗并更新 token 余额
@token_usage_records_bp.route('/token_usage', methods=['POST'])
def record_token_usage():
    data = request.get_json()
    domain_account = data.get('domain_account')
    model_name = data.get('model_name')
    model_version = data.get('model_version')
    used_tokens = data.get('used_tokens')
    used_type = data.get('used_type')
    message_id = data.get('message_id')

    # 查找用户当前的 token 余额
    token_balance = TokenBalance.query.filter_by(domain_account=domain_account).first()

    if not token_balance:
        return jsonify({'status': 'error', 'message': 'Token balance not found for this user'}), 404

    # 检查用户是否有足够的 token，如果不够，token为0
    if token_balance.token_count < used_tokens:
        token_balance.token_count = 0
    else:
        # 更新用户 token 余额，扣除消耗的 token 数量
        token_balance.token_count -= used_tokens
    token_balance.updated_at = db.func.now()
    db.session.commit()

    # 记录 token 消耗
    new_usage_record = TokenUsageRecord(
        domain_account=domain_account,
        model_name=model_name,
        model_version=model_version,
        used_tokens=used_tokens,
        used_type=used_type,
        message_id=message_id
    )

    db.session.add(new_usage_record)
    db.session.commit()

    return jsonify({'message': 'Token usage record added and balance updated successfully'}), 201

# 获取用户的 token 消耗记录
@token_usage_records_bp.route('/<string:domain_account>', methods=['GET'])
def get_token_usage_records(domain_account):
    usage_records = TokenUsageRecord.query.filter_by(domain_account=domain_account).all()
    if usage_records:
        return jsonify([{
            'usage_id': record.usage_id,
            'model_name': record.model_name,
            'model_version': record.model_version,
            'used_tokens': record.used_tokens,
            'used_type': record.used_type,
            'message_id': record.message_id,
            'created_at': record.created_at
        } for record in usage_records]), 200
    else:
        return jsonify({'message': 'No usage records found for this user'}), 404
