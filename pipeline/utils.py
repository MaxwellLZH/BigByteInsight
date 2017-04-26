from __future__ import division
import numpy as np
import pandas as pd


def create_lag(data, lag, timestep=True):
    #create lagged time series for training RNN
    #params: data:a single variate time series
    #        lag:period of lagging
    #        timestep: if equals True, return array with shape (length, 1, lag)
    #return: lagged training data and corresponding label
    if lag >= len(data):
        raise ValueError('Lag should be smaller than then length of time series')
    x, y = [], []
    for i in range(len(data)-lag-1):
        x.append(data[i:(i+lag), 0])
        y.append(data[i+lag, 0])
    x, y = np.array(x), np.array(y)
    if timestep:
        x = x.reshape(x.shape[0], x.shape[1], 1)
    return x, y


def to_binary(data):
    #transforming a time series into 1 and 0
    #1 => price higher than or equal to previous day
    #0 => price lower than previous day
    if len(data.shape)>1:
        diff = np.diff(data.flatten())
    else:
        diff = np.diff(data)
    diff = [0 if x<0 else 1 for x in diff]
    return np.array(diff, dtype=np.int)


def to_percent(data):
    #transform a time series stock price into percentage changes
    #params: data: a single variate time series
    #return: time series of percentage price changes
    if len(data.shape)>1:
        data = data.flatten
    diff = np.diff(data)
    base = data[:-1]
    return np.log1p(diff/base)



