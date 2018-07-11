#!/usr/bin/env python
import subprocess

subprocess.call('curl --max-time 30 172.18.8.17/log.txt > /Library/WebServer/Documents/log.txt',
                shell=True)
with open("/Library/WebServer/Documents/log.txt") as f:
    today = f.readlines()[-1].split()[0]
yesterday = today.split('/')
yesterday[1] = str(int(yesterday[1]) - 1)
yesterday = '/'.join(yesterday)
tomorrow = today.split('/')
tomorrow[1] = str(int(tomorrow[1]) + 1)
tomorrow = '/'.join(tomorrow)

command = '''gnuplot -e 'yesterday=\"%s\"; today=\"%s\"; tomorrow=\"%s\"' /Library/WebServer/Documents/gnuplot_script;
echo "system time: $(date);"
''' % (yesterday, today, tomorrow)

subprocess.call(command, shell=True)
