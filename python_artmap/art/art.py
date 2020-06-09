import numpy as np

class ART():
    Y          = []
    Js         = []
    _W         = []
    categories = []
    
    def __init__(self, I, alpha = 0.001, rho = 0.5, beta = 1):
        self._alpha = alpha
        self._rho   = rho
        self._beta  = beta
        self.setI(I)  
        self.setW(np.ones(self.I.shape))
        #self.setW(np.ones((1,len(self.I[0]))))        

    @staticmethod
    def layerF0(I, valueMax = 0):
        IC = ART.normalize(I, valueMax)
        IC = ART.complement(IC)    
        return IC
    
    @staticmethod
    def normalize(arr, valueMax = 0):
        if valueMax == 0:
            valueMax = arr.max()

        I  = np.divide(arr, valueMax)
        return I
    
    @staticmethod
    def complement(I):
        I = np.concatenate((I, (1-I)), axis=1)
        return I        
        

    def AND(self, arr1, arr2):        
        try:        
            return np.minimum(arr1, arr2)
        except Exception as e:
            print(e)
            print("AND", arr1, arr2)
            quit()
    
    @property
    def I(self):
        return self._I
    
    
    def setI(self, I):
        if isinstance(I, np.ndarray):
            self._I = I
        else:
            self._I = np.array(I)
    
    @property
    def W(self):
        return self._W
    
    
    def setW(self, W):
        if isinstance(W, np.ndarray):
            self._W = W
        else:
            self._W = np.array(W)

    def hadRessonance(self, IC, W, rho):
        try:
            IC  = np.asarray(IC)        
            x   = np.asarray(self.AND(IC, W))
            y   = x.sum(axis=0) / IC.sum(axis=0)
            return (y >= rho)
        except Exception as e:
            print(e)
            print("HAD", IC, W)
            quit()
    
    def vigilanceValue(self, IC, W):
        x   = self.AND(IC, W)
        return (sum(x) / sum(IC))
    
    def groupCategories(self, IC, W, alpha = 0.0001):
        categories  = []
        for i in range(0, len(IC)):
            a       = np.sum(self.AND(IC[i], W[i]))
            temp    = round(a / (alpha + np.sum(W[i])), 5)
            categories.append(temp)
        return categories
    
    def indexOfChampion(self, categories):
        championB      = max(categories)
        
        return categories.index(championB)
    
    def valueOfChampion(self, categories):
        return max(categories)