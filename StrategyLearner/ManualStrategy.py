from indicators import indicators
import pandas as pd  
import numpy as np   
import datetime as dt
import matplotlib.pyplot as plt
import os     
from marketsimcode import compute_portvals
from util import get_data, plot_data   
from indicators import indicators


def author():
  return 'achavan7' # replace tb34 with your Georgia Tech username.

def testPolicy(symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000):
  price=  get_data([symbol],pd.date_range(sd,ed))  
  sma,bbp,mom=indicators(symbol,sd,ed)

 
      
  df=price.ix[:,symbol].copy()
  df[:]=0


  K=5
  for i in range((price.shape[0]-1)):
    if (i%K==0): #check every Kth day, to avoid high commissions 
      itr= i
      if (np.isnan(sma[itr]) or np.isnan(bbp[itr]) or np.isnan(mom[itr])):#if nan, hold at 0
          df[itr+1]=0
          continue
          
      if(sma[itr-K*4:itr].mean()>1): #bullish market #stricter conditions to short

        if(bbp[itr]>1 or (sma[itr-K*2:itr].mean()>1.2 or mom[itr-K*2:itr].mean()<0.1)): #use the mean of the indicator for the last N days
          #short
          df[itr+1]=-1# use ith indicators to calculate i+1th day, its like using yesterdays indicator to make todays decision.
        elif (bbp[itr]<0.3 or (sma[itr-K*2:itr].mean()<0.9 or mom[itr-K*2:itr].mean()>0)):
          #buy
          df[itr+1]=1 
        else :
          df[itr+1]=0  
      
      else: #bearish market #tend to buy

        if (bbp[itr]<0.2 or (sma[itr-K*2:itr].mean()<0.9 or mom[itr-K*2:itr].mean()>0)):
          #buy
          df[itr+1]=1 
        elif(bbp[itr]>0.8 or (sma[itr-K*2:itr].mean()>1.1 or mom[itr-K*2:itr].mean()<0)):
          #short
          df[itr+1]=-1
        else :
          df[itr+1]=0          
    else:
      df[i+1]=df[i]#hold for next 5 days
      
      
  data_frame=df.copy()
  for i in range(price.shape[0]-1):
      data_frame[i+1]=(df[i+1]-df[i])*1000
  
  anss = price[[symbol,]].copy()  # only portfolio symbols  		   	  			    		  		  		    	 		 		   		 		  
  for i in range(price.shape[0]):
      anss.values[i,:]=data_frame[i]
        

  return anss

def test_code():
  sd = dt.datetime(2008,1,1)                                              
  ed = dt.datetime(2009,12,31)
  symbol = 'BRK.B'
  sv = 100000
  testPolicy(symbol, sd, ed, sv) 
   
  
if __name__ == "__main__":              
   test_code()  
   