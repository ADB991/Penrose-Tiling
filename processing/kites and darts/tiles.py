'''
this is different from the pentagon version
because we need to grow the tiling out
we will need ways of telling which tiles are on the border
and which of those are adjacent


probably the best will be to have edge and vertex objects
with methods to compare if they are the same.
then the tiles will have edges and vertices

the edges and vertices will be used to decide which shape to put
'''

import math


def rotate(centre, point, angle):
    d = difference(centre, point)
    cos, sin = math.cos(angle), math.sin(angle)
    rotated = (cos*d[0] - sin*d[1], sin*d[0] + cos*d[1])
    return addition(centre, rotated)

def difference(coords1, coords2):
    return tuple(x2 - x1 for x1, x2 in zip(coords1, coords2))

def addition(coords1, coords2):
    return tuple(x1 + x2 for x1, x2 in zip(coords1, coords2))

def length(displacement):
    return math.sqrt(displacement[0]**2 + displacement[1]**2)

def scale(displacement, factor):
    return tuple(factor*x for x in displacement)


class Vertex(object):
    ''' A vertex has coordinates, and colour'''
    def __init__(self, coords, colour):
        self.coords = coords
        self.colour = colour

    def __repr__(self):
        colour = "White" if self.colour == 'w' else 'Black'
        return colour+' vertex at '+str(self.coords)

    def __hash__(self):
        return hash((self.coords, self.colour))

    def __eq__(self, other):
        ''' Two vertices are the same if they share
            coordinates and colour'''
        if self.colour == other.colour :
            return self.coords == other.coords
        else: return False


class  Edge(object):
    ''' An edge has two edges and a colour'''
    def __init__(self, vertex1, vertex2, colour):
        if vertex1 == vertex2:
            print('Same vertices!!')
        self.vertices = set([vertex1, vertex2])
        self.colour = colour

    def __repr__(self):
        colour = "Green" if self.colour == 'g' else 'Red'
        coords = [v.coords for v in self.vertices]
        return colour+' edge between '+str(coords[0])+' and '+str(coords[1])

    def __hash__(self):
        return hash(self.vertices, self.colour)

    def __eq__(self, other):
        '''Two edges are the same if they share colour
            and vertices
        '''
        if self.colour == other.colour :
            return self.vertices == other.vertices
        else: return False

    def __contains__(self, vertex):
        return vertex in self.vertices

    @property
    def white_vertex(self):
        for v in self.vertices:
            if v.colour == 'w':
                return v
    @property
    def black_vertex(self):
        for v in self.vertices:
            if v.colour == 'b':
                return v

    @property
    def white_black(self):
        return (self.white_vertex, self.black_vertex)
    


''' Can make basic tiles, then make 'aware' tiles later'''

class Kite(object):
    def __init__(self, edge):
        if edge.colour == 'g':
            self.build_from_green(edge)
        else: self.build_from_red(edge)

    def build_from_green(self, edge, clockwise=False):
        white, black = edge.white_black
        # getting the other black edge
        # need only to rotate the first one through 72 degrees
        angle = math.pi*2.0/5.0
        if clockwise: angle *= -1
        new_black_coords = rotate(white.coords, black.coords, angle)
        new_black = Vertex(new_black_coords, 'b')
        # getting the other white one
        # bisect te two green edges and scale
        white_to_black = difference(white.coords, black.coords)
        white_to_new_black = difference(white.coords, new_black.coords)
        direction = scale(addition(white_to_black, white_to_new_black), .5)
        height = length(difference(black.coords, new_black.coords))
        additonal_distance = height/length(direction)*math.cos(0.2*math.pi)/math.tan(0.1*math.pi)
        displacement = scale(direction, 1.0 + additonal_distance)
        new_white_coords = addition(white.coords,displacement)
        new_white = Vertex(new_white_coords, 'w')

        self.vertices = [white, black, new_white, new_black]
        self.edges = [  edge, 
                        Edge(black, new_white,'r'), 
                        Edge(new_white,new_black,'r'),
                        Edge(new_black, white, 'g')
                    ]

    def __rep__(self):
        return 'Kite with '+str(self.vertices)













