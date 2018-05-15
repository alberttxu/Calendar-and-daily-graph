#!/usr/bin/env python
import smtplib
import time
from gmail_data import gmail_user, gmail_passwd, recipients

def avg(lst):
    return float(sum(lst)) / len(lst)


# Email settings ---------------
subject = "Arctica - "
message_body = "operations console: 508-856-3292"

#https://stackoverflow.com/questions/101O47455/how-to-send-an-email-with-gmail-as-provider-using-python
def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent mail to %s' % recipient
    except:
        print "failed to send mail"
# --------------- End of Email settings


# Alarm ---------------------
temp_threshold = 73.0 # F
rh_threshold = 45.0 # % humidity

def thirtyMinutesPassedSinceLastAlarm():
    with open("/Library/WebServer/Documents/timeOfLastAlarm.txt") as alarmfile:
        lastAlarm = float(alarmfile.readline())
        #print(lastAlarm)
    return (time.time() - lastAlarm) / 60 > 30

def updateTimeOfLastAlarm():
    with open("/Library/WebServer/Documents/timeOfLastAlarm.txt", 'w') as alarmfile:
        alarmfile.write(str(time.time())) # update last alarm time

def sendEmails():
    for recipient in recipients:
        send_email(gmail_user, gmail_passwd, recipient, subject, message_body) # send to all recipients

def getRecentAlarmCount():
    with open("/Library/WebServer/Documents/recentAlarmsCounter.txt") as counterfile:
        count = int(counterfile.readline())
    print("recentAlarmCount: %d" % count)
    return count

def resetAlarmCounter():
    print("resetting alarm count")
    with open("/Library/WebServer/Documents/recentAlarmsCounter.txt", 'w') as counterfile:
        counterfile.write('0')

def incrementAlarmCounter():
    print("incrementing alarm")
    with open("/Library/WebServer/Documents/recentAlarmsCounter.txt", 'r+') as counterfile:
        count = int(counterfile.readline())
        counterfile.truncate()
        counterfile.write(str(count + 1))
# ----------------------- Alarm


if __name__ == '__main__':
    import datetime

    with open("/Library/WebServer/Documents/log.txt") as logfile:
        pastMin = logfile.readlines()[-6:]

    pastMinTemps = [float(line.split(',')[1]) for line in pastMin]
    pastMinRh = [float(line.split(',')[2]) for line in pastMin]
    print(pastMinRh)
    temp_avg = avg(pastMinTemps) 
    rh_avg = avg(pastMinRh) 

    tempTooHigh = temp_avg > temp_threshold
    rhTooHigh = rh_avg > rh_threshold
    if tempTooHigh:
        print("temperature too high")
    if rhTooHigh:
        print("rh too high")

    if tempTooHigh:
        subject += "temp %.2f F" % temp_avg
        if rhTooHigh:
            subject += " and RH %.2f%%" % rh_avg
        subject += " above threshold"
    elif rhTooHigh:
        subject += "RH %.2f%% above threshold" % rh_avg
    subject += " of %.1f deg F, %.1f%% RH" % (temp_threshold, rh_threshold)

    if (tempTooHigh or rhTooHigh) and thirtyMinutesPassedSinceLastAlarm():
        if getRecentAlarmCount() > 2: # not false positve
            sendEmails()
            updateTimeOfLastAlarm()
            resetAlarmCounter()
        else:
            incrementAlarmCounter()
    else:
        resetAlarmCounter()

    print("past min temp_avg: %.2f F, past min rh_avg: %.2f %%RH\n\n" % (temp_avg, rh_avg))
