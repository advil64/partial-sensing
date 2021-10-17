# Partial Sensing
### Advith Chegu (ac1771) & Naveenan Yogeswaran (nry7)
### Both group members contributed equally to the code, data collection, and report.

## How is Agent 3 implemented?
For Agent 3, we use the same planning step as in Agent 1 and 2, but we modify the execution step to take the partial sensing into account to make inferences.

**Information Representation**

To represent our information, we create a Cell object for each cell in the grid which holds information about the cell. The following information is stored:
- *neighbors*: The number of neighbors the cell has.
- *visited*: Boolean value that represents if we visited the cell while executing a path.
- *confirmed*: Boolean value that represents if we were able to confirm whether the cell is empty or a block, either by visiting or through inference.
- *block_sense*: Number of neighbors we sensed to be blocks.
- *confirm_block*: Number of neighbors we confirmed to be blocks.
- *confirm_empty*: Number of neighbors we confirmed to be empty.
- *hidden*: Number of neighbors that we haven't confirmed yet.

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

## Design of Agent 4

Not only is Agent 4 capable of making the same inferences as Agent 3, but Agent 4 is able to make even more inferences with the same amount of information about its environment.

**What rules / inferences / other methods does Agent 4 perform? How does Agent 4 differ from Agent 3?**

By comparing the neighbors of two separate cells, Agent 4 is able to possibly infer the identity of those neighbors. It does this by modeling the neighbors of the cell as an equation.
Take the following example:

U U 1

0 1 1

0 U U

Block Sense = 3

Assume we want to model the neighbors of cell (1,1) as an equation.
This equation would we (0,0) + (0,1) + (2,1) + (2,2) = 1

The reason we don’t include (0,2) and the other neighbors is because we discovered them already. The reason our right hand side is 1 and not 3 is because we already discovered two neighboring blocks.

We can make more inferences with these equations, than in Agent 3, by taking two cell’s equations and performing systems of equations. In the resulting equation, we observe the equation to make the following inferences:

- If the right side of the equation is equal to 0 and the left side are all positive values, then all values in the left side are equal to 0.
    - Example: (0,0) + (0,1) + (1,0) = 0 means (0,0), (0,1), (1,0) must be 0 in order to satisfy the equation.

- If the right side of the equation is greater than 0 and it is equal to the number of positive values in the left side of the equation, then all positive values in the left side must be blocks and all negative values must be 0.
    - Example: (0,0) + (0,1) + (1,0) - (1,2) - (2,2) = 3 means (0,0), (0,1), (1,0) must be 1, and (1,2) and (2,2) must be 0 in order to satisfy the equation.

We also make sure to observe an individual cell’s equation to see if we can make inferences from that, using the same rules as above. This will replicate the inferences that can be made in Agent 3.

**Can you show that there are situations where Agent 4 can infer things that Agent 3 can't, even if they both have the same knowledge base?**

Take the following example:

1 U 0 U U

0 X U Y 0

U 0 U 1 0

X block sense = 4

Y block sense = 2

The equation for cell X is (0,1) + (1,2) + (2,0) + (2,2) = 3

The equation for cell Y is (0,3) + (0,4) + (1,2) + (2,2) = 1

The resulting equation when subtracting is (0,1) + (2,0) - (0,3) - (0,4) = 2

From our inference rules, we can determine that (0,1) and (2,0) are 1 and (0,3) and (0,4) are 0.

1 1 0 0 0

0 X U Y 0

1 0 U 1 0

Agent 3 on the other hand would not have been able to make these inferences as cell X does not have block_sense = confirm_block nor does it have neighbors - block_sense = confirm_empty. The same can be said for cell Y as well. Thus, Agent 4 was able to make more inferences than Agent 3.

**Does Agent 3 ever get anything that Agent 4 does not?**

Agent 3 won’t ever get anything that Agent 4 will not. This is because the equation representation can also replicate the inferences made by Agent 3 when we make inferences on a single cell’s equation.

For example, we can replicate Agent 3’s inference rule that checks if block_sense = confirm_block.

1 U 1

0 X 1

0 U U

X block sense = 3

The equation for X is (0,1) + (2,1) + (2,2) = 0
From our first new rule of inference, we know that (0,1), (2,1) and (2,2) must be 0 to satisfy the equation. And so we replicated this inference from Agent 3 in Agent 4.

We can also replicate Agent 3’s inference rule that checks if neighbors - block_sense = confirm_empty.

1 U 1

0 X 0

0 0 U

X block sense = 4

The equation for X is (0,1) + (2,1) = 2

From our second new rule of inference, we know that (0,1) and (2,1) must be 1 to satisfy the equation. And so we replicated this inference from Agent 3 in Agent 4.

Because our Agent 4 can make the same inferences as Agent 3, Agent 3 shouldn’t be able to get any more information than what Agent 4 can.

**Does Agent 4 infer "everything that is possible to infer" and if not, why not? Can you construct situations where inference is possible, but Agent 4 doesn't infer anything?**


