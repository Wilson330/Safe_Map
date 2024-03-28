import os
import pickle
data_dir = f'{os.path.dirname(__file__)}/scores'

def load_score(score_type):
    if score_type not in ['light', 'monitor', 'safety']:
        raise KeyError("score type should be one of ['light', 'monitor', 'safety']")

    with open (f'{data_dir}/edge_{score_type}_scores.pickle', 'rb') as f:
        scores = pickle.load(f)
    return scores