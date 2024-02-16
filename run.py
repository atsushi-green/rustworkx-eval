# convert +append new_result_d=0.1.png new_result_d=1.0.png concated.png

import time
from dataclasses import dataclass
from typing import Any

import matplotlib.pyplot as plt
import networkc as nc
import networkit as nk
import networkx as nx
import rustworkx as rx

from src.runtime_util import calc_func_time, make_large_graph

plt.style.use(["seaborn-v0_8-colorblind"])
plt.rcParams["font.size"] = 15
# NOTE: 800以降から特に実行時間が長くなるので注意
NUM_NODES_LIST = [100, 200, 400, 800, 1600, 3200, 6400]


def main():
    # エッジ密度Dを変えて実験
    for d in [0.1, 0.5, 1.0]:
        run(d)


def edge_cost_fn(e):
    # edge_cost_fn for rustworkx
    return e


@dataclass
class Result:
    process_time: float
    result: Any


@calc_func_time
def run_networkx(G) -> Result:
    start = time.time()
    nx_result = dict(nx.all_pairs_dijkstra_path(G, weight="weight"))
    process_time = time.time() - start
    return Result(process_time, nx_result)


@calc_func_time
def run_networkit(G) -> Result:
    start = time.time()
    nkG = nk.nxadapter.nx2nk(G)
    ap_dijkstra = nk.distance.DynAPSP(nkG)
    nk_result = ap_dijkstra.run()

    process_time = time.time() - start
    return Result(process_time, nk_result)


@calc_func_time
def run_networkc(G) -> Result:
    start = time.time()
    nc_result = nc.all_pairs_dijkstra_path(G)
    process_time = time.time() - start
    return Result(process_time, nc_result)


@calc_func_time
def run_rustworkx(G) -> Result:
    start = time.time()

    ruG = rx.PyDiGraph()
    node_map = {n: ruG.add_node(n) for n in G.nodes()}

    for u, v, w in G.edges(data=True):
        ruG.add_edge(node_map[u], node_map[v], w["weight"])

    ru_result = rx.all_pairs_dijkstra_shortest_paths(ruG, edge_cost_fn)
    process_time = time.time() - start
    # print("Rust実装のall_pairs_dijkstra_path\t", rustworkx_el_time)
    return Result(process_time, ru_result)


def assert_rustworkx_result(ru_result: rx.AllPairsPathMapping, nx_result: dict):
    for start_node, paths in ru_result.items():
        for end_node, path in paths.items():
            assert path == nx_result[start_node][end_node]


def run(edge_density):
    nx_result_list = []
    nc_result_list = []
    kit_result_list = []
    ru_result_list = []
    for num_nodes in NUM_NODES_LIST:
        G = make_large_graph(num_nodes=num_nodes, edge_density=edge_density)
        print(f"======trial: num_nodes: {num_nodes}, edge_density: {edge_density}=====")
        print(G.number_of_nodes(), G.number_of_edges())
        if num_nodes <= 2000:
            # networkx
            nx_result = run_networkx(G)
            nx_result_list.append(nx_result)
            # networkc
            nc_result = run_networkc(G)
            nc_result_list.append(nc_result)
        # rustworkx
        ru_result = run_rustworkx(G)
        ru_result_list.append(ru_result)
        # networkit
        kit_result = run_networkit(G)
        kit_result_list.append(kit_result)

        # 出力が一致していることの確認
        # assert nc_result.result == nx_result.result
        # assert_rustworkx_result(ru_result.result, nx_result.result)

        print("\n\n")

    draw_eltime_plot(edge_density, nx_result_list, nc_result_list, kit_result_list, ru_result_list)


def draw_eltime_plot(
    edge_density: float, nx_result_list: list[Result], nc_result_list: list[Result], kit_result: list[Result], ru_result_list: list[Result]
):
    # 横軸にnum_node, process_timeをとり、それぞれのライブラリごとに色分けして折れ線グラフで描画する

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.subplots_adjust(left=0.12, right=0.95, bottom=0.07, top=0.96)

    nx_times = [nx_res.process_time for nx_res in nx_result_list]
    nc_times = [nc_res.process_time for nc_res in nc_result_list]
    kit_times = [kit_res.process_time for kit_res in kit_result]
    rx_times = [ru_res.process_time for ru_res in ru_result_list]

    ax.plot(range(len(nx_times)), nx_times, "o-", label="NetworkX")
    ax.plot(range(len(nc_times)), nc_times, "o-", label="networkc")
    ax.plot(range(len(kit_times)), kit_times, "o-", label="NetworKit")
    ax.plot(range(len(rx_times)), rx_times, "o-", label="rustworkx")

    ax.set_xticks(range(len(NUM_NODES_LIST)))
    ax.set_xticklabels(NUM_NODES_LIST)
    ax.set_xlabel("number of graph nodes")
    ax.set_ylabel("runtime [sec]")
    ax.set_title(f"D={edge_density}")
    ax.legend(loc="upper left")

    plt.savefig(f"result_d={edge_density}.png", dpi=300)


if __name__ == "__main__":
    main()
