import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
class LinRegLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False):  		   	  			    		  		  		    	 		 		   		 		  
        pass  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    def addEvidence(self,dataX,dataY):  		   	  			    		  		  		    	 		 		   		 		  
        newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])  		   	  			    		  		  		    	 		 		   		 		  
        newdataX[:,0:dataX.shape[1]]=dataX  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
        # build and save the model  		   	  			    		  		  		    	 		 		   		 		  
        self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    def query(self,points):  		   	  			    		  		  		    	 		 		   		 		  
        return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  