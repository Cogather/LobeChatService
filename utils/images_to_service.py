
import requests
from flask import Blueprint, request, jsonify
upload_to_server_bp = Blueprint('upload_to_server', __name__)
# 文件上传
@upload_to_server_bp.route('/upload', methods=['POST'])
def upload_to_server():
    # 获取上传的图片名
    if 'file' not in request.files:
        print("没有文件上传")
        return jsonify({'error': '没有文件上传'}), 400

        # 获取上传的文件
    uploaded_file = request.files['file']

    # 上传服务器
    url = "http://fuyao.rnd.huawei.com/resource/resource-management/v1/storage/file"
    file_dir = "lobechat/home_page/images"  # 文件在服务器上的存放路径
    data = {
        'fileDir': file_dir
    }
    # 使用 with 语句打开文件
    with uploaded_file.stream as f:
        # 使用 files 参数指定要上传的文件
        files = [('uploadFile', (uploaded_file.filename, f))]
        # 发起请求
        response = requests.post(url, files=files, data=data, verify=False)

    # 处理响应
    try:
        response_data = response.json()
        if response.status_code == 200 and response_data.get('meta', {}).get('success', False):
            print("文件上传成功，返回路径: %s", response_data.get('data'))
            result_url = f"http://fuyao.rnd.huawei.com/resource/resource-management/v1/storage/file?fileName={uploaded_file.filename}&fileDir={file_dir}"
            return jsonify({'message': '上传成功', 'url': result_url}), 200
        else:
            print("文件上传失败，响应信息: %s", response_data)
            return jsonify({'error': '上传失败'}), response.status_code
    except requests.exceptions.JSONDecodeError:
        print("服务器返回非 JSON 响应: %s", response.text)
        return jsonify({'error': '服务器返回无效响应'}), 500

