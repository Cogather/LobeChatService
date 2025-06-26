import json
import pytest
from datetime import datetime


def test_session_model_creation(db_session):
    """测试Session模型的创建"""
    from models.session import Session
    
    session = Session(
        session_id='model_test_session',
        creation_time=datetime.utcnow(),
        session_name='模型测试会话',
        topics='测试,模型',
        domain_account='test_model_user',
        initial_persona='测试角色'
    )
    
    db_session.add(session)
    db_session.commit()
    
    # 验证创建成功
    retrieved_session = Session.query.filter_by(session_id='model_test_session').first()
    assert retrieved_session is not None
    assert retrieved_session.session_name == '模型测试会话'
    assert retrieved_session.domain_account == 'test_model_user'


def test_message_model_creation(db_session, sample_session):
    """测试Message模型的创建"""
    from models.message import Message
    
    message = Message(
        model_name='test_model',
        model_version='2.0',
        tool_version='2.0',
        user_input='模型测试输入',
        model_output='模型测试输出',
        sequence=1,
        access_time=datetime.utcnow(),
        persona='测试角色',
        session_id=sample_session.session_id,
        domain_account='test_model_user'
    )
    
    db_session.add(message)
    db_session.commit()
    
    # 验证创建成功
    retrieved_message = Message.query.filter_by(user_input='模型测试输入').first()
    assert retrieved_message is not None
    assert retrieved_message.model_name == 'test_model'
    assert retrieved_message.session_id == sample_session.session_id


def test_token_balance_model_operations(db_session):
    """测试TokenBalance模型的操作"""
    from models.token_balance import TokenBalance
    
    # 创建token余额记录
    balance = TokenBalance(
        domain_account='model_test_user',
        token_count=500
    )
    
    db_session.add(balance)
    db_session.commit()
    
    # 验证创建
    retrieved_balance = TokenBalance.query.filter_by(domain_account='model_test_user').first()
    assert retrieved_balance is not None
    assert retrieved_balance.token_count == 500
    
    # 更新余额
    retrieved_balance.token_count = 750
    db_session.commit()
    
    # 验证更新
    updated_balance = TokenBalance.query.filter_by(domain_account='model_test_user').first()
    assert updated_balance.token_count == 750


def test_token_application_model_lifecycle(db_session):
    """测试TokenApplication模型的生命周期"""
    from models.token_application import TokenApplication
    
    # 创建申请
    application = TokenApplication(
        domain_account='model_test_applicant',
        requested_tokens=1000,
        application_status='pending',
        reason_for_request='模型测试申请'
    )
    
    db_session.add(application)
    db_session.commit()
    
    # 验证创建
    retrieved_app = TokenApplication.query.filter_by(domain_account='model_test_applicant').first()
    assert retrieved_app is not None
    assert retrieved_app.application_status == 'pending'
    assert retrieved_app.requested_tokens == 1000
    
    # 审批申请
    retrieved_app.application_status = 'approved'
    retrieved_app.approved_by = 'admin_user'
    db_session.commit()
    
    # 验证审批
    approved_app = TokenApplication.query.filter_by(domain_account='model_test_applicant').first()
    assert approved_app.application_status == 'approved'
    assert approved_app.approved_by == 'admin_user'


def test_user_info_model(db_session):
    """测试UserInfo模型"""
    from models.user_info import User_Info
    
    user = User_Info(
        user_name='model_test_user_info',
        chn_name='模型测试用户',
        departmentL1='一级部门',
        departmentL2='二级部门',
        departmentL3='三级部门',
        departmentL4='四级部门',
        departmentL5='五级部门',
        departmentL6='六级部门'
    )
    
    db_session.add(user)
    db_session.commit()
    
    # 验证创建
    retrieved_user = User_Info.query.filter_by(user_name='model_test_user_info').first()
    assert retrieved_user is not None
    assert retrieved_user.chn_name == '模型测试用户'
    assert retrieved_user.departmentL1 == '一级部门'


def test_home_page_tool_model(db_session):
    """测试HomePageTool模型"""
    from models.home_page_tool import HomePageTool
    
    tool = HomePageTool(
        name='模型测试工具',
        category_id=1,
        category_name='测试分类',
        description='这是一个模型测试工具',
        url='http://test.tool.com',
        image_url='http://test.image.com',
        icon_url='http://test.icon.com',
        tags='测试,模型,工具',
        favorites=0
    )
    
    db_session.add(tool)
    db_session.commit()
    
    # 验证创建
    retrieved_tool = HomePageTool.query.filter_by(name='模型测试工具').first()
    assert retrieved_tool is not None
    assert retrieved_tool.description == '这是一个模型测试工具'
    assert retrieved_tool.category_name == '测试分类'


