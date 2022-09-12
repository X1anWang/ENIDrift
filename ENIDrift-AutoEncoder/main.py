import time
from iP2Vmain import *
from numpy import *
from pandas import *
from measure import *
from ENIDrift_main import *

settings = {
        'data_name': 'CICIDS2017-Wednesday',
        'num_run': 1,
        'release_speed': 1000,
        'lamda': [0.1, 0.1],
        'delta': [0.05, 0.05],
        'incremental': True,
        'save': False,
        'vector': False
        }

path_label = '..//data//labels.npy'
path_packet = '..//data//packets.csv'
num_run = settings['num_run']
release_speed = settings['release_speed']
lamd = settings['lamda']
delt = settings['delta']
incre = settings['incremental']
s = settings['save']
label = load(path_label)

print("\n\n**********ENIDrift**********\n\n")

for i_run in range(num_run):
    ENIDrift = ENIDRIFTtrain(lamda = lamd, delta=delt, incremental=incre)
    FE = increPacket2Vectormain(path = path_packet, incremental=incre)
    
    ENIDrift.loadpara()
    FE.loadpara()
    prediction = []
    num_released = 0
    
    start = time.time()
    for i_packet in range(label.shape[0]):
        
        if i_packet%50000 == 0:
            print(str(i_packet)+' processed...')
            
        packet_extracted = FE.iP2Vrun().reshape(1, -1)
        prediction.append(ENIDrift.predict(packet_extracted))
            
        # Release labels
        if i_packet % release_speed == 0:
            ENIDrift.update(label[num_released:i_packet+1])
            num_released = i_packet + 1

    stop = time.time()
    print("[info] Time elapsed for round "+str(i_run)+": "+str(stop-start)+" seconds")
    overall(prediction, label)