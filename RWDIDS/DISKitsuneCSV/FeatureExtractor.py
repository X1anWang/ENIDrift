#Check if cython code has been compiled
import os
import subprocess

use_extrapolation=False #experimental correlation code
if use_extrapolation:
    print("Importing AfterImage Cython Library")
    if not os.path.isfile("AfterImage.c"): #has not yet been compiled, so try to do so...
        cmd = "python setup.py build_ext --inplace"
        subprocess.call(cmd,shell=True)
#Import dependencies
import netStat as ns
import csv
import numpy as np
print("Importing Scapy Library")
from scapy.all import *
import os.path
import platform
import subprocess
import pandas as pd


#Extracts Kitsune features from given pcap file one packet at a time using "get_next_vector()"
# If wireshark is installed (tshark) it is used to parse (it's faster), otherwise, scapy is used (much slower).
# If wireshark is used then a tsv file (parsed version of the pcap) will be made -which you can use as your input next time
class FE:
    def __init__(self,file_path,limit=np.inf):
        self.path = file_path
        self.limit = limit
        self.parse_type = None #unknown
        self.curPacketIndx = 0
        self.tsvin = None #used for parsing TSV file
        self.scapyin = None #used for parsing pcap with scapy

        ### Prep pcap ##
        self.__prep__()

        ### Prep Feature extractor (AfterImage) ###
        maxHost = 100000000000
        maxSess = 100000000000
        self.nstat = ns.netStat(np.nan, maxHost, maxSess)

    def _get_tshark_path(self):
        if platform.system() == 'Windows':
            return 'C:\Program Files\Wireshark\\tshark.exe'
        else:
            system_path = os.environ['PATH']
            for path in system_path.split(os.pathsep):
                filename = os.path.join(path, 'tshark')
                if os.path.isfile(filename):
                    return filename
        return ''

    def __prep__(self):
        
        self.packets = pd.read_csv(self.path)

    def get_next_vector(self):
        if self.curPacketIndx >= self.limit:
            return []        

        timestamp = self.packets['timestamp'][self.curPacketIndx]
        framelen = self.packets['len'][self.curPacketIndx]
        if not pd.isnull(self.packets['srcIP'][self.curPacketIndx]):
            srcIP = self.packets['srcIP'][self.curPacketIndx]
            dstIP = self.packets['dstIP'][self.curPacketIndx]
            IPtype = self.packets['IPtype'][self.curPacketIndx]
        elif not pd.isnull(self.packets['srcIP'][self.curPacketIndx]):
            srcIP = self.packets['srcIP'][self.curPacketIndx]
            dstIP = self.packets['dstIP'][self.curPacketIndx]
            IPtype = self.packets['IPtype'][self.curPacketIndx]
        else:
            srcIP = ''
            dstIP = ''
        
        if not pd.isnull(self.packets['srcproto'][self.curPacketIndx]):
            srcproto = str(self.packets['srcproto'][self.curPacketIndx])
            dstproto = str(self.packets['dstproto'][self.curPacketIndx])
        elif not pd.isnull(self.packets['srcproto'][self.curPacketIndx]):
            srcproto = str(self.packets['srcproto'][self.curPacketIndx])
            dstproto = str(self.packets['dstproto'][self.curPacketIndx])
        else:
            srcproto = ''
            dstproto = ''
        
        srcMAC = self.packets['srcMAC'][self.curPacketIndx]
        dstMAC = self.packets['dstMAC'][self.curPacketIndx]
        if srcIP + srcproto + dstIP + dstproto == '':
                srcIP = srcMAC
                dstIP = dstMAC
        
        self.curPacketIndx = self.curPacketIndx + 1


        ### Extract Features
        try:
            return self.nstat.updateGetStats(IPtype, srcMAC, dstMAC, srcIP, srcproto, dstIP, dstproto,
                                                 int(framelen),
                                                 float(timestamp))
        except Exception as e:
            print(e)
            return []


    def pcap2tsv_with_tshark(self):
        print('Parsing with tshark...')
        fields = "-e frame.time_epoch -e frame.len -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e icmp.type -e icmp.code -e arp.opcode -e arp.src.hw_mac -e arp.src.proto_ipv4 -e arp.dst.hw_mac -e arp.dst.proto_ipv4 -e ipv6.src -e ipv6.dst"
        cmd =  '"' + self._tshark + '" -r '+ self.path +' -T fields '+ fields +' -E header=y -E occurrence=f > '+self.path+".tsv"
        subprocess.call(cmd,shell=True)
        print("tshark parsing complete. File saved as: "+self.path +".tsv")

    def get_num_features(self):
        return len(self.nstat.getNetStatHeaders())
