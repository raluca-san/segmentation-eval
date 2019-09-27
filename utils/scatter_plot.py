# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import linear_model

import graphing as gh

sns.set(style="ticks")
plt.style.use('ggplot')


def scatter_plot(df, **kwargs):
    """
    df, x_data, y_data, title, x_label=False, y_label='', lin_reg=''
    :param df:
    :param x_data:
    :param x_data:
    :param title:
    :param x_label:
    :param x_label:
    :param lin_reg:
    :return:
    """
    fig, ax = plt.subplots()
    if kwargs.get('x_data') is None:
        print('No X input data to plot')
        return
    if kwargs.get('y_data') is None:
        print('No Y input data to plot')
        return
    df.plot.scatter(x=kwargs["x_data"], y=kwargs["y_data"], s=80)
    if kwargs.get('x_label') is not None:
        plt.xlabel(kwargs['x_label'], fontsize=20)
    elif kwargs.get('y_label') is not None:
        plt.ylabel(kwargs['y_label'], fontsize=20)
    else:
        plt.xlabel(kwargs['x_data'], fontsize=20)
        plt.ylabel(kwargs['y_data'], fontsize=20)
    if kwargs.get('lin_reg') is not None:
        X = np.array(df[kwargs['x_data']])
        Y = np.array(df[kwargs['y_data']])
        regr = linear_model.LinearRegression()
        X = X.reshape(len(X), 1)
        Y = Y.reshape(len(Y), 1)
        #TODO: plot R-square
        regr.fit(X, Y)
        plt.plot(X, regr.predict(X), color='orange', linewidth=3)
    plt.title(kwargs['title'], fontsize=20)
    plt.tick_params(labelsize=20, color='black')
    ax.tick_params(colors='black', labelsize=20)
    figpathHist = kwargs['title'] + '.png'
    gh.save(figpathHist, width=18, height=16)

