import numpy as np
from python_artmap import ART, ARTFUZZY

class ARTMAPFUZZY(ART):    
    rho        = 0
    WAB        = []
    championsA =[]
    Map        = []

    def __init__(self, INPUT, OUTPUT, rhoARTa=0.5, rhoARTb=0.5, rho=0.5):
        self.ArtA = ARTFUZZY(INPUT, rho=rhoARTa)
        self.ArtB = ARTFUZZY(OUTPUT, rho=rhoARTb)
        self.rho  = rho
        self.WAB  = np.ones([1, OUTPUT.shape[0]])

    def train(self):
        interator = 0
        for inputB in self.ArtB.I:            
            categories      = self.ArtB.categories(inputB, self.ArtB.W)
            champion        = categories.max()
            championIndexB  = categories.argmax()

            while champion != 0:                            
                if self.ArtB.hadRessonance(inputB, self.ArtB.W[championIndexB]):                    
                    self.ArtB.W[championIndexB]    = self.ArtB.learn(inputB, self.ArtB.W[championIndexB])                                    
                    self.ArtB.activate(championIndexB)

                    break
                else:                    
                    categories[championIndexB] = 0
                    champion                   = categories.max()
                    championIndexB             = categories.argmax()
            else:                      
                self.ArtB.setW(np.insert(self.ArtB.W, len(self.ArtB.W), inputB, 0))                            
                championIndexB += 1
                self.ArtB.activate(championIndexB)
            
            for inputA in self.ArtA.I[interator:]:
                categories      = self.ArtA.categories(inputA, self.ArtA.W, self.ArtA._alpha)
                championA       = categories.max()
                championIndexA  = categories.argmax()                

                while championA != 0:                                    
                    if self.ArtA.hadRessonance(inputA, self.ArtA.W[championIndexA]):
                                                
                        if self.hadRessonance(self.ArtB.Y[championIndexB], self.WAB[championIndexA], self.rho):
                            self.ArtA.W[championIndexA]  = self.ArtA.learn(inputA, self.ArtA.W[championIndexA])
                            self.WAB[championIndexA]     = self.activate(self.WAB[championIndexA], championIndexB)
                            break

                        else:
                            categories[championIndexA] = 0                
                            championA                  = categories.max()
                            championIndexA             = categories.argmax()

                            x                          = self.AND(inputA, self.ArtA.W[championIndexA])
                            newRho                     = (sum(x) / sum(inputA))                            

                            self.ArtA._rho            = newRho                        
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
                                                                    
                
                interator += 1
                break
    
    def train2(self):
        print("Treinando ...")
        
        for i in range(0, len(self.WAB)):            
                        
            self.ArtB.match(i)
            
            championIndexB  = self.ArtB.getIndexOfChampion()
            categories      = self.ArtA.categories()            
            championA       = categories.max()
            championIndexA  = categories.argmax()            

            while championA != 0:                                
                if self.ArtA.hadRessonance(self.ArtA.I[i], self.ArtA.W[championIndexA]):
                                        
                    if self.hadRessonance(self.ArtB.Y[championIndexB], self.WAB[championIndexA], self.rho):
                        self.ArtA.W[championIndexA]    = self.ArtA.learn(self.ArtA.I[i], self.ArtA.W[championIndexA])
                        self.ArtA.activate(championIndexA)
                        self.ArtA.Js.append([i, championIndexA])                                                                    
                        self.WAB[championIndexA]  = self.activate(self.WAB[championIndexA], championIndexB)
                        break
                    else:
                        categories[championIndexA] = 0                
                        championA                  = categories.max()
                        championIndexA             = categories.argmax()
                        x                          = self.AND(self.ArtA.I[i], self.ArtA.W[championIndexA])
                        newRho                     = (sum(x) / sum(self.ArtA.I[i]))

                        self.ArtA._rho            = newRho
                else:                    
                    categories[championIndexA] = 0                
                    championA                  = categories.max()
                    championIndexA             = categories.argmax()


    def activate(self, W, i):
        temp    = np.zeros(len(W))
        temp[i] = 1
        return list(temp)

    def test(self, INPUT, rho):
        categories      = self.ArtA.categories()            
        championA       = self.valueOfChampion(categories)
        championIndexA  = self.indexOfChampion(categories)

        while championA != 0:
            if self.hadRessonance(INPUT, self.ArtA.I[championIndexA], rho):
                return self.WAB[championIndexA]
            else:
                categories[championIndexA] = 0                
                championA                  = categories.max()
                championIndexA             = categories.argmax()
        
        return -1
    
    def testMapped(self, INPUT, rho):        
        categories      = self.ArtA.categories(INPUT, self.ArtA.W, self.ArtA._alpha)
        championA       = categories.max()
        championIndexA  = categories.argmax()        

        while championA != 0:
            if self.hadRessonance(INPUT, self.ArtA.I[championIndexA], rho):
                t    = list(self.WAB[championIndexA])
                artB = list(self.ArtB.W[t.index(1)])
                s    = [str(i) for i in artB]
                return {
                    "index": t.index(1),
                    #"value": self.WAB[championIndexA],
                    "ArtB": artB,
                    "id": "".join(s).replace(".", "")
                }
            else:
                categories[championIndexA] = 0                
                championA                  = categories.max()
                championIndexA             = categories.argmax()
        
        return -1

            

    
