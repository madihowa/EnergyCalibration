
import glob
import numpy as np
import pandas as pd
import tensorflow as tf
import os

from Plotting import *
from DataHandler import DataHandler
from RNN import *


# In[13]:


def load_model(input_dir):
    results_csv_dir = input_dir + "/results.csv"
    history_csv_dir = input_dir + "/callback_history.csv"
    model_checkpoint = find_min_weights(input_dir)
    model = tf.keras.models.load_model(model_checkpoint)
    return model


# ### Making Predictions Using Trained Models

# In[49]:


def make_predictions(NN_model, df_train, df_train_all, target, emissions):
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


# # Main Program

# In[18]:


input_dir = "/lustre/work/madihowa/CERN/EnergyCalibration/results/run1_e100_multiple_inputs_2021-07-21-22_54_33"


# In[25]:


common_csvs = [input_dir+"/callback_history.csv", input_dir+"/results.csv"]


# In[27]:


all_csvs = glob.glob(input_dir+"/*csv")


# In[38]:


for csvs in all_csvs:
    if csvs not in common_csvs:
        list_inputs_dir = csvs


# In[39]:


list_inputs_dir


# In[20]:


model = load_model(input_dir)


# In[51]:


emissions = input_dir+"/jetDataPredictions"


# In[40]:


#specifying the testing and training data files
test_csv_dir, train_csv_dir = "/lustre/work/madihowa/CERN/EnergyCalibration/data/jetData/jets.csv", "/lustre/work/madihowa/CERN/EnergyCalibration/data/jetData/jets.csv"

#instantiate the Data Handler object
all_data = DataHandler(test_csv_dir, train_csv_dir, list_inputs_dir)


# In[41]:


#get all the required DFs from the DataHandler object
train_df = all_data.train_df
train_all_df = all_data.train_all
target_df = all_data.target_df


# ### Since Jet Data File right now doesn't truthPDG. We are avoiding creating Had_Tree and EM_Tree

# In[52]:


def createROOTPlots(df, emissions):
    og_df = df
   # em_df = og_df[og_df["truthPDG"] == 111]
   # had_df = og_df[og_df["truthPDG"] == 211]
    Plot_performance(og_df, "All Data", emissions)
   # Plot_performance(em_df, "EM Tree", emissions)
   # Plot_performance(had_df, "Had Tree", emissions)


# In[53]:


make_predictions(model, train_df, train_all_df, target_df, emissions)