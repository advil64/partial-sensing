# Partial Sensing
### Advith Chegu (ac1771) & Naveenan Yogeswaran (nry7)
### Both group members contributed equally to the code, data collection, and report.

## How is Agent 3 implemented?
For Agent 3, we use the same planning step as in Agent 1 and 2, but we modify the execution step to take the partial sensing into account to make inferences.

**Information Representation**

To represent our information, we create a Cell object for each cell in the grid which holds information about the cell. The following information is stored:
- neighbors: The number of neighbors the cell has.
- visited: Boolean value that represents if we visited the cell while executing a path.
- confirmed: Boolean value that represents if we were able to confirm whether the cell is empty or a block, either by visiting or through inference.
- block_sense: Number of neighbors we sensed to be blocks.
- confirm_block: Number of neighbors we confirmed to be blocks.
- confirm_empty: Number of neighbors we confirmed to be empty.
- hidden: Number of neighbors that we haven't confirmed yet.

Agent 3 stores a grid of these cells (cell_info) to keep track of their information.
Agent 3 will also update its discovered_grid whenever a cell is confirmed.

**Agent 3 Workflow**

In `execute_path`, we traverse the path given to us by our A*. For each cell in the path, we check if the cell is empty or blocked.

If the cell is empty:
- We first sense our surroundings by calling `sense_neighbors`. We do this by looking at the complete_grid and counting the number of blocks that neighbor the cell. We then store the number of blocks in the corresponding cell object's block_sense value.
- We then update the cell's value on the discovered_grid.

If the cell is blocked:
- We update the cell's value on the discovered_grid.
- We set our to_ret value (value to be returned) to the cell before.

For both cases:
- We set the cell's visited value to True.
- We set the cell's confirmed value to True.
- We call `update_neighbors` on that cell to see if we can make any new inferences with this information.

When calling `update_neighbors`, we first add our cell and our neighbors to a set. We then iterate through the set and pop a cell. We first call `update_cell_info` on that cell so the cell gets up to date info on it's neighbors (which neighbors are hidden, confirmed to be empty, confirmed to be block) using the discovered_grid. If the cell was visited and it sensed it's neighbors, we then call `update_knowledgebase` on this cell to begin making inferences.

When calling `update_knowledgebase`, we look at the cell's information.
- If the cell has no hidden neighbors, leave. Nothing more needs to be inferred here.
- If the cell's block_sense is equal to the cell's confirm_block, then turn all hidden cells to empty and add them to the list of updated cells. This is because we've discovered all our block neighbors and know the rest of the hidden must be empty.
- If the cell's neighbors - block_sense is equal to the cell's confirm_empty, then turn all hidden cells to block and add them to the list of updated cells. This is because we've discovered all our empty neighbors and know the rest of the hidden must be block.

After we're done making inferences on that cell, we return the list of cells we just confirmed.

Back in `update_neighbors`, we add the updated cells and their neighbors to our set for further inferences.

We continue doing this in `update_neighbors` until no more cells are updated. Afterwards, we return to execute_path. We then check if any of the newly updated blocks are in our path. If there are, then we stop executing the path.