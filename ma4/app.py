from flask import Flask
from flask_cors import CORS
from fn.data import data_bp
from mall.mall import mall_bp

app = Flask(__name__)
CORS(app)

# 注册蓝图
app.register_blueprint(data_bp)
app.register_blueprint(mall_bp)

if __name__ == '__main__':
    app.run(debug=True)