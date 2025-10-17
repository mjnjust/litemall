from peewee import *
from flask import Flask
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    # 注册蓝图
    from.routes.items import items_bp
    from.routes.category import category_bp

    app.register_blueprint(items_bp, url_prefix='/api/items')
    app.register_blueprint(category_bp, url_prefix='/wx')

    return app