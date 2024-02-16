from typing import Union

import networkx as nx
import rustworkx as rx
from deepdiff import DeepDiff


def convert_rustworkx_to_networkx(graph: rx.PyGraph) -> Union[nx.Graph, nx.MultiGraph, nx.DiGraph, nx.MultiDiGraph]:
    """Convert a rustworkx PyGraph or PyDiGraph to a networkx graph."""
    edge_list = [(graph[x[0]], graph[x[1]], {"weight": x[2]}) for x in graph.weighted_edge_list()]

    if isinstance(graph, rx.PyGraph):
        if graph.multigraph:
            return nx.MultiGraph(edge_list)
        else:
            return nx.Graph(edge_list)
    else:
        if graph.multigraph:
            return nx.MultiDiGraph(edge_list)
        else:
            return nx.DiGraph(edge_list)


nx_orig_graph = nx.DiGraph()
nx_orig_graph.add_node("node_a", value=1)
nx_orig_graph.add_node("node_b", value=2)
nx_orig_graph.add_edge("node_a", "node_b", weight=1)

# NetworkX -> rustworkx
rx_graph = rx.networkx_converter(nx_orig_graph)
# print(rx_graph)
# <rustworkx.PyDiGraph object at 0x101242d40>

# rustworkx -> NetworkX
nx_graph = convert_rustworkx_to_networkx(rx_graph)

assert type(nx_orig_graph) == type(nx_graph)
# このままでは属性情報が落ちるので注意
print(DeepDiff(nx_orig_graph.nodes, nx_graph.nodes, ignore_order=True))
print(DeepDiff(nx_orig_graph.edges, nx_graph.edges, ignore_order=True))
