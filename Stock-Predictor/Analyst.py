class Analyst:
  def __init__(self, ticker):
    from Stock import Stock as Stock
    from sklearn.model_selection import train_test_split
    
    stock = Stock(ticker)
    self.stock = stock

    xTrain, xTest, yTrain, yTest = train_test_split(stock.features, stock.y)

    from sklearn import svm
    clf = svm.SVC()
    clf.fit(xTrain, yTrain)
    
    self.bestModel = clf
    self.bestScore = clf.score(xTest, yTest)

  #Returns prediction with best score in an indexed tuple
  def predict(self, info):
    return (self.bestModel.predict(info), self.bestScore)

  def cTl(self, transFeat, r):
    
    import numpy as np
    features = []
    for i in r:
      #print(f"r: {r}, FL: {len(transFeat)}")
      features.append(transFeat[i])
    
    return np.transpose(features)
  
  def optimize(self, stock):
    from sklearn.model_selection import train_test_split
    from itertools import combinations
    from sklearn import svm
    import numpy as np
    import copy

    transposed_features = np.transpose(copy.deepcopy(stock.features))
    indexSets = list(range(len(transposed_features)-1))

    done = {}

    end_counter = 0
    for i in range(1,len(stock.features)-1):
      if end_counter >= 500:
        break

      elif end_counter < 500:
        for combo in combinations(indexSets, i):

          if end_counter >= 500:
            break

          if combo not in done:
            done[combo] = 1
            
            combo_data = self.cTl(transposed_features, combo)

            xTrain, xTest, yTrain, yTest = train_test_split(combo_data, stock.y)       

            clf = svm.SVC()
            clf.fit(xTrain, yTrain)
            score = clf.score(xTest,yTest)

            end_counter = 0 if score > self.bestScore else end_counter + 1

            if score > self.bestScore:
              self.bestCombo = combo
              self.bestScore = score
              self.bestModel = clf
              print(f"New best score: {score}")
    print(f"Optimized Score: {self.bestScore}")
    

