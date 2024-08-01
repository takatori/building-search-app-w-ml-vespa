#!/usr//bin/env python

from argparse import ArgumentParser
import numpy as np

parser = ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()

x = np.loadtxt(args.input)
took = x[:, 1]

print("Average Took:")
print(np.average(took))
for percentile in [50, 90, 99]:
    print(f"{percentile} Percentile:")
    print(np.percentile(took, percentile))
