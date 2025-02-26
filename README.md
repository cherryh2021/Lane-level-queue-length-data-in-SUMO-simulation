# Lane-level Queue Length Dataset Generated from SUMO Simulation

This dataset contains queue length, signal cycle, and lane adjacency matrix data. The queue length dataset is stored in 'output_file.csv', the adjacency matrix in 'adjacency_matrix.pkl', and the signal cycle data in 'signal.csv'

## Requirements
pandas   
numpy   
sumolib   
traci

## Getting started
- run `python simulation.py` to generate raw output data from the SUMO simulation.
- run `python queue_length_extraction.py` to process the raw data and generate the final dataset.
