import pandas as pd
import csv
import numpy as np
from Cuts import *

def normalizeDF(df):
    df_norm = df.subtract(df.mean())
    df_norm = df_norm.divide(df.std())
    return df_norm


class DataHandler:
    def __init__(self, path2test, path2train, path2list_inputs, cuts_dir):
        self.path2test = path2test
        self.path2train = path2train
        self.path2cuts = cuts_dir
        self.list_inputs = self.getListInputs(path2list_inputs)
        
        self.train_raw = self.getAllTrainDF()
        self.test_raw = self.getAllTestDF()
        self.allColumns = self.train_raw.columns
        
        self.train_all_normed = normalizeDF(self.train_raw)
        self.test_all_normed = normalizeDF(self.test_raw)
        
        self.train_df = self.getTrainingData()
        self.test_df = self.getTestingData()
        self.target_df = self.train_raw["cluster_ENG_CALIB_TOT"]
        
        self.processCuts(self.train_all_normed)
    
    def processCuts(self, df):
        cuts_df = pd.read_json(self.path2cuts)
        if len(cuts_df) == 0:
            print("No cuts applied...")
            return
        else:
            c = Cuts(cuts_df, df)
            df = c.getCuts(df)
            self.train_df = self.getTrainingDataFromCutDF(df)
            self.test_df = self.getTestingDataFromCutDF(df)
            self.target_df = self.getTargetDatafromCutDF(df, self.train_raw)
            
    def getTargetDatafromCutDF(self, df, test_df):
        indices = list(df.index.values)
        df = test_df.iloc[indices]
        return df["cluster_ENG_CALIB_TOT"]
    
    def getTestingDataFromCutDF(self, df):
        test_df = df[self.list_inputs]
        normed_df = normalizeDF(test_df)
        return normed_df

    def getTrainingDataFromCutDF(self, df):
        train_df = df[self.list_inputs]
        normed_df = normalizeDF(train_df)
        return normed_df
        
    def getListInputs(self, path2inputs): #gets list inputs data
        with open(path2inputs, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        data = list(np.array(data).flatten())
        return data
    
    def getAllTestDF(self): #gets testing data frame
        test_all = pd.read_csv(self.path2test)
        return test_all

    def getAllTrainDF(self):#gets training data frame
        train_all = pd.read_csv(self.path2train)
        return train_all

    def getAllDataColumns(self): #gets the names of the data columns in the data frame
        columns = pd.read_csv(self.path2test, nrows=1)
        return columns

    def getTestingData(self):#gets list inputs testing data from normalized data frame
        test_df = self.test_raw[self.list_inputs]
        normed_df = normalizeDF(test_df)
        return normed_df

    def getTrainingData(self):#gets list inputs training data from normalized data frame
        train_df = self.train_raw[self.list_inputs]
        normed_df = normalizeDF(train_df)
        return normed_df
