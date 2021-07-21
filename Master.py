import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
import os
import warnings
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.layers import Dense, Activation, Flatten, LSTM, SimpleRNN, Embedding
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from tensorflow.python.framework.ops import disable_eager_execution
from sklearn.model_selection import train_test_split
from DataHandler import DataHandler
from RNN import FitRNetwork

warnings.filterwarnings('ignore')
disable_eager_execution()

if __name__ == "__main__":
    specifyer = sys.argv[1]  #name of folder
    inputs_dir = sys.argv[2]  #pathway to the .csv file with the inputs

    date = datetime.datetime.today().strftime('%Y-%m-%d-%H_%M_%S')

    #appending the folder name with time so that there is no overwrite
    emissions = "{}_{}".format(specifyer, date)
    os.system("mkdir {}".format(emissions))

    #specifying the testing and training data files
    test_csv_dir, train_csv_dir = "data/test.csv", "data/train.csv"

    #instantiate the Data Handler object
    all_data = DataHandler(test_csv_dir, train_csv_dir, inputs_dir)

    #get all the required DFs from the DataHandler object
    train_df = all_data.train_df
    train_all_df = all_data.train_df
    test_df = all_data.test_df
    target_df = all_data.target_df

    # train the network and create the necessary plots
    FitRNetwork(train_df, train_all_df, target_df, emissions)
