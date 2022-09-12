import numpy as np
from iP2Vutil import *

class negative_pool:
    def __init__(self, a=0.75, mode = 'unigram-table', max_size=1e8, n_negative=5):
        self.a = a
        self.mode = mode
        self.max_size = int(max_size)
        self.n_negative = n_negative
        
        # for self.mode == 'unigram-table':        
        self.total_count = 0
        self.weight_sum = 0
        self.n_size = 0
        self.uni_table = [None] * self.max_size
        self.vocab_count = dict()
        
        # for self.mode == 'simple-window'
        
    def update(self, e_p):
        if self.mode == 'unigram-table':
            for field in e_p:
                # update vocabulary
                if not self.vocab_count.__contains__(field):
                    self.vocab_count[field] = 1
                else:
                    self.vocab_count[field] = self.vocab_count[field] + 1
                
                self.total_count += 1
                
                # update unigram table
                self.uni_update(field, pow(self.vocab_count[field], self.a) - pow(self.vocab_count[field]-1, self.a))
        
    def get(self):
        # the negative pool is empty
        if self.n_size <= 0:
            return []
        
        # select n_negative negative samples
        negative_samples = []
        for i in range(self.n_negative):
            negative_samples.append(self.uni_table[np.random.randint(0, self.n_size)])
        
        return negative_samples
        
         
    def uni_update(self, field, weight):
        self.weight_sum += weight
        
        if self.n_size < self.max_size:
            new_size = min(round_(weight), self.max_size)
            for i in range(self.n_size, new_size):
                self.uni_table[i] = field
            self.n_size = new_size
        else:
            num = round_((weight / self.weight_sum) * self.max_size)
            for i in range(num):
                self.uni_table[random.randint(0, (self.max_size-1))] = field