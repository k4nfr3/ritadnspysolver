import pymongo
import argparse

def exists(var):
     var_exists = var in locals() or var in globals()
     return var_exists

def get_hostname(myip,limit,full,short,db):
 myclient = pymongo.MongoClient("mongodb://localhost:27017/")
 mydb=myclient[db]
 mycol = mydb["hostnames"]
 mycount=0
 myreturn=""
 if (full):
  for myresult in mycol.find({"dat.ips":myip}):
   print(myresult)
 elif (short):
  dbanswer = mycol.find({"dat.ips":myip},{"_id":0, "host":1})
  if dbanswer.count()==0:
    myreturn=myip
  # for some reason find_one doesnt return the data
  for myresult in dbanswer:
    myreturn=myresult['host']
    break
 else :
  dbanswer = mycol.find({"dat.ips":myip},{"_id":0, "host":1})
  total=dbanswer.count()
  for myresult in dbanswer:
   mycount+=1
   print("%d/%d : %s" % (mycount,total,myresult['host']))
   if(mycount>=limit):
    break 
 return myreturn

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('-d','--db', type=str, help='Ritas DB name', required=True)
 parser.add_argument('-ip','--ipaddress', type=str, help='IP address to solve', required=False)
 parser.add_argument('-f','--showfull', help='Show full record from DB', required=False, action="store_true")
 parser.add_argument('-n','--limit', type=int, help='Number max of returned entries, default=1', required=False)
 parser.add_argument('-s','--short', help='Output will be short', action="store_true")
 args=parser.parse_args()

 if args.limit is not None: 
  limit=args.limit
 else:
  limit=1
 print(get_hostname(args.ipaddress,limit,args.showfull,args.short,args.db))

if __name__ == "__main__":
    main()