## How is Agent 4 implemented?
Agent 4 is very similar to Agent 3 in that we must either make inferences to find the blockers or bump into them.

**Information Representation**

To represent our information, we create a Cell object for each cell in the grid which holds information about the cell. The following information is used by agent four:

- *visited*: Indicates whether our agent has physically traversed that cell or not
- *confirmed*: Indicates whether we have been able to make an inference about that cell
- *block_sense*: Number of blocked neighbors. This value is calculated when the given node is visited.
- *equation*: The tuples of coordinates which will be used to create the left hand side of the system of equations
- *right_side*: The number of hidden cells that are blocked. This value is decremented when a hidden neighbor is found to be a block. It is also the right hand side of the system of equations.

Agent 4 stores a grid of these cells (cell_info) to keep track of their information.
Agent 4 will also update its discovered_grid whenever a cell is confirmed.

**Agent 4 Workflow**

Just like Agent 3, in Agent 4 we start off in its `execute_path` function where we are passed the path from an iteration of repeated A* as well as the complete gridworld used for block sensing.

For each cell in the path, we check if the cell is empty or blocked.

If the cell is empty:
- Calculate the number of blocks around the cell by calling `sense_neighbors`. We do this by looking at the complete_grid and counting the number of blocks that neighbor the cell. We then store the number of blocks in the corresponding cell object's block_sense value.
- Update our cell's value in the discovered gridworld
- If the cell was not visited already we add it to the set of visited cells to try to make inferences against every time a cell has been updated.

If the cell is blocked:

- We update the cell's value on the discovered_grid.
- We set our to_ret value (value to be returned) to the cell before.
- We set our bump value to *true* which means that there exists an obstacle in the path

For both cases:

- We set the cell's visited value to True.
- We set the cell's confirmed value to True.
- We call `update_neighbors` on that cell to see if we can make any new inferences with this information.

When calling `update_neighbors` we first create a set of the newly confirmed cells. This set will update with any cells we have made an inference on.

We also create a neighbors list which updates with all of the neighbors of the cells we make inferences on. This is because these are the cells that get updated when another is confirmed so to optimize our code we only update these equations rather than all the equations in the grid.

We traverse through the neighbors list popping one at a time until there have been no new inferences, in which case the neighbors list will be empty. Each time we pop from the list we update the cell's equations in `update_equation` by looking at the unconfirmed neighbors and replacing the old equation with the new equation. We also recalculate the right hand side of the equation by first recalculating the confirmed blocks in the cell's neighbors and subtracting that from block sense.

To make inferences we first confirm that the given cell has been visited, or else the right hand side of the equation will be -1. Next we call `update_knowledgebase` where the following steps take place:
- We first get all of the current cell's neighbors
- Next we try to make an inference using only the cell's current equation. Basically if the terms in the equation's left hand side equals the right hand side we can assume that all the terms in the equation are blocked
- Then we have a double for loop to try to make inferences by subtracting every possible combination of equations. We do subtract by finding the coordinates which are not shared amongst the equation sets for the left side and taking the difference of the unconfirmed blocked nodes on the right.
```python
result = cell1.equation.symmetric_difference(cell2.equation)
right_hand_side = abs(cell1.right_side - cell2.right_side)
```
- When subtracting we set the third element of the coordinate tuple to be negative one if it comes from the equation being subtracted.
- Now we make a few inferences, if the right hand side is zero but there are still coordinates in the equation after we subtracted, then we know that all of those cells are zero, we set them as such
- We can also infer that if the positive coordinates are the same as the number of blocks that all the cells at the positive coordinates must be blocks and the negative ones must be open.
- Once we make those inferences and update the discovered gridworld, we can go back and append those cells and its neighbors to have their equations updated.

## Computational Optimizations
In Agent 3 and 4, we take multiple steps to minimize computations in order to ensure our Agents run as efficiently as they can.

The first step we take to minimize computations is how we traverse our grid and update our cell_info. We realized that when updating a cell, not every cell will be affected by this change and therefore will not make any new inferences. The only cells we need to update and can possibly make inferences on are the neighboring cells and the current cell. And so, rather than updating every cell in the grid and checking for new inferences on them, we add these neighboring cells and the current cell to a set and we traverse only through the cells in the set. 

Whenever we infer the identity of a cell, we make sure to add this cell and its neighbors to our set. Whenever we pop the cell from the set, we update it’s info on neighbors to ensure it’s up to date and we make inferences if we can. We repeat this until the set is empty, which means there are no more inferences to be made. Thus, we significantly improve our computational overhead by ignoring cells that aren’t affected by the changes.

The next step we take to minimize computations is to ignore non-sensed cells when making inferences on them. We can ignore these cells because they haven’t sensed how many of their neighbors are blocks. Without access to this information, we can’t make any inferences on them. As a result we choose to ignore these cells when making inferences in order to avoid wasting any computations on these cells.
