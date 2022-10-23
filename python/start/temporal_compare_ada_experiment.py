from experiments.experiments import TemporalTimeAdaKatzCompareExperiment
from simulator.graph_simulator import *

tennis_rg17_data_path = '../../data/rg17_data/raw/rg17_mentions_test.csv'
simulator = OnlineGraphSimulator(tennis_rg17_data_path)
print(simulator.get_edges())
beta = 0.1
base = 2.0
norm = 0.0001
output_path = '../../data/rg17_data/centrality_measures/'
experiment = TemporalTimeAdaKatzCompareExperiment(beta, base, norm, output_path)
simulator.simulate(experiment)
