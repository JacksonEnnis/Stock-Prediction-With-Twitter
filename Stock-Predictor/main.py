def generatePrediction(ticker):
  pred_info = Stock(ticker, 0).features
  pred_info = pred_info[-1]

  thinker = Analyst(ticker)
  thinker.optimize(thinker.stock)
      
  cleaned_pred_info = []
  for i in thinker.bestCombo:
    cleaned_pred_info.append(pred_info[i])

  result = thinker.predict(np.transpose(cleaned_pred_info).reshape(1,-1))

  return result

from Analyst import Analyst as Analyst
from Stock import Stock as Stock

from colorama import Fore, Back, Style 

print("Welcome to my stock predictor...\n")
print(Fore.GREEN + "Type 'help' if you don't know how to run the program. \n Otherwise, type your command now.\n")

user_prompt = ""
while("help" not in user_prompt or "query" not in user_prompt  or "battery" not in user_prompt): 
  user_prompt = input(Fore.WHITE + "" + "\n")

  if "help" in user_prompt:
    print(Fore.LIGHTYELLOW_EX + "Currently, this program has 3 commands:\n")
    print("help: an up-to-date list of usable commands\n")
    print("query TICKER_GOES_HERE: prints a prediction for the requested stock along with it's accuracy\n")
    print("battery: runs a battery of stocks for accuracy and prediction and writes the results to a csv file.\n")
    user_prompt = ""
  
  elif "query" in user_prompt:
    import numpy as np
    ticker = user_prompt.split(" ")[1]

    result = generatePrediction(ticker[1])

    if result[0] == 1:
      print(Fore.LIGHTBLUE_EX +f"{ticker} is going to go up by at least +1% next trade day! {result[1]}")

    elif result[0] == 0:
      print(Fore.LIGHTBLUE_EX +f"{ticker} is going to go up by at least +0% next trade day! {result[1]}")
    
    else:
      print(Fore.LIGHTBLUE_EX +f"{ticker} is going to go down by at least -0% next trade day! {result[1]}")
  
  elif "battery" in user_prompt:
    stocks = ['AAPL','TSLA','AMZN','GOOG','F']
    print(Fore.YELLOW + f"Battery of queries for: {stocks} being written into 'analysis.txt'")
    f = open('analysis.txt', 'w')

    import numpy as np
    ticker = "F"
    for ticker in stocks:
      result = generatePrediction(ticker)
      line = str(result[0][0]) + ',' + str(result[1]) + '\n'
      f.write(line)
    f.close()
    print("\nFile finished! Check 'analysis.txt'!")
    break

  
  else:
    print(Fore.RED + "Sorry, what was that?")