from centrality_computer.time_adaptive_katz_centrality_computer import *
from centrality_computer.temporal_katz_centrality_computer import *
from centrality_computer.weight_function import *
from sketch_utils.sketch_holder import *
from centrality_computer.time_amplify_functions import *
from sketch_utils.sketches import *
from evaluation.evaluation_utils import *
from plot_util.plot_utils import *
import matplotlib.pyplot as plt

# e
e = 2.718281828459


class TemporalTimeAdaKatzCompareExperiment:
    """
    比较Temporal Katz Centrality 和 Time Adaptive Katz的异同。
    """

    def __init__(self, beta=0.5, base=e, norm=0.001, output_path=None):
        ada_params = AdaKatzComputerParams(beta, ExponentialFunction(base, norm))
        ada_sketch = MemoryDictionary()
        ada_sketch_holder = SketchHolder(ada_sketch)
        self.ada_katz_computer = AdaKatzComputer(ada_sketch_holder, ada_params)
        temporal_params = TemporalKatzParams(beta, ExponentialFunction(base, norm))
        temporal_sketch = MemoryDictionary()
        temporal_sketch_holder = SketchHolder(temporal_sketch)
        self.temporal_katz_computer = TemporalKatzComputer(temporal_sketch_holder, temporal_params)
        self.output_path = output_path

    def start(self, src, trg, timestamp):
        self.ada_katz_computer.ada_update(src, trg, timestamp)
        self.temporal_katz_computer.update(src, trg, timestamp)

    def show_result(self):
        print('ada_katz_result: ')
        self._show_ada_katz_result(self.temporal_katz_computer.get_node_last_activation())
        print('katz_computer: ')
        self.temporal_katz_computer.get_sketch_holder().show_values()

    def _show_ada_katz_result(self, node_last_activation):
        kvs = self.ada_katz_computer.get_sketch_holder().get_values()
        for node_id in kvs:
            sketch_value = kvs[node_id]
            rank = self.ada_katz_computer.sketch_value_to_rank(sketch_value, node_last_activation[node_id])
            print('key: ' + str(node_id) + ', value: ' + str(rank), end='; ')
        print()

    def _get_ada_katz_result(self, node_last_activation):
        result_rank = []
        kvs = self.ada_katz_computer.get_sketch_holder().get_values()
        for node_id in kvs:
            sketch_value = kvs[node_id]
            rank = self.ada_katz_computer.sketch_value_to_rank(sketch_value, node_last_activation[node_id])
            result_rank.append('node_id: ' + str(node_id) + ', rank_value: ' + str(rank))
        return result_rank

    def _get_temporal_katz_result(self):
        result_rank = []
        kvs = self.ada_katz_computer.get_sketch_holder().get_values()
        for node_id in kvs:
            rank = kvs[node_id]
            result_rank.append('node_id: ' + str(node_id) + ', rank_value: ' + str(rank))
        return result_rank

    def save_result(self):
        save_list_as_file(
            self.output_path + 'ada_' + str(self.ada_katz_computer.get_params().get_time_amplify_function()) + '.txt',
            self._get_ada_katz_result(self.temporal_katz_computer.get_node_last_activation()))
        save_list_as_file(
            self.output_path + 'temporal_' + str(
                self.temporal_katz_computer.get_params().get_weight_function()) + '.txt',
            self._get_temporal_katz_result())


def save_list_as_file(out_path, ranks):
    print('save to ' + out_path)
    with open(out_path, 'w') as f:
        for rank in ranks:
            f.write(rank + '\n')


