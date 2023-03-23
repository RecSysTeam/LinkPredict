from typing import Dict

import numpy as np
import pandas as pd


def recall_n(recs: pd.DataFrame, holdout_links: pd.DataFrame) -> float:
    """[summary]

    Args:
        recs: pd.DataFrame
        'note_id', 'links to'
        id_1, [note_id_1, ..., note_id_n]
        id_1, [note_id_1, ..., note_id_k]


        holdout_links: pd.DataFrame
        'note_id', 'links to'
        id_1, [note_id_1, ..., note_id_n]
        id_2, [note_id_1, ..., note_id_k]

    Returns:
        recall score: float
    """
    recall = []
    for idx in recs.index:
        r = recs[idx]
        l = holdout_links[idx]
        recall.append(len(set(r).intersection(l)) / len(l))
    return np.mean(recall)
