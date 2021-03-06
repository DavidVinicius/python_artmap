import numpy as np
from python_artmap import ART, ARTFUZZY

class ARTMAPFUZZY(ART):    
    rho        = 0
    WAB        = []
    championsA = []


    def __init__(self, INPUT, OUTPUT, rhoARTa=0.5, rhoARTb=0.5, alphaARTa=0.001, betaARTa=1, alphaARTb=0.001, betaARTb=1, maxValueArta=1, maxValueArtb=1, epsilon=0.001):
        self.ArtA = ARTFUZZY(self.layerF0(INPUT, maxValueArta), rho=rhoARTa, alpha=alphaARTa, beta=betaARTa)
        self.ArtB = ARTFUZZY(self.layerF0(OUTPUT, maxValueArtb), rho=rhoARTb, alpha=alphaARTb, beta=betaARTb)
        self.epsilon = epsilon
        
        self.rho  = 1
        self.WAB  = np.ones([1, OUTPUT.shape[0]])

    def train(self):
        interator = 0
        for inputB in self.ArtB.I:            
            championIndexB = self.ArtB.match(inputB)
            
            rhoArtABase = self.ArtA._rho
            for inputA in self.ArtA.I[interator:]:
                categories      = self.ArtA.categories(inputA, self.ArtA.W)
                championA       = categories.max()
                championIndexA  = categories.argmax()                

                while championA != 0:                                    
                    if self.ArtA.hadRessonance(inputA, self.ArtA.W[championIndexA]):
                                                
                        if self.hadRessonance(self.ArtB.Y[championIndexB], self.WAB[championIndexA], self.rho):
                            self.ArtA.W[championIndexA]  = self.ArtA.learn(inputA, self.ArtA.W[championIndexA])
                            self.WAB[championIndexA]     = self.activate(self.WAB[championIndexA], championIndexB)
                            break

                        else:                           
                            x      = self.AND(inputA, self.ArtA.W[championIndexA])
                            newRho = (sum(x) / sum(inputA))                            

                            self.ArtA._rho = newRho + self.epsilon
                    else:
                        categories[championIndexA] = 0                
                        championA                  = categories.max()
                        championIndexA             = categories.argmax()
                else:
                    self.ArtA.setW(
                        np.insert(self.ArtA.W, len(self.ArtA.W), inputA, 0)
                    )                    
                    self.ArtA.activate(championIndexA+1)
                    self.WAB = np.insert(self.WAB, len(self.WAB), self.activate(self.WAB[championIndexA], championIndexB), 0)                    
                                                                    
                self.ArtA._rho = rhoArtABase
                interator += 1
                break
        
    def activate(self, W, i):
        temp    = np.zeros(len(W))
        temp[i] = 1
        return list(temp)
    
    def test(self, INPUT, maxInputValue=1):  
        INPUT           = np.divide(INPUT, maxInputValue)                         
        INPUT           = np.concatenate((INPUT, (1-INPUT)), axis=0)
        categories      = self.ArtA.categories(INPUT, self.ArtA.W)
        championA       = categories.max()
        championIndexA  = categories.argmax()
        rhoTest         = self.ArtA._rho - (self.ArtA._rho * 0.1)
        while rhoTest > 0.00001:
            while championA != 0:
                if self.hadRessonance(INPUT, self.ArtA.I[championIndexA], rhoTest):
                    t    = list(self.WAB[championIndexA])
                    artB = list(self.ArtB.W[t.index(1)])                
                    s    = [str(i) for i in artB]
                    return {
                        "index": t.index(1),                    
                        "ArtB": artB,
                        "id": "".join(s).replace(".", "")
                    }
                else:
                    categories[championIndexA] = 0                
                    championA                  = categories.max()
                    championIndexA             = categories.argmax()
            categories      = self.ArtA.categories(INPUT, self.ArtA.W)
            championA       = categories.max()
            championIndexA  = categories.argmax()
            rhoTest         = rhoTest - (rhoTest * 0.25)            
            
        return -1

            

    
