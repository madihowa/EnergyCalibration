import pandas as pd
import numpy as np


class Cuts:
    def __init__(self, cuts_df, df):
        self.cuts_df = cuts_df
        self.df = df

    def getCuts(self, df):
        for col in self.cuts_df.columns:
            data = self.cuts_df[col].values
            fname = data[0]
            term = data[1]
            operation = data[2]
            value = data[3]
            df = getattr(self, fname)(
                df, term, value, operation,
                col)  #selects the corresponding func from the json
            # and executes
            print("Size of dataframe: {}\n".format(len(df)))
        return df

    def summedEnergyCut(self, df, term, value, operation, col):
        print("Applying Cut: {}".format(col, term, operation, value))
        return df

    def trimDF(self, df, term, value, operation, col):
        print("Applying Cut: {}".format(col, term, operation, value))

        if operation == "<":
            df = df[df[term] < value]
        elif operation == ">":
            df = df[df[term] > value]
        elif operation == "==":
            df = df[df[term] == value]

        return df

    def trimAbsDF(self, df, term, value, operation, col):
        print("Applying Cut: {}".format(col, term, operation, value))

        if operation == "<":
            df = df[abs(df[term]) < value]
        elif operation == ">":
            df = df[abs(df[term]) > value]
        elif operation == "==":
            df = df[abs(df[term]) == value]

        return df
