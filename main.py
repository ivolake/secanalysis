import sys

from Processors import Step1Processor, Step2Processor
from functions import parse_args, get_yaml

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    config = get_yaml(args.config_path)
