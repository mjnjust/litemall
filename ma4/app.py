from flask import Flask
from flask_cors import CORS
from fn.data import data_bp
from mall.mall import mall_bp
from mall.jdy_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from datetime import datetime,timedelta  
import threading
import time

app = Flask(__name__)
CORS(app)
# 注册蓝图
app.register_blueprint(data_bp)
app.register_blueprint(mall_bp)

def refresh(name, delay):
    time.sleep(delay)
    manager = LoginManager("13236586829", "ycxx123#")                
    for i in range(10000):
        print(f"正在执行第 {i+1} 次...")
        try:        
            res = manager.fetch_and_save()        
            if res == 2:
                manager.log("刷新失败，等待5秒后重刷")
                time.sleep(5)
            else:
                manager.log("刷新成功，等待8小时候重刷")
                time.sleep(60*60*8)
        except Exception as e:
            print(f"第 {i+1} 次执行失败: {e}")    
            manager.log("刷新失败，等待5秒后重刷")
            time.sleep(5)

if __name__ == '__main__':
    t = threading.Thread(target=refresh, args=("Worker-1", 3))
    t.daemon = True
    t.start()
    app.run(debug=True)    
