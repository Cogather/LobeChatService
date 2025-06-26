"""
敏感信息过滤模块的单元测试
"""
import sys
import os
import unittest

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from routes.security.mask_message import (
    mask_sensitive_info,
    mask_password,
    mask_api_keys,
    mask_tokens,
    mask_private_keys,
    mask_company_names,
    mask_employee_ids,
    mask_sql_credentials,
    mask_uri_sensitive_fields
)


class TestMaskPassword(unittest.TestCase):
    """测试密码信息过滤功能"""

    def test_mask_password(self):
        """测试密码过滤"""
        test_cases = [
            # 测试格式: (原始文本, 预期结果是否包含, 预期结果是否不包含)
            ("password=secret123", "password=******", "secret123"),
            ("password: mypassword", "password: ******", "mypassword"),
            ("PASSWORD=topsecret", "PASSWORD=******", "topsecret"),
            ("PASSWORD: Admin@123", "PASSWORD: ******", "Admin@123"),
            ("passwd=1234", "passwd=******", "1234"),
            ("passwd: abcd", "passwd: ******", "abcd"),
            ("db_password='my-secret'", "db_password=******", "my-secret"),
            ("user_password:strong_password", "user_password:******", "strong_password"),
            # 嵌入在文本中的密码
            ("配置文件包含password=sensitive内容", "配置文件包含password=******内容", "sensitive"),
            ("数据库连接字符串: password:dbpass;", "数据库连接字符串: password:******;", "dbpass"),
            # 含有空格的情况
            ("password = 123456", "password = ******", "123456"),
            ("passwd = admin", "passwd = ******", "admin"),
        ]

        for test_text, should_contain, should_not_contain in test_cases:
            result = mask_password(test_text)
            self.assertIn(should_contain, result, f"应包含 '{should_contain}'，但实际结果为: '{result}'")
            self.assertNotIn(should_not_contain, result, f"不应包含 '{should_not_contain}'，但实际结果为: '{result}'")

    def test_no_password(self):
        """测试不包含密码的文本"""
        test_texts = [
            "普通文本，不含敏感信息",
            "user=admin",
            "api_endpoint=https://example.com",
            "pass the exam",  # "pass"不是独立的单词，不应被过滤
        ]

        for text in test_texts:
            result = mask_password(text)
            self.assertEqual(result, text, f"不应修改文本，但实际结果为: '{result}'")


class TestMaskApiKeys(unittest.TestCase):
    """测试API密钥过滤功能"""

    def test_mask_api_keys(self):
        """测试API密钥过滤"""
        test_cases = [
            # API密钥
            ("api_key=sk-abcdef123456", "api_key=******", "sk-abcdef123456"),
            ("api_key: xyz789", "api_key: ******", "xyz789"),
            ("API_KEY=secret_key", "API_KEY=******", "secret_key"),
            ("apikey:mykey", "apikey:******", "mykey"),
            ("api-key=test123", "api-key=******", "test123"),
            # 独立key
            ("key=value123", "key=******", "value123"),
            ("key: secretvalue", "key: ******", "secretvalue"),
            ("KEY=important", "KEY=******", "important"),
            # 嵌入在文本中
            ("配置包含api_key=sensitive_value字段", "配置包含api_key=******字段", "sensitive_value"),
            ("认证信息: key:auth_token;", "认证信息: key:******;", "auth_token"),
            # 含有空格的情况
            ("api_key = abcdefg", "api_key = ******", "abcdefg"),
            ("key = 123456", "key = ******", "123456"),
        ]

        for test_text, should_contain, should_not_contain in test_cases:
            result = mask_api_keys(test_text)
            self.assertIn(should_contain, result, f"应包含 '{should_contain}'，但实际结果为: '{result}'")
            self.assertNotIn(should_not_contain, result, f"不应包含 '{should_not_contain}'，但实际结果为: '{result}'")

    def test_no_api_keys(self):
        """测试不包含API密钥的文本"""
        test_texts = [
            "普通文本，不含敏感信息",
            "username=admin",
            "keyword=search",  # keyword不应被过滤
            "turkey dinner",  # key是单词的一部分，不应被过滤
        ]

        for text in test_texts:
            result = mask_api_keys(text)
            self.assertEqual(result, text, f"不应修改文本，但实际结果为: '{result}'")