def test_notices_model(db_session):
    """测试Notices模型"""
    from models.notices import Notices
    
    notice = Notices(
        notice='模型测试公告内容',
        start_time='2024-01-01 10:00:00',
        creator='model_test_creator',
        expiration_time=1440,
        expected_end_time='2024-01-02 10:00:00',
        is_valid=1,
        platform_id=1,
        type=1
    )
    
    db_session.add(notice)
    db_session.commit()
    
    # 验证创建
    retrieved_notice = Notices.query.filter_by(notice='模型测试公告内容').first()
    assert retrieved_notice is not None
    assert retrieved_notice.creator == 'model_test_creator'
    assert retrieved_notice.is_valid == 1


def test_user_favorites_data_model(db_session, sample_home_page_tool, sample_user_info_tool):
    """测试UserFavoritesData模型"""
    from models.user_favorites_data import UserFavoritesData
    
    favorite = UserFavoritesData(
        user_name=sample_user_info_tool.user_name,
        tool_id=sample_home_page_tool.id
    )
    
    db_session.add(favorite)
    db_session.commit()
    
    # 验证创建
    retrieved_favorite = UserFavoritesData.query.filter_by(
        user_name=sample_user_info_tool.user_name,
        tool_id=sample_home_page_tool.id
    ).first()
    assert retrieved_favorite is not None


def test_user_access_model(db_session):
    """测试UserAccessInfo模型"""
    from models.user_access import UserAccessInfo
    
    access_info = UserAccessInfo(
        user_name='model_test_access_user',
        access_time='2024-01-01 15:30:00',
        access_platform='web'
    )
    
    db_session.add(access_info)
    db_session.commit()
    
    # 验证创建
    retrieved_access = UserAccessInfo.query.filter_by(user_name='model_test_access_user').first()
    assert retrieved_access is not None
    assert retrieved_access.access_platform == 'web'


def test_news_catalog_model(db_session):
    """测试Catalog模型"""
    from models.news_catalog import Catalog
    
    catalog = Catalog(
        value='model_test_catalog',
        label='模型测试目录',
        title='模型测试标题'
    )
    
    db_session.add(catalog)
    db_session.commit()
    
    # 验证创建
    retrieved_catalog = Catalog.query.filter_by(value='model_test_catalog').first()
    assert retrieved_catalog is not None
    assert retrieved_catalog.label == '模型测试目录'


def test_news_data_model(db_session):
    """测试NewsData模型"""
    from models.news_data import NewsData
    
    section_data = {"title": "测试新闻", "content": "这是测试新闻内容"}
    another_data = {"metadata": "测试元数据"}
    
    news = NewsData(
        value='model_test_news',
        catalog_id=1,
        sectionData=json.dumps(section_data),
        anotherData=json.dumps(another_data)
    )
    
    db_session.add(news)
    db_session.commit()
    
    # 验证创建
    retrieved_news = NewsData.query.filter_by(value='model_test_news').first()
    assert retrieved_news is not None
    assert retrieved_news.catalog_id == 1


def test_model_relationships(db_session, sample_session):
    """测试模型之间的关系"""
    from models.message import Message
    
    # 创建多个消息关联到同一个会话
    messages = []
    for i in range(3):
        message = Message(
            model_name='test_model',
            model_version='1.0',
            tool_version='1.0',
            user_input=f'测试输入 {i+1}',
            model_output=f'测试输出 {i+1}',
            sequence=i+1,
            access_time=datetime.utcnow(),
            persona='测试角色',
            session_id=sample_session.session_id,
            domain_account='test_user'
        )
        messages.append(message)
        db_session.add(message)
    
    db_session.commit()
    
    # 验证关系
    session_messages = Message.query.filter_by(session_id=sample_session.session_id).all()
    assert len(session_messages) >= 3  # 至少包含我们新增的3个消息


def test_model_field_constraints(db_session):
    """测试模型字段约束"""
    from models.session import Session
    
    # 测试创建具有边界值的记录
    session = Session(
        session_id='a' * 100,  # 长session_id
        creation_time=datetime.utcnow(),
        session_name='',  # 空session_name
        topics='',
        domain_account='test_constraint_user'
    )
    
    db_session.add(session)
    db_session.commit()
    
    # 验证可以创建
    retrieved_session = Session.query.filter_by(domain_account='test_constraint_user').first()
    assert retrieved_session is not None


def test_model_unicode_support(db_session):
    """测试模型的Unicode支持"""
    from models.session import Session
    
    unicode_content = "Unicode测试: 🚀 测试中文 🤖 Special chars: àáâãäåæçèéêë"
    
    session = Session(
        session_id='unicode_test_session',
        creation_time=datetime.utcnow(),
        session_name=unicode_content,
        topics=unicode_content,
        domain_account='unicode_test_user',
        initial_persona=unicode_content
    )
    
    db_session.add(session)
    db_session.commit()
    
    # 验证Unicode内容保存正确
    retrieved_session = Session.query.filter_by(session_id='unicode_test_session').first()
    assert retrieved_session is not None
    assert retrieved_session.session_name == unicode_content
    assert retrieved_session.topics == unicode_content