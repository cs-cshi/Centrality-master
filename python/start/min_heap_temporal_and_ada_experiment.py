from simulator.graph_simulator import *
from experiments.experiments import *
from experiments.experiments import MinHeapTopKExperiment

# 原实验
# k = 200
# beta = 0.5
# base = 2
# norm = 0.000001
#
#
# """
# k = 100
# beta = 0.3
# base = 1.1
# norm = 0.00000001
# """
#
#
# ex = MinHeapTopKExperiment(k, beta, base, norm)
# #tennis_rg17_data_path = '../../data/rg17_data/raw/rg17_mentions_test.csv'
# data_path = '../../data/equinix-chicago.dirA.20160121-125911.UTC.anon3.flows'
# # simulator = OnlineGraphSimulator(tennis_rg17_data_path)
# simulator = OnlineGraphSimulator(data_path)
# simulator.simulate(ex)


## 以下使用equinix-chicago.dirA.20160121-125911.UTC.anon1.flows数据集
# truth_rank_1: node_id: 198.88.219.113, rank: 913.8159444088435
# norm过大，count-min值迅速起飞，但实际上此时的时间窗口值很小
# 上述现象原因为count-min size太小，还有一种可能是时间戳需要预处理减少不必要的位数



beta = 0.2
base = 2.718281828459
norm = 0.0001 # 针对anon1.flows
k = 200
sketch_size = 16384
ada_exp = True

ex = AdaWithCountMinAndMemoryDictCompareExperiment(k, beta, base, norm, sketch_size, ada_exp)

data_path = '../../data/equinix-chicago.dirA.20160121-125911.UTC.anon1.flows'

simulator = OnlineGraphSimulator(data_path)
simulator.simulate(ex)