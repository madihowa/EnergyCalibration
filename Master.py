import pandas as pd
import datetime
import sys
import os
import warnings
from tensorflow.python.framework.ops import disable_eager_execution
from shutil import copyfile
from DataHandler import DataHandler
from RNN import FitRNetwork

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

    #specifying the path to the cuts json file
    cuts_json_dir = sys.argv[5]

    #instantiate the Data Handler object
    all_data = DataHandler(test_csv_dir, train_csv_dir, inputs_dir, cuts_json_dir)

    #get all the required DFs from the DataHandler object
    train_df = all_data.train_df
    train_raw_df = all_data.train_raw
    test_df = all_data.test_df
    target_df = all_data.target_df

    FitRNetwork(train_df, train_raw_df, target_df, emissions)
    
