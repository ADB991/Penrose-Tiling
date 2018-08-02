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
PHI_SCALE = 1.0 / (PHI + 1)



def rotation_matrix(angle):
    return np.matrix([[np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)]])


#used to get the next edge of a pentagon
PHI_ROTATION = rotation_matrix(PHI_ANGLE).T
#used to get the second edge of the central pentagon in a deflation
CENTRE_PHI_ROTATION = -rotation_matrix(3*PHI_ANGLE).T



class Pentagon(object):


    def __init__(self, coords1, coords2):
        vertices = np.zeros((5,2))
        vertices[:2] = np.array([coords1,coords2])
        for i in range(2,5):
            displacement = vertices[i-1] - vertices[i-2]
            displacement = displacement*PHI_ROTATION
            vertices[i] = vertices[i-1]+displacement
        self.vertices = vertices

    def loop_vertices(self, start=0):
        '''generates all vertex 0, 1, ... 0'''
        for v in self.vertices[start:]: yield v
        yield self.vertices[0]

    def loop_vertices_as_array(self, start=0):
        '''generates all vertex 0, 1, ... 0'''
        return np.array(list(self.loop_vertices()))


    def deflate(self):
        ''' Returns an array of tile objects
            In this case, one pentagon per vertex and one at the centre
        '''
        firsts = self.vertices
        seconds = self.loop_vertices(1)

        # pentagons on the vertices
        for v0, v1 in zip(firsts, seconds):
            displacement = v1 - v0
            new_vertex = PHI_SCALE * displacement + v0
            yield Pentagon(v0, new_vertex)
        # the pentagon at the centre
        v0, v1 = self.vertices[:2] #grab the two vertices
        displacement = PHI_SCALE * (v1-v0)
        v1 = v0 + displacement #rescale seconf vertex
        v0 = np.array(v1 + displacement*PHI_ROTATION)[0]
        v1 = np.array(v0 + displacement*CENTRE_PHI_ROTATION)[0]
        yield Pentagon(v0,v1)


class Tiling(object):
    ''' Contains many tiles inside which can be deflated'''
    def __init__(self, start_tiles):
        self.tiles = start_tiles

    def deflate(self, iterations=1):
        ''' Deflates each tile'''
        for i in range(iterations):
            new_tiles = []
            for tile in self.tiles:
                new_tiles += list(tile.deflate())
            self.tiles = new_tiles
