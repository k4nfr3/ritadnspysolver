#!/usr/bin/python3
from ritadns import get_hostname
import subprocess
import sys
import os
import pandas as pd
import numpy as np
import logging
import socket
from logging.handlers import SysLogHandler

class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


DB="lab"
MIN=0.7
SYSLOG_SERVER="192.168.0.10"
SYSLOG_PORT=515
CMD="/usr/local/bin/rita"
ALERTS="/home/change/rita_alerts.txt"
ALERT_IF_NEW_IP=False

def read_old_alerts():
  my_cols = ["FQDN","IP1","IP2","IP3","IP4","IP5","IP6","IP7","IP8","IP9","IP10"]

  if os.path.isfile(ALERTS): # skipping if file doesn't exist
    df = pd.read_csv(ALERTS,names=my_cols,engine='python')
    return df

def send_alert(hostname,ip):
  print("SEND Syslog for " +hostname + "@"+ip + " to " + SYSLOG_SERVER + ":"+str(SYSLOG_PORT))
  #syslogger = logging.getLogger('SyslogLogger')
  syslog = SysLogHandler(address=(SYSLOG_SERVER,SYSLOG_PORT))
  syslog.addFilter(ContextFilter())
  format = '%(message)s'
  formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')
  syslog.setFormatter(formatter)

  logger = logging.getLogger()
  logger.addHandler(syslog)
  logger.setLevel(logging.INFO)

  message="New Beacon,https://"+hostname + ","+ip+","

  logger.info(message)

def check_if_new_alert(data,hostname,ip):
  found_host=False
  found_ip=False
  saved_index=0
  for i, row in enumerate(data.values):
     if (data.iloc[i]['FQDN']==hostname): # find FQDN in csv file  
       found_host=True
       saved_index=i
       for j in range(1,9):
         if (data.iloc[i][j]==ip): # already saved IP in csv
           #print("FOUND " + hostname + " " + ip  + " DO NOTHING!!!")
           found_ip=True
  if (found_host==False):
    #print("Adding new HOSTNAME +  IP to db")         
    send_alert(hostname,ip)
    new_entry={'FQDN':hostname,'IP1':ip}
    data=data.append(new_entry, ignore_index = True)
  else:
     if(found_ip==False):
       print("FOUND new IP beacon for " + hostname + " = "+ ip)         
       if (ALERT_IF_NEW_IP):
         send_alert(hostname,ip)
       for k in range(2,9):
         if (data.iloc[saved_index][k]!=np.nan):
           data.at[saved_index,"IP"+str(k)] = ip 
           break

  return data



def write_csv(data):
   data.to_csv(ALERTS,header=False,index=False)
  

def main(data,DB,MIN):
  result = subprocess.run([CMD+"  show-beacons " +DB], shell=True, check=True, stdout=subprocess.PIPE)
  array_rita=result.stdout.splitlines()
  if (array_rita[0].decode('utf-8').find("Score")==-1):
    sys.exit("Didn't find \"Score\" in output:\n"+result.stdout.decode('utf-8')) 
  elif (array_rita[0].decode('utf-8').find("Destination IP")==-1):
    sys.exit("Didn't find \"Destination IP\" in output:\n"+result.stdout.decode('utf-8')) 
  else:
    print(array_rita[0].decode('utf-8'))
    column=array_rita[0].decode('utf-8').split(',')
    DstIPColumn=1
    ScoreColumn=0
    for j in range(len(column)):
      if column[j].find("Destination IP")!=-1: 
       DstIPColumn=j 
      if column[j].find("Score IP")!=-1: 
       ScoreColumn=j
       print("Score column = " + j)
  for line in result.stdout.splitlines()[1:]:  #without header
    finaline=""
    columnanswer=line.decode('utf-8').split(',') #split line csv into cells
    if (float(columnanswer[ScoreColumn])>MIN):
      for k in range(len(columnanswer)):
        if k==DstIPColumn: # Is it the Column that contain "Destination IP"
          hostname=get_hostname(columnanswer[k],1,False,True,DB)
          finaline+=columnanswer[k]+","+hostname+"," 
          data=check_if_new_alert(data,hostname,columnanswer[k])
        else :
          finaline+=(columnanswer[k])+","
      print(finaline)
  return data

if __name__ == "__main__":
  known_beacons=read_old_alerts()           # get old alerts
  known_beacons=main(known_beacons,DB,MIN)  # get new beacons and Alert
  write_csv(known_beacons)                  # save alert list for next run


