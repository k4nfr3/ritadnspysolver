# RitaPySolver

$ python3 ./ritadns.py -s -ip 3.235.69.6  
us04web.zoom.us

or to integrate with the rita show command (it will search for the column header "Destination IP" and do a dnsresolution on that column.  
./ritadnspysolver show-beacons <db> | head -n 10  
./ritadnspysolver show-long-connections home | head -n 10  
    
Todo : 
- Hostname records seem to be deleted before the beacons are removed. So will need to cache the results for next run.  
- make it compatible with -H --human-readable option  
- do it in Go in Rita  




