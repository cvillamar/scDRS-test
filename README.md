# scDRS-test
Take an input config file and output a command to run scDRS’ “munge-gs” and “compute-score” functions

## Purpose

## Input
YAML configuration file with some scDRS parameters. 
For documentation of the parameters included see the example config.yml file.
Details available in the original scDRS docs: 
https://martinjzhang.github.io/scDRS/reference_cli.html

## Output
A shell script named "run.sh" with the properly configured scDRS commands to run “munge-gs” and “compute-score” functions on the command line.

## Usage

Download

```
git clone https://github.com/cvillamar/scDRS-test.git
cd scDRS-test/data
tar -xvzf demo.tar.gz
cd ..
```

Edit the config.yml file provided with the appropriate path to the input data (you can use the test data provided in the data subfolder)

Run

```
python src/run.py /Path/to/config.yml
```

## Scope

For simplicity, I have ommited exception handling and unit testing.

In production, we may want to output instead a Nextflow script to manage scalability and dependencies.
