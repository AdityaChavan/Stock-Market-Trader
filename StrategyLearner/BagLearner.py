import numpy as np

class BagLearner(object):
  def __init__(self,learner=None, kwargs = {}, bags = 20, boost = False,verbose=False):
    if not learner:
      import learner
    self.learner=learner
    self.kwargs=kwargs
    self.bags=bags
    self.boost=boost
    self.verbose=verbose
    
    self.learners=[]
    for i in range(self.bags):
      self.learners.append(self.learner(**self.kwargs))
    
    
  def author(self):
    return 'achavan7'
  
  def addEvidence(self,Xtrain,Ytrain):
    global bags
    global learners
    
    for learner in self.learners:
      sample_data_indexes=np.random.choice(range(np.size(Ytrain)),size=np.size(Ytrain),replace=True)#select random indexes
      #np.random.shuffle(sample_data_indexes)
      learner.addEvidence(Xtrain[sample_data_indexes,:],Ytrain[sample_data_indexes])#use the random indexes
      
  def query(self,Xtest):
    global learners
    global bags
    
    results=[]
    for learner in self.learners:
      results.append(learner.query(Xtest))
      
    Ytest=np.mean(results,axis=0) 
  
    for t in range(Ytest.shape[0]):
          ret = Ytest[t]
          if ret > 0.1:
              Ytest[t] = +1 # LONG
          elif ret < -0.1:
              Ytest[t] = -1 # SHORT
          else:
              Ytest[t] = 0 # CASH
    
 
        
    #print Ytest 
    return Ytest