from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    """返回首页"""
    return send_from_directory('static', 'index.html')

@app.route('/health')
def health():
    """健康检查接口"""
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 443))
    app.run(host='0.0.0.0', port=port, debug=True)
