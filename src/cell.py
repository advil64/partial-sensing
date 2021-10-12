class Cell:

  def __init__(self, x, y, dim):
    self.x = x
    self.y = y

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

    self.visited = False
    self.confirmed = False
    self.block_sense = 0
    self.confirm_block = 0
    self.confirm_empty = 0
    self.hidden = 0