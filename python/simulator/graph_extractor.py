from model.flow_definitions import *
from model.tennis_data_model import *


class GraphExtractor:
    def __init__(self, edge_data_path):
        self._edge_data_path = edge_data_path

    def get_edge_data(self):
        return self._edge_data_path

    def extract_edges(self):
        if self._edge_data_path[-1] == 'v':
            edges = self._extract_tennis_edges()
        else:
            edges = self._extract_flow_edges()

        return edges

    def _extract_flow_edges(self):
        with open(self._edge_data_path, 'r') as f:
            raw_data = f.readlines()
            for i in range(len(raw_data)):
                raw_data[i] = raw_data[i].rstrip('\n')
                if not raw_data[i].startswith('!'):
                    attr = raw_data[i].split(' ')
                    raw_data[i] = Flow(attr[0], attr[1], int(float(attr[2]) * 1000), attr[3])
                    # print(raw_data[i])
            raw_data = raw_data[5:]
            flow_records = FlowRecords(raw_data)
            # print(flow_records.records)
            return flow_records.get_records()

    def _extract_tennis_edges(self):
        mentions = []
        with open(self._edge_data_path, 'r') as f:
            raw_data = f.readlines()
            for i in range(len(raw_data)):
                raw_data[i] = raw_data[i].rstrip('\n')
                attr = raw_data[i].split(' ')
                mentions.append(Mention(attr[1], attr[2], int(attr[0])))
        return mentions