class MinHeapTopKExperiment:
    """
    测试MinHeap保存Top K rank Node。
    """

    def __init__(self, k, beta=0.5, base=e, norm=0.001, output_path=None):
        self.__k = k
        ada_sketch_holder = SketchHolder(MemoryDictionary(), MinHeap(k, key=lambda item: item.get_rank()))
        # ada_sketch_holder = SketchHolder(CountMinSketch(128), MinHeap(k, key=lambda item: item.get_rank()))
        self.__ada_katz_computer = AdaKatzComputer(ada_sketch_holder,
                                                   AdaKatzComputerParams(beta, ExponentialFunction(base, norm)))
        temporal_sketch_holder = SketchHolder(MemoryDictionary(), MinHeap(k, key=lambda item: item.get_rank()))
        self.__temporal_katz_computer = TemporalKatzComputer(temporal_sketch_holder,
                                                             TemporalKatzParams(beta, ExponentialFunction(base, norm)))
        self.__output_path = output_path

    def start(self, src, dst, time):
        # self.__ada_katz_computer.ada_update(src, dst, time)
        self.__ada_katz_computer.update(src, dst, time)
        self.__temporal_katz_computer.update(src, dst, time)

    def show_result(self):
        top_k_ada = sorted(self.__ada_katz_computer.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                           reverse=True)
        top_k_temporal = sorted(self.__temporal_katz_computer.get_sketch_holder().min_heap_get_all(),
                                key=lambda x: x.get_rank(), reverse=True)
        print('************ada************')
        print(top_k_ada)
        print('************temporal************')
        print(top_k_temporal)

        print('************jaccard similarity************')
        top_k_ada_node_id = [node.get_node_id() for node in top_k_ada]
        top_k_temporal_node_id = [node.get_node_id() for node in top_k_temporal]
        jaccard_similarity = get_jaccard_similarity(top_k_ada_node_id, top_k_temporal_node_id)
        print('jaccard similarity: ' + str(jaccard_similarity))


