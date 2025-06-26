from flask import Blueprint, jsonify, request
from models import db
from models.token_balance import TokenBalance

token_balances_bp = Blueprint('token_balances', __name__)

# 查询用户的 token 余额
@token_balances_bp.route('/<string:domain_account>', methods=['GET'])
def get_token_balance(domain_account):

    if not domain_account:
        return jsonify({'status': 'error', 'message': 'domain_account is required'}), 400

    token_balance = TokenBalance.query.filter_by(domain_account=domain_account).first()

    if token_balance:
        return jsonify({
            'status': 'success',
            'message': 'The query is successful.',
            'data': {
                'domain_account': token_balance.domain_account,
                'token_count': token_balance.token_count,
                'created_at': token_balance.created_at.isoformat(),
                'updated_at': token_balance.updated_at.isoformat()
            }
        }), 200
    else:
        return jsonify({'status': 'error', 'message': 'Token balance not found for this user'}), 404

# 新建用户的 token 余额（初始化为0）
@token_balances_bp.route('/new_token_balance', methods=['POST'])
def create_token_balance():
    data = request.get_json()
    domain_account = data.get('domain_account')

    if not domain_account:
        return jsonify({'status': 'error', 'message': 'domain_account is required'}), 400

    # 判断用户是否已有token余额记录
    existing_balance = TokenBalance.query.filter_by(domain_account=domain_account).first()

    if existing_balance:
        return jsonify({'status': 'error', 'message': 'Token balance already exists for this user'}), 400

    # 创建新的 TokenBalance 记录，初始 token 数量为0
    new_balance = TokenBalance(domain_account=domain_account, token_count=0)

    db.session.add(new_balance)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Token balance created successfully with 0 tokens.',
        'data': {
            'domain_account': new_balance.domain_account,
            'token_count': new_balance.token_count,
            'created_at': new_balance.created_at.isoformat(),
            'updated_at': new_balance.updated_at.isoformat()
        }
    }), 201

# 更新用户的 token 余额
@token_balances_bp.route('/<string:domain_account>', methods=['PUT'])
def update_token_balance(domain_account):
    data = request.get_json()
    token_balance = TokenBalance.query.filter_by(domain_account=domain_account).first()

    if token_balance:
        token_balance.token_count = data.get('token_count', token_balance.token_count)
        token_balance.updated_at = db.func.now()
        db.session.commit()
        return jsonify({'message': 'Token balance updated successfully'}), 200
    else:
        return jsonify({'message': 'Token balance not found for this user'}), 404
