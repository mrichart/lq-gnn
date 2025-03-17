# LQ-GNN: A Graph Neural Network Model for Response Time Prediction of Microservice-based Applications in the Computing Continuum

## Overview
This code implements the LQ-GNN model and related tools, leveraging Graph Neural Networks (GNN) to predict response times of microservice-based applications.

## Features
- GNN implementation using the IGNNITION framework
- Simulation data processing
- Training and evaluation scripts

## Directories

#### Model Versions
Six model versions tailored to specific prediction objectives:
- **delay-ms-avg**: Predicts average response time of each microservice.
- **delay-ms-p95**: Predicts 95th percentile response time of each microservice.
- **delay-path-avg**: Predicts average response time of each path.
- **delay-path-p95**: Predicts 95th percentile response time of each path.
- **delay-total-avg**: Predicts average response time of the entire application.
- **delay-total-p95**: Predicts 95th percentile response time of the entire application.

#### Training Sets
Four training sets with scripts for pre-processing uqsim simulator data to create input graphs for the GNN:
- **4tier**: Single application with 4 microservice tiers.
- **social-network**: Mimics a social-network application's home timeline read requests.
- **social-network-ut**: Mimics a social-network application's user timeline read requests.
- **mix**: Combination of the above three applications.

## Installation
Install dependencies with:
```bash
pip install -r requirements.txt
```

## Usage

For training the model we use data generated with an extension of the uqSim Simulator available in: https://github.com/mrichart/uqsim-simulator

### Data generation using uqSim (for each application to simulate)

1. Define the application to simulate and implement in uqSim:
   1. Implement each microservice, the graph, the paths, and the deployment. Create a script for each of these tasks.
   2. Implement the `start_architecture.py` script that creates the architecture.
2. Define the scenarios to test (threads, cores, traffic, deployment, etc.):
   1. Create the script that generates each case: `generateCSVSocial.py`
   2. Execute the script: `python generateCSVSocial.py --deployment cloud --numConns 320 --endTime 30 --monInterval 0 --delayEdgeCloud 0 --delayEdgeFog 0 --delayFogCloud 0 --kqps 2,4,6,8,10,12 --threads 4,8-4,8-4,8-4,8-4,8-4,8-4,8 --cores 4,8-4,8-4,8-4,8-4,8-4,8-4,8 --output cloudSocial.csv`
3. Run the simulations (example using cluster.uy machines):
   1. Use the `runSocial.slurm` script which creates the architecture and runs the simulator for each CSV file.
   2. `sbatch --array=1-49 runSocial.slurm csv/cloudSocial.csv`
   3. The data is copied to `uqsim-results/<dir>`. Do not forget to create this directory, otherwise the data will not be copied.
4. After obtaining the logs from all simulations, process them to generate the graph dataset as indicated below.

### Data Pre-processing (for each application to simulate)

Process simulation logs to generate the graph dataset using `generate_dataset.py`. This script parses logs, creates corresponding graphs, and splits the dataset into training and test sets. Configuration is sourced from the uqsim input graph and filenames (load, cores, threads). Simulation results (response times) are parsed from each file.

### Configuration (for each model and each application)

Adjust training and evaluation parameters in `train_options.yaml`.
Several example are provided within the directories of each model for different applications.

### Normalization (for each model and each application)

Obtain mean and variance of training data for normalization using `calculate_mean_variance.py`. 
Output should be added to `additional_functions.py`.

### Training (for each model and each application)

Train an MS-GNN model by navigating to the corresponding directory and running:
```bash
python main.py
```
### Example script for training

An example script for running a model with the 4tier application can be found in `runTrain_4tier.slurm`.
