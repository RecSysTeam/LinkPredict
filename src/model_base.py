from copy import deepcopy
from typing import Generator, Iterator, List, Tuple

import networkx as nx
import pandas as pd
from tqdm import tqdm

from src.data import holdout
from src.metrics import recall_n


def create_pairs_for_nodes(
    nodes: List[str],
    graph: nx.Graph,
    tqdm_disable: bool = True,
) -> List[Tuple["str", "str"]]:
    """
    create pairs of given nodes with each node of given graph
    """

    result = []
    graph_nodes = list(graph.nodes)

    for node in tqdm(nodes, disable=tqdm_disable):
        result = result + [(node, gn) for gn in graph_nodes if node != gn]

    return result


def generate_recomendations(
    scores: pd.DataFrame, topn: int = 10, score_name: str = "adamic_adar_index"
) -> pd.DataFrame:
    recs = []

    for idx in scores.index:
        sorted_recs = [
            x
            for x, _ in sorted(
                zip(scores["node_to"][idx], scores[score_name][idx]),
                key=lambda pair: pair[1],
                reverse=True,
            )
        ]
        recs.append([idx, sorted_recs])

    recs = pd.DataFrame.from_records(recs, columns=["note_id", "recomendations"])
    recs.set_index("note_id", inplace=True)
    return recs


def calculate_adamic_adar(
    graph: nx.Graph,
    pair_nodes: List[Tuple[str, str]],
) -> pd.DataFrame:
    graph_ = deepcopy(graph)

    preds = nx.adamic_adar_index(nx.DiGraph(graph_).to_undirected(), ebunch=pair_nodes)
    scores = [(u, v, p) for u, v, p in preds]
    scores = pd.DataFrame.from_records(
        scores, columns=["node_from", "node_to", "adamic_adar_index"]
    )
    scores.set_index("node_from", inplace=True)
    return scores


def evaluate_baseline(graph: nx.Graph, n_exp: int = 1000, alpha=0.1, topn: int = 5):

    recall = []
    for _ in tqdm(range(n_exp)):
        train_graph, holdout_links = holdout(graph, seed=None, alpha=0.1)
        sum([hl in train_graph.edges for hl in holdout_links])

        holdout_nodes = [hl[0] for hl in holdout_links]
        pairs = create_pairs_for_nodes(nodes=holdout_nodes, graph=train_graph)
        scores = (
            calculate_adamic_adar(graph=train_graph, pair_nodes=pairs)
            .groupby("node_from")
            .agg(lambda x: list(x))
        )

        recs = generate_recomendations(scores)

        holdout_links_df = (
            pd.DataFrame.from_records(
                holdout_links, columns=["note_id", "notes_to", "p"]
            )
            .groupby("note_id")
            .agg(lambda x: list(x))[["notes_to"]]
        )

        recall.append(recall_n(recs=recs, holdout_links=holdout_links_df, topn=topn))

    return recall
