# used to read in command line args (dim p heuristic algo)
import argparse
from time import sleep, time


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-d", "--dimension", type=int, default=10, help="dimension of gridworld")
    p.add_argument("-p", "--probability", type=float, default=0.33, help="probability of a blocked square")
    p.add_argument("-m", "--heuristic", type=str, default="euclidian", help="heuristic of your desired algorithm (if possible)")
    p.add_argument("-a", "--agent", type=str, default="example_inference", help="one of the 4 types of agents described in the assignment")

    # parse arguments and create the gridworld
    args = p.parse_args()

    # call the solver method with the args
    
        