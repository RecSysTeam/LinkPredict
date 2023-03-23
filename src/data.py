from pathlib import Path
from typing import List, Tuple, Union

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


def holdout(
    graph: nx.Graph, alpha: float = 0.1, seed=42
) -> Tuple[nx.Graph, List[Tuple[str, str]]]:
    """
    delete some links in Graph, and return them with modified graph
    Args:
        graph: nx.Graph
        alpha: percent of edges to delete frm graph
    Returns:
        modified_graph, edges
    """
    np.random.seed(seed=seed)

    modified_graph = graph
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
