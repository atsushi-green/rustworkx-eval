import networkx as nx
import numpy as np
import rustworkx as rx

graph = nx.DiGraph()

graph.add_node("node_a", value=1)
graph.add_node("node_b")
graph.add_node(2)
graph.add_node(("a", 2))

# ノードへのアクセスはノードオブジェクトで指定できる
print(graph.nodes["node_a"])  # {'value': 1}

# エッジの追加はノードオブジェクトで指定できる
graph.add_edge("node_a", "node_b", weight=1)
graph.add_edge(2, ("a", 2), weight=5)
# エッジへのアクセス
edge_data = graph.get_edge_data("node_a", "node_b")
print(edge_data["weight"])  # 1


# rustworkx
graph = rx.PyDiGraph()
node_a = graph.add_node("my_node_a")
node_b = graph.add_node("my_node_b")
node_c = graph.add_node(2)
node_d = graph.add_node(("a", 2))

print(node_a)  # 0
print(node_b)  # 1
print(node_c)  # 2
print(node_d)  # 3

print(graph[node_a])  # my_node_a
print(graph[node_b])  # my_node_b
print(graph[node_c])  # 2
print(graph[node_d])  # ('a', 2)

edge_a_b = graph.add_edge(node_a, node_b, "edge_a_b")
edge_c_d = graph.add_edge(node_c, node_d, 100)
print(edge_a_b)  # 0
print(edge_c_d)  # 1
print(graph.edges())  # ['edge_a_b', 100]


# ================
graph = rx.PyDiGraph()
graph.extend_from_weighted_edge_list(
    [
        (0, 1, {"weight": 1}),
        (0, 2, {"weight": 2}),
        (1, 3, {"weight": 2}),
        (3, 0, {"weight": 3}),
    ]
)
dist_matrix = rx.digraph_floyd_warshall_numpy(graph, weight_fn=lambda edge: edge["weight"])
# [[ 0.  1.  2.  3.]
#  [ 5.  0.  7.  2.]
#  [inf inf  0. inf]
#  [ 3.  4.  5.  0.]]
print(dist_matrix)


# ================
graph = rx.PyGraph()
# graph.extend_from_edge_list([(0, 1, 2), (1, 0, 1)])

# graph.extend_from_edge_list([(0, 1), (1, 0)])
a = rx.PyGraph.from_adjacency_matrix(np.array([[0, 1, 10], [1, 0, 10], [1, 0, 10]], dtype=np.float64))
print(a.nodes())
print(a.edge_list())


graph = rx.PyGraph()
node_a = graph.add_node({"time": "5pm"})
node_b = graph.add_nodes_from([{"time": "2pm"}])
graph[node_a]["room"] = 714
