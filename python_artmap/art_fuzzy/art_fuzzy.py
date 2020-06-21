import numpy as np
from python_artmap import ART


class ARTFUZZY(ART):

    championIndex = 0
    championValue = 0
    categoriesArray = []

    def __init__(self, I, alpha=0.001, rho=0.5, beta=1):
        super().__init__(I, alpha, rho, beta)

    def learn(self, IC, W):
        temp1 = self._beta * self.AND(IC, W)
        temp2 = (1 - self._beta) * IC
        return temp1 + temp2

    def activate(self, i):
        temp    = np.zeros(len(self.I))
        temp[i] = 1
        self.Y.append(list(temp))

    def hadRessonance(self, IC, W):
        x = self.AND(IC, W)
        return ((sum(x) / sum(IC)) >= self._rho)    

    def train(self):        
        for i in self.I:
            self.match(i)

    def match(self, inputValue):
        categories    = self.categories(inputValue, self.W)        
        champion      = categories.max()
        championIndex = categories.argmax()

        while champion != 0:            
            if self.hadRessonance(inputValue, self.W[championIndex]):                
                self.W[championIndex] = self.learn(inputValue, self.W[championIndex])
                self.activate(championIndex)                

                self.championIndex = championIndex
                self.championValue = champion

                break
            else:
                categories[championIndex] = 0
                champion = categories.max()
                championIndex = categories.argmax()
        else:
            self.setW(
                np.insert(self.W, len(self.W), inputValue, 0)
            )
            championIndex += 1            
            self.activate(championIndex)
            self.championIndex = championIndex
            self.championValue = champion
        
        return self.championIndex