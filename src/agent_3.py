from gridworld import Gridworld
from cell import Cell

class Agent_3:

  def __init__(self, dim):
    self.dim = dim
    self.discovered_grid = Gridworld(dim)
    # grid that Agent uses to keep track of each cell info
    self.cell_info = []
    for i in range(dim):
      row = []
      for j in range(dim):
        row.append(Cell(i, j, dim))
      self.cell_info.append(row)

  '''
    Given a path (from repeated A*) we traverse through the gridworld and gather information
    @param path: given path as a list of nodes
    @param complete_grid: the full gridworld to check for obstacles along the way
    @return list: the last node of the gridworld or the parent node
  '''
  def execute_path(self, path, complete_grid):
    for node in path:
      curr = node.curr_block
      cell = self.cell_info[curr[0]][curr[1]]
      to_ret = None

      # check if path is open
      if complete_grid.gridworld[cell.x][cell.y] == 0:
        # sense Agent's surroundings to determine number of blocks around
        self.sense_neighbors(cell, complete_grid) 
        # update our knowledge of blocked nodes
        self.discovered_grid.update_grid_obstacle(curr, 0)
        # return the last node
        to_ret = path[-1]

      else:
        self.discovered_grid.update_grid_obstacle(curr, 1)
        # return the parent and tell the gridworld to find a new path
        to_ret = node.parent_block

      # mark the cell as visited
      cell.visited = True
      # mark cell as a confirmed value because it was visited
      cell.confirmed = True
      # use the new info to draw conclusions about neighbors
      self.update_neighbors(cell)

    return to_ret

  def update_neighbors(self, cell):
    
    # add the neighbors of the current cell and itself to the list
    neighbors = set(cell.get_neighbors(self.cell_info, self.dim))
    neighbors.add(cell)

    # loop through the cells and keep looping until neighbors is empty
    while neighbors:
      curr_cell = neighbors.pop()
      changed = self.update_cell_info(curr_cell)

      # if the cell was visited we have the block sense
      if curr_cell.visited and changed:
        updated_cells = self.update_knowledgebase(curr_cell)

        # update all of the neighbors neighbors by adding those to the set
        for n in updated_cells:
          neighbors.update(n.get_neighbors(self.cell_info, self.dim))
          neighbors.add(n)
  
  '''
    This method returns the number of blocked neighbors a given cell has
    @param cell: the current cell in the path traversal
    @param complete_grid: grid with the obstacles
  '''
  def sense_neighbors(self, cell, complete_grid):
    num_sensed = 0
    neighbors = cell.get_neighbors(self.cell_info, self.dim)

    # loop through the neighbors to be checked and take the sum (1 is block)
    num_sensed = sum(complete_grid.gridworld[n.x][n.y] for n in neighbors)

    # return the number of obstacles surrounding the current node
    cell.block_sense = num_sensed

  '''
    This method stores the surrounding information of any given cell based on the discovered grid
    @param cell: cell to calculate surroundings
    @return boolean: indicating if any values have changed
  '''
  def update_cell_info(self, cell):
    num_hidden = 0
    num_block = 0
    num_empty = 0
    neighbors = cell.get_neighbors(self.cell_info, self.dim)

    # loop through the neighbors to be checked
    for n in neighbors:
      if n.confirmed:
        # check and increment if it is blocked
        if self.discovered_grid.gridworld[n.x][n.y] == 1:
          num_block += 1
        # otherwise increment the empty counter
        else:
          num_empty += 1
      # the neighbor cell has not been explored yet
      else:
        num_hidden += 1

    has_changed = (cell.hidden - num_hidden) or (cell.confirm_block - num_block) or (cell.confirm_empty - num_empty)

    if has_changed:
      cell.hidden = num_hidden
      cell.confirm_block = num_block
      cell.confirm_empty = num_empty
    
    return has_changed
    
  def update_knowledgebase(self, cell):

    updated_cells = []

    # if there are hidden not cells, leave
    if cell.hidden == 0:
      return updated_cells
    
    # get the neighbors and check to see which are blockers
    neighbors = cell.get_neighbors(self.cell_info, self.dim)

    # if we know all block cells, update the other cells to be empty
    if cell.block_sense == cell.confirm_block:
      for n in neighbors:
        if not n.confirmed:
          self.discovered_grid.update_grid_obstacle((cell.x - 1, cell.y), 0)
          self.cell_info[cell.x - 1][cell.y].confirmed = True
          updated_cells.append(cell)
      return updated_cells
    
    # if we know all empty cells, update the other cells to be blocked
    if cell.neighbors - cell.block_sense == cell.confirm_empty:
      for n in neighbors:
        if not n.confirmed:
          self.discovered_grid.update_grid_obstacle((cell.x - 1, cell.y), 1)
          self.cell_info[cell.x - 1][cell.y].confirmed = True
          updated_cells.append(cell)
    
    return updated_cells