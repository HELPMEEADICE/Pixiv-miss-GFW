import logging
from flask import Flask, Response, stream_with_context
import requests
from requests.packages import urllib3
import itertools
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# 创建持久的Session对象，共享连接池
session = requests.Session()

# 配置日志
logging.basicConfig(level=logging.INFO)

# 常量定义
IP_ADDRESSES = [
    '210.140.139.135',
    '210.140.139.132',
    '210.140.139.137',
    '210.140.139.136',
    '210.140.139.134',
    '210.140.139.131'
]
DEFAULT_HEADERS = {
    'Referer': 'https://www.pixiv.net/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}
ip_cycle = itertools.cycle(IP_ADDRESSES)

@app.route('/', methods=['GET'])
def root():
    response_text = '<p style="font-family: Arial;">Pixiv Image Proxy to miss GFW</p>'
    return Response(response_text, status=200, content_type='text/html;charset=UTF-8')

@app.route('/<path:path>', methods=['GET'])
def proxy(path):
    # 检查是否是 /favicon.ico 请求
    if path == 'favicon.ico':
        return Response("Not Found", status=404)

    try:
        # 选择下一个 IP 地址
        ip_address = next(ip_cycle)
        print(f'Used IP:{ip_address}')
        target_url = f'https://{ip_address}/{path}'
        response = session.get(target_url, headers=DEFAULT_HEADERS, timeout=10, verify=False, stream=True)

        def generate():
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk

        return Response(stream_with_context(generate()), status=response.status_code, content_type=response.headers.get('Content-Type'))

    except requests.RequestException as request_error:
        logging.error(f"Request error: {request_error}")
        return Response("Error fetching image", status=500)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return Response("Internal server error", status=500)

if __name__ == '__main__':
    app.run(debug=True, port=5181, threaded=True)
