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

  def execute_path(self, path, complete_grid):
    for index, node in enumerate(path):
      curr = node.curr_block
      # check if path is blocked
      if complete_grid.gridworld[curr[0]][curr[1]] == 1:
        # update our knowledge of blocked nodes
        self.discovered_grid.update_grid_obstacle(curr, 1)
        # mark cell as confirmed to be blocked
        self.cell_info[curr[0]][curr[1]].confirmed = True
        return node.parent_block
      self.discovered_grid.update_grid_obstacle(curr, 0)

      # mark Cell as visited
      self.cell_info[curr[0]][curr[1]].visited = True
      # mark cell as confirmed to be empty
      self.cell_info[curr[0]][curr[1]].confirmed = True
      # sense Agent's surroundings to determine number of blocks around
      self.sense_neighbors(self.cell_info[curr[0]][curr[1]], complete_grid) 
      # update knowledge base of agent using new info
      self.update_cell_info(self.cell_info[curr[0]][curr[1]])


    return path[-1]
  
  def sense_neighbors(self, cell, complete_grid):
    num_sensed = 0
    # check the neighbor above the block
    if cell.x - 1 >= 0:
      if complete_grid.gridworld[cell.x - 1][cell.y] == 1:
        num_sensed += 1
    # check the neighbor below the block
    if cell.x + 1 < self.dim:
      if complete_grid.gridworld[cell.x + 1][cell.y] == 1:
        num_sensed += 1
    # check the neighbor left of the block
    if cell.y - 1 >= 0:
      if complete_grid.gridworld[cell.x][cell.y - 1] == 1:
        num_sensed += 1
    # check the neighbor right of the block
    if cell.y + 1 < self.dim:
      if complete_grid.gridworld[cell.x][cell.y + 1] == 1:
        num_sensed += 1
    # check the neighbor up-left of the block
    if cell.x - 1 >= 0 and cell.y - 1 >= 0:
      if complete_grid.gridworld[cell.x - 1][cell.y - 1] == 1:
        num_sensed += 1
    # check the neighbor down-left of the block
    if cell.x + 1 >= 0 and cell.y - 1 >= 0:
      if complete_grid.gridworld[cell.x + 1][cell.y - 1] == 1:
        num_sensed += 1
    # check the neighbor up-right of the block
    if cell.x - 1 >= 0 and cell.y + 1 >= 0:
      if complete_grid.gridworld[cell.x - 1][cell.y + 1] == 1:
        num_sensed += 1
    # check the neighbor down-right of the block
    if cell.x + 1 >= 0 and cell.y + 1 >= 0:
      if complete_grid.gridworld[cell.x + 1][cell.y + 1] == 1:
        num_sensed += 1
    cell.block_sense = num_sensed

    def update_cell_info(self, cell):
      num_hidden = 0
      num_block = 0
      num_empty = 0
      # check the neighbor above the block
      if cell.x - 1 >= 0:
        if self.cell_info[cell.x - 1][cell.y].confirmed:
          if self.discovered_grid.gridworld[cell.x - 1][cell.y] == 1:
            num_block += 1
          else:
            num_empty += 1
        else:
          num_hidden += 1
      # check the neighbor below the block
      if cell.x + 1 < self.dim:
        if self.cell_info[cell.x + 1][cell.y].confirmed:
          if self.discovered_grid.gridworld[cell.x + 1][cell.y] == 1:
            num_block += 1
          else:
            num_empty += 1
        else:
          num_hidden += 1
      # check the neighbor left of the block
      if cell.y - 1 >= 0:
        if self.cell_info[cell.x][cell.y - 1].confirmed:
          if self.discovered_grid.gridworld[cell.x][cell.y - 1] == 1:
            num_block += 1
          else:
            num_empty += 1
        else:
          num_hidden += 1
      # check the neighbor right of the block
      if cell.y + 1 < self.dim:
        if self.cell_info[cell.x][cell.y + 1].confirmed:
          if self.discovered_grid.gridworld[cell.x][cell.y + 1] == 1:
            num_block += 1
          else:
            num_empty += 1
        else:
          num_hidden += 1
      # check the neighbor up-left of the block
      if cell.x - 1 >= 0 and cell.y - 1 >= 0:
        if self.cell_info[cell.x - 1][cell.y - 1].confirmed:
          if self.discovered_grid.gridworld[cell.x - 1][cell.y - 1] == 1:
            num_block += 1
          else:
            num_empty += 1
        else:
          num_hidden += 1
      # check the neighbor down-left of the block
      if cell.x + 1 >= 0 and cell.y - 1 >= 0:
        if self.cell_info[cell.x + 1][cell.y - 1].confirmed:
          if self.discovered_grid.gridworld[cell.x + 1][cell.y - 1] == 1:
            num_block += 1
          else:
            num_empty += 1
        else:
          num_hidden += 1
      # check the neighbor up-right of the block
      if cell.x - 1 >= 0 and cell.y + 1 >= 0:
        if self.cell_info[cell.x - 1][cell.y + 1].confirmed:
          if self.discovered_grid.gridworld[cell.x - 1][cell.y + 1] == 1:
            num_block += 1
          else:
            num_empty += 1
        else:
          num_hidden += 1
      # check the neighbor down-right of the block
      if cell.x + 1 >= 0 and cell.y + 1 >= 0:
        if self.cell_info[cell.x + 1][cell.y + 1].confirmed:
          if self.discovered_grid.gridworld[cell.x + 1][cell.y + 1] == 1:
            num_block += 1
          else:
            num_empty += 1
        else:
          num_hidden += 1

      cell.hidden = num_hidden
      cell.confirm_block = num_block
      cell.confirm_empty = num_empty

      # Update knowledgebase with new info
      self.update_knowledgebase(cell)
    
    def update_knowledgebase(self, cell):
      # if there are not hidden cells, leave
      if cell.hidden == 0:
        return

      # if we know all block cells, update the other cells to be empty
      if cell.block_sense == cell.confirm_block:
        # check the neighbor above the block
        if cell.x - 1 >= 0:
          if not self.cell_info[cell.x - 1][cell.y].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x - 1, cell.y), 0)
            self.cell_info[cell.x - 1][cell.y].confirmed = True
        # check the neighbor below the block
        if cell.x + 1 < self.dim:
          if not self.cell_info[cell.x + 1][cell.y].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x + 1, cell.y), 0)
            self.cell_info[cell.x + 1][cell.y].confirmed = True
        # check the neighbor left of the block
        if cell.y - 1 >= 0:
          if not self.cell_info[cell.x][cell.y - 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x, cell.y - 1), 0)
            self.cell_info[cell.x][cell.y - 1].confirmed = True
        # check the neighbor right of the block
        if cell.y + 1 < self.dim:
          if not self.cell_info[cell.x][cell.y + 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x, cell.y + 1), 0)
            self.cell_info[cell.x][cell.y + 1].confirmed = True
        # check the neighbor up-left of the block
        if cell.x - 1 >= 0 and cell.y - 1 >= 0:
          if not self.cell_info[cell.x - 1][cell.y - 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x - 1, cell.y - 1), 0)
            self.cell_info[cell.x - 1][cell.y - 1].confirmed = True
        # check the neighbor down-left of the block
        if cell.x + 1 >= 0 and cell.y - 1 >= 0:
          if not self.cell_info[cell.x + 1][cell.y - 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x + 1, cell.y - 1), 0)
            self.cell_info[cell.x + 1][cell.y - 1].confirmed = True
        # check the neighbor up-right of the block
        if cell.x - 1 >= 0 and cell.y + 1 >= 0:
          if not self.cell_info[cell.x - 1][cell.y + 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x - 1, cell.y + 1), 0)
            self.cell_info[cell.x - 1][cell.y + 1].confirmed = True
        # check the neighbor down-right of the block
        if cell.x + 1 >= 0 and cell.y + 1 >= 0:
          if not self.cell_info[cell.x + 1][cell.y + 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x + 1, cell.y + 1), 0)
            self.cell_info[cell.x + 1][cell.y + 1].confirmed = True
        
        return
      
      # if we know all empty cells, update the other cells to be blocked
      if cell.neighbors - cell.block_sense == cell.confirm_empty:
        # check the neighbor above the block
        if cell.x - 1 >= 0:
          if not self.cell_info[cell.x - 1][cell.y].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x - 1, cell.y), 1)
            self.cell_info[cell.x - 1][cell.y].confirmed = True
        # check the neighbor below the block
        if cell.x + 1 < self.dim:
          if not self.cell_info[cell.x + 1][cell.y].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x + 1, cell.y), 1)
            self.cell_info[cell.x + 1][cell.y].confirmed = True
        # check the neighbor left of the block
        if cell.y - 1 >= 0:
          if not self.cell_info[cell.x][cell.y - 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x, cell.y - 1), 1)
            self.cell_info[cell.x][cell.y - 1].confirmed = True
        # check the neighbor right of the block
        if cell.y + 1 < self.dim:
          if not self.cell_info[cell.x][cell.y + 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x, cell.y + 1), 1)
            self.cell_info[cell.x][cell.y + 1].confirmed = True
        # check the neighbor up-left of the block
        if cell.x - 1 >= 0 and cell.y - 1 >= 0:
          if not self.cell_info[cell.x - 1][cell.y - 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x - 1, cell.y - 1), 1)
            self.cell_info[cell.x - 1][cell.y - 1].confirmed = True
        # check the neighbor down-left of the block
        if cell.x + 1 >= 0 and cell.y - 1 >= 0:
          if not self.cell_info[cell.x + 1][cell.y - 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x + 1, cell.y - 1), 1)
            self.cell_info[cell.x + 1][cell.y - 1].confirmed = True
        # check the neighbor up-right of the block
        if cell.x - 1 >= 0 and cell.y + 1 >= 0:
          if not self.cell_info[cell.x - 1][cell.y + 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x - 1, cell.y + 1), 1)
            self.cell_info[cell.x - 1][cell.y + 1].confirmed = True
        # check the neighbor down-right of the block
        if cell.x + 1 >= 0 and cell.y + 1 >= 0:
          if not self.cell_info[cell.x + 1][cell.y + 1].confirmed:
            self.discovered_grid.update_grid_obstacle((cell.x + 1, cell.y + 1), 1)
            self.cell_info[cell.x + 1][cell.y + 1].confirmed = True
        
        return

      
  