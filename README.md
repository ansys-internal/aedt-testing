## Description
This project aims to provide an Automated Framework to test Ansys Electronics Desktop (AEDT). 
Users can set up a suite of tests to validate stability/regression of results between 
different versions of Ansys Electronics Desktop.


## Table of Contents

<!-- toc -->

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  * [Configuration file](#configuration-file)
  * [Local machine](#local-machine)
    + [Generate only reference results](#generate-only-reference-results)
    + [Run comparison between versions](#run-comparison-between-versions)
  * [Slurm](#slurm)
    + [Generate only reference results](#generate-only-reference-results-1)
    + [Run comparison between versions](#run-comparison-between-versions-1)
- [Limitations](#limitations)
- [Contributors](#contributors)

<!-- tocstop -->

## Features
The current framework provides the following features:
* Compare results of XY plots, mesh statistics and simulation time.
* Web page output format for visual comparison
* JSON file output format to support automated workflows and use of test results downstream.
* Parallel distribution of test projects
* Cross-platform: support for Windows and Linux
* Compatibility with local machine and most known cluster schedulers: 
  LSF, SGE, Slurm, PBS, Windows HPC
* Control of required resources for each project and optimized distribution of tasks
* Automatic generation of reference results (AEDT versions 2019R1+)

## Installation
To install the package use:
```bash
pip install .
```

## Usage
Electronics Desktop testing framework automatically identifies environment where it was launched. In this chapter we 
will show basic examples of starting tests on local machine or on clusters with scheduler. In all scenarios we use 
Command Line Interface (CLI).

### Configuration file
Framework requires configuration file as input. Please read [configuration.md](docs/configuration.md) to understand how 
to create a file.

### CLI Commands
To expose the available commands use the following command line

#### Open CLI commands Help
```bash
aedt_test_runner -h
```

### Examples

#### Local machine
To start test on local machine use following command line

#### Generate only reference results
```bash
aedt_test_runner --config-file=config.json --aedt-version=193 --only-reference
```

#### Run comparison between versions
```bash
aedt_test_runner --config-file=config.json --aedt-version=222 --reference-file=input/reference_results.json
```

#### Slurm
#### Generate only reference results
```bash
sbatch \
  --job-name aedttest \
  --partition ottc01 \
  --export "ALL,ANSYSEM_ROOT193=/apps/software/ANSYS_EM_2019R1/AnsysEM19.3/Linux64,ANS_NODEPCHECK=1" \
  --nodes 2-2 --ntasks 56 \
  --wrap "aedt_test_runner --config-file=config.json --aedt-version=193 --only-reference"
```

#### Run comparison between versions
```bash
sbatch \
  --job-name aedttest \
  --partition ottc01 \
  --export "ALL,ANSYSEM_ROOT222=/ott/apps/software/ANSYS_EM_2022R2_211129/v222/Linux64,ANS_NODEPCHECK=1" \
  --nodes 2-2 --ntasks 56 \
  --wrap "aedt_test_runner --config-file=config.json --aedt-version=222 --reference-file=~/reference_results.json"
```

## Limitations
Currently, project does not support or partially supports following features:
* Automatic results creation is possible only for versions 2019R1+
* LS-DSO is not supported
* Linux clusters require SSH to be pre-configured for the user

## Contributors
If you would like to contribute to this project, please see [CONTRIBUTE](docs/CONTRIBUTE.md).
