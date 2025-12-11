ps aux | grep ma2.py | grep -v grep | awk '{print $2}' | xargs kill
