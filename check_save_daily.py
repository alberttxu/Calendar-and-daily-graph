#!/usr/bin/env python
import subprocess

with open('/Library/WebServer/Documents/log.txt') as f:
    lines = f.readlines()

date, time = lines[-1].split(',')[0].split()[:2]
hour, minute = map(int, time.split(':')[:2])
print 'latest log time: %s %s' % (date, time)

save_command = ('cp /Library/WebServer/Documents/temp-humid.svg '
               '/Library/WebServer/Documents/logs/%s-%s-%s.svg'
               % (date.split('/')[2], date.split('/')[0],date.split('/')[1])
               )

if hour == 23 and 55 < minute < 59:
    print 'saving daily graph'
    print save_command
    subprocess.call(save_command, shell=True)
