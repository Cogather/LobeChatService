import json
from datetime import datetime

import pytest

from app import create_app
from models import db
from models.group_permission_records import GroupApplication
from models.home_page_tool import HomePageTool
from models.news_catalog import Catalog
from models.news_data import NewsData
from models.notices import Notices
from models.token_balance import TokenBalance
from models.session import Session
from models.message import Message
from models.user_access import UserAccessInfo
from models.user_favorites_data import UserFavoritesData
from models.user_group_role_link import User_Link
from models.user_info import User_Info


@pytest.fixture
def app():
    """创建测试用的 Flask 应用"""
    app = create_app("test")
    return app

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """创建测试命令行运行器"""
    return app.test_cli_runner()


@pytest.fixture
def db_session(app):
    """创建数据库会话"""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_session(db_session,sample_user_info_tool ):
    """创建示例会话"""
    session = Session(
        session_id='test_session',
        session_name='测试会话',
        initial_persona='技术专家',
        topics='',
        domain_account=sample_user_info_tool.user_name,
        creation_time=datetime.utcnow()
    )
    db_session.add(session)
    db_session.commit()
    return session





@pytest.fixture
def sample_message(db_session, sample_user_info_tool, sample_session):
    """创建示例消息"""
    message = Message(
        model_name='test_model',
        model_version='1.0',
        tool_version='1.0',
        user_input='测试输入',
        model_output='测试输出',
        sequence=1,
        access_time=datetime.utcnow(),
        persona="persona",
        session_id=sample_session.session_id,
        domain_account=sample_user_info_tool.user_name
    )
    db_session.add(message)

    message1 = Message(
        model_name='test_name',
        model_version='1.0',
        tool_version='1.0',
        user_input='测试输入',
        model_output='测试输出',
        sequence=1,
        access_time=datetime.utcnow(),
        persona="persona",
        session_id=sample_session.session_id,
        domain_account=sample_user_info_tool.user_name
    )
    db_session.add(message1)
    db_session.commit()
    return message

@pytest.fixture
def sample_home_page_tool(db_session):
    """创建示例用户"""
    mock_tool = HomePageTool(
        name="name", category_id=1, category_name="category_name",
        description="description", url="url", image_url="image_url", icon_url="icon", tags="tags", favorites=1
    )
    db_session.add(mock_tool)
    db_session.commit()
    return mock_tool

@pytest.fixture
def sample_catalog(db_session):
    """创建示例用户"""
    mock_tool = Catalog(
        value='1', label="测试", title="测试"
    )
    db_session.add(mock_tool)
    db_session.commit()
    return mock_tool

@pytest.fixture
def sample_news(db_session):
    sectionData = {
        "aaa":"text"
    }
    """创建示例用户"""
    mock_tool = NewsData(
        value='1', catalog_id=1, sectionData=json.dumps(sectionData, ensure_ascii=False), anotherData=json.dumps(sectionData, ensure_ascii=False)
    )
    db_session.add(mock_tool)
    db_session.commit()
    return mock_tool
@pytest.fixture
def sample_user_info_tool(db_session):
    """创建示例用户"""
    mock_tool = User_Info(
        user_name='test_name',
        chn_name='测试用户',
        departmentL1='测试部门1',
        departmentL2='测试部门2',
        departmentL3='测试部门3',
        departmentL4='测试部门4',
        departmentL5='测试部门5',
        departmentL6='测试部门6'
    )
    db_session.add(mock_tool)
    db_session.commit()
    return mock_tool

@pytest.fixture
def sample_user_favorites_data(db_session,sample_home_page_tool):
    """创建示例用户"""
    mock_tool = UserFavoritesData(
        user_name="test_name",
        tool_id=sample_home_page_tool.id
    )
    db_session.add(mock_tool)
    db_session.commit()
    return mock_tool

@pytest.fixture
def sample_token_balance(db_session):
    """创建示例用户"""
    mock_tool =TokenBalance (
        domain_account='test_name',
        token_count=250,
    )
    db_session.add(mock_tool)
    db_session.commit()
    return mock_tool

@pytest.fixture
def sample_user_link(db_session):
    """创建示例用户"""
    mock_tool =User_Link (
        user_name = 'test_name',
        link_group_id='1,2',
        link_role_id='2'
    )
    db_session.add(mock_tool)
    db_session.commit()
    return mock_tool

@pytest.fixture
def sample_group_permission_records(db_session):
    """创建示例用户"""
    mock_tool =GroupApplication (
        user_name = 'test_name',
        modify_group = '2',
        requested_status = "aaa",
        operate_type = "delete"
    )
    db_session.add(mock_tool)
    db_session.commit()
    return mock_tool

@pytest.fixture
def sample_notice(db_session):
    """创建示例用户"""
    mock_tool =Notices (
        notice="notice", start_time="2024-11", creator="user_name", expiration_time=2,
        expected_end_time="expected_end_time", is_valid=1, platform_id=1,type=1
    )
    db_session.add(mock_tool)
    db_session.commit()
    return mock_tool

@pytest.fixture
def sample_user_access(db_session):
    """创建示例用户"""
    mock_tool =UserAccessInfo (user_name="test1", access_time="2024-11", access_platform="platform")
    db_session.add(mock_tool)
    db_session.commit()
    return mock_tool