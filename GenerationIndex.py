from scipy.stats import f
from scipy.stats import chi2
from measure import *
from numpy import *
from SubLearner import *

class G_index():
    
    def __init__(self, lamda, delta, num_test=1000, kind='PCA', num_simulation=100, mute=True, ID='normal'):
        self.ID = ID
        self.delta = delta
        self.lamda = 0.3
        self.round = 0
        self.num_simulation = num_simulation
        self.G_idx_last = None
        self.G_idx_cur = None
        self.data_store = array([])
        self.data_test = array([])
        self.data_train = array([])
        self.num_test = num_test
        self.model = None
        self.time_try_retrain = 0
        
    def check(self, x):
        
        if self.round == 0:
            self.round = self.round + 1
            self.data_store = x
            self.data_test = x[random.permutation(x.shape[0])[:self.num_test]]
            self.update_model()
            self.data_train = x
            self.time_try_retrain = 0
            return 'Training'
        
        if self.G_idx_last is None:
            self.G_idx_last = self.G_idx(x)
            self.data_store = x
            return 'Initialize G-idx'
        
        if self.data_store.shape[0] == 0:
            x_ = x
        else:
            x_ = append(self.data_store, x, axis=0)
        
        self.G_idx_cur = self.G_idx(x_)
        # p = self.check_significance()
        
        if self.G_idx_last < self.G_idx_cur:
            self.G_idx_last = self.G_idx_cur
            self.data_store = x_
            self.time_try_retrain = self.time_try_retrain + 1
            return 'More Sample'
        else:
            # data_test_temp = append(self.data_test, self.store_chunk_data)
            # self.data_test = data_test_temp[random.permutation(data_test_temp.shape[0])[:self.num_test]]
            if self.data_store.shape[0] != 0:
                self.data_test = append(self.data_test, self.data_store, axis=0)[-self.num_test:]
            self.update_model()
            self.data_train = x_
            self.data_store = x
            self.G_idx_last = self.G_idx(x)
            self.time_try_retrain = 0
            return 'Training'
    
    def G_idx(self, x):
        result = self.model.pred(x)
        v = var(result)
        e = 1 - (sum(result)/len(result))
        G = v + self.lamda * e
        
        return G
    
    def check_significance(self):
        f_p = []
        for i in range(self.num_test):
            if self.G_idx_cur[i] != 0:
                f_p.append(1 - f.cdf(self.G_idx_last[i] / self.G_idx_cur[i], self.num_test - 1, self.num_test - 1))
        f_p = [x for x in f_p if x != 0]
        K = -2 * sum(log(array(f_p)))
        chi2_p_value = 1 - chi2.cdf(K, 2 * len(f_p))
        
        return chi2_p_value
    
    def get(self):
        return self.data_train
    
    def clear(self):
        self.data_store = array([])
        self.time_try_retrain = 0
    
    def update_model(self):
        self.model = SubLearn()
        self.model.train(self.data_test)
    
    def times(self):
        return self.time_try_retrain