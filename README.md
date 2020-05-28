# RitaPySolver
## Python scripts to add on RITA (Real Intelligence Threat Analytics)
Rita Github link : https://github.com/activecm/rita  

### ritadns.py
$ python3 ./ritadns.py -s -ip 3.235.69.6 -d lab  
us04web.zoom.us  

### rita-python.py
integration of DNS resolution to the rita command (it will search for the column header "Destination IP" and do a dnsresolution on that column)
./rita-python.py show-beacons lab | head -n 10  
./rita-python.py show-long-connections home | head -n 10  

### rita-alerter.py
we can set a threshold
I will alert when new beacons are returned by rita-python.py via SYSLOG

Todo : 
make it compatible with -H --human-readable option  
do it in Go in Rita  

if somebody requests it, I can add SMTP alerting instead of SYSLOG




