from numpy import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import ENIDrift_ae as AE

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
        self.n_dim = 200
        self.hr = 0.75
        self.lr = 0.05
        self.epoch = 50
    
    def train(self, t):
        
        try:
            num = t.shape[0]
        except:
            num = len(t)

        params = AE.dA_params(n_visible=self.n_dim, n_hidden=0, lr=self.lr, corruption_level=0, gracePeriod=0, hiddenRatio=self.hr)
        self.learner_pool = AE.dA(params, "unknown")
        
        scores = []
        for r in range(self.epoch):
            for i in range(num):
                self.learner_pool.train(t[i, :].reshape(1, -1))

        for i in range(num):
            scores.append(self.learner_pool.train(t[i, :].reshape(1, -1)))
        self.threshold_list = max(scores)
        
        """
        model = PCA(n_components=0.99)
        model.fit(t)
        scores = model.score_samples(t)
        self.threshold_list = sorted(scores)[0]
        self.learner_pool = model
        """
        
        """
        x = mat(x)
        all_idx = arange(x.shape[0])
        k = int(sqrt(x.shape[0]))
        
        for i in range(self.num_simulation):
            
            t_idx = all_idx
            random.shuffle(t_idx)
            
            # if self.replace == True:
            # if self.replace == False:
            sampled_data = x[t_idx[:k]]
            
            # scaler = StandardScaler()
            # sampled_data = scaler.fit_transform(sampled_data)
            # self.scaler_pool.append(scaler)
            
            # if self.l == 'PCA':
            model = PCA(n_components=0.99)
            model.fit(sampled_data)
            
            try:
                scores = model.score_samples(sampled_data)
            except:
                print(sampled_data)
                print(sampled_data.shape)
                print(str(isinf(sampled_data).any == True))
                print(str(isnan(sampled_data).any == True))
                print(str(x.shape))
                scores = model.score_samples(sampled_data)
            
            self.threshold_list.append(sorted(scores)[int(k*self.alpha)])
            self.learner_pool.append(model)
        """
    
    def pred(self, x):
        
        result = [0]*x.shape[0]
        
        for i in range(x.shape[0]):
            if not self.threshold_list <= self.learner_pool.execute(x[i].reshape(1, -1)):
                result[i] = 1 # belong to the class
        
        """
        temp_result = zeros((self.time_test, self.ensemble_size))
        all_pred = zeros((self.num_simulation, ))
        for i in range(self.num_simulation):
            if self.threshold_list[i] <= self.learner_pool[i].score(x.reshape(1, -1)):
                all_pred[i] = 1 # belong to the class
            else:
                all_pred[i] = 0 # doesn't belong to the class
        
        for i in range(self.time_test):
            rand_idx = random.permutation(self.num_simulation)
            temp_result[i, :] = all_pred[rand_idx[:self.ensemble_size]]
        
        pred_result = mean(temp_result, 1)
        """
        return result