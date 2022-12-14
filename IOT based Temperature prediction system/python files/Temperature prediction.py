# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XsscSNVSyEokNJkpbLHyxhuLC16JfNDO
"""

pip install pmdarima

import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARMA
import statsmodels.api as sm 
import pandas as pd
import numpy as np

data=pd.read_csv('GlobalLandTemperaturesByCity.csv') #read dataset
data=data.dropna()  #to drop null values
print('Shape of data',data.shape) #give a topic to display dataset
#data.head() #to select top upper data rows
data

df = pd.DataFrame(data)
df

df.isnull().sum()

df

df = df.drop(['City','Country'],1)
df

df.index = pd.to_datetime(df.dt)
df

df = df.drop('dt',1)
# Replacing NaN values with the previous effective data
df.AverageTemperature.fillna(method='pad', inplace=True)
df

df2 = df['AverageTemperature']['1980-01-01': '2013-08-01']
df2

#max Temperature
df['Max_Temperature'] = df['AverageTemperature'] + df['AverageTemperatureUncertainty']

#min temperature
df['Min_Temperature'] = df['AverageTemperature'] - df['AverageTemperatureUncertainty']

#plot diagram 
plt.figure(figsize=(16,7))
fig = plt.figure(1)
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Date')
ax1.set_ylabel('Temperature')
ax1.plot(df2)

#make data stationary
plt.figure(figsize=(16,7))
fig = plt.figure(1)
ts_log = np.log(df2)
plt.plot(ts_log)

#differencing data
plt.figure(figsize=(16,7))
fig = plt.figure(1)
ts_log_diff = ts_log - ts_log.shift()
plt.plot(ts_log_diff)

rol_mean = ts_log_diff.rolling(12).mean()
rol_std = ts_log_diff.rolling(12).std()

#rolling statistics
original = plt.plot(ts_log_diff, color= 'green', label= 'original')
mean = plt.plot(rol_mean, color= 'blue', label= 'mean')
std = plt.plot(rol_std, color= 'red', label= 'std')

plt.legend(loc='best')
plt.title('Rolling statistics among original, mean and std')
plt.show(block = False)

#to check whether data is stationary or not, we run a fixed statistical test
from statsmodels.tsa.stattools import adfuller
def ad_test(dataset):
     dftest = adfuller(dataset, autolag = 'AIC')
     print("1. ADF : ",dftest[0])
     print("2. P-Value : ", dftest[1])
     print("3. Num Of Lags : ", dftest[2])
     print("4. Num Of Observations Used For ADF Regression:",      dftest[3])
     print("5. Critical Values :")
     for key, val in dftest[4].items():
         print("\t",key, ": ", val)

ad_test(df2)

df2.sort_index(inplace=True)

from statsmodels.tsa.stattools import acf, pacf
lag_acf = acf(ts_log_diff, nlags = 20)
lag_pacf = pacf(ts_log_diff, nlags = 20)

import statsmodels.api as sm
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(ts_log_diff.dropna(), lags=40, ax =ax1 )
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(ts_log_diff.dropna(), lags=40, ax =ax2 )

#p< 0.05 ; Data is stationary

#Now figure out order for ARIMA model
from pmdarima import auto_arima

#ignore harmless warnings
import warnings
warnings.filterwarnings('ignore')

stepwise_fit = auto_arima(df2, trace=True,
suppress_warnings=True)

#to get summery for best model fit
stepwise_fit.summary()

#to begin the actual fitting the model
from statsmodels.tsa.arima_model import ARIMA

df2

#split data into training and testing tests.
print(df2.shape)
training_set = df2.iloc[:-30]
testing_set = df2.iloc[-30:]
print(training_set.shape,testing_set.shape)

training_set

testing_set

#train the model
model= sm.tsa.arima.ARIMA(training_set,order=(3,0,2))
model=model.fit()
model.summary()

start=len(training_set)
end=len(training_set)+len(testing_set)-1
pred = model.predict(start = start, end= 0,typ='levels')
print(pred)
print(testing_set)

#to get the index column as in date values
pred.index= df.index[start:end+1]
print(pred)

#plot predictions
pred.plot(legend=True)
training_set.plot(legend=True, xlabel = 'date' , ylabel = 'temperature')

predicts = model.predict('2013-08-01', '2014-08-01')
predicts
