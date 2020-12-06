# 2D_ising_model
 An animated 2D ising model with interactive components to control the model parameters (temporarily excluded but will be reincorporated soon).

For more scalable performance, the model updates the cells in batches. This can cause strange behavior when several neighbors are changed at the same time. This shouldn't cause issues as long as the batch size is much smaller than the number of cells.

![An example of a 100x100 Ising model](example.gif)

