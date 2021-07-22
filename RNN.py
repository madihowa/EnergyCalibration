import seaborn as sb
import pandas as pd
import numpy as np
import warnings
import os
import matplotlib.pyplot as plt
import tensorflow as tf
import math

from keras.callbacks import ModelCheckpoint 
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, LSTM, SimpleRNN, Embedding
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from tensorflow import keras
from keras.utils.vis_utils import plot_model

from Plotting import *

warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    # pydot-ng is a fork of pydot that is better maintained.
    import pydot_ng as pydot
except ImportError:
    # pydotplus is an improved version of pydot
    try:
        import pydotplus as pydot
    except ImportError:
        # Fall back on pydot if necessary.
        try:
            import pydot
        except ImportError:
            pydot = None


def CSV_Callbacks(callbacks, emissions):

    f = open("callback_history.csv", "w")
    print(type(callbacks.history))
    for title in callbacks.history:
        print(title)

    history_df = pd.DataFrame.from_dict(callbacks.history)
    history_df.to_csv("{}/callback_history.csv".format(emissions), index=False)
    return history_df


def write_csv_file(df, dir, file_name='results.csv'):
    df.to_csv(os.path.join(dir, file_name), header=True, index=False)
    print("CSV file written")
    return


def find_min_weights(directory):
    pwd = os.getcwd()
    min_loss = None
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('hdf5'):
                splt = file.split('--')
                if min_loss == None:
                    min_loss = float(splt[1][:-5])
                    min_file = os.path.join(root, file)
                elif min_loss > float(splt[1][:-5]):
                    min_loss = float(splt[1][:-5])
                    min_file = os.path.join(root, file)
    return min_file


def FitRNetwork(df_train, df_train_all, target, emissions):

    NN_model = Make_RNN(df_train.shape[1])

    checkpoint_name = emissions + '/Weights-{epoch:03d}--{val_loss:.5f}.hdf5'
    checkpoint = ModelCheckpoint(checkpoint_name,
                                 monitor='val_loss',
                                 verbose=1,
                                 save_best_only=True,
                                 mode='auto')
    callbacks_list = [checkpoint]

    #Fit network
    history_callback = NN_model.fit(x=df_train,
                                    y=target,
                                    shuffle=True,
                                    epochs=100,
                                    batch_size=128,
                                    workers=10,
                                    validation_split=0.1,
                                    callbacks=callbacks_list)

    history_df = CSV_Callbacks(history_callback, emissions)

    # test the network
    NetworkRPredict(NN_model, df_train, df_train_all, target, history_df, emissions)


def NetworkRPredict(NN_model, df_train, df_train_all, target, history_df, emissions):

    ##Make predictions
    predictions = (NN_model.predict(df_train))
    df_train_all['CalibratedE'] = predictions

    """
    add delta stuff
    """

    #create all plots
    MakeAllPlots(df_train, df_train_all, predictions, target, history_df, emissions)

    # write to disk
    write_csv_file(df_train_all, emissions)


def MakeAllPlots(df_train, df_train_all, predictions, target, history, emissions):
    plt_result(df_train, predictions, target, emissions)
    loss_func_ana(history, emissions)
    createROOTPlots(df_train_all, emissions)


##Here is where you pick the shape and size of the network. This is really where the magic happens. Everything else was just to make runing this work faster.
def Make_RNN(in_shape):
    NN_model = Sequential()
    NN_model.add(
        Dense(1024,
              kernel_initializer='RandomNormal',
              input_dim=in_shape,
              activation="relu"))
    NN_model.add(
        Dense(1024, kernel_initializer='RandomNormal', activation="relu"))
    NN_model.add(Dense(1, kernel_initializer='RandomNormal', activation=None))
    NN_model = compile_NN(NN_model)
    NN_model.summary()

    return NN_model


def learning_schedule(epoch):
    learning_rate = .001 * math.exp(-epoch / 20)

    tf.summary.scalar('learning rate', data=learning_rate, step=epoch)
    return learning_rate


def compile_NN(NN_model):
    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        .001, decay_rate=.36, decay_steps=1e5)
    optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)

    NN_model.compile(
        loss=tf.keras.losses.MeanAbsoluteError(),
        optimizer=optimizer,
        metrics=['mse', 'mae', 'mape', 'msle', 'hinge', 'squared_hinge'])

    return NN_model
