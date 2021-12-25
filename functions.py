import argparse
import ruamel.yaml
import os
import pandas as pd
import numpy as np

def get_yaml(path: str) -> dict:
    with open(os.path.abspath(path), 'r', encoding='utf-8') as f:
        lines = f.readlines()
    config = ruamel.yaml.load('\n'.join(lines), Loader=ruamel.yaml.SafeLoader)
    return config


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path')
    parser.add_argument('--data_path')
    return parser.parse_args(args)

def flatten(rich_df):
    df_t = pd.DataFrame(data=rich_df.to_dict(),
                        index=rich_df.index.to_flat_index(),
                        columns=rich_df.columns.to_flat_index())
    df_t.reset_index(inplace=True)
    df_t['index'] = df_t['index'].apply(lambda t: t[1])
    df_t = df_t.rename({'index': rich_df.columns.names[0]}, axis=1)
    if not df_t.columns.empty:
        df_t.columns = pd.Series(map(lambda t: ' '.join([str(x) for x in t]) if isinstance(t, tuple) else t, df_t.columns))
    df_t = df_t.T.reset_index().T.reset_index(drop=True)
    return df_t

def minmax_scale(X):
    X_min = min(X)
    X_max = max(X)
    return np.array([(x - X_min)/(X_max - X_min) for x in X])
