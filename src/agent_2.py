from gridworld import Gridworld

class Agent_2:

  def __init__(self, dim):
    self.dim = dim
    self.discovered_grid = Gridworld(dim)

  def execute_path(self, path, complete_grid, path_coord):
    explored = 0
    for index, node in enumerate(path):
      curr = node.curr_block
      # check if path is blocked
      if complete_grid.gridworld[curr[0]][curr[1]] == 1:
        # update our knowledge of blocked nodes
        self.discovered_grid.update_grid_obstacle(curr, 1)
        return node.parent_block, explored
      self.discovered_grid.update_grid_obstacle(curr, 0)
      explored += 1
    return path[-1], explored