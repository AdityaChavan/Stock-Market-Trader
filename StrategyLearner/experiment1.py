import cv2
import csv
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt  		   	  			    		  		  		    	 		 		   		 		  
import math  
import numpy as np
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import os
from random import shuffle
import sys  		
import time
import util    	  			    		  		  		    	 		 		   		 		  

from indicators import indicators		   	  			    		  		  		    	 		 		   		 		  
import StrategyLearner as st
import ManualStrategy as ms
from marketsimcode import compute_portvals 
import DTLearner as dt
import LinRegLearner as lrl
import CNNLearner as cnn

  	


        	   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    if len(sys.argv) != 1:  		   	  			    		  		  		    	 		 		   		 		  
        print "Usage: python testlearner.py"  		   	  			    		  		  		    	 		 		   		 		  
        sys.exit(1)  		   	  			    		  		  		    	 		 		   		 		  
    
    sym='AAPL'
    sv=100000
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2011,12,31)
    
    ###Strategy Learner
    learner = st.StrategyLearner(verbose=False)    
    learner.addEvidence(sym,sd,ed,sv) # train it  		   	  			    		  		  		    	 		 		   		   
    trade_rf,trade_dt=learner.testPolicy(sym,sd,ed,sv)
    print "\nRandom Forest\n"
    portval1=compute_portvals(sym,trade_rf,commission=0,impact=0.001,start_val=sv)
    print "\nDecision Trees\n"
    portval_dt=compute_portvals(sym,trade_dt,commission=0,impact=0.001,start_val=sv)
 
    
    ##Manual Strategy    
    trade2 = ms.testPolicy(sym, sd, ed, sv)  		   
    print "\nManual Strategy\n"
    portval2=compute_portvals(sym,trade2,commission=0,impact=0.00,start_val=sv)




    ##CNN 
    original=sys.stdout#temporarily redirect output
    sys.stdout = open('CNN_debug.log', 'w')
    trade_cnn=cnn.cnn( sym,sd,ed) 
    sys.stdout = original
    print "\nCNN\n"
    portval_cnn=compute_portvals(sym,trade_cnn,commission=0,impact=0,start_val=sv)

          
    
       
       
    plt.figure(figsize=(15, 6))
    price=  util.get_data([sym],pd.date_range(sd,ed))     
    df_temp = pd.concat([ portval_cnn,portval_dt,portval1,price.ix[:,sym]/price.ix[0,sym] ], keys=[ 'a','b','c','d','e','f'], axis=1) 
    plt.plot(df_temp)
    plt.legend([ 'CNN','Decision Trees','Random Forest','Stock-AAPL'])
    plt.savefig('Experiment-1.png')  
    
    
    
    	  			    		  		  		    	 		 		   		
 