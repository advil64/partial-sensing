class Cell:

  def __init__(self, x, y, dim):
    self.x = x
    self.y = y

    self.neighbor_directions = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]

    if x == 0 and y == 0:
      self.neighbors = 3
    elif x == 0 and y == dim-1:
      self.neighbors = 3
    elif x == dim-1 and y == 0:
      self.neighbors = 3
    elif x == dim-1 and y == dim-1:
      self.neighbors = 3
    elif x == 0 or x == dim-1 or y == 0 or y == dim-1:
      self.neighbors = 5
    else:
      self.neighbors = 8

    # indicates if the agent has visited the current cell
    self.visited = False
    # indicates if the agent has made an inference on this cell
    self.confirmed = False
    # indicates the number of obstacles that surround the cell
    self.block_sense = -1
    # indicate the number of confirmed obstacles that surround the cell
    self.confirm_block = 0
    # indicates the number of confirmed empty cells that surround the current cell
    self.confirm_empty = 0
    # indicates the number of surrounding cells that we do not have information for
    self.hidden = self.neighbors
    # indicates the current equation of the cell and its neighbors
    self.equation = {(self.x + n[0], self.y + n[1], 1) for n in self.neighbor_directions if 0 <= self.x + n[0] < dim and 0 <= self.y + n[1] < dim}
    # indicates right side of self.equation
    self.right_side = self.block_sense

  '''
    Defines equality used for set operations
  '''
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  '''
    Used for set operations
  '''
  def __hash__(self):
    return hash(self.__repr__())

  '''
    Method checks all directions and returns neighbors depending on location
    @return list: list of neighbors of cell type
  '''
  def get_neighbors(self, cell_info, dim):
    neighbors = []

    # find all the neighbors for the current cell
    for n in self.neighbor_directions:
      # the cordinates of the neighbor
      curr_neighbor = (self.x + n[0], self.y + n[1])
      # check bounds
      if curr_neighbor[0] >= 0 and curr_neighbor[0] < dim and curr_neighbor[1] >= 0 and curr_neighbor[1] < dim:
        # add the neighbor cell to our list
        neighbors.append(cell_info[curr_neighbor[0]][curr_neighbor[1]])
    
    return neighbors