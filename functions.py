import argparse
import ruamel.yaml
import os

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