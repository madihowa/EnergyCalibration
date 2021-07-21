# Energy Calibration Project for Atlas

**Madison Howard**

## Highlevel Algorithm:

0. Take in `2` arguments that specify `emission_folder` name and `inputs_list.csv` csv file that specifies the columns needed for training.

1. Read the test and train data.

    - Record and save all the columns.


2. Format the datasets:

    - Trim the datasets with required columns.
    
    - Make any cuts if needed
    
    - Drop the target column from training data.
    
    - Normalize the data sets.



3. Train the model with required callbacks and learning schemes.

    - generate validation data from training data.
    
    - store the model using checkpoints.
    
    - store the learning history.



4. Predict using the trained model.

    - Create the predictions figure.
    
    - Create the results.csv with the new column being the predicted values' vector
    
    - Use Boosthistogram to create the plots.

---

## To Do:

-[] Add all methods to generate all ROOT plots

