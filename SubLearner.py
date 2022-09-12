from numpy import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class SubLearn():
    
    def __init__(self, learner='PCA', num_simulation=100, time_test=100,
                 ensemble_size=100, alpha=0.05):
        
        self.learner = learner
        self.num_simulation = num_simulation
        self.ensemble_size = ensemble_size
        self.time_test = time_test
        self.learner_pool = []
        self.threshold_list = []
        self.alpha = alpha
        self.scaler_pool = []
    
    def train(self, t):
        
        model = PCA(n_components=0.99)
        model.fit(t)
        scores = model.score_samples(t)
        self.threshold_list = sorted(scores)[0]
        self.learner_pool = model
        
    
    def pred(self, x):
        
        result = [0]*x.shape[0]
        
        for i in range(x.shape[0]):
            if self.threshold_list <= self.learner_pool.score(x[i].reshape(1, -1)):
                result[i] = 1
        
        return result