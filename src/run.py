#!/usr/bin/env python

# Purpose: This script demonstrates a simple interface based on user-provided configuration files.
# Input: YAML configuration file with some scDRS parameters. For a documentation of the parameters included see the example config.yml file and details here: https://martinjzhang.github.io/scDRS/reference_cli.html
# Output: A shell script named run.sh with the properly configured commands to run scDRS “munge-gs” and “compute-score” functions on the command line
# Author: Carlos Villacorta
# Date: 01/18/2024

import os
import sys
from pathlib import Path
import yaml


## Parse config

# Default method: take /Path/to/config.yml as a command line argument
if len(sys.argv) < 2:
    sys.exit('''\
A configuration YAML file must be provided as an argument. 
Example:
$ python run.py /Path/to/config.yml
            ''')
else:
    config_file = sys.argv[1]

# Alternative method: config.yml must be in parent dir of this script
# def get_config_path():
#   current_directory = os.path.dirname(os.path.abspath(__file__))
#   config_file = os.path.join(current_directory, '../config.yml') # assumes config file is located in parent directory of current script
#   return config_file
# 
# config_file = get_config_path() # it still avoids hard-coding paths and gets the correct path even if calling the script from a different directory

with open(config_file, "r") as stream:
    try:
        config = yaml.safe_load(stream) # prevents code injection
    except yaml.YAMLError as exc:
        print(exc)

zscores_file = config['munge-gs']['zscores_file']  # either zscores OR pval (one of these must be 'None')
pval_file = config['munge-gs']['pval_file']
out_file = config['munge-gs']['out_file']
n_max = config['munge-gs']['n_max']
n_min = config['munge-gs']['n_min']

hd5anndata_file = config['compute-score']['hd5anndata']
h5ad_species = config['compute-score']['h5ad_species']
gs_species = config['compute-score']['gs_species']


output_dir = os.path.join(os.path.dirname(os.path.abspath(out_file)), '') # output dir with trailing slash

if not os.path.isfile(hd5anndata_file):
    sys.exit("{} doesn't exist".format(hd5anndata_file))

Path(output_dir).mkdir(parents=True, exist_ok=True) # create output dir if missing (Python > 3.5)

## Generate call for munge-gs

command_call_munge_gs = '''\
scdrs munge-gs \\
    --out-file {} \\
    --zscore-file {} \\
    --pval_file {} \\
    --weight zscore \\
    --n-max {} \\
    --n-min {}
'''.format(out_file, zscores_file, pval_file, n_max, n_min)

with open("run.sh", "w") as file1:
    file1.write(command_call_munge_gs)

## Generate call for compute-score

command_call_compute_score = '''\
scdrs compute-score \\
    --h5ad-file {} \\
    --h5ad-species {} \\
    --gs-file {} \\
    --gs-species {} \\
    --cov-file None \\
    --flag-filter-data True \\
    --flag-raw-count True \\
    --flag-return-ctrl-raw-score False \\
    --flag-return-ctrl-norm-score True \\
    --out-folder {}
'''.format(hd5anndata_file, h5ad_species, out_file, gs_species, output_dir)

with open("run.sh", "a") as file1:
    file1.write(command_call_compute_score)
    
# I have mostly omitted exception handling here for simplicity