class TestMaskTokens(unittest.TestCase):
    """测试Token过滤功能"""

    def test_mask_tokens(self):
        """测试Token过滤"""
        test_cases = [
            ("token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "token=******", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"),
            ("token: bearer12345", "token: ******", "bearer12345"),
            ("TOKEN=access123", "TOKEN=******", "access123"),
            ("access_token:xyz789", "access_token:******", "xyz789"),
            # 嵌入在文本中
            ("认证头部包含token=jwt_value信息", "认证头部包含token=******信息", "jwt_value"),
            ("请求参数: token:auth_code;", "请求参数: token:******;", "auth_code"),
            # 含有空格的情况
            ("token = abcdefg", "token = ******", "abcdefg"),
            ("refresh_token = 123456", "refresh_token = ******", "123456"),
        ]

        for test_text, should_contain, should_not_contain in test_cases:
            result = mask_tokens(test_text)
            self.assertIn(should_contain, result, f"应包含 '{should_contain}'，但实际结果为: '{result}'")
            self.assertNotIn(should_not_contain, result, f"不应包含 '{should_not_contain}'，但实际结果为: '{result}'")

    def test_no_tokens(self):
        """测试不包含Token的文本"""
        test_texts = [
            "普通文本，不含敏感信息",
            "username=admin",
            "this is a tokenizer",  # token是单词的一部分，不应被过滤
        ]

        for text in test_texts:
            result = mask_tokens(text)
            self.assertEqual(result, text, f"不应修改文本，但实际结果为: '{result}'")


class TestMaskPrivateKeys(unittest.TestCase):
    """测试私钥过滤功能"""

    def test_mask_private_keys(self):
        """测试私钥过滤"""
        # PEM格式私钥
        private_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj
MzEfYyjiWA4R4/M2bS1GB4t7NXp98C3SC6dVMvDuictGeurT8jNbvJZHtCSuYEvu
NMoSfm76oqFvAp8Gy0iz5sxjZmSnXyCdPEovGhLa0VzMaQ8s+CLOyS56YyCFGeJZ
agasNM/GrZwYgYMXOXFUoKjc7zbHfZwcEWQQf+YzWmF+WTuEH+38yAChWYbgvTW
RnLJOv9sPPIrHOALoAsCWLWe/vsLzehWImYlGM6iPGLOeYA/rA/0q4Qy6i8NN9c
aLnZ/4Opyd4rYmNXmkBIqbiTCI5J3+M75/Vh/ZLKESMgB2Q0G1DxauUnGdFLlX
AGMXtSgPAgMBAAECggEAF8Hzm6B7rBxRTPebgH9qtGmBCJWFE7mzXI69FxWudv/
-----END PRIVATE KEY-----"""

        masked_key = "-----BEGIN PRIVATE KEY-----******-----END PRIVATE KEY-----"

        result = mask_private_keys(private_key)
        self.assertIn(masked_key, result)
        self.assertNotIn("MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj", result)

    def test_private_key_in_text(self):
        """测试嵌入在文本中的私钥"""
        text_with_key = """配置文件包含以下私钥:
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj
MzEfYyjiWA4R4/M2bS1GB4t7NXp98C3SC6dVMvDuictGeurT8jNbvJZHtCSuYEvu
-----END PRIVATE KEY-----
请妥善保管"""

        result = mask_private_keys(text_with_key)
        self.assertIn("-----BEGIN PRIVATE KEY-----******-----END PRIVATE KEY-----", result)
        self.assertNotIn("MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj", result)
        self.assertIn("配置文件包含以下私钥:", result)
        self.assertIn("请妥善保管", result)

    def test_no_private_keys(self):
        """测试不包含私钥的文本"""
        test_texts = [
            "普通文本，不含敏感信息",
            "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA\n-----END PUBLIC KEY-----",
            "这不是私钥 PRIVATE KEY 只是普通文本",
        ]

        for text in test_texts:
            result = mask_private_keys(text)
            self.assertEqual(result, text, f"不应修改文本，但实际结果为: '{result}'")


class TestMaskCompanyNames(unittest.TestCase):
    """测试公司名称过滤功能"""

    def test_mask_company_names(self):
        """测试公司名称过滤（出现就替换，不论位置/边界）"""
        test_cases = [
            ("Huawei is a company", "MockCompany is a company"),
            ("HUAWEI is a company", "MockCompany is a company"),
            ("huawei is a company", "MockCompany is a company"),
            ("HuaWei is a company", "MockCompany is a company"),
            ("HUaWei is a company", "MockCompany is a company"),
            ("HuAwEi is a company", "MockCompany is a company"),
            # 测试边界情况
            ("An Huawei project", "An MockCompany project"),
            ("Working at HuaWei.", "Working at MockCompany."),
            ("Huawei,", "MockCompany,"),
            ("Huawei.", "MockCompany."),
            # 测试作为单词一部分的情况
            ("MyHuaweiProject", "MyMockCompanyProject"),  # 应该替换
            ("PreHuaweiPost", "PreMockCompanyPost"),  # 应该替换
        ]

        for test_text, expected in test_cases:
            result = mask_company_names(test_text)
            self.assertEqual(result, expected, f"期望结果为 '{expected}'，但实际结果为: '{result}'")

    def test_no_company_names(self):
        """测试不包含公司名称的文本"""
        test_texts = [
            "普通文本，不含敏感信息",
            "AI technologies",
            "Open source project",
            "OpenSource initiative",
        ]

        for text in test_texts:
            result = mask_company_names(text)
            self.assertEqual(result, text, f"不应修改文本，但实际结果为: '{result}'")


class TestMaskEmployeeIds(unittest.TestCase):
    """测试工号过滤功能"""

    def test_mask_employee_ids_with_letter_prefix(self):
        """测试带字母前缀的工号格式"""
        test_cases = [
            # 字母+00开头的8位数字
            ("员工A00123456的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("员工Z00987654的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("用户名: B00112233", "用户名: YOUR_DOMAIN_ACCOUNT"),
            ("C00445566在线", "YOUR_DOMAIN_ACCOUNT在线"),

            # 字母+300+5个数字
            ("员工A30012345的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("员工B30098765的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("用户名: C30011223", "用户名: YOUR_DOMAIN_ACCOUNT"),
            ("D30044556在线", "YOUR_DOMAIN_ACCOUNT在线"),

            # 字母+600+5个数字
            ("员工C60012345的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("员工D60098765的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("用户名: E60011223", "用户名: YOUR_DOMAIN_ACCOUNT"),
            ("F60044556在线", "YOUR_DOMAIN_ACCOUNT在线"),

            # 字母+wx+7个数字
            ("员工Ewx1234567的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("员工Fwx7654321的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("用户名: Gwx1122334", "用户名: YOUR_DOMAIN_ACCOUNT"),
            ("Hwx4455667在线", "YOUR_DOMAIN_ACCOUNT在线"),
        ]

        for test_text, expected in test_cases:
            result = mask_employee_ids(test_text)
            self.assertEqual(result, expected, f"期望结果为 '{expected}'，但实际结果为: '{result}'")

    def test_mask_employee_ids_without_letter_prefix(self):
        """测试不带字母前缀的工号格式"""
        test_cases = [
            # 纯00开头的8位数字
            ("员工00123456的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("员工00987654的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("用户名: 00112233", "用户名: YOUR_DOMAIN_ACCOUNT"),
            ("00445566在线", "YOUR_DOMAIN_ACCOUNT在线"),

            # 纯300+5个数字
            ("员工30012345的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("员工30098765的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("用户名: 30011223", "用户名: YOUR_DOMAIN_ACCOUNT"),
            ("30044556在线", "YOUR_DOMAIN_ACCOUNT在线"),

            # 纯600+5个数字
            ("员工60012345的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("员工60098765的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("用户名: 60011223", "用户名: YOUR_DOMAIN_ACCOUNT"),
            ("60044556在线", "YOUR_DOMAIN_ACCOUNT在线"),

            # 纯wx+7个数字
            ("员工wx1234567的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("员工wx7654321的账号", "员工YOUR_DOMAIN_ACCOUNT的账号"),
            ("用户名: wx1122334", "用户名: YOUR_DOMAIN_ACCOUNT"),
            ("wx4455667在线", "YOUR_DOMAIN_ACCOUNT在线"),
        ]

        for test_text, expected in test_cases:
            result = mask_employee_ids(test_text)
            self.assertEqual(result, expected, f"期望结果为 '{expected}'，但实际结果为: '{result}'")

    def test_no_employee_ids(self):
        """测试不应被过滤的类似格式"""
        test_cases = [
            # 不符合任何工号格式的文本
            ("员工A12345678的账号", "员工A12345678的账号"),  # 不再匹配旧的格式
            ("员工12345678的账号", "员工12345678的账号"),
            ("员工300的账号", "员工300的账号"),  # 数字不足
            ("员工600的账号", "员工600的账号"),  # 数字不足
            ("员工wx123的账号", "员工wx123的账号"),  # 数字不足
            ("300123456", "300123456"),  # 数字太多
            ("6001234567", "6001234567"),  # 数字太多
            ("wxabcdefg", "wxabcdefg"),  # 非数字
            ("A001", "A001"),  # 数字不足
        ]

        for test_text, expected in test_cases:
            result = mask_employee_ids(test_text)
            self.assertEqual(result, expected, f"不应修改文本，但实际结果为: '{result}'")


class TestMaskSqlCredentials(unittest.TestCase):
    """测试SQL账号信息过滤功能"""

    def test_mask_sql_credentials(self):
        """测试SQL账号信息过滤"""
        test_cases = [
            ("user=admin", "user=******", "admin"),
            ("user: root", "user: ******", "root"),
            ("USER=sa", "USER=******", "sa"),
            ("username:postgres", "username:******", "postgres"),
            ("username = web_user", "username = ******", "web_user"),
            # 嵌入在文本中
            ("连接字符串包含user=dbuser信息", "连接字符串包含user=******信息", "dbuser"),
            ("数据库配置: username:admin;", "数据库配置: username:******;", "admin"),
        ]

        for test_text, should_contain, should_not_contain in test_cases:
            result = mask_sql_credentials(test_text)
            self.assertIn(should_contain, result, f"应包含 '{should_contain}'，但实际结果为: '{result}'")
            self.assertNotIn(should_not_contain, result, f"不应包含 '{should_not_contain}'，但实际结果为: '{result}'")

    def test_no_sql_credentials(self):
        """测试不包含SQL账号信息的文本"""
        test_texts = [
            "普通文本，不含敏感信息",
            "use the function",  # use是单词的一部分，不应被过滤
            "useful information",  # user是单词的一部分，不应被过滤
        ]

        for text in test_texts:
            result = mask_sql_credentials(text)
            self.assertEqual(result, text, f"不应修改文本，但实际结果为: '{result}'")


class TestMaskUriSensitiveFields(unittest.TestCase):
    """测试URI中的敏感字段过滤功能"""

    def test_mask_http_auth(self):
        """测试HTTP认证信息过滤"""
        test_cases = [
            ("http://user:pass@example.com", "http://******:******@example.com"),
            ("https://admin:secret@secure.org", "https://******:******@secure.org"),
            ("https://user:complex%23pass@api.com/v1", "https://******:******@api.com/v1"),
            # 嵌入在文本中
            ("连接到 http://root:toor@server.com", "连接到 http://******:******@server.com"),
            ("API地址: https://api:key@service.org/v2", "API地址: https://******:******@service.org/v2"),
        ]

        for test_text, expected in test_cases:
            result = mask_uri_sensitive_fields(test_text)
            self.assertEqual(result, expected, f"期望结果为 '{expected}'，但实际结果为: '{result}'")

    def test_mask_url_params(self):
        """测试URL参数中的敏感信息过滤"""
        test_cases = [
            # 敏感参数
            ("https://api.com?apikey=123456", "https://api.com?apikey=******"),
            ("https://service.org?token=abcdef", "https://service.org?token=******"),
            ("https://auth.com?password=secret", "https://auth.com?password=******"),
            ("https://secure.net?secret=hidden", "https://secure.net?secret=******"),
            ("https://login.com?pass=12345", "https://login.com?pass=******"),
            ("https://db.org?pwd=admin", "https://db.org?pwd=******"),

            # 多个参数，混合敏感和非敏感
            ("https://api.com?apikey=123&user=john", "https://api.com?apikey=******&user=john"),
            ("https://service.org?name=test&token=abc", "https://service.org?name=test&token=******"),
            ("https://auth.com?id=1&password=secret&page=2", "https://auth.com?id=1&password=******&page=2"),

            # 嵌入在文本中
            ("请访问 https://api.com?key=value", "请访问 https://api.com?key=******"),
            ("API示例: https://example.com?token=abc&id=123", "API示例: https://example.com?token=******&id=123"),
        ]

        for test_text, expected in test_cases:
            result = mask_uri_sensitive_fields(test_text)
            self.assertEqual(result, expected, f"期望结果为 '{expected}'，但实际结果为: '{result}'")

    def test_no_uri_sensitive_fields(self):
        """测试不包含URI敏感字段的文本"""
        test_texts = [
            "普通文本，不含敏感信息",
            "https://example.com",
            "https://api.com?id=123&page=1",  # 无敏感参数
            "email: user@example.com",  # 非HTTP认证格式
        ]

        for text in test_texts:
            result = mask_uri_sensitive_fields(text)
            self.assertEqual(result, text, f"不应修改文本，但实际结果为: '{result}'")


class TestMaskSensitiveInfo(unittest.TestCase):
    """测试整体敏感信息过滤功能"""

    def test_mask_sensitive_info_comprehensive(self):
        """综合测试：测试所有类型的敏感信息过滤"""
        test_text = """
        # 配置信息
        password=secret123
        passwd: admin456
        api_key=sk-abcdef123456
        key: xyz789
        token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
        
        # 私钥
        -----BEGIN PRIVATE KEY-----
        MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj
        -----END PRIVATE KEY-----
        
        # 公司和员工信息
        公司: Huawei (也写作huawei或HUAWEI)
        员工工号: A00123456, B30012345, C60098765, Dwx1234567
        工号2: 00123456, 30012345, 60098765, wx1234567
        
        # 数据库配置
        user=dbadmin
        username: postgres
        
        # URI敏感信息
        http://user:pass@example.com
        https://api.com?apikey=123&token=abc
        """

        result = mask_sensitive_info(test_text)

        # 验证所有敏感信息是否已被过滤
        self.assertIn("password=******", result)
        self.assertIn("passwd: ******", result)
        self.assertIn("api_key=******", result)
        self.assertIn("key: ******", result)
        self.assertIn("token=******", result)
        self.assertIn("-----BEGIN PRIVATE KEY-----******-----END PRIVATE KEY-----", result)
        self.assertIn("YOUR_DOMAIN_ACCOUNT", result)
        self.assertNotIn("A00123456", result)
        self.assertNotIn("B30012345", result)
        self.assertNotIn("C60098765", result)
        self.assertNotIn("Dwx1234567", result)
        self.assertNotIn("00123456", result)
        self.assertNotIn("30012345", result)
        self.assertNotIn("60098765", result)
        self.assertNotIn("wx1234567", result)
        self.assertIn("user=******", result)
        self.assertIn("username: ******", result)
        self.assertIn("http://******:******@example.com", result)
        self.assertIn("https://api.com?apikey=******&token=******", result)

    def test_empty_input(self):
        """测试空输入"""
        self.assertEqual(mask_sensitive_info(""), "")
        self.assertEqual(mask_sensitive_info(None), None)

    def test_no_sensitive_info(self):
        """测试不包含敏感信息的文本"""
        test_text = """
        这是一段普通文本，不包含任何敏感信息。
        The quick brown fox jumps over the lazy dog.
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        """

        result = mask_sensitive_info(test_text)
        self.assertEqual(result, test_text, "不应修改不含敏感信息的文本")


if __name__ == '__main__':
    unittest.main()