class AdaWithCountSketchAndMemoryDictCompareExperiment:
    """
    测试Time Adaptive Katz Centrality 在 CountSketch和 MemoryDict存储模式下的异同.
    """

    def __init__(self, k, beta=0.5, base=e, norm=0.001, cm_sketch_size=256, output_path=None):
        self.__kk = k
        self.__ada_computer_cs = AdaKatzComputer(
            SketchHolder(CountSketch(cm_sketch_size), MinHeap(k, key=lambda x: x.get_rank())),
            AdaKatzComputerParams(beta, ExponentialFunction(base, norm)))

        self.__ada_computer_md = AdaKatzComputer(
            SketchHolder(MemoryDictionary(), MinHeap(k, key=lambda x: x.get_rank())),
            AdaKatzComputerParams(beta, ExponentialFunction(base, norm)))
        self.__output_path = output_path

    def start(self, src, dst, time):
        self.__ada_computer_cs.ada_update(src, dst, time)
        self.__ada_computer_md.ada_update(src, dst, time)

    def show_result(self):
        top_k_ada_cs = sorted(self.__ada_computer_cs.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        top_k_ada_md = sorted(self.__ada_computer_md.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        for i in range(len(top_k_ada_cs)):
            print('countsketch_rank_' + str(i + 1) + ': ' + str(top_k_ada_cs[i]) +
                  ', -----> truth_rank_' + str(i + 1) + ': ' + str(top_k_ada_md[i]))

        print('************jaccard similarity************')
        top_k_ada_cs_node_id = [node.get_node_id() for node in top_k_ada_cs]
        top_k_ada_md_node_id = [node.get_node_id() for node in top_k_ada_md]

        jaccard_similarity = get_jaccard_similarity(top_k_ada_cs_node_id, top_k_ada_md_node_id)
        hit_k, precision_k, recall_k, map_k, ndcg_k, mrr_k = top_k_eval(top_k_ada_cs_node_id, top_k_ada_md_node_id,
                                                                        self.__kk)
        print('jaccard similarity: ' + str(jaccard_similarity))
        print('hit_rate@%d:' % self.__kk, hit_k)
        print('precision@%d:' % self.__kk, precision_k)
        print('recall@%d:' % self.__kk, recall_k)
        print('map@%d:' % self.__kk, map_k)
        print('ndcg@%d:' % self.__kk, ndcg_k)
        print('mrr@%d:' % self.__kk, mrr_k)

        self.plot()

    def plot(self):
        top_k_ada_cs = sorted(self.__ada_computer_cs.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        top_k_ada_md = sorted(self.__ada_computer_md.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        ada_cs_rank, ada_cs_centrality_score = [], []
        ada_md_rank, ada_md_centrality_score = [], []
        for i in range(len(top_k_ada_cs)):
            ada_cs_rank.append(i + 1)
            ada_cs_centrality_score.append(top_k_ada_cs[i].get_value())
            ada_md_rank.append(i + 1)
            ada_md_centrality_score.append(top_k_ada_md[i].get_value())

        plot_2(ada_cs_rank, ada_cs_centrality_score, ada_md_rank, ada_md_centrality_score, 'count_min_sketch', 'memory',
               'rank', 'centrality score')


class AdaWithCountMinAndMemoryDictCompareExperiment:
    """
    测试Time Adaptive Katz Centrality 在 Ada-CountMinSketch和 MemoryDict存储模式下的异同.
    """

    def __init__(self, k, beta=0.5, base=e, norm=0.001, cm_sketch_size=256, output_path=None, ada_exp=True):
        self.__kk = k
        if ada_exp:
            self.__ada_computer_cm = AdaKatzComputer(
                SketchHolder(CountMinSketch(cm_sketch_size), MinHeap(k, key=lambda x: x.get_rank())),
                AdaKatzComputerParams(beta, ExponentialFunction(base, norm)))

            self.__ada_computer_md = AdaKatzComputer(
                SketchHolder(MemoryDictionary(), MinHeap(k, key=lambda x: x.get_rank())),
                AdaKatzComputerParams(beta, ExponentialFunction(base, norm)))
        else:
            self.__ada_computer_cm = AdaKatzComputer(
                SketchHolder(CountMinSketch(cm_sketch_size), MinHeap(k, key=lambda x: x.get_rank())),
                AdaKatzComputerParams(beta, LinearFunction(base, norm)))

            self.__ada_computer_md = AdaKatzComputer(
                SketchHolder(MemoryDictionary(), MinHeap(k, key=lambda x: x.get_rank())),
                AdaKatzComputerParams(beta, LinearFunction(base, norm)))

        self.__output_path = output_path

    def start(self, src, dst, time):
        self.__ada_computer_cm.ada_update(src, dst, time)
        self.__ada_computer_md.ada_update(src, dst, time)

    def show_result(self):
        top_k_ada_cm = sorted(self.__ada_computer_cm.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        top_k_ada_md = sorted(self.__ada_computer_md.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        sumofare = 0
        for i in range(len(top_k_ada_cm)):
            print('count_min_rank_' + str(i + 1) + ': ' + str(top_k_ada_cm[i]) +
                  ', -----> truth_rank_' + str(i + 1) + ': ' + str(top_k_ada_md[i]))

            tmpare = (top_k_ada_cm[i].get_value() - top_k_ada_md[i].get_value()) / top_k_ada_md[i].get_value()
            sumofare += tmpare
        are = sumofare / self.__kk
        print('ARE@%d:' % self.__kk, are)

        # print('----------count min sketches:----------')
        # sketches = self.__ada_computer_cm.get_sketch_holder().get_values()
        # for sketch_num in range(len(sketches)):
        #     print('sketch_' + str(sketch_num + 1) + ': ')
        #     sketch = sketches[sketch_num]
        #     for i in range(len(sketch)):
        #         print('sketch_' + str(sketch_num + 1) + ': ' + str(i) + ' ---> ' + str(sketch[i]))
        # print('----------truth:----------')
        # kvs = self.__ada_computer_md.get_sketch_holder().get_values()
        # for i in kvs:
        #     print(str(i) + ' ------> ' + str(kvs[i]))

        print('************jaccard similarity************')
        top_k_ada_cm_node_id = [node.get_node_id() for node in top_k_ada_cm]
        top_k_ada_md_node_id = [node.get_node_id() for node in top_k_ada_md]

        jaccard_similarity = get_jaccard_similarity(top_k_ada_cm_node_id, top_k_ada_md_node_id)
        hit_k, precision_k, recall_k, map_k, ndcg_k, mrr_k = top_k_eval(top_k_ada_cm_node_id, top_k_ada_md_node_id,
                                                                        self.__kk)
        print('jaccard similarity: ' + str(jaccard_similarity))
        print('hit_rate@%d:' % self.__kk, hit_k)
        print('precision@%d:' % self.__kk, precision_k)
        print('recall@%d:' % self.__kk, recall_k)
        # print('map@%d:' % self.__kk, map_k)
        print('ndcg@%d:' % self.__kk, ndcg_k)
        print('mrr@%d:' % self.__kk, mrr_k)

        self.plot()

    def plot(self):
        top_k_ada_cm = sorted(self.__ada_computer_cm.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        top_k_ada_md = sorted(self.__ada_computer_md.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        ada_cm_rank, ada_cm_centrality_score = [], []
        ada_md_rank, ada_md_centrality_score = [], []
        for i in range(len(top_k_ada_cm)):
            ada_cm_rank.append(i + 1)
            ada_cm_centrality_score.append(top_k_ada_cm[i].get_value())
            ada_md_rank.append(i + 1)
            ada_md_centrality_score.append(top_k_ada_md[i].get_value())

        plot_2(ada_cm_rank, ada_cm_centrality_score, ada_md_rank, ada_md_centrality_score, 'count_min_sketch', 'memory',
               'rank', 'centrality score')


class CountMinAndMemoryDictCompareExperiment:
    """
    测试Time Adaptive Katz Centrality 在 CountMinSketch和 MemoryDict存储模式下的异同.
    """

    def __init__(self, k, beta=0.5, base=e, norm=0.001, cm_sketch_size=256, output_path=None):
        self.__ada_computer_cm = AdaKatzComputer(
            SketchHolder(CountMinSketch(cm_sketch_size), MinHeap(k, key=lambda x: x.get_rank())),
            AdaKatzComputerParams(beta, ExponentialFunction(base, norm)))

        self.__ada_computer_md = TemporalKatzComputer(
            SketchHolder(MemoryDictionary(), MinHeap(k, key=lambda x: x.get_rank())),
            TemporalKatzParams(beta, ExponentialFunction(base, norm)))
        self.__output_path = output_path

    def start(self, src, dst, time):
        # naive count-min without time decay
        # failed
        self.__ada_computer_cm.ada_update(src, dst, time)
        self.__ada_computer_md.update(src, dst, time)

    def show_result(self):
        top_k_ada_cm = sorted(self.__ada_computer_cm.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        top_k_ada_md = sorted(self.__ada_computer_md.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        for i in range(len(top_k_ada_cm)):
            print('ada_cm_rank_' + str(i + 1) + ': ' + str(top_k_ada_cm[i]) +
                  ', -----> truth_rank_' + str(i + 1) + ': ' + str(top_k_ada_md[i]))

        # print('----------count min sketches:----------')
        # sketches = self.__ada_computer_cm.get_sketch_holder().get_values()
        # for sketch_num in range(len(sketches)):
        #     print('sketch_' + str(sketch_num + 1) + ': ')
        #     sketch = sketches[sketch_num]
        #     for i in range(len(sketch)):
        #         print('sketch_' + str(sketch_num + 1) + ': ' + str(i) + ' ---> ' + str(sketch[i]))
        # print('----------truth:----------')
        # kvs = self.__ada_computer_md.get_sketch_holder().get_values()
        # for i in kvs:
        #     print(str(i) + ' ------> ' + str(kvs[i]))

        print('************jaccard similarity************')
        top_k_ada_cm_node_id = [node.get_node_id() for node in top_k_ada_cm]
        top_k_ada_md_node_id = [node.get_node_id() for node in top_k_ada_md]
        jaccard_similarity = get_jaccard_similarity(top_k_ada_cm_node_id, top_k_ada_md_node_id)
        print('jaccard similarity: ' + str(jaccard_similarity))

        self.plot()

    def plot(self):
        top_k_ada_cm = sorted(self.__ada_computer_cm.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        top_k_ada_md = sorted(self.__ada_computer_md.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        ada_cm_rank, ada_cm_centrality_score = [], []
        ada_md_rank, ada_md_centrality_score = [], []
        for i in range(len(top_k_ada_cm)):
            ada_cm_rank.append(i + 1)
            ada_cm_centrality_score.append(top_k_ada_cm[i].get_value())
            ada_md_rank.append(i + 1)
            ada_md_centrality_score.append(top_k_ada_md[i].get_value())

        plot_2(ada_cm_rank, ada_cm_centrality_score, ada_md_rank, ada_md_centrality_score, 'count_min_sketch', 'memory',
               'rank', 'centrality score')


class AdaKatzCentralityWithWeightExperiment:
    def __init__(self, k, beta=0.5, base=e, norm=0.001, cm_sketch_size=256, output_path=None):
        # truth centrality score
        self.__ada_computer_md = AdaKatzComputer(
            SketchHolder(MemoryDictionary(), MinHeap(k, key=lambda x: x.get_rank())),
            AdaKatzComputerParams(beta, ExponentialFunction(base, norm)))

        # centrality score with count min sketch
        self.__ada_computer_cm = AdaKatzComputer(
            SketchHolder(CountMinSketch(cm_sketch_size), MinHeap(k, key=lambda x: x.get_rank())),
            AdaKatzComputerParams(beta, ExponentialFunction(base, norm)))

        # centrality score with count min sketch and log2(weight)
        self.__ada_computer_cm_log_2_weight = AdaKatzComputer(
            SketchHolder(CountMinSketch(cm_sketch_size), MinHeap(k, key=lambda x: x.get_rank())),
            AdaKatzComputerParams(beta, ExponentialFunction(base, norm), LogFunction(2)))

        # centrality score with count min sketch and ln(weight)
        self.__ada_computer_cm_ln_weight = AdaKatzComputer(
            SketchHolder(CountMinSketch(cm_sketch_size), MinHeap(k, key=lambda x: x.get_rank())),
            AdaKatzComputerParams(beta, ExponentialFunction(base, norm), LogFunction(e)))

    def start_with_weight(self, src, dst, timestamp, weight):
        self.__ada_computer_md.ada_update(src, dst, timestamp)
        self.__ada_computer_cm.ada_update(src, dst, timestamp)
        self.__ada_computer_cm_log_2_weight.ada_update(src, dst, timestamp, weight)
        self.__ada_computer_cm_ln_weight.ada_update(src, dst, timestamp, weight)

    def show_result(self):
        top_k_ada_md = sorted(self.__ada_computer_md.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)
        top_k_ada_cm = sorted(self.__ada_computer_cm.get_sketch_holder().min_heap_get_all(), key=lambda x: x.get_rank(),
                              reverse=True)

        top_k_ada_cm_log_2_weight = sorted(self.__ada_computer_cm_log_2_weight.get_sketch_holder().min_heap_get_all(),
                                           key=lambda x: x.get_rank(),
                                           reverse=True)
        top_k_ada_cm_ln_weight = sorted(self.__ada_computer_cm_ln_weight.get_sketch_holder().min_heap_get_all(),
                                        key=lambda x: x.get_rank(),
                                        reverse=True)

        ada_cm_rank, ada_cm_centrality_score = [], []
        ada_md_rank, ada_md_centrality_score = [], []
        ada_cm_log_2_weight_rank, ada_cm_log_2_centrality_score = [], []
        ada_cm_ln_rank, ada_cm_ln_centrality_score = [], []
        for i in range(len(top_k_ada_cm)):
            ada_md_rank.append(i + 1)
            ada_md_centrality_score.append(top_k_ada_md[i].get_value())

            ada_cm_rank.append(i + 1)
            ada_cm_centrality_score.append(top_k_ada_cm[i].get_value())

            ada_cm_log_2_weight_rank.append(i + 1)
            ada_cm_log_2_centrality_score.append(top_k_ada_cm_log_2_weight[i].get_value())

            ada_cm_ln_rank.append(i + 1)
            ada_cm_ln_centrality_score.append(top_k_ada_cm_ln_weight[i].get_value())

        plot_4(ada_md_rank, ada_md_centrality_score,
               ada_cm_rank, ada_cm_centrality_score,
               ada_cm_log_2_weight_rank, ada_cm_log_2_centrality_score,
               ada_cm_ln_rank, ada_cm_ln_centrality_score,
               'truth', 'CMS', 'CMS with log(weight)', 'CMS with ln(weight)',
               'Rank', 'Centrality Score')
