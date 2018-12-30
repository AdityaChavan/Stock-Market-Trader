import pandas as pd                                                                                               
import numpy as np                                                                                                
import datetime as dt                                                                                             
import os                                                                                      
import matplotlib.pyplot as plt
       
from util import get_data, plot_data                                                                                              

def author():
        return 'achavan7' # replace tb34 with your Georgia Tech username.

def stats(p ):
    
    cr_p=(p[-1]/p[0]) -1
    
    dr_p=p.copy()
    
    dr_p[1:]=(p[1:]/p[:-1].values)-1
    
    dr_p[0]=0
  
    k= np.sqrt(252)
    adr_p=dr_p[1:].mean()
    sddr_p=dr_p[1:].std(ddof=1)
    sr_p=k*adr_p/sddr_p      
    #print ''
    #print "Benchmark: CR: ",round(cr_b,4),"  ADR: ",round(adr_b,4),"  SDDR: ",round(sddr_b,4),"  SR: ",round(sr_b,4)
    print "Statistics: CR: ",round(cr_p,4),"  ADR: ",round(adr_p,4),"  SDDR: ",round(sddr_p,4),"  SR: ",round(sr_p,4)
    #print ''
    return round(cr_p,4),round(adr_p,4),round(sddr_p,4),round(sr_p,4)
                                                            
def compute_portvals(symbol,df1, start_val = 1000000, commission=9.95, impact=0.005):            
  
 
  
  start_date= df1.index[0]
  end_date=df1.index[-1]
  price=  get_data([symbol],pd.date_range(start_date, end_date))  
  #print price
  
  df=price.ix[:,symbol].copy()
  df[:]=0
  
  for i in range(price.shape[0]):
     df[i]=df1.values[i]
        
  
  
  
  portval=df.copy()
  cash=df.copy()
  stock_no=df.copy()
  stock_val=df.copy()
  
  cash[0]=start_val-df[0] * price.ix[0,symbol]
  stock_no[0]=df[0]
  stock_val[0]=stock_no[0]*price.ix[0,symbol]
  portval[0]=stock_val[0]+cash[0]

  
  for i in range(df.shape[0]-1):
    if not (df[i+1]==0):
      stock_no[i+1]=stock_no[i]+df[i+1]
    else:
      stock_no[i+1]=stock_no[i]  
    stock_val[i+1]=stock_no[i+1]*price.ix[i+1,symbol]  
    cash[i+1]=cash[i]-df[i+1]*price.ix[i+1,symbol]
    cash[i+1]=cash[i+1]- np.absolute(df[i+1]*price.ix[i+1,symbol])*(impact) 
    if not(df[i+1]==0):
      cash[i+1]=cash[i+1]-commission
    portval[i+1]=stock_val[i+1]+cash[i+1]
  

  print("Stock:")
  stats(portval)
  
  portval_b=1000*price.ix[:,symbol]+start_val-1000*price.ix[0,symbol]
  
  print("Benchmark:")
  stats(portval_b)
 
  port=portval/portval[0]
  portval=portval/portval[0]  
  portval_b=portval_b/portval_b[0]  
  

  return port