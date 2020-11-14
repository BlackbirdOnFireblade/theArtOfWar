import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
import plotutil as prj
from target import Target
from builder import Builder

# conda install  matplotlib
# conda install -c conda-forge opencv


def parse_args():
	tp = lambda x:list(map(int, x.split('.')))
	parser = argparse.ArgumentParser(description='Houchi Plannner Configuration Args')
	parser.add_argument('--resolution', type=float, default="2", help='click scale per min')
	parser.add_argument('--timerate', type=float, default="1.8", help='')
	parser.add_argument('--unit', type=tp, default='2.2.3', help='unit size for Red, Blue, Gold')
	parser.add_argument('-r', '--resource', type=int, default=2000, help='')
	parser.add_argument('--resource_step', type=int, default=100, help='')
	parser.add_argument('-m', '--margin', type=int, default=30, help='')
	parser.add_argument('-o', '--offence', type=tp, default='0.2.1', help='Red, Blue, Gold')
	parser.add_argument('-d', '--defense', type=tp, default='3.1.0', help='Red, Blue, Gold')
	args = parser.parse_args()
	return args

def build_targets(args):
	GRADE = ['Red', 'Blue', 'Gold']
	o = [Target("{}-{}".format(GRADE[2 - i], j + 1), args.unit[2 - i], args.timerate, True, False) for i in range(len(GRADE)) for j in range(args.offence[2 - i])]
	d = [Target("{}-{}".format(GRADE[2 - i], j + 1), args.unit[2 - i], args.timerate, False, True) for i in range(len(GRADE)) for j in range(args.defense[2 - i])]
	return o, d


def main():
	args = parse_args()
	o, d = build_targets(args)
	builder = Builder(args, o, d)
	builder.show()

if __name__ == "__main__":
    main()
