from pathlib import Path
import sys
import logging

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        try:
            # 计算项目根目录 (假设此脚本在根目录某处)
            project_root = Path(__file__).parent.parent.resolve()
            log_dir = project_root / "log"
            log_dir.mkdir(exist_ok=True)

            # 控制台日志
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

            # 文件日志
            log_file = log_dir / "lobe_chat_log.log"
            file_handler = logging.FileHandler(
                log_file,
                mode='a',  # 追加模式，不覆盖旧日志
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)  # 文件记录DEBUG及以上级别
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            logger.debug("日志系统初始化完成")

        except Exception as e:
            print(f"日志初始化失败: {e}", file=sys.stderr)
            # 回退到基础控制台日志
            if not logger.handlers:
                logger.addHandler(logging.StreamHandler(sys.stdout))

    return logger