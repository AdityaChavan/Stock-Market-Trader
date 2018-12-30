import pandas as pd  
import numpy as np   
import datetime as dt
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import os     
from util import get_data, plot_data   

def author():
  return 'achavan7' # replace tb34 with your Georgia Tech username.
  
def indicators(symbols,start_date, end_date):
 
  price=  get_data([symbols],pd.date_range(start_date, end_date))  
  #ffill, bfill
  price=price/price.ix[0,:]
  lookback=10
  sma=price.copy()
  for day in range(price.shape[0]):
    #for sym in symbols:
      sma.ix[day,symbols]=0
      
  for day in range(price.shape[0]):
      if day==0:
        sma.ix[day,symbols]=price.ix[day,symbols]
        continue
      if day<lookback:
    #    for sym in symbols:
        sma.ix[day,symbols]=sma.ix[day-1,symbols]+price.ix[day,symbols]
        continue
        
      sma.ix[day,symbols]=sma.ix[day-1,symbols]+price.ix[day,symbols]-price.ix[day-lookback,symbols]
      
  sma.ix[:,symbols]=sma.ix[:,symbols]/lookback 
  
  for day in range(lookback):
    sma.ix[day,symbols]=np.nan        
  #print price
  indicator=price.copy()
  indicator=indicator.ix[:,symbols]/sma.ix[:,symbols]
  
#  df_temp = pd.concat([    sma.ix[:,symbols],  price.ix[:,symbols],  indicator.ix[:] -1 ], keys=['SMA', 'Prices','Indicator'], axis=1) 
#  plt.figure(figsize=(10,5))
#  plt.plot(  df_temp)
#  plt.legend(['SMA', 'Prices','Price/SMA'])
#  plt.suptitle('Price / SMA')
#  plt.xlabel('Normalized Price')
#  plt.xlabel('Dates')
#  plt.axhline(y=0, color='k')
#  plt.xlim([start_date,end_date])
#  plt.savefig('plot_SMA.png')
  
  
  #bolinger
    
  rolling=price.rolling(window=lookback,min_periods=lookback).std()
  top_band=sma+(2*rolling)
  bottom_band=sma-(2*rolling)
  bbp=(price-bottom_band)/(top_band-bottom_band)
  bb=bbp.ix[:,symbols].copy()
#  df_temp = pd.concat([ top_band.ix[:,symbols],bottom_band.ix[:,symbols],price.ix[:,symbols],(bb-0.5)/5], keys=['LB','UB','price','BB'], axis=1) 
#  plt.fill_between(price.index, top_band.ix[:,symbols], bottom_band.ix[:,symbols],alpha=0.2)
#  plt.figure(figsize=(15, 6))
#  plt.suptitle('Bolinger Bands')
#  plt.xlabel('Normalized Price')
#  plt.xlabel('Dates')
#  plt.axhline(y=0, color='k')
#  plt.plot(  df_temp)
#  plt.legend(['Yaxis','Upper Band', 'Bottom Band','Price','BB Percentage','Bolinger Area'])
#  plt.xlim([start_date,end_date])
#  
#  plt.savefig('plot_BB.png')
  
  #momentum
  N=10
  momentum=price.ix[:,symbols].copy()
  for t in range(N):
    momentum[t]=np.nan
  for t in range(price.shape[0]-N):
    momentum[t+N] = (price.ix[t+N,symbols]/price.ix[t,symbols]) - 1
  
#  df_temp = pd.concat([ price.ix[:,symbols], momentum], keys=['P','M'], axis=1)
#  plt.figure(figsize=(6,5))
#  plt.plot(  df_temp)
#  plt.legend(['Price', 'Momentum'])
#  plt.suptitle('Momentum')
#  plt.xlabel('Normalized Price')
#  plt.xlabel('Dates')
#  plt.axhline(y=0, color='k')
#  plt.xlim([start_date,end_date])
#  plt.savefig('plot_M.png')
  
  
  
  return indicator,bb,momentum
  
  
def test_code():
  sd = dt.datetime(2008,1,1)                                              
  ed = dt.datetime(2008,7,30) 
 
  #sma('JPM')
  indicators('JPM',sd,ed)
    
if __name__ == "__main__":              
   test_code()                                                                                     