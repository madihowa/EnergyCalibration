# Energy Calibration Project for Atlas

**Madison Howard**


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#high-level-algorithm">High Level Algorithm</a></li>
    <li><a href="#to-do">To Do</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

The signals used to form jets in the ATLAS detector are  clusters  of  topologically  connected  calorimeter  cell signals commonly called topo-clusters. The energy calibration method used in run 1 of the ATLAS detector was called local cell weighting (LCW) calibration. While LCW calibration is generally effective for energy calibration at most energy levels, it is less effective for lower energy levels due to a mixture of noise and lower statistics of data. The purpose of this project was to explore calibrating the energy using machine learning. This was initially implemented in a combination of C and Python but this repsoitory is the refactored, fully Python version.


### Built With

This section lists major frameworks or libraries used for this project.
* [Pandas](https://pandas.pydata.org)
* [NumPy](https://numpy.org)
* [Seaborn](https://seaborn.pydata.org)
* [TensorFlow](https://www.tensorflow.org)
* [Matplotlib](https://matplotlib.org)
* [Scikit-learn](https://scikit-learn.org/stable/)
* [XGBoost](https://xgboost.readthedocs.io/en/latest/)
* [Keras](https://keras.io)
* [Boost-histogram](https://boost-histogram.readthedocs.io/en/latest/)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

First, install pip!

* [pip](https://pip.pypa.io/en/stable/installation/)
  

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/madihowa/EnergyCalibration
   ```
2. Go the base directory 
   ```sh
   cd EnergyCalibration
   ```
3. Install the required python libraries and set up the directory structure for the program
   ```sh
   ./setup.sh
   ```

<!-- USAGE -->
## Usage

There are two ways that I have set this up to work. You can run it locally or a HPC system that uses the Slurm Workload Manager. You also have the option of training and testing the network or testing on an already trained network. First through you need to do the following:

* Add your data files into the data directory 
* Add an inputs csv file to inputs directroy. 
    * This should be formatted as a comma separated values in a continuos line with NO spaces.
* Start in the EnergyCalibration directory to begin a run.

### Usage for training and testing

#### USAGE ON LOCAL MACHINE:


```
python Master.py emission_folder path/to/inputs/list/csv
```

#### USAGE ON HPC SYSTEMS:

To know all the input parameters
```
python qjob.py --help
```

To run a job
```
sbatch quanah_job.sh emission_folder path/to/inputs/list/csv
```

### Usage for testing a trained network

#### USAGE ON LOCAL MACHINE:

Work in progress

#### USAGE ON HPC SYSTEMS:

Work in progress

<!-- HIGH LEVEL ALGORITHM -->
## Highlevel Algorithm:

0. Take in `2` arguments that specify `emission_folder` name and `inputs_list.csv` csv file that specifies the columns needed for training. The emission folder is what will be created after training a network. The input list is what we give the network while training. It will copy this csv file into the emission folder when training is complete.

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

    - Create the predictions figure
    
    - Create the results.csv with the new column being the predicted values' vector
    
    - Use Boosthistogram to create the plots

---

<!-- TO DO -->
## To Do:

-[] Add columns for Delta stuff in NetworkRPedict

-[] Update GraphMean to generate  ROOT plots

-[] Update IQR to generate ROOT plots


<!-- CONTACT -->
## Contact

Please contact me with any questions.

Madison Howard - madison7howard@gmail.com

Project Link: [https://github.com/madihowa/EnergyCalibration](https://github.com/madihowa/EnergyCalibration)





