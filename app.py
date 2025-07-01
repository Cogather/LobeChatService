from flask import Flask
from flask_cors import CORS

from config_cache import cache, CacheConfig
from routes.data_operation_api.user_access_operation import operation_api_bp
from routes.data_track.user_access_data import user_access_api_bp
from routes.home_page_api.home_page_api import home_page_api_bp
from routes.home_page_api.home_page_news_api import news_api_bp

from routes.home_page_josn.request_home_page_json_backend import home_page_backend_bp
from routes.open_ai_ecosystem_api.anthropic import anthropic_bp
from routes.open_ai_ecosystem_api.deepseek import deepseek_bp
from routes.open_ai_ecosystem_api.google import google_bp
from routes.open_ai_ecosystem_api.kimi import kimi_bp
from routes.open_ai_ecosystem_api.open_ai import open_ai_bp
from routes.security.mask_message import mask_blueprint
from routes.user_group_api import user_group_bp
from routes.user_permission.user_permission_api import users_bp
from routes.user_permission.repo_permission import repo_permissions_bp

from config import Config, Test_Config
from models import db
from routes.cloud_core import cloud_core_bp
from routes.sessions import sessions_bp
from routes.messages import messages_bp
from routes.token_balances import token_balances_bp
from routes.token_applications import token_applications_bp
from routes.token_usage_records import token_usage_records_bp
from utils.images_to_service import upload_to_server_bp
from routes.notice_api import notice_api_bp
from utils.log import setup_logger
from utils.notice_scheduler import LatestNoticeChecker

logger = setup_logger()


def create_app(config=None):
    app = Flask(__name__)
    Config.init_app(app)
    # 加载缓存配置
    if config is not None and str(config) == "test":
        Test_Config.init_app(app)
    else:
        Config.init_app(app)
    app.config.from_object(CacheConfig)
    # 初始化缓存
    cache.init_app(app)
    # 初始化数据库
    db.init_app(app)
    # 将CORS配置放在蓝图注册之前
    # 定时任务
    notice_checker = LatestNoticeChecker(app)
    notice_checker.start()
    CORS(app, supports_credentials=True, origins="*")
    # 注册蓝图
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(cloud_core_bp, url_prefix='/api/cloud_core')
    app.register_blueprint(open_ai_bp, url_prefix='/api/open_ai')
    app.register_blueprint(deepseek_bp, url_prefix='/api/deepseek')
    app.register_blueprint(google_bp, url_prefix='/api/google')
    app.register_blueprint(anthropic_bp, url_prefix='/api/anthropic')
    app.register_blueprint(kimi_bp, url_prefix='/api/kimi')
    app.register_blueprint(home_page_backend_bp, url_prefix='/api/home_page_backend')

    app.register_blueprint(token_balances_bp, url_prefix='/api/token_balances')
    app.register_blueprint(token_applications_bp, url_prefix='/api/token_applications')
    app.register_blueprint(token_usage_records_bp, url_prefix='/api/token_usage_records')
    app.register_blueprint(home_page_api_bp, url_prefix='/api/home_page_api')
    app.register_blueprint(upload_to_server_bp, url_prefix='/api/upload_to_server')
    app.register_blueprint(notice_api_bp, url_prefix='/api/notice_api')
    app.register_blueprint(user_access_api_bp, url_prefix='/api/user_access')
    app.register_blueprint(operation_api_bp, url_prefix='/api/operation_api')
    app.register_blueprint(user_group_bp, url_prefix='/api/user_group_api')
    app.register_blueprint(repo_permissions_bp, url_prefix='/api/v1/repo_permissions')
    app.register_blueprint(mask_blueprint, url_prefix='/api/security')
    app.register_blueprint(news_api_bp, url_prefix='/api/news_api')

    logger.info(f"当前数据库默认连接池大小：{app.config.get('SQLALCHEMY_POOL_SIZE')}")

    return app


import os

# 只在非测试环境下创建应用实例
if os.environ.get('TESTING') != 'true':
    application = create_app()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8000)