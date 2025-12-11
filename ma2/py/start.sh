ps aux | grep ma2.py | grep -v grep | awk '{print $2}' | xargs kill
nohup python3 ma2.py > a.log 2>&1 &
