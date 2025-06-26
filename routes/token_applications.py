from flask import Blueprint, jsonify, request
from models import db
from models.token_application import TokenApplication
from models.token_balance import TokenBalance

token_applications_bp = Blueprint('token_applications', __name__)

# 提交 token 申请
@token_applications_bp.route('', methods=['POST'])
def submit_token_application():
    data = request.get_json()
    domain_account = data.get('domain_account')
    requested_tokens = data.get('requested_tokens')
    reason_for_request = data.get('reason_for_request')

    if domain_account is None or domain_account == '':
        return jsonify({
            'message': 'Please enter a valid employee ID',
        }), 500
    # 创建新的 TokenApplication 记录
    try:
        new_application = TokenApplication(
            domain_account=domain_account,
            requested_tokens=requested_tokens,
            application_status='pending',
            reason_for_request=reason_for_request
        )

        db.session.add(new_application)
        db.session.commit()
        # 获取新记录的 request_id
        new_request_id = new_application.request_id

        return jsonify({
            'message': 'Token application submitted successfully',
            'request_id': new_request_id  # 返回新插入记录的主键
        }), 201
    except Exception as e:
        return jsonify({
            'message': 'Submission failed',
        }), 500
    finally:
        # 释放数据库资源
        db.session.close()


# 获取用户的 token 申请记录
@token_applications_bp.route('/<string:domain_account>', methods=['GET'])
def get_token_applications(domain_account):
    applications = TokenApplication.query.filter_by(domain_account=domain_account).all()
    if applications:
        return jsonify([{
            'request_id': app.request_id,
            'domain_account': app.domain_account,
            'requested_tokens': app.requested_tokens,
            'application_status': app.application_status,
            'reason_for_request': app.reason_for_request,
            'approved_by': app.approved_by,
            'approved_at': app.approved_at,
            'approval_comments': app.approval_comments,
            'created_at': app.created_at,
            'updated_at': app.updated_at
        } for app in applications]), 200
    else:
        return jsonify({'message': 'No applications found for this user'}), 404


@token_applications_bp.route('/approve/<int:request_id>', methods=['PUT'])
def approve_token_application(request_id):
    data = request.get_json()
    application = TokenApplication.query.filter_by(request_id=request_id).first()

    if application:
        # 如果申请已经审批通过，则直接返回
        if application.application_status == 'approved':
            return jsonify({'message': 'This application has already been approved'}), 400

        # 审批通过
        application.application_status = 'approved'
        application.approved_by = data.get('approved_by')
        application.approved_at = db.func.now()
        application.approval_comments = data.get('approval_comments', '')

        # 获取对应用户的 TokenBalance 记录
        token_balance = TokenBalance.query.filter_by(domain_account=application.domain_account).first()

        if token_balance:
            # 如果 TokenBalance 已存在，增加用户的 token 数量
            token_balance.token_count += application.requested_tokens
            token_balance.updated_at = db.func.now()
        else:
            # 如果 TokenBalance 记录不存在，创建一条新的记录
            token_balance = TokenBalance(domain_account=application.domain_account,
                                         token_count=application.requested_tokens)
            db.session.add(token_balance)

        db.session.commit()
        return jsonify({'message': 'Token application approved and tokens added successfully'}), 200
    else:
        return jsonify({'message': 'Token application not found'}), 404
