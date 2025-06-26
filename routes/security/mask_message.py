"""
敏感信息过滤模块 - 提供对外部或内部传入的敏感内容进行自动脱敏的功能
"""
import re
from flask import Blueprint, request, jsonify


# 创建Blueprint
mask_blueprint = Blueprint('mask', __name__)

@mask_blueprint.route('/mask_sensitive', methods=['POST'])
def mask_sensitive():
    """
    对输入的文本进行敏感信息过滤

    请求参数:
        message (str): 需要脱敏的内容（可为代码、配置、SQL等文本）
        repo_name (str): 代码仓库名称（目前未用，可留空或随意填写）

    返回:
        JSON: 包含脱敏后的内容
    """
    try:
        # 获取请求参数
        data = request.get_json()
        if data is None:
            return jsonify({"error": "请求参数不能为空"}), 400

        message = data.get('message')
        repo_name = data.get('repo_name', '')

        if not message:
            return jsonify({"error": "message参数不能为空"}), 400

        # 执行敏感信息过滤
        masked_message = mask_sensitive_info(message)

        # 预留: 根据repo_name查询数据库，获取定制化敏感词表，继续处理（本版暂不实现）
        # TODO: 实现repo_name定制化敏感词处理

        return jsonify({"masked_message": masked_message}), 200

    except Exception as e:
        return jsonify({"error": f"处理失败: {str(e)}"}), 500


