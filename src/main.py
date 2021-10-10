# used to read in command line args (dim p heuristic algo)
import argparse
from time import sleep, time
from gridworld import Gridworld

"""
  Creates a gridworld and carrys out repeated A* based on the agent
  @param dim: dimension of the grid
  @param prob: probability of having a blocker
  @param agent: the type of visibility we have
  @param complete_grid: optional supplied grid instead of creating one 
"""


def solver(dim, prob, agent, complete_grid=None):

  # create a gridworld
  if not complete_grid:
    complete_grid = Gridworld(dim, prob, False)
    complete_grid.print()
  
  # create gridworld that agent uses to take note of blocks
  discovered_grid = Gridworld(dim)

  # check the agent and act accordingly

# method for 4-neighbor agent
def update_neighbor_obstacles(curr, discovered_grid, complete_grid, dim):
  # check the neighbor above the block
  if curr[0] - 1 >= 0:
    if complete_grid.gridworld[curr[0] - 1][curr[1]] == 1:
      discovered_grid.update_grid_obstacle((curr[0] - 1, curr[1]), 1)
    else:
      discovered_grid.update_grid_obstacle((curr[0] - 1, curr[1]), 0)
  # check the neighbor below the block
  if curr[0] + 1 < dim:
    if complete_grid.gridworld[curr[0] + 1][curr[1]] == 1:
      discovered_grid.update_grid_obstacle((curr[0] + 1, curr[1]), 1)
    else:
      discovered_grid.update_grid_obstacle((curr[0] + 1, curr[1]), 0)
  # check the neighbor left of the block
  if curr[1] - 1 >= 0:
    if complete_grid.gridworld[curr[0]][curr[1] - 1] == 1:
      discovered_grid.update_grid_obstacle((curr[0], curr[1] - 1), 1)
    else:
      discovered_grid.update_grid_obstacle((curr[0], curr[1] - 1), 0)
  # check the neighbor right of the block
  if curr[1] + 1 < dim:
    if complete_grid.gridworld[curr[0]][curr[1] + 1] == 1:
      discovered_grid.update_grid_obstacle((curr[0], curr[1] + 1), 1)
    else:
      discovered_grid.update_grid_obstacle((curr[0], curr[1] + 1), 0)


def main():
  p = argparse.ArgumentParser()
  p.add_argument(
    "-d", "--dimension", type=int, default=10, help="dimension of gridworld"
  )
  p.add_argument(
    "-p",
    "--probability",
    type=float,
    default=0.33,
    help="probability of a blocked square",
  )
  p.add_argument(
    "-m",
    "--heuristic",
    type=str,
    default="euclidian",
    help="heuristic of your desired algorithm (if possible)",
  )
  p.add_argument(
    "-a",
    "--agent",
    type=str,
    default="example_inference",
    help="one of the 4 types of agents described in the assignment",
  )

  # parse arguments and create the gridworld
  args = p.parse_args()

  # call the solver method with the args
  solver(args.dimension, args.probability, args.agent)

if __name__ == "__main__":
  main()
