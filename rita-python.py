#!/usr/bin/python3
from ritadns import get_hostname
import subprocess
import sys

RITA_CMD="/usr/local/bin/rita"

def main(argument,db):
  try:
    result = subprocess.run([RITA_CMD +argument], shell=True, check=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  except subprocess.CalledProcessError as error:
    sys.exit("Exiting ! called Rita with command : " + str(error.cmd) + " returned error : " + str(error.output.decode('ascii')))

  array_rita=result.stdout.splitlines()
  if (array_rita[0].decode('utf-8').find("Destination IP")==-1):
    sys.exit("Didn't find \"Destination IP\" in output:\n"+result.stdout.decode('utf-8')) 
  else:
    print(array_rita[0].decode('utf-8'))
    column=array_rita[0].decode('utf-8').split(',')
    DstIPColumn=1
    for j in range(len(column)):
      if column[j].find("Destination IP")!=-1: 
       DstIPColumn=j

  for line in result.stdout.splitlines()[1:]:  #without header
    finaline=""
    columnanswer=line.decode('utf-8').split(',') #split line csv into cells
    for k in range(len(columnanswer)):
      if k==DstIPColumn: # Does output Column contain "Destination IP"
        finaline+=columnanswer[k]+","+(get_hostname(columnanswer[k],1,False,True,db))+"," 
      else :
        finaline+=(columnanswer[k])+","
    print(finaline)

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    sys.exit("Usage " + sys.argv[0] + " show-beacons <db>")
  argument=""
  for i in range(1,len(sys.argv)):
    argument+= " " + sys.argv[i]
  db=sys.argv[2]
  main(argument,db)


