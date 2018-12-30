import numpy as np
import warnings
from datetime import datetime

class RTLearner(object):
  def __init__(self,leaf_size=1,verbose=False):
    self.leaf_size=leaf_size 
    self.node_number=0
    self.tree=np.array([])
    self.verbose=verbose
    
  def author(self):
    return 'achavan7'
  
  def inc_no(self):
    global node_number
    self.node_number+=1
    return self.node_number
    
  def addEvidence(self,Xtrain,Ytrain):
    startTrainingTime = datetime.now()
    np.set_printoptions(threshold='nan')
    global leaf_size,tree
    
    s1=np.size(Xtrain[:,0])
    
    flag1=(s1<self.leaf_size)
    flag2=np.all(Ytrain[0]==Ytrain[:],axis=0)#all elements same y
    
    if (flag1 or flag2 ):#its a leaf!
      stat=self.inc_no()
      return np.array([stat,'leaf',np.mean(Ytrain),np.nan,np.nan])
      
    else:  
      with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        Xtrain=np.nan_to_num(Xtrain)       
        max_corr_index=np.random.randint(0, (np.size(Xtrain[0,:])) )
        median=np.nanmedian(Xtrain[:,max_corr_index])
      greater_x= Xtrain[Xtrain[:,max_corr_index]>median]
      greater_y= Ytrain[Xtrain[:,max_corr_index]>median]
      lesser_x= Xtrain[Xtrain[:,max_corr_index]<=median]
      lesser_y= Ytrain[Xtrain[:,max_corr_index]<=median]
      s1=np.size(greater_x[:,0])
      s2=np.size(greater_y)
      s3=np.size(lesser_x[:,0])
      s4=np.size(lesser_y)
      if(np.size(lesser_y)==0)or(np.size(greater_y)==0):#if any tree is empty, use mean
        mean=np.mean(Xtrain[:,max_corr_index])
        greater_x= Xtrain[Xtrain[:,max_corr_index]>mean]
        greater_y= Ytrain[Xtrain[:,max_corr_index]>mean]
        lesser_x= Xtrain[Xtrain[:,max_corr_index]<=mean]
        lesser_y= Ytrain[Xtrain[:,max_corr_index]<=mean]
        s1a=np.size(greater_x[:,0])
        s2a=np.size(greater_y)
        s3a=np.size(lesser_x[:,0])
        s4a=np.size(lesser_y)
        median=mean
      
      if len(set(Xtrain[:,max_corr_index]))==1:
        stat=self.inc_no()
        return np.array([stat,'leaf',np.mean(Ytrain),np.nan,np.nan])
      stat=self.inc_no()
      left_tree=self.addEvidence(lesser_x,lesser_y)
      right_tree=self.addEvidence(greater_x,greater_y)
      
      root=np.array([('%d' % stat),max_corr_index,median,1,(np.size(left_tree)/5)+1])#np.size(left_tree[0])+1]
      self.tree=np.vstack((root,left_tree,right_tree))
      if stat==1:
        np.set_printoptions(threshold='nan')
        total_training_time= datetime.now() - startTrainingTime
        if(self.verbose):
          print 'Total training time: ',total_training_time          
      return self.tree
    
  def query(self,Xtest): 
    startTestingTime = datetime.now()
    global tree
    row=0
    Ytest=np.zeros(np.size(Xtest[:,0]))
    for i in range(np.size(Xtest[:,0])):
      row=0
      while(self.tree[row,1]!='leaf'):
        if Xtest[i,int(self.tree[row,1])]<=float(self.tree[row,2]):
          row=row+int(self.tree[row,3])
        else:
          row=row+int(self.tree[row,4])
      Ytest[i]=float(self.tree[row,2])
    total_testing_time= datetime.now() - startTestingTime  
    if(self.verbose):
        print 'Total testing time: ',total_testing_time          
  
    return Ytest #[:,0]
    
    
    
    
    
    
    
    
    
    