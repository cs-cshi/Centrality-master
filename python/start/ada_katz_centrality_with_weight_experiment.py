from simulator.graph_simulator import *
from experiments.experiments import AdaKatzCentralityWithWeightExperiment

e = 2.718281828459
k, beta, base, norm, cm_sketch_size = 100, 0.3, e, 0.0000001, 10240
ex = AdaKatzCentralityWithWeightExperiment(k, beta, base, norm, cm_sketch_size)

data_path = '../../data/equinix-chicago.dirA.20160121-125911.UTC.anon3_test.flows'
simulator = OnlineGraphSimulator(data_path)
simulator.simulate_with_weight(ex)
