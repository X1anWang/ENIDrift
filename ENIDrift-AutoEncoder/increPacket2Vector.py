import numpy as np
import pandas as pd
import NegativePool
import VectorDict

class increPacket2Vector:
    def __init__(self, path, lr, n_epoch, limit=50000000, dim=100, mode='unigram-table', a=0.75, n_negative=5, sgd='adagrad', kind='input', max_size_np=1e8):
        # initiate parameters
        self.n_processed = 0 # the number of packets that have been processed
        self.n_epoch = n_epoch
        self.limit = limit # the limit of the packet number
        
        # initiate the vector dictionary and the negative sample pool
        self.vec_dict = VectorDict.vector_dict(dim, lr, sgd, kind)
        self.ne_pool = NegativePool.negative_pool(a, mode, max_size_np, n_negative)
        
        # load data
        self.load_data(path)
        
    def load_data(self, p):
        self.packets = pd.read_csv(p, dtype=str)
        self.limit = self.packets.shape[0]
        
    def preproc_packet(self, p_idx):
        srcIP = self.packets['srcIP'][p_idx]
        dstIP = self.packets['dstIP'][p_idx]
        if srcIP < dstIP:
            flow_name = srcIP+dstIP
        else:
            flow_name = dstIP+srcIP
        
        return [flow_name] + [srcIP, dstIP, self.packets['srcproto'][p_idx], self.packets['dstproto'][p_idx],
                self.packets['srcMAC'][p_idx], self.packets['dstMAC'][p_idx], self.packets['protocol'][p_idx],
                self.packets['len'][p_idx], self.packets['IPtype'][p_idx]]
        
    def proc_packet(self):
        # preprocess and update vocabulary
        ext_packet = self.preproc_packet(self.n_processed)
        self.vec_dict.update(ext_packet)
        
        # train
        for target in ext_packet:
            for context in ext_packet:
                # target and context cannot be the same
                if target == context:
                    continue
                
                # select negative samples
                neg_samples = self.ne_pool.get()
                
                # gradient descendent
                for i in range(self.n_epoch):
                    self.vec_dict.gradient_descendent(target, context, neg_samples)
        
        self.ne_pool.update(ext_packet)
        self.n_processed += 1
        
        return self.vec_dict.get(ext_packet[0])
    
    def next_packet(self):
        if self.limit <= self.n_processed:
            print(str(self.n_processed)+" processed, P2V: off")
            return []
        else:
            return self.proc_packet()

    def sav(self):
        self.vec_dict.save_vec()
    
    def loa(self):
        self.vec_dict.load_vec()