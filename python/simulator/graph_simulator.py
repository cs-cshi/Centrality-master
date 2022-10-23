from simulator.graph_extractor import *


class OnlineGraphSimulator:
    def __init__(self, data_path):
        self._edges = sorted(GraphExtractor(data_path).extract_edges(), key=lambda item: item.get_timestamp())
        self._edges = self._edge_timestamp_begin_with_start()  # start time is 1.

    def get_edges(self):
        return self._edges

    def simulate(self, experiment=None):
        for i in range(len(self._edges)):
            experiment.start(self._edges[i].get_src(), self._edges[i].get_dst(), self._edges[i].get_timestamp())
        # experiment.save_result()
        experiment.show_result()

    def simulate_with_weight(self, experiment=None):
        for i in range(len(self._edges)):
            experiment.start_with_weight(self._edges[i].get_src(), self._edges[i].get_dst(),
                                         self._edges[i].get_timestamp(), self._edges[i].get_length())
        experiment.show_result()

    def _edge_timestamp_begin_with_start(self):
        start_time = self._edges[0].get_timestamp() - 1
        for edge in self._edges:
            actual_timestamp = edge.get_timestamp()
            edge.set_timestamp(actual_timestamp - start_time)
        return self._edges
