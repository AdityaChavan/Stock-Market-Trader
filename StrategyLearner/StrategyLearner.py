import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import util as ut  		   	  			    		  		  		    	 		 		   		 		  
import random  		   	  			    		  		  		    	 		 		   		 		  
from indicators import indicators
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals   		   	  			    		  		  		    	 		 		   		 		  
import numpy as np
import RTLearner as rt
import BagLearner as bl
import DTLearner as dt
import LinRegLearner as lrl

class StrategyLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
   # constructor  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			    		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			    		  		  		    	 		 		   		 		  
        self.impact = impact  		   	  			    		  		  		    	 		 		   		 		  
        self.learner = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size":5}, bags = 20, boost = False, verbose = False) 
        self.learner2 = bl.BagLearner(learner = dt.DTLearner, kwargs = {"leaf_size":5}, bags = 20, boost = False, verbose = False) 
    
        	
          	
    # this method should create a QLearner, and train it for trading  		   	  			    		  		  		    	 		 		   		 		  
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
        # add your code to do learning here  	
        
        price=  ut.get_data([symbol],pd.date_range(sd,ed))  
        sma,bbp,mom=indicators(symbol,sd,ed)	   	  		
        
            
        N=10 #N day return 
        
        Y=np.zeros(price.shape[0])
        
        
        for t in range(price.shape[0]-N):
          ret = (price.ix[t+N,symbol]/price.ix[t,symbol]) - 1.0
          Y[t]=ret
        #print Y.shape#996 1006
        
        
        
        margin=np.amax(Y)-np.amin(Y)
        imp=min(10*self.impact,0.2)

        ybuy=np.mean(Y)+margin*(0.1+imp)
        ysell=np.mean(Y)-margin*(0.1+imp)
        
        for t in range(price.shape[0]-N):
          if Y[t] > ybuy:
              Y[t] = +1 # LONG
          elif Y[t] < ysell:
              Y[t] = -1 # SHORT
          else:
              Y[t] = 0 # CASH
        


        X=np.array([bbp,mom,sma])
        X=np.transpose(X)
        X=X[10:]
        Y=Y[10:]
        Y_df=np.array(Y)
        
        #print X.shape,Y_df.shape
        
        
        self.learner.addEvidence(X, Y_df)    
        self.learner2.addEvidence(X, Y_df)    
        #self.learner3.addEvidence(X, Y_df)    
            
       	  			    		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		   	  			    		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):  		   	  			    		  		  		    	 		 		   		 		  
  		  
        price=  ut.get_data([symbol],pd.date_range(sd,ed))  
        sma,bbp,mom=indicators(symbol,sd,ed)	   	  		
        
        X=np.array([bbp,mom,sma])
        X=np.transpose(X)
        
        Y=self.learner.query(X)
        Y_df=pd.DataFrame({'Y':Y,'date':price.index  }	)
        Y_df=Y_df.set_index('date') 	  
        data_frame = price[[symbol,]].copy()  # only portfolio symbols  		   	  
        for i in range(price.shape[0]-1):
          data_frame.values[i+1,:]=(Y_df.ix[i+1]-Y_df.ix[i])*1000
        data_frame.values[0,:]=Y_df.ix[0]*1000#data_frame.values[0,:]*1000
        trades_rf=data_frame		    		  		  		    	 		 		   		 		  

        Y=self.learner2.query(X)
        Y_df=pd.DataFrame({'Y':Y,'date':price.index  }	)
        Y_df=Y_df.set_index('date') 	  
        data_frame = price[[symbol,]].copy()  # only portfolio symbols  		   	  
        for i in range(price.shape[0]-1):
          data_frame.values[i+1,:]=(Y_df.ix[i+1]-Y_df.ix[i])*1000
        data_frame.values[0,:]=Y_df.ix[0]*1000#data_frame.values[0,:]*1000
        trades_dt=data_frame		    		  		  		    	 		 		   		 		  


#changed this to 3
        return trades_rf,trades_dt  	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "One does not simply think up a strategy"  		   	  			    		  		  		    	 		 		   		 		  
