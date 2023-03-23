from copy import deepcopy
from pathlib import Path
from typing import List, Optional, Tuple, Union

import networkx as nx
import numpy as np
import obsidiantools.api as otools

ATTACHMENTS = True


def extract_vault(path_voult_folder: Union[Path, str]) -> otools.Vault:
    path_voult_folder = Path(path_voult_folder)

    assert path_voult_folder.exists(), f"Directory {path_voult_folder} does not exsist"

    vault = otools.Vault(path_voult_folder).connect(attachments=ATTACHMENTS).gather()
    df = vault.get_all_file_metadata()
    print(df.info())

    return vault


def delete_self_linking(graph: nx.Graph) -> nx.Graph:
    """
    delete all links of type A <-> A
    (self linking is bad for calculation adamic adar index, because of 1 /  log(degree(w)))
    """

    graph_new = deepcopy(graph)
    edges = graph_new.edges

    for edge in edges:
        if edge[0] == edge[1]:
            graph_new.remove_edge(edge)

    return graph_new


def holdout(
    graph: nx.Graph, alpha: float = 0.1, seed: Optional[int] = None
) -> Tuple[nx.Graph, List[Tuple[str, str]]]:
    """
    delete some links in Graph, and return them with modified graph
    Args:
        graph: nx.Graph
        alpha: percent of edges to delete frm graph [0., 1.]
    Returns:
        modified_graph, edges
    """
    if seed:
        np.random.seed(seed=seed)

    modified_graph = deepcopy(graph)
    edges = list(modified_graph.edges)
    n_edges = len(edges)
    delete_edges_idx = np.random.choice(
        np.arange(0, n_edges),
        size=int(alpha * n_edges),
        replace=False,
    ).tolist()

    delete_edges_idx.sort(reverse=True)

    deleted_edges = []
    for idx in delete_edges_idx:
        deleted_edges.append(edges.pop(idx))

    for e in deleted_edges:
        modified_graph.remove_edge(*e[:2])

    return modified_graph, deleted_edges
