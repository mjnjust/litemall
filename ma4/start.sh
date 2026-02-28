ps aux | grep app.py | grep -v grep | awk '{print $2}' | xargs kill
nohup python3 app.py > a.log 2>&1 &
