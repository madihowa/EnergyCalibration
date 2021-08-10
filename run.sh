#!/usr/bin/env bash

# setting XDG dir and permissions -> MIH
export XDG_RUNTIME_DIR=/lustre/scratch/madihowa/xdg
chown -R madihowa $XDG_RUNTIME_DIR
chmod -R 0700 $XDG_RUNTIME_DIR
chmod 000700 $XDG_RUNTIME_DIR 

# setting QT var -> MIH
export QT_QPA_PLATFORM='offscreen'


# load foldername, path2Inputcsvfile,  path2testcsvfile, and path2traincsvfile as variables
FNAME=$1
PCSV=$2
TESTCSV=$3
TRAINCSV=$4
CUTSJSON=$5

python Master.py $FNAME $PCSV $TESTCSV $TRAINCSV $CUTSJSON
