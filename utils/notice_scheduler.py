from datetime import datetime
from threading import Timer
from models import db
from models.notices import Notices

class LatestNoticeChecker:
    def __init__(self, app=None, interval=300):
        self.interval = interval
        self.timer = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """初始化应用"""
        self.app = app
        # 确保在应用上下文中启动
        with app.app_context():
            self.start()

    def start(self):
        """启动定时检查"""
        if not hasattr(self, 'app'):
            raise RuntimeError("未初始化应用，请先调用init_app()")

        print("启动公告检查定时任务...")
        self._check_latest_notice()
        self._check_latest_work()
    def _check_latest_notice(self):
        """检查并更新最新公告状态"""
        with self.app.app_context():  # 确保在应用上下文中运行
            try:
                with db.session.begin():
                    latest_notice = Notices.query.filter(
                        (Notices.is_valid == 1) ,
                        (Notices.type == 1) ,
                        (Notices.platform_id == 1)
                    ).order_by(
                        Notices.start_time.desc()
                    ).first()

                    if not latest_notice:
                        print(f"[{datetime.now()}] 不存在有效公告")
                        return

                    format_code = "%Y-%m-%d %H:%M:%S"
                    datetime_obj = datetime.strptime(latest_notice.expected_end_time, format_code)
                    if datetime_obj <= datetime.now():
                        latest_notice.is_valid = 0
                        # 不需要显式commit，因为with db.session.begin()会自动提交
                        print(f"[{datetime.now()}] 最新公告已失效 (ID: {latest_notice.id})")
                    else:
                        print(f"[{datetime.now()}] 最新公告仍有效 (ID: {latest_notice.id})")
            except Exception as e:
                print(f"检查公告出错: {e}")
                db.session.rollback()

        # 设置下次检查
        self.timer = Timer(self.interval, self._check_latest_notice)
        self.timer.daemon = True
        self.timer.start()

    def _check_latest_work(self):
        """检查并更新最新公告状态"""
        with self.app.app_context():  # 确保在应用上下文中运行
            try:
                with db.session.begin():
                    latest_notice = Notices.query.filter(
                        (Notices.is_valid == 1) ,
                        (Notices.type == 2) ,
                        (Notices.platform_id == 1)
                    ).order_by(
                        Notices.start_time.desc()
                    ).first()

                    if not latest_notice:
                        print(f"[{datetime.now()}] 不存在有效work")
                        return

                    format_code = "%Y-%m-%d %H:%M:%S"
                    datetime_obj = datetime.strptime(latest_notice.expected_end_time, format_code)
                    if datetime_obj <= datetime.now():
                        latest_notice.is_valid = 0
                        # 不需要显式commit，因为with db.session.begin()会自动提交
                        print(f"[{datetime.now()}] 最新work已失效 (ID: {latest_notice.id})")
                    else:
                        print(f"[{datetime.now()}] 最新work仍有效 (ID: {latest_notice.id})")
            except Exception as e:
                print(f"检查公告出错: {e}")
                db.session.rollback()

        # 设置下次检查
        self.timer = Timer(self.interval, self._check_latest_work)
        self.timer.daemon = True
        self.timer.start()

    def stop(self):
        """停止检查"""
        if self.timer:
            self.timer.cancel()