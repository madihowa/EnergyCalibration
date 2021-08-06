import pandas as pd
import datetime
import sys
import os
import warnings
from tensorflow.python.framework.ops import disable_eager_execution
from shutil import copyfile
from DataHandler import DataHandler
from RNN import FitRNetwork
from Cuts import *

warnings.filterwarnings('ignore')
disable_eager_execution()

if __name__ == "__main__":
    specifyer = sys.argv[1]  #name of folder
    inputs_dir = sys.argv[2]  #pathway to the .csv file with the inputs

    date = datetime.datetime.today().strftime('%Y-%m-%d-%H_%M_%S')

    #appending the folder name with time so that there is no overwrite
    emissions = "./results/{}_{}".format(specifyer, date)
    os.mkdir("{}".format(emissions))

    #copy the list inputs csv to the newly formed directory   
    copyfile("./{}".format(inputs_dir), emissions+"/{}".format(inputs_dir.split("/")[1]))

    #specifying the testing and training data files
    test_csv_dir, train_csv_dir = sys.argv[3], sys.argv[4]
    """
    example:
    test_csv_dir, train_csv_dir = "./data/test.csv", "./data/train.csv"
    """

    #instantiate the Data Handler object
    all_data = DataHandler(test_csv_dir, train_csv_dir, inputs_dir)

    #get all the required DFs from the DataHandler object
    train_df = all_data.train_df
    train_all_df = all_data.train_all
    test_df = all_data.test_df
    target_df = all_data.target_df

    """
    MAKE YOUR CUTS HERE ON THE DATAFRAMES (SAME CUTS ON TRAIN AND TRAIN_ALL)
   # train_df = train_df[train_df['individualEnergy'] > 0.2 * train_df[sumEnergyCluster]]
    """
    #make any cuts

    #sum energy cuts logic: take all like event numbers and sum up their corresponding clusterE. Next, multiply that value by .2 and compare this number to the individual values. if it is greater than that then keep it, otherwise throw it out.

    train_df = makeAbsoluteCuts(train_df,'clusterEta',0.8,"<",normed=True) 

    target_df = makeAbsoluteCuts(train_all_df,'clusterEta',0.8,"<", normed=False) 

    # train the network and create the necessary plots
    FitRNetwork(train_df, train_all_df, target_df, emissions)
