from typing import Iterator, List, Tuple

import networkx as nx


def create_pairs_for_nodes(
    nodes: List[str], graph: nx.Graph
) -> List[Tuple["str", "str"]]:
    """
    create pairs of given nodes with each node of given graph
    """

    result = []
    graph_nodes = list(graph.nodes)

    for node in nodes:
        result += [(node, gn) for gn in graph_nodes]

    return result


def calculate_adamic_adar(
    graph: nx.Graph, pair_nodes: List[Tuple[str, str]]
) -> Iterator:
    return nx.adamic_adar_index(graph, ebunch=pair_nodes)
