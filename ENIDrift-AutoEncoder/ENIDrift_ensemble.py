from numpy import *
from sklearn.decomposition import PCA
import ENIDrift_ae as AE
import joblib
import pickle

class ensemble():
    
    def __init__(self, learner='PCA', threshold=0.80, alpha=0.05, limit=30, ID = 'normal', ttttt=30):
        self.learner = 'PCA'
        self.threshold = threshold
        self.alpha = alpha
        self.detector_pool = []
        self.weight_list = []
        self.threshold_list = []
        self.limit = ttttt
        self.ID = ID
        self.threshold_update = 0.80
        self.threshold_adjust = 0.05
        self.n_dim = 200
        self.hr = 0.75
        self.lr = 0.05
        self.n_detector = 0
        self.epoch = 50
        
        self.weight_mat = []
        
    def sub_predict(self, x):
        pred_raw = 0
        
        for i in range(len(self.detector_pool)):
            if self.threshold_list[i] <= self.detector_pool[i].execute(x.reshape(1, -1)):
                pred_raw = pred_raw - self.weight_list[i]
            else:
                pred_raw = pred_raw + self.weight_list[i]
        
        return pred_raw

    def adjust(self, x, update=True):
        
        try:
            num = x.shape[0]
        except:
            num = len(x)
        
        if update == True:
            num_sample = x.shape[0]
            for i in range(len(self.detector_pool)):
                scores = []
                for o in range(num):
                    scores.append(self.detector_pool[i].execute(x[o,:].reshape(1, -1)))
                decay = sum([1 for o in range(num) if self.threshold_list[i] <= scores[o]])
                decay = decay / num_sample
                decay = 1 - decay
                if self.threshold_update <= decay:
                    self.weight_list[i] = 1
                else:
                    self.weight_list[i] = self.weight_list[i] * decay
            
            params = AE.dA_params(n_visible=self.n_dim, n_hidden=0, lr=self.lr, corruption_level=0, gracePeriod=0, hiddenRatio=self.hr)
            self.detector_pool.append(AE.dA(params, str(self.n_detector)))
            
            scores = []
            for r in range(self.epoch):
                for i in range(num):
                    self.detector_pool[self.n_detector].train(x[i, :].reshape(1, -1))
            
            for i in range(num):
                scores.append(self.detector_pool[self.n_detector].train(x[i, :].reshape(1, -1)))

            # self.threshold_list.append(sorted(scores)[int(x.shape[0]*self.alpha)])
            self.threshold_list.append(max(scores))
            self.weight_list.append(1)
            self.n_detector = self.n_detector + 1
            
            while self.limit <= len(self.detector_pool):
                idx_delete = self.weight_list.index(min(self.weight_list))
                del self.weight_list[idx_delete]
                del self.detector_pool[idx_delete]
                del self.threshold_list[idx_delete]
                self.n_detector = self.n_detector - 1
            
            self.weight_mat.append(self.weight_list+[0]*(200-len(self.weight_list)))
            
        else:
            num_sample = x.shape[0]
            for i in range(len(self.detector_pool)):
                scores = []
                for o in range(num):
                    scores.append(self.detector_pool[i].execute(x[o,:].reshape(1, -1)))
                decay = sum([1 for o in range(num) if self.threshold_list[i] <= scores[o]])
                decay = decay / num_sample
                if self.threshold_update <= decay:
                    self.weight_list[i] = 1
                else:
                    self.weight_list[i] = self.weight_list[i] * decay
                
    def save_ae(self, name):
        temp = [self.n_detector]
        save("model//num.npy", temp)
        for i in range(self.n_detector):
            out_put = open(("model//"+str(i)+"thmodel.pkl"), 'wb')
            temp = pickle.dumps(self.detector_pool[i])
            out_put.write(temp)
            out_put.close()
        save("model//weight.npy", self.weight_list)
        save("model//threshold.npy", self.threshold_list)
            
    def load_ae(self):
        try:
            temp = load("model//num.npy")
            self.n_detector = temp[0]
            temp = load("model//threshold.npy")
            self.threshold_list = list(temp)
            temp = load("model//weight.npy")
            self.weight_list = list(temp)
            
            print("[info] Trained Models Found...")
        except:
            print("[info] No Trained Models Found...")
            print("[info] But Its OK to Train New Models...")
            return 0
        
        params = AE.dA_params(n_visible=self.n_dim, n_hidden=0, lr=self.lr, corruption_level=0, gracePeriod=0, hiddenRatio=self.hr)
        for i in range(self.n_detector):
            temp = AE.dA(params, str(i))
            with open(("model//"+str(i)+"thmodel.pkl"), 'rb') as file:
                temp = pickle.loads(file.read())
            self.detector_pool.append(temp)
    
    def get_num(self):
        return len(self.detector_pool)

    def get_weimay(self):
        return self.weight_mat
    
class dual_ensemble():
    
    def __init__(self, learner='PCA', lim = 30, tttt=30):
        self.learner = learner
        self.dual_normal = ensemble(limit = lim, ttttt=tttt)
    
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
        self.dual_normal.save_ae('normal')
    
    def ensembleupdate(self, x):
        self.dual_normal.adjust(x, update=False)
    
    def load(self):
        self.dual_normal.load_ae()
    
    def retsyspara(self):
        return self.dual_normal.get_weimay()