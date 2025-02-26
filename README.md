# Lane-level Queue Length Dataset Generated from SUMO Simulation

This dataset contains queue length, signal cycle, and lane adjacency matrix data. The queue length dataset is stored in 'output_file.csv', the adjacency matrix in 'adjacency_matrix.pkl', and the signal cycle data in 'signal.csv'. The simulation is modeled after the real-world road network of Wangjing, Beijing, featuring a total of 47 junctions and 361 lanes. Below is a visualization of the road network as displayed in SUMO NetEdit:

<img width="371" alt="Wangjing Road Network" src="https://github.com/user-attachments/assets/2a0e74fc-84f8-415c-8f1a-6a7f28a9770b" />

## Requirements
pandas   
numpy   
sumolib   
traci

## Getting started
- run `python simulation.py` to generate raw output data from the SUMO simulation.
- run `python queue_length_extraction.py` to process the raw data and generate the final dataset.
