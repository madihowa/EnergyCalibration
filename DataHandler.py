import pandas as pd
import csv
import numpy as np


def normalizeDF(df):
    df_norm = df.subtract(df.mean())
    df_norm = df_norm.divide(df.std())
    return df_norm


class DataHandler:
    def __init__(self, path2test, path2train, path2list_inputs):
        self.path2test = path2test
        self.path2train = path2train
        self.list_inputs = self.getListInputs(path2list_inputs)

        self.train_all = self.getAllTrainDF()
        self.test_all = self.getAllTestDF()
        self.allColumns = self.train_all.columns
        self.train_df = self.getTrainingData()
        self.test_df = self.getTestingData()
        self.target_df = self.train_all["cluster_ENG_CALIB_TOT"]

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
        test_df = self.test_all[self.list_inputs]
        normed_df = normalizeDF(test_df)
        return normed_df

    def getTrainingData(self):#gets list inputs training data from normalized data frame
        train_df = self.train_all[self.list_inputs]
        normed_df = normalizeDF(train_df)
        return normed_df
