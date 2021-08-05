
import glob
import numpy as np
import pandas as pd
import tensorflow as tf
import os
import sys

from Plotting import *
from DataHandler import DataHandler
from RNN import *


def load_model(input_dir):
"""
Inputs: input directory
Outputs: trained model
Process: takes in directory of trained model, uses weights output to choose most recent model that was trained
"""
    results_csv_dir = input_dir + "/results.csv"
    history_csv_dir = input_dir + "/callback_history.csv"
    model_checkpoint = find_min_weights(input_dir)
    model = tf.keras.models.load_model(model_checkpoint)
    return model

#  Making Predictions Using Trained Models

def make_predictions(NN_model, df_train, df_train_all, target, emissions):
"""
inputs: Neural Network model, train dataframe, df_train_all, target of the network, emissions directory
outputs:figures.png, new Delta values to dataframe, 
"""    
    try:
        #creates the new directory for storing the results of testing
        os.mkdir("{}".format(emissions))
    except:
        pass
    #makes prediction using the trained model and the training/testing data set
    predictions = (NN_model.predict(df_train))
    
    #adds a column to the overall dataframe with the prediction values
    df_train_all['CalibratedE'] = predictions
    
    #calculating the Delta_E and Delta_Calib_E quantities
    l_true = df_train_all["cluster_ENG_CALIB_TOT"].values
    l_calib = df_train_all["CalibratedE"].values
    l_cluster_calib = df_train_all["clusterECalib"]
    Delta_E= l_true - l_calib
    Delta_Calib_E = l_true - l_cluster_calib
    
    #adds two columns to the overall dataframe with the Delta_E and Delta_Calib_E values
    df_train_all['Delta_Calib_E '] = Delta_Calib_E
    df_train_all['Delta_E'] = Delta_E
    
    #creating the Figures.png
    plt_result(df_train, predictions, target, emissions)
    
    #creates the ROOT plots
    createROOTPlots(df_train_all, emissions)
    
    #writing the updated dataframe to memory
    write_csv_file(df_train_all, emissions)


#Main Program

#input_dir = "/lustre/work/madihowa/CERN/EnergyCalibration/results/run1_e100_multiple_inputs_2021-07-21-22_54_33" #where the saved model (hdf5) are
input_dir = sys.argv[1] #must pass in path to foleder with  hdf5's for trained model
common_csvs = [input_dir+"/callback_history.csv", input_dir+"/results.csv"]
all_csvs = glob.glob(input_dir+"/*csv")

for csvs in all_csvs:
    if csvs not in common_csvs:
        list_inputs_dir = csvs

model = load_model(input_dir)
emissions = input_dir+"/jetDataPredictions"

#specifying the testing and training data files
#test_csv_dir, train_csv_dir = "/lustre/work/madihowa/CERN/EnergyCalibration/data/jetData/jets.csv", "/lustre/work/madihowa/CERN/EnergyCalibration/data/jetData/jets.csv"
test_csv_dir, train_csv_dir = sys.argv[2], sys.argv[3] #must pass in path to test and train csv files

#instantiate the Data Handler object
all_data = DataHandler(test_csv_dir, train_csv_dir, list_inputs_dir)

#get all the required DFs from the DataHandler object
train_df = all_data.train_df
train_all_df = all_data.train_all
target_df = all_data.target_df

# Since Jet Data File right now doesn't truthPDG. We are avoiding creating Had_Tree and EM_Tree

def createROOTPlots(df, emissions):
"""
inputs:dataframe, emissions folder name
outputs:Plot_performance graph
"""
    og_df = df
   # em_df = og_df[og_df["truthPDG"] == 111]
   # had_df = og_df[og_df["truthPDG"] == 211]
    Plot_performance(og_df, "All Data", emissions)
   # Plot_performance(em_df, "EM Tree", emissions)
   # Plot_performance(had_df, "Had Tree", emissions)
   
make_predictions(model, train_df, train_all_df, target_df, emissions)
