# Rita python DNS add-ons  
## Python scripts to add on RITA (Real Intelligence Threat Analytics)  
Rita Github link : https://github.com/activecm/rita   

### ritadns.py
A little script that will reverse DNS an IP by looking in the MangoDB  
    
$ python3 ./ritadns.py -s -ip 3.235.69.6 -d lab  
us04web.zoom.us  

### rita-python.py
integration of DNS python script to the rita command (it will search for the column header "Destination IP" and do a dnsresolution on that column)  
./rita-python.py show-beacons lab | head -n 10    
./rita-python.py show-long-connections home | head -n 10  

### rita-alerter.py
As the name states, it's an SYSLOG alerter. I will save the states of 
we can set a threshold
I will alert when new beacons are returned by rita-python.py via SYSLOG

Todo : 
add show-long-connections and show-exploded-dns to the rita-alerter.py  
make it compatible with -H --human-readable option  
do it in Go in Rita  

if somebody requests it, I can add SMTP alerting instead of SYSLOG




