from Kitsune import Kitsune
import numpy as np
import time
import showdata
##############################################################################
# Kitsune a lightweight online network intrusion detection system based on an ensemble of autoencoders (kitNET).
# For more information and citation, please see our NDSS'18 paper: Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection

# This script demonstrates Kitsune's ability to incrementally learn, and detect anomalies in recorded a pcap of the Mirai Malware.
# The demo involves an m-by-n dataset with n=115 dimensions (features), and m=100,000 observations.
# Each observation is a snapshot of the network's state in terms of incremental damped statistics (see the NDSS paper for more details)

#The runtimes presented in the paper, are based on the C++ implimentation (roughly 100x faster than the python implimentation)
###################  Last Tested with Anaconda 3.6.3   #######################

# Load Mirai pcap (a recording of the Mirai botnet malware being activated)
# The first 70,000 observations are clean...
#print("Unzipping Sample Capture...")
#import zipfile
#with zipfile.ZipFile("mirai.zip","r") as zip_ref:
#    zip_ref.extractall()


# File location
path = "..//p2veva//data//mawilab.csv" #the pcap, pcapng, or tsv file to process.
packet_limit = 300404 #the number of packets to process

# KitNET params:
maxAE = 10 #maximum size for any autoencoder in the ensemble layer
FMgrace = 5000 #the number of instances taken to learn the feature mapping (the ensemble's architecture)
ADgrace = 50000 #the number of instances used to train the anomaly detector (ensemble itself)

showdata.showinfo()

# Build Kitsune
K = Kitsune(path,packet_limit,maxAE,FMgrace,ADgrace)

print("Running Kitsune:")
RMSEs = []
i = 0
start = time.time()
# Here we process (train/execute) each individual packet.
# In this way, each observation is discarded after performing process() method.
while True:
    i+=1
    if i % 1000 == 0:
        print(i)
    rmse = K.proc_next_packet()
    if len(rmse) == 0:
        break
    RMSEs.append(rmse)
stop = time.time()
print("Complete. Time elapsed: "+ str(stop - start))

np.save("..//p2veva//result//mawilabkitsune.npy", RMSEs)
showdata.showinfo()

#
#
## Here we demonstrate how one can fit the RMSE scores to a log-normal distribution (useful for finding/setting a cutoff threshold \phi)
#from scipy.stats import norm
#benignSample = np.log(RMSEs[FMgrace+ADgrace+1:100000])
#logProbs = norm.logsf(np.log(RMSEs), np.mean(benignSample), np.std(benignSample))
#
## plot the RMSE anomaly scores
#print("Plotting results")
#from matplotlib import pyplot as plt
#from matplotlib import cm
#plt.figure(figsize=(10,5))
#fig = plt.scatter(range(FMgrace+ADgrace+1,len(RMSEs)),RMSEs[FMgrace+ADgrace+1:],s=0.1,c=logProbs[FMgrace+ADgrace+1:],cmap='RdYlGn')
#plt.yscale("log")
#plt.title("Anomaly Scores from Kitsune's Execution Phase")
#plt.ylabel("RMSE (log scaled)")
#plt.xlabel("Time elapsed [min]")
#plt.annotate('Mirai C&C channel opened [Telnet]', xy=(121662,RMSEs[121662]), xytext=(151662,1),arrowprops=dict(facecolor='black', shrink=0.05),)
#plt.annotate('Mirai Bot Activated\nMirai scans network\nfor vulnerable devices', xy=(122662,10), xytext=(122662,150),arrowprops=dict(facecolor='black', shrink=0.05),)
#plt.annotate('Mirai Bot launches DoS attack', xy=(370000,100), xytext=(390000,1000),arrowprops=dict(facecolor='black', shrink=0.05),)
#figbar=plt.colorbar()
#figbar.ax.set_ylabel('Log Probability\n ', rotation=270)
#plt.show()
