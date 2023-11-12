#Pandas/Python PCAP file analyzer 
#pip install scapy
from scapy.all import *
from prettytable import PrettyTable
from collections import Counter
packets = rdpcap("Path/to/pcap_file.pcap")
srcIP = []
for pkt in packets:
    if IP in pkt:
        try:
            srcIP.append(pkt[IP].src)
        except:
            pass
cnt = Counter()
for ip in srcIP:
    cnt[ip] += 1
    
table = PrettyTable(["IP", "Count"])

for ip, count in cnt.most_common():
    table.add_row([ip,count])
    
print(table)
