# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 20:43:50 2018

@author: SERGIO
"""
# data source: http://www.macrotrends.net/2532/corn-prices-historical-chart-data

from pandas import read_csv
from numpy import array, reshape
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import load_model
from math import sqrt

toPredNum = 29
toTrainNum = 2520
timeSteps = 128
train = False
test = False

dataSet = read_csv('corn-prices-historical-chart-data.csv')
trainingSet = dataSet.iloc[len(dataSet)-toTrainNum-toPredNum:len(dataSet)-toPredNum,1:2].values

toTrainTh = len(dataSet) - (toTrainNum + toPredNum + 1)
toPredTh = len(dataSet) - (toPredNum + 1)

scaler = MinMaxScaler(feature_range = (0, 1))
trainingSetScale = scaler.fit_transform(trainingSet)

xTrain, yTrain = [], []
for i in range(timeSteps+toTrainTh,len(dataSet)-toPredNum):
    xTrain.append(trainingSetScale[i-(timeSteps+toTrainTh):i-toTrainTh, 0])
    yTrain.append(trainingSetScale[i-(toTrainTh+1), 0])
xTrain, yTrain = array(xTrain), array(yTrain)
xTrain = reshape(xTrain, (xTrain.shape[0], xTrain.shape[1], 1))

if train:
    lstm = Sequential()
    lstm.add(LSTM(units = 64, return_sequences = True, input_shape = (xTrain.shape[1], 1)))
    lstm.add(Dropout(0.2))
    lstm.add(LSTM(units = 64, return_sequences = True))
    lstm.add(Dropout(0.2))
    lstm.add(LSTM(units = 64, return_sequences = True))
    lstm.add(Dropout(0.2))
    lstm.add(LSTM(units = 64))
    lstm.add(Dropout(0.2))
    lstm.add(Dense(units = 1))    
    lstm.compile(optimizer = 'rmsprop', loss = 'mean_squared_error')
    lstm.fit(xTrain, yTrain, epochs = 128, batch_size = 32)    
    lstm.save('lstm_corn-128ep-64n.h5')
else:
    lstm = load_model('lstm_corn-128ep-64n.h5')

<<<<<<< HEAD
yRealSet = dataSet.iloc[len(dataSet)-(toPredNum):len(dataSet)+1, 1:2].values
=======
lstm.compile(optimizer = 'rmsprop', loss = 'mean_squared_error')
lstm.fit(xTrain, yTrain, epochs = 128, batch_size = 32)
>>>>>>> 711933c293a5f6804101069f14eec69001c4d1b8

predSet = dataSet.iloc[len(dataSet)-(toPredNum+timeSteps+1):len(dataSet), 1:2].values
predSet = predSet.reshape(-1,1)
predSet = scaler.transform(predSet)

if test:
    xPred = []
    for i in range(timeSteps + 1 , timeSteps + toPredNum + 1):
        xPred.append(predSet[i-timeSteps :i, 0])
    xPred = array(xPred)
    xPred = reshape(xPred, (xPred.shape[0], xPred.shape[1], 1))
    yPred = scaler.inverse_transform(lstm.predict(xPred))
else:
    yPred = []
    for n in range(timeSteps, timeSteps + toPredNum):
        xPred = []
        xPred.append(predSet[n-timeSteps+1: n+1, 0])
        xPred = array(xPred)
        xPred = reshape(xPred, (xPred.shape[0], xPred.shape[1], 1))
        y = lstm.predict(xPred)
        predSet[n+1] = y
        yPred.append(scaler.inverse_transform(y)[0,0])    
    yPred = array(yPred)

score = sqrt(mean_squared_error(yRealSet, yPred))
>>>>>>> 582824133e6f9c015ce682e2e0b75425bf747190
