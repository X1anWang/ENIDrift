from numpy import *
from ENIDrift_ensemble import *
from GenerationIndex import *

class ENIDrift_train():
    
    def __init__(self, lamda=None, delta=None, size=[700, 5, 700, 5],
                 num_test=10, learner='PCA', mute=True, incremental=True, max_subs=30):
        
        self.G_idx_normal = G_index(lamda[0], delta[0], num_test = size[0], ID='normal')
        self.generate_size_normal = [size[0], size[1]]
        self.num_test = num_test
        self.learner = learner
        self.mute = True
        self.incremental = incremental
        self.generate_temp = array([])
        self.num_generate_temp = 0
        self.normal_set = array([])
        self.detector = dual_ensemble(learner, max_sublearner=max_subs)
        self.attack_set = array([])
        
        
    def predict(self, x):
        
        if not self.incremental:
            return self.detector.predict(x)
        
        if self.num_generate_temp != 0:
            self.generate_temp = append(self.generate_temp, x, axis=0)
        else:
            self.generate_temp = x
            self.num_generate_temp = 1
        
        return self.detector.predict(x)
    
    
    def update(self, y):
        
        if not self.incremental:
            return 0
        
        normal_temp = array([self.generate_temp[i_y] for i_y in range(y.shape[0]) if y[i_y] == 0])
        attack_temp = array([self.generate_temp[i_y] for i_y in range(y.shape[0]) if y[i_y] != 0])
        
        if normal_temp.shape[0]!= 0:
            if self.normal_set.shape[0] == 0:
                self.normal_set = normal_temp
            else:
                self.normal_set = append(self.normal_set, normal_temp, axis=0)
            
            # Update normal class
            if self.normal_set.shape[0] < self.generate_size_normal[0]:
                pass
            elif self.generate_size_normal[1] <= self.G_idx_normal.times():
                self.G_idx_normal.clear()
                self.normal_set = array([])
            else:
                if self.G_idx_normal.check(self.normal_set) == 'Training':
                    data_temp = self.G_idx_normal.get()
                    self.detector.generate('normal', data_temp)
                self.normal_set = array([])
        
        if attack_temp.shape[0] != 0:
            if self.attack_set.shape[0] == 0:
                self.attack_set = attack_temp
            else:
                self.attack_set = append(self.attack_set.reshape(-1, 200), attack_temp.reshape(-1, 200), axis=0)

            # Update attack class
            if self.attack_set.shape[0] < self.generate_size_normal[0]:
                pass
            else:
                self.detector.ensembleupdate(self.attack_set)
                self.attack_set = array([])
        
        self.generate_temp = array([])
        self.num_generate_temp = 0
    
    def save(self):
        self.detector.save_classifier()
    
    def loadpara(self):
        self.detector.load_classifier()