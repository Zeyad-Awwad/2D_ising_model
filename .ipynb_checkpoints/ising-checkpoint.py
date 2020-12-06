import numpy as np
import matplotlib.pyplot as plt



class Ising:
    
    def __init__(self, N, coupling, inv_temp, magnetic_moment, magnetic_field, batch_size):
        """
        Initializes an object that encapsulates a 2D Ising model
        
        Inputs:
            N: Defines the size of the square grid (NxN) stored in self.G
            coupling: Defines the interaction strength between between adjacent cells
            inv_temp: Defines the inverse temperature (Beta = 1 / kT)
            magnetic_moment: Defines the intrinsic magentic moment for each particle
            magnetic_field: Defines a net magnetic field passing through the lattice
            N_flip: The number of particles flipped in each step (should be << N^2)
        
        Returns:
            An instance of the Ising class
            
        """
        self.G = np.random.randint(0,2,(N,N))
        self.G[ self.G == 0 ] = -1
        self.N = N
        self.C = coupling
        self.B = inv_temp
        self.u = magnetic_moment
        self.h = magnetic_field
        self.IJ = np.nonzero(self.G)
        self.idx = np.arange( 0, len(self.IJ[0]) )
        self.H = np.zeros_like(self.G, dtype=np.float64)
        self.batch_size = batch_size
    
    
    def update(self):
        """
        Updates the cells of the grid based on the model parameters.
        
        Inputs:
            None (obtains all parameters from the current instance)
        
        Returns:
            None (updates the current instance directly)
        """
        N = self.N
        I, J = self.IJ
        idx = np.random.choice(self.idx, self.batch_size, replace=False)
        I, J = I[idx], J[idx]
        self.H *= 0
        for i in [-1,0,1]:
            for j in [-1,0,1]: 
                self.H[I,J] += self.G[ (I+i)%N,(J+j)%N] 
        self.H2 = self.H.copy()
        self.H[I,J] *= -self.C * self.G[I,J]
        self.H2 = self.H.copy()
        self.H[I,J] -=  self.u * self.h * self.G[I,J]
        P = np.exp(2 * self.B * self.H)
        flip = P < np.random.random( (N,N) )
        self.G[I,J] *= -1  + 2*flip[I,J]
    
        

def init(ising):
    """
    Initializes plots to animate an Ising model instance
    
    Inputs:
        ising: An instance of the Ising class
        
    Returns:
        fig: The active pyplot figure
        ax: The active pyplot axis within the figure
        mat: The matrix visualization that will be updated by the animation
    """
    fig, ax = plt.subplots(figsize=(10,10))
    mat = ax.matshow(ising.G, cmap = plt.cm.gray)
    return fig, ax, (mat,)


def animate(i, mat, ising, update_param = None):
    """
    The animation function that updates the model in each frame
    
    Inputs:
        i: The current frame index
        mat: The matrix visualization that will be updated by the animation
        ising: The Ising model instance that will be updated and visualized
        update_param: An optional function that can update the model parameters
    
    Returns:
        mat: The matrix visualization that will be updated by the animation

    """
    if update_param is not None:
        update_param(i, ising)
    ising.update()
    mat.set_data( ising.G )
    return (mat,)

def update_param(i, ising):
    """
    An example function that updates the model parameters. In ths case, it will
    lower the temperature after 1000 frames and add a magentic field after 1500
    
    Inputs:
        i: The current frame index
        ising: The Ising model instance that will be updated
    
    Returns:
        None
    """
    if i > 1000:
        ising.B = 1.
    if i > 1500:
        ising.h = -0.1

        


