import numpy as np
from iP2Vutil import *

class vector_dict:
    def __init__(self, dim=100, lr=0.1, mode='adagrad', kind='input'):
        self.input_vec = dict()
        self.output_vec = dict()
        self.lr = lr
        self.dim = dim
        self.kind = kind
        self.mode = mode
        
        self.v_min = -0.5/self.dim
        self.v_max = 0.5/self.dim
        
        # for self.mode == 'adagrad':
        self.input_vec_squared_grad = dict()
        self.output_vec_squared_grad = dict()
        
    def update(self, packet):
        for field in packet:
            # if has not been initialized yet
            if not self.input_vec.__contains__(field):
                self.input_vec[field] = np.random.uniform(self.v_min, self.v_max, (1, self.dim))
                self.output_vec[field] = np.random.uniform(self.v_min, self.v_max, (1, self.dim))
                
                # for self.mode == 'adagrad'
                if self.mode == 'adagrad':
                    self.input_vec_squared_grad[field] = 0
                    self.output_vec_squared_grad[field] = 0
        
    def get(self, x):
        if self.kind == 'input':
            return self.input_vec[x]
        elif self.kind == 'output':
            return self.output_vec[x]
        elif self.kind == 'hybrid':
            return self.input_vec[x] + self.output_vec[x]
        
    def gradient_descendent(self, t, c, n):
        # using sgd
        if self.mode == 'sgd':
            # predict positive sample and sgd for its output_vec
            sigma = sigmoid(np.dot(self.input_vec[t], self.output_vec[c].T))
            grad = (sigma - 1) * self.output_vec[c]
            self.output_vec[c] = self.output_vec[c] - self.lr * (sigma - 1) * self.input_vec[t]
            
            # predict negative samples and sgd for their output_vec
            for n_s in n:
                sigma = sigmoid(np.dot(self.input_vec[t], self.output_vec[n_s].T))
                grad = grad + sigma * self.output_vec[n_s]
                
                # sgd for output_vec of the negative sample
                self.output_vec[n_s] = self.output_vec[n_s] - self.lr * sigma * self.input_vec[t]
            
            # sgd for target input_vec
            self.input_vec[t] = self.input_vec[t] - self.lr * grad
        
        #using adagrad
        elif self.mode == 'adagrad':
            # predict positive sample and adagrad for its output_vec
            sigma = sigmoid(np.dot(self.input_vec[t], self.output_vec[c].T))
            grad = (sigma - 1) * self.output_vec[c]
            self.output_vec_squared_grad[c] = self.output_vec_squared_grad[c] + pow((sigma - 1), 2) * self.input_vec[t] * self.input_vec[t]
            self.output_vec[c] = self.output_vec[c] - self.lr * (sigma - 1) * self.input_vec[t] / (self.output_vec_squared_grad[c] ** 0.5)
            
            # predict positive samples and adagrad for their output_vec
            for n_s in n:
                sigma = sigmoid(np.dot(self.input_vec[t], self.output_vec[n_s].T))
                grad = grad + sigma * self.output_vec[n_s]
                
                # adagrad for its output_vec
                self.output_vec_squared_grad[n_s] = self.output_vec_squared_grad[n_s] + pow(sigma, 2) * self.input_vec[t] * self.input_vec[t]
                self.output_vec[n_s] = self.output_vec[n_s] - self.lr * sigma * self.input_vec[t] / (self.output_vec_squared_grad[n_s] ** 0.5)
            
            # adagrad for target input_vec
            self.input_vec_squared_grad[t] = self.input_vec_squared_grad[t] + pow(grad, 2)
            self.input_vec[t] = self.input_vec[t] - self.lr * grad / (self.input_vec_squared_grad[t] ** 0.5)
    
    def save_vec(self):
        np.save('para//iP2Vinput.npy', self.input_vec)
        np.save('para//iP2Vinputgrad.npy', self.input_vec_squared_grad)
        np.save('para//iP2Voutput.npy', self.output_vec)
        np.save('para//iP2Voutputgrad.npy', self.output_vec_squared_grad)
    
    def load_vec(self):
        try:
            self.input_vec = np.load('para//iP2Vinput.npy', allow_pickle=True).item()
            self.input_vec_squared_grad = np.load('para//iP2Vinputgrad.npy', allow_pickle=True).item()
            self.output_vec = np.load('para//iP2Voutput.npy', allow_pickle=True).item()
            self.output_vec_squared_grad = np.load('para//iP2Voutputgrad.npy', allow_pickle=True).item()
            print("[info] find parameter for iP2V")
        except:
            print('[info] No Trained Parameter Provided for iP2V...')
            print('[info] iP2V will Run Without Previous Parameter...')