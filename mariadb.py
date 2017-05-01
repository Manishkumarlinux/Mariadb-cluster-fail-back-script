import subprocess
import MySQLdb
import sys, os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


fp = open('/opt/con.txt', 'r')
msg = MIMEText(fp.read())
fp.close()

me = 'DNSHA@cyberspace.in'
you = 'manish@cloudmailstore.com'
msg['Subject'] = 'DNS Cluster problem'
msg['From'] = me
msg['To'] = you
s = smtplib.SMTP("localhost",25)
s.ehlo()

IP = ['78']

for ping in IP:
    address = "103.11.86." + str(ping)
    res = subprocess.call(['ping', '-c', '3', address])
    
    if res == 0:
        print "ping to", address, "ok"
    else:
        db1 = MySQLdb.connect(host="localhost",user="root",passwd="cyberspace")
        cursor = db1.cursor()
        print "mysql login done"
        cursor.execute("SET GLOBAL wsrep_provider_options='pc.bootstrap=True'")
        print cursor.fetchone()
        cursor.close()
        croncmd = "systemctl" + " stop" + " crond"
        os.system(croncmd)
        s.sendmail(me, [you], msg.as_string())
        s.quit()
