# In this file, we define a number of objects that will be
# the tiles in our penrose tilings.
# They will need a few things:
# - defining points
# - list of all vertices (either as method or as attribute)
# - methods to be replaced
# if they are to be made adjacent, then they will need a method to chose how to add them

import numpy as np

PHI = 0.5*(1+np.sqrt(5))
PHI_ANGLE =  np.pi*2.0/5.0 


def rotation_matrix(angle):
    return np.matrix([[np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)]])

PHI_ROTATION = rotation_matrix(PHI_ANGLE).T



class Pentagon(object):

    def __init__(self, coords1, coords2):
        vertices = np.zeros((5,2))
        vertices[0:2] = np.array([coords1,coords2])
        for i in range(2,5):
            displacement = vertices[i-1] - vertices[i-2]
            displacement = displacement*PHI_ROTATION
            vertices[i] = vertices[i-1]+displacement
        self.vertices = vertices





