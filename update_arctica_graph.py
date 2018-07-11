#!/usr/bin/env python3
import time
import subprocess

while True:
    try:
        subprocess.run("/Library/WebServer/Documents/download_log_and_generate_plot.py",
                       timeout=30 # sec; requires python3
                      )
        time.sleep(1)
        subprocess.run("/Library/WebServer/Documents/check_save_daily.py")
        subprocess.run("/Library/WebServer/Documents/alarm.py")
    except Exception as e:
        print(e)
    time.sleep(89)
