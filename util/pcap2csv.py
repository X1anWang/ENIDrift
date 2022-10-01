from scapy.all import *
import pandas as pd
import numpy as np

file_list = ['packet_0.pcap', 'packet_1.pcap']

for file in file_list:
    pcap = PcapReader(file)
    dataset = []
    while True:
        try:
            packet = pcap.read_packet()
            IPtype = np.nan
            timestamp = str(packet.time+1)
            framelen = str(len(packet))
            if packet.haslayer(IP):  # IPv4
                srcIP = packet[IP].src
                dstIP = packet[IP].dst
                IPtype = 0
            elif packet.haslayer(IPv6):  # ipv6
                srcIP = packet[IPv6].src
                dstIP = packet[IPv6].dst
                IPtype = 1
            else:
                srcIP = ''
                dstIP = ''

            if packet.haslayer(TCP):
                srcproto = str(packet[TCP].sport)
                dstproto = str(packet[TCP].dport)
            elif packet.haslayer(UDP):
                srcproto = str(packet[UDP].sport)
                dstproto = str(packet[UDP].dport)
            else:
                srcproto = ''
                dstproto = ''

            srcMAC = packet.src
            dstMAC = packet.dst
            if srcproto == '':  # it's a L2/L1 level protocol
                if packet.haslayer(ARP):  # is ARP
                    srcproto = 'arp'
                    dstproto = 'arp'
                    srcIP = packet[ARP].psrc  # src IP (ARP)
                    dstIP = packet[ARP].pdst  # dst IP (ARP)
                    IPtype = 0
                elif packet.haslayer(ICMP):  # is ICMP
                    srcproto = 'icmp'
                    dstproto = 'icmp'
                    IPtype = 0
                elif srcIP + srcproto + dstIP + dstproto == '':  # some other protocol
                    srcIP = packet.src  # src MAC
                    dstIP = packet.dst  # dst MAC
            dataset.append([srcIP, dstIP, srcproto, dstproto, srcMAC, dstMAC, IPtype, framelen, timestamp])
        except:
            dtst = np.mat(dataset)
            dataset_csv = pd.DataFrame(dtst, columns = ['srcIP', 'dstIP', 'srcproto', 'dstproto', 'srcMAC', 'dstMAC', 'IPtype', 'framelen', 'timestamp'])
            dataset_csv.to_csv((file[:-4]+str('csv')), index=False)
            break
