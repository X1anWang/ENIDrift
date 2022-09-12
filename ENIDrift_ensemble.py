from numpy import *
from sklearn.decomposition import PCA
import joblib

class ensemble():
    
    def __init__(self, learner='PCA', threshold=0.80, alpha=0.05, ID = 'normal', limit=30):
        
        self.learner = 'PCA'
        self.threshold = threshold
        self.alpha = alpha
        self.detector_pool = []
        self.weight_list = []
        self.threshold_list = []
        self.limit = limit
        self.ID = ID
        self.threshold_update = 0.80
        self.threshold_adjust = 0.05
        
    def sub_predict(self, x):
                
        pred_raw = 0
        
        for i in range(len(self.detector_pool)):
            if self.threshold_list[i] <= self.detector_pool[i].score(x.reshape(1, -1)):
                pred_raw = pred_raw + self.weight_list[i]
            else:
                pred_raw = pred_raw - self.weight_list[i]
        
        return pred_raw

    def adjust(self, x, update=True):
        
        if update == True:
            
            num_sample = x.shape[0]
            for i in range(len(self.detector_pool)):
                scores = self.detector_pool[i].score_samples(x)
                decay = sum([1 for o in range(num_sample) if self.threshold_list[i] <= scores[o]])
                decay = decay / num_sample
                if self.threshold_update <= decay:
                    self.weight_list[i] = 1
                else:
                    self.weight_list[i] = self.weight_list[i] * decay
            
            model = PCA(n_components=0.99)
            model.fit(x)
            scores = model.score_samples(x)
            
            self.threshold_list.append(sorted(scores)[0])
            self.detector_pool.append(model)
            self.weight_list.append(1)
            
            while self.limit <= len(self.detector_pool):
                idx_delete = self.weight_list.index(min(self.weight_list))
                del self.weight_list[idx_delete]
                del self.detector_pool[idx_delete]
                del self.threshold_list[idx_delete]
                
        else:
            num_sample = x.shape[0]
            for i in range(len(self.detector_pool)):
                scores = self.detector_pool[i].score_samples(x)
                decay = sum([1 for o in range(num_sample) if scores[o] < self.threshold_list[i]])
                decay = decay / num_sample
                if self.threshold_update <= decay:
                    self.weight_list[i] = 1
                else:
                    self.weight_list[i] = self.weight_list[i] * decay
                
    def save_pcas(self, name):
        for i in range(len(self.detector_pool)):
            joblib.dump(self.detector_pool[i], ("model//"+str(i)+'thpca.m'))
        save('model//weight.npy', self.weight_list)
        save('model//threshold.npy', self.threshold_list)
        temp = [len(self.detector_pool)]
        save('model//num.npy', temp)
    
    def get_num(self):
        return len(self.detector_pool)
    
    def load_pca(self):
        try:
            temp = load('model//num.npy')
            num = temp[0]
            for i in range(num):
                temp = joblib.load('model//'+str(i)+'thpca.m')
                self.detector_pool.append(temp)
            temp = load('model//weight.npy')
            self.weight_list = list(temp)
            temp = load('model//threshold.npy')
            self.threshold_list = list(temp)
        except:
            print("[info] No previous trained model for ENIDrift ensemble...")
            print("[info] ENIDrift will train new model...")

class dual_ensemble():
    
    def __init__(self, learner='PCA', max_sublearner=30):
        self.learner = learner
        self.dual_normal = ensemble(limit = max_sublearner)
    
    def predict(self, x):
        prob_n = self.dual_normal.sub_predict(x)
        # attack
        if prob_n <= 0:
            return 1
        # normal
        else:
            return 0
    
    def generate(self, target, x):
        self.dual_normal.adjust(x, update=True)
            
    def save_classifier(self):
        self.dual_normal.save_pcas('normal')
    
    def ensembleupdate(self, x):
        self.dual_normal.adjust(x, update=False)
    
    def load_classifier(self):
        self.dual_normal.load_pca()