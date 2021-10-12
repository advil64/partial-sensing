from gridworld import Gridworld

class Agent_1:

  def __init__(self, dim):
    self.dim = dim
    self.discovered_grid = Gridworld(dim)

  def execute_path(self, path, complete_grid):
    for index, node in enumerate(path):
      curr = node.curr_block
      # check if path is blocked
      if complete_grid.gridworld[curr[0]][curr[1]] == 1:
        # update our knowledge of blocked nodes
        self.discovered_grid.update_grid_obstacle(curr, 1)
        return node.parent_block
      self.discovered_grid.update_grid_obstacle(curr, 0)
      # update knowledge of neighbor blocks
      self.update_neighbor_obstacles(curr, complete_grid)
    return path[-1]

  # method for 4-neighbor agent
  def update_neighbor_obstacles(self, curr, complete_grid):
    # check the neighbor above the block
    if curr[0] - 1 >= 0:
      if complete_grid.gridworld[curr[0] - 1][curr[1]] == 1:
        self.discovered_grid.update_grid_obstacle((curr[0] - 1, curr[1]), 1)
      else:
        self.discovered_grid.update_grid_obstacle((curr[0] - 1, curr[1]), 0)
    # check the neighbor below the block
    if curr[0] + 1 < self.dim:
      if complete_grid.gridworld[curr[0] + 1][curr[1]] == 1:
        self.discovered_grid.update_grid_obstacle((curr[0] + 1, curr[1]), 1)
      else:
        self.discovered_grid.update_grid_obstacle((curr[0] + 1, curr[1]), 0)
    # check the neighbor left of the block
    if curr[1] - 1 >= 0:
      if complete_grid.gridworld[curr[0]][curr[1] - 1] == 1:
        self.discovered_grid.update_grid_obstacle((curr[0], curr[1] - 1), 1)
      else:
        self.discovered_grid.update_grid_obstacle((curr[0], curr[1] - 1), 0)
    # check the neighbor right of the block
    if curr[1] + 1 < self.dim:
      if complete_grid.gridworld[curr[0]][curr[1] + 1] == 1:
        self.discovered_grid.update_grid_obstacle((curr[0], curr[1] + 1), 1)
      else:
        self.discovered_grid.update_grid_obstacle((curr[0], curr[1] + 1), 0)