def mask_password(text):
    text = re.sub(
        r'(\b\w*password\w*\b\s*[:=]\s*)[a-zA-Z0-9_\-]+(?=[^a-zA-Z0-9_\-]|$)',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(\b\w*passwd\w*\b\s*[:=]\s*)[a-zA-Z0-9_\-]+(?=[^a-zA-Z0-9_\-]|$)',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(\b\w*password\w*\b\s*[:=]\s*)[\'"]([a-zA-Z0-9_\-]+)[\'"]',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(\b\w*passwd\w*\b\s*[:=]\s*)[\'"]([a-zA-Z0-9_\-]+)[\'"]',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(\b\w*password\w*\b\s+)[a-zA-Z0-9_\-]+(?=[^a-zA-Z0-9_\-]|$)',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(\b\w*passwd\w*\b\s+)[a-zA-Z0-9_\-]+(?=[^a-zA-Z0-9_\-]|$)',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    return text


def mask_api_keys(text):
    # 先脱敏 api_key, api-key, apikey 等带key的变量
    text = re.sub(
        r'(\b\w*api[_-]?key\w*\b\s*[:=]\s*)[a-zA-Z0-9_\-]+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(\b\w*api[_-]?key\w*\b\s*[:=]\s*)[\'"]([a-zA-Z0-9_\-]+)[\'"]',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(\b\w*api[_-]?key\w*\b\s+)[a-zA-Z0-9_\-]+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    # 只处理独立key变量，避免误伤 keyword、monkey 等
    text = re.sub(
        r'(\bkey\b\s*[:=]\s*)[a-zA-Z0-9_\-]+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(\bkey\b\s*[:=]\s*)[\'"]([a-zA-Z0-9_\-]+)[\'"]',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(\bkey\b\s+)[a-zA-Z0-9_\-]+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    return text


def mask_tokens(text):
    """
    过滤Token信息

    Args:
        text (str): 需要处理的文本

    Returns:
        str: 处理后的文本
    """
    # 匹配所有包含token的变量（例如token、access_token等）
    text = re.sub(
        r'(\b\w*token\w*\b\s*[:=]\s*)[a-zA-Z0-9_\-\.]+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    # 匹配带引号的token值
    text = re.sub(
        r'(\b\w*token\w*\b\s*[:=]\s*)[\'"]([a-zA-Z0-9_\-\.]+)[\'"]',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    # 匹配带空格的token值
    text = re.sub(
        r'(\b\w*token\w*\b\s+)[a-zA-Z0-9_\-\.]+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    # 处理冒号形式（token: xxx）
    text = re.sub(
        r'(\b\w*token\w*\b\s*:\s*)[a-zA-Z0-9_\-\.]+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    # 处理冒号+引号形式（token: "xxx"）
    text = re.sub(
        r'(\b\w*token\w*\b\s*:\s*)[\'"]([a-zA-Z0-9_\-\.]+)[\'"]',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )
    return text


def mask_private_keys(text):
    # 脱敏PEM格式私钥
    text = re.sub(
        r'-----BEGIN PRIVATE KEY-----[\s\S]*?-----END PRIVATE KEY-----',
        r'-----BEGIN PRIVATE KEY-----******-----END PRIVATE KEY-----',
        text
    )
    return text


def mask_company_names(text):
    # 全文替换所有 Huawei（忽略大小写，不用单词边界）
    return re.sub(r'Huawei', 'MockCompany', text, flags=re.IGNORECASE)


def mask_employee_ids(text):
    # 字母+00+6位数字
    text = re.sub(r'(?<![a-zA-Z0-9])[A-Za-z]00\d{6}(?=[^a-zA-Z0-9]|$)', 'YOUR_DOMAIN_ACCOUNT', text)
    # 字母+300+5位数字
    text = re.sub(r'(?<![a-zA-Z0-9])[A-Za-z]300\d{5}(?=[^a-zA-Z0-9]|$)', 'YOUR_DOMAIN_ACCOUNT', text)
    # 字母+600+5位数字
    text = re.sub(r'(?<![a-zA-Z0-9])[A-Za-z]600\d{5}(?=[^a-zA-Z0-9]|$)', 'YOUR_DOMAIN_ACCOUNT', text)
    # 字母+wx+7位数字
    text = re.sub(r'(?<![a-zA-Z0-9])[A-Za-z]wx\d{7}(?=[^a-zA-Z0-9]|$)', 'YOUR_DOMAIN_ACCOUNT', text)
    # 纯00+6位数字
    text = re.sub(r'(?<![a-zA-Z0-9])00\d{6}(?=[^a-zA-Z0-9]|$)', 'YOUR_DOMAIN_ACCOUNT', text)
    # 纯300+5位数字
    text = re.sub(r'(?<![a-zA-Z0-9])300\d{5}(?=[^a-zA-Z0-9]|$)', 'YOUR_DOMAIN_ACCOUNT', text)
    # 纯600+5位数字
    text = re.sub(r'(?<![a-zA-Z0-9])600\d{5}(?=[^a-zA-Z0-9]|$)', 'YOUR_DOMAIN_ACCOUNT', text)
    # 纯wx+7位数字
    text = re.sub(r'(?<![a-zA-Z0-9])wx\d{7}(?=[^a-zA-Z0-9]|$)', 'YOUR_DOMAIN_ACCOUNT', text)
    return text


def mask_sql_credentials(text):
    # 账号名遇到：空白、标点、或中文字符就停
    pattern = r'(user(name)?\s*[:=]\s*)([a-zA-Z0-9_\-]+)(?=(\s|;|,|\)|\]|\(|\'|\"|:|=|$|[\u4e00-\u9fa5]))'
    text = re.sub(pattern, r'\1******', text, flags=re.IGNORECASE)
    # 引号包裹
    pattern_quote = \
        r'(user(name)?\s*[:=]\s*)([\'"])[a-zA-Z0-9_\-]+([\'"])(?=(\s|;|,|\)|\]|\(|\'|\"|:|=|$|[\u4e00-\u9fa5]))'
    text = re.sub(pattern_quote, r'\1\3******\4', text, flags=re.IGNORECASE)
    return text


def mask_uri_sensitive_fields(text):
    # HTTP Basic Auth
    text = re.sub(r'(https?://)[^:/\s]+:[^@/\s]+@', r'\1******:******@', text)

    # 定义敏感参数列表
    sensitive_keys = ['key', 'token', 'secret', 'password', 'pass', 'pwd', 'apikey', 'api_key']

    # 正则找出URL参数串
    def mask_params(m):
        param_str = m.group(0)
        # 分割所有参数对
        def mask_param(param):
            # 拆分成 key 和 value
            parts = param.split('=', 1)
            if len(parts) != 2:
                return param
            key, value = parts
            lkey = key.lower().replace('-', '').replace('_', '')
            if any(sk in lkey for sk in sensitive_keys):
                return f"{key}=******"
            return param
        # 重新组装每个参数
        sep = '&' if '&' in param_str else ';'
        prefix = '?' if param_str.startswith('?') else '&'
        param_body = param_str[1:]
        masked = sep.join([mask_param(p) for p in re.split(r'[&;]', param_body)])
        return prefix + masked

    # 用 (?=[^\s\'\"\),;]+) 保证处理整段URL参数串
    text = re.sub(r'(\?[^\s\'\"\),;]+)', mask_params, text)
    text = re.sub(r'(&[^\s\'\"\),;]+)', mask_params, text)
    return text


def mask_sensitive_info(text):
    """
    对输入文本进行敏感信息过滤

    Args:
        text (str): 需要脱敏的文本内容

    Returns:
        str: 脱敏后的文本内容
    """
    if not text:
        return text

    # 应用各种过滤器
    text = mask_password(text)
    text = mask_api_keys(text)
    text = mask_tokens(text)
    text = mask_private_keys(text)
    text = mask_employee_ids(text)
    text = mask_sql_credentials(text)
    text = mask_uri_sensitive_fields(text)

    return text

