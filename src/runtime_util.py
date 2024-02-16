import datetime
import random
from functools import wraps

import networkx as nx

random.seed(0)


def make_large_graph(num_nodes: int = 1000, edge_density: float = 0.5) -> nx.Graph:
    graph = nx.DiGraph()
    graph.add_nodes_from(range(0, num_nodes))
    for i in range(0, num_nodes):
        for j in range(0, num_nodes):
            # edge_densityの確率で辺を追加する
            if random.random() <= edge_density and i != j:
                graph.add_edge(i, j, weight=(random.randint(1, 100000) / 100))
    return graph


def calc_func_time(f: callable):
    """実行時間を測定するラッパー関数

    Args:
        f (callable): _description_

    Returns:
        _type_: _description_
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = f(*args, **kwargs)
        end = datetime.datetime.now()
        print(f"elapsed time: {f.__name__}: { end - start }")
        return result

    return wrapper
