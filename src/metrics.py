from typing import Dict

import numpy as np
import pandas as pd


def recall_n(recs: pd.DataFrame, holdout_links: pd.DataFrame, topn: int = 5) -> float:
    """
    Args:
        recs: pd.DataFrame
        'note_id', 'recomendations'
        id_1, [note_id_1, ..., note_id_n]
        id_1, [note_id_1, ..., note_id_k]


        holdout_links: pd.DataFrame
        'note_id', 'notes_to'
        id_1, [note_id_1, ..., note_id_n]
        id_2, [note_id_1, ..., note_id_k]

    Returns:
        recall score: float
    """
    recall = []
    for idx in recs.index:
        r = recs["recomendations"][idx][:topn]
        l = holdout_links["notes_to"][idx]
        recall.append(len(set(r).intersection(l)) / len(l))
    return np.mean(recall)
