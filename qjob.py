import os
import sys
import csv
import glob
import argparse

"""
DEMO USAGE:
python qjob.py -f=test_e100 -s=test_qj
"""

def createContent(jname,nodes,cpu,cuts):
    header = "#!/bin/bash\n#SBATCH --job-name={}\n#SBATCH --output=quanah_outputs/%x.o%j\n#SBATCH --error=quanah_errors/%x.e%j\n#SBATCH --partition quanah\n#SBATCH --nodes={}\n#SBATCH --ntasks-per-node={}\n#SBATCH --mail-user=<madison.howard@ttu.edu>\n#SBATCH --mail-type=ALL\n\n".format(jname,nodes,cpu)
    command = "/run.sh {} {}\n".format(jname,cuts)
    return header, command

def createShellScript(header,command,sh_name):
    with open (sh_name, 'w') as rsh:
        rsh.write(header)
        rsh.write(command)
    print("Shell Script {} has been created".format(sh_name))
    os.system("sbatch {}".format(sh_name))
    print("sbatch {}".format(sh_name))
    print("Shell Script Job has been submitted")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--fname', '-f', help="folder name of output file", type= str)
    parser.add_argument('--nodes', '-n', help="number of nodes", type= int, default= 5)
    parser.add_argument('--cpus', '-c', help="number of cpus", type= int, default= 10)
    parser.add_argument('--sname', '-s', help="shell script name", type=str)

    args = vars(parser.parse_args())
    
    jname = args["fname"] 
    nodes = args["nodes"] 
    cpu =   args["cpus"] 
    sh_name = args["sname"]  

    cuts = glob.glob("inputs/*csv")

    for i,cut in enumerate(cuts):
        inputs = cut.split("/")[-1].split(".")[0]
        h, c = createContent(jname+"_run_"+str(i)+"_"+inputs,nodes,cpu,cut)
        createShellScript(h,c,sh_name+"_"+inputs+".sh")
    os.system("squeue -u madihowa")
