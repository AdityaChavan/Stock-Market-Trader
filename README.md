# Stock-Market-Trader
A program to predict the stock market. ML Algorithms: Random Forest, Decision Trees ans also a CNN (TensorFlow) were implemented and their performance compared.

Shown below are the outputs of the program:
![alt text](https://github.com/AdityaChavan/Stock-Market-Trader/blob/master/Experiment-1.png)

We trade based on the stock Apple (NYSE:AAPL).

We limit our problem to 3 states: having 1000 shares, shorting 1000 shares or just holding (0 shares).

The red line, the stock price, represents the amount we would have if we bought 1000 shares of AAPL and held it till the end.

The other lines represent trading strategies given by the ML Algorithms.

The Cumulative returns (End Price/ Start price) provided over the time period are: 
CNN: 6.6926
Forest of Decision Trees: 4.1891
Random Forest: 3.5388
Benchmark AAPL: 2.0926

How to frame the trading problem as a Machine Learning problem:
We dont give the stock prices directly to the Algorithm. We calculate 3 stock indicators (described below) based on the stock price and use that as the training data (X). The Y array for the training set is a look forward to whether the stock went up or not. In other words, the Y is a 3 column matrix with for each of the 3 outcomes: shorting, selling or holding the stock for that day. 
We can postulate that similar indicators at any time will lead to similar results in the future. Based on our results we can conclude that the assumption holds.
A big factor is selecting the indicators. They must be normalized and must accurately reflect the current state of the stock, its past and expected future values. Here are the 3 indicators that I used:

Indicators:
Simple Moving Average: (SMA):
This is a N day average of the stock. It reflects the average of the previous N days that the stock traded for. 
Bolinger Bands Percentage (BBP):
This indicates the standard deviation of the stock from its average value. More info here: <a href="https://www.tradingview.com/wiki/Bollinger_Bands_%25B_(%25B)" target="_blank">BB%</a>.
Momentum (RSI):
We notice that when a stock price is going up (or down), it will maintain the trend for a certain number of days before reversing directions. We can use the slope of the stock price as an indicator to trade. <a href="https://www.tradingview.com/wiki/Relative_Strength_Index_(RSI)" target="_blank">RSI</a>.

Algorithms:
Random Forest:
20 trees, Max Leaf Size: 5

Decision trees: 
Max Leaf size: 5

CNN: Implemented in Tensorflow (tflearn)
2D Convolution >> Max Pool >> Fully Connected >> Dropout >> Fully Connected >> SoftMax
Activation: Relu 
Optimizer: Adam
Learning Rate: 1e-2

Other stats from results:

CR:(Cumulative Return) ADR:(average Daily Return) SDDR:(Standard Deviation of Daily Return) SR: (Sharpe Ratio)

Random Forest
CR:  3.5388   ADR:  0.0016   SDDR:  0.0125   SR:  2.0058

Decision Trees
CR:  4.1891   ADR:  0.0017   SDDR:  0.012   SR:  2.254

CNN
CR:  6.6926   ADR:  0.0021   SDDR:  0.0154   SR:  2.2105

Benchmark (AAPL):
CR:  2.0926   ADR:  0.0464   SDDR:  3.0535   SR:  0.2411



