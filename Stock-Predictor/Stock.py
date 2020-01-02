class Stock:
    def __init__(self, ticker, endBias=1):
        print("Creating a new stock file")
        from yahoo_historical import Fetcher
        #B is the starting day relative to the list.
        #This is because you have to be looking BACKWARDS to see the answer...
        self.b = endBias
        self.data = Fetcher(ticker, [2019,1,1]).getHistorical()
        data = self.data
        self.y = self.genYs(data['Close'], data['Open']) if endBias == 1 else []
        

        opens, highs, lows, closes, adjCloses, volumes = data['Open'], data['High'], data['Low'], data['Close'], data['Adj Close'], data['Volume']

        self.features = [
          self.mmm(opens, opens), 
          self.mmm(highs, highs), 
          self.mmm(lows, lows), 
          self.mmm(closes, closes), 
          self.mmm(adjCloses, adjCloses), 
          self.mmm(volumes, volumes),
          
          self.mmm(opens, closes),
          self.mmm(highs, lows),
          self.mmm(lows, closes),
          self.mmm(opens, highs),

          self.numatize(opens),
          self.numatize(closes),
          self.numatize(lows),
          self.numatize(volumes),
          self.numatize(highs),
          self.numatize(adjCloses)
          ]

        #for i in self.features:
        #  print(len(i))

        import numpy as np
        self.features = np.transpose(self.features)
        #for i in self.features:
        #  print(len(i))

    #Takes the data and rounds it to the int value for additional features
    def numatize(self, feature):
      cleaned_data = []
      for i in range(3, len(feature)-self.b):
        cleaned_data.append(int(i))
      return cleaned_data

    #The function evaluates the momentum between two features (which can be the same feature)
    def mmm(self, aFet, bFet):
      cleaned_data = []
      
      for i in range(3, len(aFet)-self.b):
        #Today's Percentage Increase
        tpi = (aFet[i]- bFet[i-1] / bFet[i-1])*100
        #Yesterday's Percentage Increase
        ypi = (aFet[i-1] - bFet[i-2] / bFet[i-2])*100

        if tpi >= ypi:
          cleaned_data.append(1)
        elif tpi < ypi:
          cleaned_data.append(0)

      return cleaned_data


    #Generate Y's
    def genYs(self, closes, opens):
      answers = []
      #Answers can have 3 results...      
      #1 == percent close was +1% increase from yesterday
      #0 == percent close was +0% increase from yesterday
      #-1 == percent close was -0% decrease from yesterday

      for i in range(3, len(closes)-self.b):
        percentage = ((opens[i+1] - closes[i-1])/closes[i-1])*100
        
        if percentage >= 1:
          answers.append(1)
        elif percentage >= 0:
          answers.append(0)
        else:
          answers.append(-1)

      return answers