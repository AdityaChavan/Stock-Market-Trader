import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected,flatten
from tflearn.layers.estimator import regression
import util    	  			    		  		  		    	 		 		   		 		  
import numpy as np
import pandas as pd 
from random import shuffle
from indicators import indicators
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt  
import os

LR=0.001
MODEL='stock'
NUM_DAYS=0
TRAINING_SIZE=0
TESTING_SIZE=0
LOOKBACK=10
EPOCHS=50
MARGIN=0.01




def make_model(load_old):

  
  convnet = input_data(shape=[None,1,3, 1], name='input')
  convnet = conv_2d(convnet, 256, 2, activation='relu')
  convnet = max_pool_2d(convnet, 2)

  convnet = fully_connected(convnet, 1024, activation='relu')

  convnet = fully_connected(convnet, 3, activation='softmax')
  convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
  
  model = tflearn.DNN(convnet,tensorboard_dir='log')
  
  if os.path.exists('{}.meta'.format(MODEL)):
    if(load_old):model.load(MODEL)
    print "Model LOADED"
   

  return model


def create_train_data(sd,ed,symbol):
  #price=pd.read_csv(TRAIN_DIR,index_col='Date',parse_dates=True,usecols=['Date','Open','Volume'], na_values=['nan'])
  dates=pd.date_range(sd,ed)
  price=  util.get_data([symbol],dates)
#  price.rename(index=str, columns={"AAPL":"AAPL"})
  df1=pd.DataFrame(index=dates)
  price=df1.join(price)
  price=price.dropna()
  global NUM_DAYS
  NUM_DAYS=price.shape[0]
  

  sma,bbp,mom=indicators(symbol,sd,ed)

  Y=np.zeros(price.shape[0])
  global LOOKBACK
  N=LOOKBACK #N day return 
  

  for t in range(price.shape[0]-N):
     ret = (price.ix[t+N]/price.ix[t]) - 1.0
     Y[t]=ret[symbol]

     
     
  margin=np.amax(Y)-np.amin(Y)
  #imp=min(10*self.impact,0.2)
  global MARGIN
  ybuy=np.mean(Y)+margin*MARGIN#(0.1+imp)
  ysell=np.mean(Y)-margin*MARGIN#(0.1+imp)
  
   
  for t in range(price.shape[0]-N):
    if Y[t] > ybuy:
        Y[t] = +1 # LONG
    elif Y[t] < ysell:
        Y[t] = -1 # SHORT
    else:
        Y[t] = 0 # CASH
     
    
  Y_df=np.array(Y)
  X=np.array([bbp,mom,sma])
  X=np.transpose(X)
  
  Y_pan=pd.DataFrame(data=Y_df,index=price.index.values)
  
  df_temp = pd.concat([price[symbol]/price.ix[0,symbol],Y_pan])
  plt.figure(figsize=(15, 6))
  plt.plot(df_temp)
  plt.show()
  plt.savefig('Stock.png')
  
  Y3col=X.copy()
  for i in range(Y.shape[0]):
    if( Y[i]==0):
      Y3col[i,0]=0
      Y3col[i,1]=1
      Y3col[i,2]=0
    elif( Y[i]==-1):
      Y3col[i,0]=1
      Y3col[i,1]=0
      Y3col[i,2]=0
    elif( Y[i]==1):
      Y3col[i,0]=0
      Y3col[i,1]=0
      Y3col[i,2]=1
    else:
      Y3col[i,0]=0
      Y3col[i,1]=0
      Y3col[i,2]=0
  
  return X,Y3col,price
  
     

def train_model(model,X,Y):
  print X.shape,Y.shape
  global EPOCHS
  model.fit({'input': X}, {'targets': Y}, n_epoch=EPOCHS, show_metric=True, run_id=MODEL)
  model.save(MODEL)
  return model
  
  
def cnn(sym,sd,ed):
    tf.logging.set_verbosity(tf.logging.ERROR)
    price=  util.get_data([sym],pd.date_range(sd,ed))  
    X,Y,prices=create_train_data(sd,ed,sym)
    global LOOKBACK
    TRAINING_SIZE=int(NUM_DAYS)
    TESTING_SIZE=NUM_DAYS-TRAINING_SIZE#-LOOKBACK
    #print TRAINING_SIZE,TESTING_SIZE,NUM_DAYS
    X=X[LOOKBACK:]
    Y=Y[LOOKBACK:]
    X_train=np.array(X[:,:]).reshape(TRAINING_SIZE-10,1,3,1)
    Y_train=np.array(Y[:]).reshape(TRAINING_SIZE-10,3)
    
#    X_test=np.array(X[:,:]).reshape(TESTING_SIZE-10,3,1)
#    X_test=np.array(X[0,:]).reshape(1,3,1)
    
    Y_test=np.array(Y[:])
       
    model=make_model(0)
    
    model=train_model(model,X_train,Y_train)
    
    Y_out=np.zeros(TRAINING_SIZE)
   
    for i in range(TRAINING_SIZE-10):
      X_test=np.array(X[i,:]).reshape(1,3,1)
      model_out=model.predict([X_test])[0]
      n=np.argmax(model_out)
      #print model_out,n
      Y_out[i]=n-1
      Y_test[i,:]=model_out
    Y_back=Y_out.copy()
       
  
    for i in range(Y_out.shape[0]-1,0,-1):
       Y_out[i]=(Y_out[i]-Y_out[i-1])*1000   
    Y_out[0]=Y_out[0]*1000
       
    np.set_printoptions(threshold=np.nan)
    #print Y_out  
    
    
    
    Y_pan=pd.DataFrame(data=Y_out,index=price.index.values)
      
    #print Y_out
    return Y_pan