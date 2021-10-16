from gridworld import Gridworld
from cell import Cell

class Agent_4:

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
  def execute_path(self, path, complete_grid, path_coord):
    #print("Start path")
    for node in path:
      curr = node.curr_block
      path_coord.remove(curr)
      cell = self.cell_info[curr[0]][curr[1]]
      to_ret = None
      bump = False

      # check if path is open
      if complete_grid.gridworld[cell.x][cell.y] == 0:
        # sense Agent's surroundings to determine number of blocks around
        self.sense_neighbors(cell, complete_grid) 
        # update our knowledge of blocked nodes
        self.discovered_grid.update_grid_obstacle(curr, 0)
        # return the last node
        to_ret = node

      else:
        self.discovered_grid.update_grid_obstacle(curr, 1)
        # return the parent and tell the gridworld to find a new path
        to_ret = node.parent_block
        # set bump to true to indicate we bumped into an obstacle
        bump = True

      # mark the cell as visited
      cell.visited = True
      # mark cell as a confirmed value because it was visited
      cell.confirmed = True
      # use the new info to draw conclusions about neighbors
      new_confirmed_cells = self.update_neighbors(cell)

      # self.discovered_grid.print()
      # print()

      # if we bumped into an obstacle, then leave the execution
      if bump:
        return to_ret
      # check if any new confirmed cells introduce block in your path
      if self.check_block_in_path(path_coord, new_confirmed_cells):
        return to_ret

    return path[-1]

  def update_neighbors(self, cell):
    # set that contains any cell that's been confirmed
    new_confirmed_cells = set()
    
    # add the neighbors of the current cell and itself to the list
    neighbors = set(cell.get_neighbors(self.cell_info, self.dim))
    #neighbors.add(cell)

    # loop through the cells and keep looping until neighbors is empty
    while neighbors:
      curr_cell = neighbors.pop()

      # if the cell was visited and we have the block sense, infer and add to knowledge base
      if curr_cell.visited and curr_cell.block_sense != -1:
        updated_cells = self.update_knowledgebase(curr_cell)
        new_confirmed_cells.update(updated_cells)

        # update all of the neighbors neighbors by adding those to the set
        for n in updated_cells:
          neighbors.update(n.get_neighbors(self.cell_info, self.dim))
          #neighbors.add(n)

    return new_confirmed_cells

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
      Implement systems of equations to enhance inferences, do these equations change?
      As in are we supposed to store the equations as information/variables for the cell?
      Or do we create and attempt to solve the system every time we make new inferences?
    '''
  def update_knowledgebase(self, cell):

    updated_cells = []
    
    # get the neighbors and check to see which are blockers
    neighbors = cell.get_neighbors(self.cell_info, self.dim)

    # traverse neighbors and make inferences
    for n in neighbors:

      # see if any inferences are possible
      if (cell.x, cell.y, 1) in n.equation:
        n.equation.remove((cell.x, cell.y, 1))
        # if the newly updated cell is a block then update block sense 
        if self.discovered_grid.gridworld[cell.x][cell.y]:
          n.block_sense -= 1

    # solve a system of equations
    for i,n in enumerate(neighbors):
      # ignore the neighbor if we have not visited
      if n.visited:
        # check if we can solve an equation by itself
        updated_cells.extend(self.make_inference(n.equation, n.block_sense))
        # try to subtract all the combinations of the cells
        for c in neighbors[i+1:]:
          if c.visited:
            updated_cells.extend(self.subtract(n, c))

    return updated_cells

  '''
    Subtracts any two given equations
    @return list: list of cells that have been updated
  '''
  def subtract(self, cell1, cell2):

    result = cell1.equation.symmetric_difference(cell2.equation)
    right_hand_side = abs(cell1.block_sense - cell2.block_sense)
    
    # set negative values for subtracted equations
    if cell1.block_sense >= cell2.block_sense:
      for r in result:
        if r in cell2.equation:
          result.remove(r)
          result.add((r[0], r[1], -1))
    else:
      for r in result:
        if r in cell1.equation:
          result.remove(r)
          result.add((r[0], r[1], -1))
    
    # return the updated cells if inferences were made
    return self.make_inference(result, right_hand_side)
      

  '''
    Returns the list of updated cells
  '''
  def make_inference(self, equation, blocks):
    updated_cells = []

    # if we know all empty cells, update the other cells to be blocked
    if blocks == 0:
      for cord in equation:
        if not self.cell_info[cord[0]][cord[1]].confirmed:
          self.discovered_grid.update_grid_obstacle((cord[0], cord[1]), 0)
          self.cell_info[cord[0]][cord[1]].confirmed = True
          updated_cells.append(self.cell_info[cord[0]][cord[1]])
    
    # calculates the number of positive tuples
    positive = len(list(filter(lambda x: (x[2] > 0), equation)))

    # if the positive cordinates is the same as blocks then positives are all ones
    if positive == blocks:
      for cord in equation:
        if not self.cell_info[cord[0]][cord[1]].confirmed:
          updated_cells.append(self.cell_info[cord[0]][cord[1]])
          if cord[2] > 0:
            self.discovered_grid.update_grid_obstacle((cord[0], cord[1]), 1)
          else:
            self.discovered_grid.update_grid_obstacle((cord[0], cord[1]), 0)
          self.cell_info[cord[0]][cord[1]].confirmed = True

    return updated_cells

  def check_block_in_path(self, path_coord, new_confirmed_cells):
    for cell in new_confirmed_cells:
      if self.discovered_grid.gridworld[cell.x][cell.y] == 1:
        if (cell.x, cell.y) in path_coord:
          return True
    
    return False

