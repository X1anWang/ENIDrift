import pandas as pd
import increPacket2Vector
import numpy as np

class increPacket2Vector_main():
    
    def __init__(self, path, incremental):
        self.path = path
        self.lr = 0.05
        self.epoch = 1
        self.limit = 300000
        self.dim = 200
        self.a = 0.75
        self.n_negative = 5
        self.max_size_np = 1e8        
        self.ip2v = increPacket2Vector.increPacket2Vector(self.path, self.lr, self.epoch, self.limit, self.dim, 'unigram-table',
                                          self.a, self.n_negative, 'adagrad', 'input',
                                          self.max_size_np)
        self.i = 0
    
    def iP2Vrun(self):
        
        self.i = self.i + 1
        vector = self.ip2v.next_packet()
        return np.array(vector)
    
    def loadpara(self):
        self.ip2v.loa()
    
    def save(self):
        self.ip2v.sav()