from simulator.graph_simulator import *
from experiments.experiments import *
from centrality_computer.time_amplify_functions import *
from centrality_computer.weight_function import *
from decimal import Decimal
from model.node_definitions import *
from sketch_utils.sketches import *
from sketch_utils.hash_functions import *
from data_process.data_process import *

# 1. temporal katz centrality compare to time ada katz centrality
# 1.1 flows data
# flows_file_path = '../../data/test.flows'
# simulator = OnlineGraphSimulator(flows_file_path)
# beta = 0.1
# base = 2
# norm = 0.1
# experiment = TemporalTimeAdaKatzCompareExperiment(beta, base, norm)
# simulator.simulate(experiment)
# print('***************')
# print(Decimal('0.8') * Decimal('3'))
# fun = ExponentialFunction(base, norm)
# amp = fun.amplify(1495576813)
# wei = fun.weight(1495576813)
# print(math.pow(base, amp))
# print(math.pow(base, wei))
# 1.2 tennis game data
# tennis_rg17_data_path = '../../data/rg17_data/raw/rg17_mentions_test.csv'
# simulator = OnlineGraphSimulator(tennis_rg17_data_path)
# print(simulator.get_edges())
# beta = 0.1
# base = 2.0
# norm = 0.0001
# output_path = '../../data/rg17_data/centrality_measures/'
# experiment = TemporalTimeAdaKatzCompareExperiment(beta, base, norm, output_path)
# simulator.simulate(experiment)

# 2. test min heap for top k
# k = 100
# beta = 0.5
# base = 2
# norm = 0.0001
# ex = MinHeapTopKExperiment(k, beta, base, norm)
# tennis_rg17_data_path = '../../data/rg17_data/raw/rg17_mentions.csv'
# simulator = OnlineGraphSimulator(tennis_rg17_data_path)
# simulator.simulate(ex)

# 3. test count min sketch and truth rank for Time Adaptive katz Centrality
# k = 100
# beta = 0.3
# base = 1.5
# norm = 0.00000001
# cm_sketch_size = 1024
# ex = AdaWithCountMinAndMemoryDictCompareExperiment(k, beta, base, norm, cm_sketch_size)
# tennis_rg17_data_path = '../../data/rg17_data/raw/rg17_mentions.csv'
# tennis_rg17_data_path = '../../data/maccdc2012_00000——.flows'
# tennis_rg17_data_path = '../../data/botnet-capture-20110815-fast-flux-2.flows'
# tennis_rg17_data_path = '../../data/equinix-chicago.dirA.20160121-125911.UTC.anon3_test.flows'
# simulator = OnlineGraphSimulator(tennis_rg17_data_path)
# simulator.simulate(ex)
# ex.plot()
# for sketch_num in range(4):
#     index = hash(str(sketch_num + 1) + str(56368)) & (256 - 1)
#     print(index)

# 4. etl data
# data_path = '../../data/equinix-chicago.dirA.20160121-125911.UTC.anon.flows'
# new_path = '../../data/equinix-chicago.dirA.20160121-125911.UTC.anon1.flows'
# clean_ipv6(data_path, new_path)
# print('ok')

# 5. temporal katz centrality compare to time ada katz centrality
func = LogFunction(2)
print(func.get_weight(1023))
