from collections import defaultdict
from xml.etree import ElementTree as ET
from sumolib.net import readNet
import pandas as pd
import numpy as np
import traci
import csv
import pickle


def parse_network(network_file):
    """
        Parses the .net file to get a list of edge start/end locations in the scenario.

        Args:
            network_file (string): the network file
        Returns:
            network (object): network object
    """
    return readNet(network_file)


def E2_output_processing():
    """
    Generate the queue length data
    """
    time = [x for x in range(5, 10801, 5)]
    full_df = pd.DataFrame(index=time)
    QueueLength = defaultdict(list)
    tree = ET.parse(r"scenario\output.xml")
    root = tree.getroot()
    for interval_elem in root.iter("interval"):
        lane_id = interval_elem.get("id")
        interval_end = float(interval_elem.get("end"))
        JamLength = interval_elem.get("meanMaxJamLengthInMeters")
        if interval_end >= 0 and interval_end <= 10800:
            QueueLength[lane_id].append(JamLength)

    for lane in QueueLength.keys():
        full_df[lane] = QueueLength[lane]
    full_df.to_csv('output_file.csv')
    return list(QueueLength.keys())


def adjacency_matrix_processing(lane_list):
    """
    Generate the directed binary graph:
        the directed edge refers to connectivity through intersection movement 
        or lane-changing (within the same road segment)
    """
    traci.start([
        r"E:\sumo1.20\bin\sumo.exe", "-c",
        r"scenario\wangjing_mini.sumocfg"
    ])
    node_num = len(lane_list)
    adjacency_matrix = np.zeros((node_num, node_num))
    for i, lane in enumerate(lane_list):
        link_list = traci.lane.getLinks(lane)
        linkTolane_list = [item[0] for item in link_list]
        for to_lane in linkTolane_list:
            adjacency_matrix[i][lane_list.index(to_lane)] = 1
    edge_list = traci.edge.getIDList()
    for edge in edge_list:
        if ':' in edge:
            continue
        lane_num = traci.edge.getLaneNumber(edge)
        for i in range(lane_num):
            lane_from = edge+'_'+str(i)
            for j in range(lane_num):
                lane_to = edge+'_'+str(j)
                adjacency_matrix[lane_list.index(lane_from)][lane_list.index(lane_to)] = 1
    with open('adjacency_matrix.pkl', 'wb') as f:
        pickle.dump(adjacency_matrix, f)
    traci.close()


def signal_cycle_processing(network, lane_list):
    """
    Generate the signal cycle file
    """
    tree = ET.parse(r"scenario\wangjing.net.xml")
    root = tree.getroot()
    junction_signal = {}
    signal_list = list()
    for child in root:
        if child.tag == 'tlLogic':
            tlsID = child.attrib['id']
            cycle = 0
            for subchild in child:
                if subchild.tag == 'phase':
                    cycle += int(subchild.attrib['duration'])
            junction_signal[tlsID] = cycle
    for lane in lane_list:
        edge_obj = network.getEdge('_'.join(lane.split('_')[:-1]))
        junction = edge_obj.getToNode().getID()
        if junction in junction_signal.keys():
            signal_list.append(junction_signal[junction])
        else:
            signal_list.append(0)  # no traffic light control
    with open('signal.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(signal_list)


if __name__ == "__main__":
    network = parse_network('scenario/wangjing.net.xml')
    lane_list = E2_output_processing()
    adjacency_matrix_processing(lane_list)
    signal_cycle_processing(network, lane_list)
